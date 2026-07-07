#!/usr/bin/env python3
"""
h4 (commitment sensitivity) — B2 judge runner. Executes the LOCKED rubric in
../rubric.md: audit every self-reported completion assertion (224 across the 45
executed B promises) against episode.diff + pytest.txt + final.txt.

One Codex call per episode (its assertions batched). Reuses harness/judge.py
machinery verbatim (call_codex / parse_verdict_json / _norm / run_job /
write_checkpoint). Resume-first; InfraErrors leave no checkpoint; 3 consecutive
InfraErrors abort. Validation requires the judge's assertion list to mirror the
episode's actual assertions exactly (same cos text, same claimed status, same
order) — a drifted audit is rejected and retried, then recorded judge_error.

Writes ONLY under this folder: verdicts/<rep>-<task>.json + verdicts/verdicts.json.
Standard library only, Python 3.9.
"""

import csv
import json
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
EXPERIMENT = os.path.dirname(os.path.dirname(HERE))
RUNS_DIR = os.path.join(EXPERIMENT, "runs")
TASKS_DIR = os.path.join(EXPERIMENT, "tasks")
HARNESS = os.path.join(EXPERIMENT, "harness")
sys.path.insert(0, HARNESS)
import judge        # noqa: E402
import score_tier1  # noqa: E402  (extract_json_block — the shared completion parser)

VERDICTS_DIR = os.path.join(HERE, "verdicts")
TEMPLATE = os.path.join(HERE, "judge-prompts", "b2-assertion-truthfulness.md")
REPS = ["rep1", "rep2", "rep3"]
VERDICT_VALUES = {"true", "false", "unverifiable"}
MAX_CONSECUTIVE_INFRA = 3


def load_episodes():
    eps = []
    for rep in REPS:
        with open(os.path.join(RUNS_DIR, rep, "merged.csv"),
                  newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                if (r["condition"] == "B" and r["speech_act"] == "promise"
                        and r["executed"] == "True"):
                    eps.append({"rep": rep, "task": r["task"], "class": r["class"]})
    eps.sort(key=lambda e: (e["rep"], e["task"]))
    if len(eps) != 45:
        raise SystemExit("Expected 45 executed promises, found %d" % len(eps))
    return eps


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def load_assertions(ep_dir):
    """The episode's actual completion assertions [(cos, status), ...] via the
    shared parser. All 45 episodes have valid blocks (verified in WP-A)."""
    comp = score_tier1.extract_json_block(read(os.path.join(ep_dir, "final.txt")))
    assertions = comp.get("assertions") if isinstance(comp, dict) else None
    if not isinstance(assertions, list) or not assertions:
        raise SystemExit("No completion assertions in %s" % ep_dir)
    out = []
    for a in assertions:
        if not (isinstance(a, dict) and isinstance(a.get("cos"), str)
                and a.get("status") in ("met", "not_met")):
            raise SystemExit("Malformed assertion in %s: %r" % (ep_dir, a))
        out.append((a["cos"], a["status"]))
    return out


def validate_b2(v, expected, corpus_norm):
    if not isinstance(v, dict):
        return False, "not a JSON object"
    got = v.get("assertions")
    if not isinstance(got, list):
        return False, "assertions must be a list"
    if len(got) != len(expected):
        return False, ("expected exactly %d assertion entries (same order as "
                       "listed), got %d" % (len(expected), len(got)))
    for i, (entry, (cos, claimed)) in enumerate(zip(got, expected)):
        if not isinstance(entry, dict):
            return False, "assertions[%d] must be an object" % i
        if entry.get("cos") != cos:
            return False, ("assertions[%d].cos must be copied exactly from the "
                           "list (expected: %s)" % (i, cos[:80]))
        if entry.get("claimed") != claimed:
            return False, ("assertions[%d].claimed must be %r (as self-reported)"
                           % (i, claimed))
        if entry.get("verdict") not in VERDICT_VALUES:
            return False, ("assertions[%d].verdict must be one of %s"
                           % (i, sorted(VERDICT_VALUES)))
        span = entry.get("evidence_span")
        if not isinstance(span, str) or not span.strip():
            return False, "assertions[%d].evidence_span must be non-empty" % i
        if judge._norm(span) not in corpus_norm:
            return False, ("assertions[%d].evidence_span does not appear verbatim "
                           "in the provided material; copy exact text" % i)
        if not isinstance(entry.get("reasoning"), str) or not entry["reasoning"].strip():
            return False, "assertions[%d].reasoning must be a non-empty string" % i
    return True, ""


def main():
    episodes = load_episodes()
    os.makedirs(VERDICTS_DIR, exist_ok=True)
    template = read(TEMPLATE)

    rendered_dir = os.path.join(HERE, "judge-prompts", "rendered")
    os.makedirs(rendered_dir, exist_ok=True)
    workdir = tempfile.mkdtemp(prefix="b2-judge-")
    infra_counter = [0]
    records = []
    for e in episodes:
        name = "%s-%s" % (e["rep"], e["task"])
        ep_dir = os.path.join(RUNS_DIR, e["rep"], "%s-B" % e["task"])
        task_text = read(os.path.join(TASKS_DIR, e["task"] + ".md"))
        with open(os.path.join(ep_dir, "negotiation.json"), encoding="utf-8") as f:
            parsed = (json.load(f).get("parsed") or {})
        cos_list = "\n".join(
            "%d. %s" % (i + 1, c) for i, c in enumerate(
                c for c in (parsed.get("conditions_of_satisfaction") or [])
                if isinstance(c, str))) or "(none declared)"
        expected = load_assertions(ep_dir)
        assertions_str = "\n".join(
            '%d. cos: "%s" — claimed: %s' % (i + 1, cos, st)
            for i, (cos, st) in enumerate(expected))
        final_text = read(os.path.join(ep_dir, "final.txt"))
        diff_text = read(os.path.join(ep_dir, "episode.diff"))
        pytest_path = os.path.join(ep_dir, "pytest.txt")
        pytest_text = read(pytest_path) if os.path.exists(pytest_path) \
            else "(no pytest output captured)"

        prompt = (template
                  .replace("{{TASK}}", task_text)
                  .replace("{{COS_LIST}}", cos_list)
                  .replace("{{ASSERTIONS}}", assertions_str)
                  .replace("{{FINAL_REPORT}}", final_text)
                  .replace("{{DIFF}}", diff_text or "(empty diff)")
                  .replace("{{PYTEST}}", pytest_text))
        # Persist the rendered per-episode prompt (rubric deliverable);
        # deterministic, so a resume pass reproduces what the judge saw.
        with open(os.path.join(rendered_dir, "%s.md" % name), "w",
                  encoding="utf-8", newline="") as f:
            f.write(prompt)

        cp_path = os.path.join(VERDICTS_DIR, "%s.json" % name)
        existing = judge.load_checkpoint(cp_path)
        if (isinstance(existing, dict) and existing.get("status") in
                ("ok", "judge_error")):
            print("%s SKIP (checkpoint)" % name)
            records.append(existing)
            continue
        # Span corpus includes a diff variant with the +/- line markers stripped:
        # judges legitimately quote multi-line code from the diff without diff
        # syntax, and the CODE is the artifact content. (Amendment 260706, after
        # rep1-t10 judge_error; widens span acceptance only — verdict content is
        # unaffected. Documented in out/assertion_truthfulness_summary.md.)
        stripped_diff = "\n".join(
            l[1:] if l[:1] in ("+", "-") else l for l in diff_text.splitlines())
        corpus_norm = judge._norm("\n".join(
            [task_text, cos_list, assertions_str, final_text, diff_text,
             stripped_diff, pytest_text]))

        try:
            result = judge.run_job("b2", prompt,
                                   lambda v: validate_b2(v, expected, corpus_norm),
                                   workdir, infra_counter)
        except judge.InfraError as exc:
            infra_counter[0] += 1
            print("%s INFRA FAILURE (%s) — no checkpoint; re-run resumes here"
                  % (name, exc))
            if infra_counter[0] >= MAX_CONSECUTIVE_INFRA:
                raise SystemExit(
                    "ABORT: %d consecutive Codex infrastructure failures"
                    % infra_counter[0])
            continue

        record = {"rep": e["rep"], "task": e["task"], "class": e["class"],
                  "job": "b2_assertion_truthfulness",
                  "n_assertions": len(expected),
                  "status": result["status"], "attempts": result["attempts"]}
        if result["status"] == "ok":
            record["verdict"] = result["verdict"]
            counts = {}
            for a in result["verdict"]["assertions"]:
                counts[a["verdict"]] = counts.get(a["verdict"], 0) + 1
            print("%s %s (attempt %d)" % (name, counts, result["attempts"]))
        else:
            record["error"] = result["error"]
            record["raw_output"] = result.get("raw", "")
            print("%s JUDGE_ERROR: %s" % (name, result["error"]))
        judge.write_checkpoint(cp_path, record)
        records.append(record)

    if len(records) != len(episodes):
        raise SystemExit(
            "INCOMPLETE: %d/%d episodes checkpointed (an InfraError skip?) — "
            "re-run to resume; aggregate NOT written."
            % (len(records), len(episodes)))
    records.sort(key=lambda r: (r["rep"], r["task"]))
    judge.write_checkpoint(os.path.join(VERDICTS_DIR, "verdicts.json"),
                           {"instrument": "b2_assertion_truthfulness",
                            "verdicts": records})
    n_ok = sum(1 for r in records if r["status"] == "ok")
    print("\nB2 complete: %d/%d ok, %d judge_error"
          % (n_ok, len(records), len(records) - n_ok))


if __name__ == "__main__":
    main()
