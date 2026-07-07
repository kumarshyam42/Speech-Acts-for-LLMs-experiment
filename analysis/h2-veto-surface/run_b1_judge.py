#!/usr/bin/env python3
"""
h2 (veto surface) — B1 judge runner. Executes the LOCKED rubric in ../rubric.md.

Scope: all 45 executed B promises (12 class-4 + 14 class-2 + 18 class-1 controls
+ 1 class-3 extra, per the signed-off rubric). One Codex call per episode; the
judge sees ONLY the task text and the phase-1 contract, under a blind label in a
seed-260706 shuffled order.

Reuses harness/judge.py machinery verbatim: call_codex (InfraError contract),
parse_verdict_json, _norm span matching, run_job retry-then-judge_error,
write_checkpoint atomic checkpoints. Resume-first: valid checkpoints are never
re-run; InfraErrors leave no checkpoint; 3 consecutive InfraErrors abort.

Writes ONLY under this folder: verdicts/E??.json + verdicts/label_map.json +
verdicts/verdicts.json. Never touches runs/ or the original judge dirs.
Standard library only, Python 3.9.
"""

import csv
import json
import os
import random
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
EXPERIMENT = os.path.dirname(os.path.dirname(HERE))
RUNS_DIR = os.path.join(EXPERIMENT, "runs")
TASKS_DIR = os.path.join(EXPERIMENT, "tasks")
HARNESS = os.path.join(EXPERIMENT, "harness")
sys.path.insert(0, HARNESS)
import judge  # noqa: E402  (call_codex, parse_verdict_json, _norm, run_job, checkpoints)

VERDICTS_DIR = os.path.join(HERE, "verdicts")
TEMPLATE = os.path.join(HERE, "judge-prompts", "b1-veto-readability.md")
REPS = ["rep1", "rep2", "rep3"]
SEED = 260706
ACCEPT_VALUES = {"yes", "yes_with_conditions", "no"}
MAX_CONSECUTIVE_INFRA = 3


def load_episodes():
    """All executed B promises, deterministically ordered, then seed-shuffled
    into blind labels E01..E45."""
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
    random.Random(SEED).shuffle(eps)
    for i, e in enumerate(eps):
        e["label"] = "E%02d" % (i + 1)
    return eps


def render_contract(ep):
    with open(os.path.join(RUNS_DIR, ep["rep"], "%s-B" % ep["task"],
                           "negotiation.json"), encoding="utf-8") as f:
        parsed = (json.load(f).get("parsed") or {})
    lines = ["Typed act: %s" % parsed.get("speech_act", "?"), ""]
    lines.append("Conditions of satisfaction:")
    cos = [c for c in (parsed.get("conditions_of_satisfaction") or [])
           if isinstance(c, str)]
    if cos:
        lines.extend("%d. %s" % (i + 1, c) for i, c in enumerate(cos))
    else:
        lines.append("(none declared)")
    lines.append("")
    lines.append("Scope exclusions:")
    exc = [e for e in (parsed.get("scope_exclusions") or []) if isinstance(e, str)]
    if exc:
        lines.extend("%d. %s" % (i + 1, e) for i, e in enumerate(exc))
    else:
        lines.append("(none declared)")
    lines.append("")
    lines.append("Stated concern:")
    concern = parsed.get("concern")
    lines.append(concern if isinstance(concern, str) and concern.strip()
                 else "(none stated)")
    return "\n".join(lines)


def validate_b1(v, corpus_norm):
    if not isinstance(v, dict):
        return False, "not a JSON object"
    if v.get("accept") not in ACCEPT_VALUES:
        return False, "accept must be one of %s" % sorted(ACCEPT_VALUES)
    flags = v.get("risk_flags")
    if not isinstance(flags, list):
        return False, "risk_flags must be a list"
    for i, fl in enumerate(flags):
        if not isinstance(fl, dict):
            return False, "risk_flags[%d] must be an object" % i
        if not isinstance(fl.get("description"), str) or not fl["description"].strip():
            return False, "risk_flags[%d].description must be a non-empty string" % i
        span = fl.get("span")
        if not isinstance(span, str) or not span.strip():
            return False, "risk_flags[%d].span must be a non-empty string" % i
        if judge._norm(span) not in corpus_norm:
            return False, ("risk_flags[%d].span does not appear verbatim in the "
                           "request or contract; copy the exact words" % i)
    if v.get("accept") != "yes" and not flags:
        return False, "accept != yes requires at least one risk flag"
    pr = v.get("primary_risk")
    if not isinstance(pr, str):
        return False, "primary_risk must be a string"
    if flags and not pr.strip():
        return False, "primary_risk must name the top risk when flags exist"
    return True, ""


def main():
    episodes = load_episodes()
    os.makedirs(VERDICTS_DIR, exist_ok=True)
    with open(TEMPLATE, encoding="utf-8") as f:
        template = f.read()

    # Label map (identity is NEVER in the judge prompt).
    label_map = {e["label"]: {"rep": e["rep"], "task": e["task"],
                              "class": e["class"]} for e in episodes}
    judge.write_checkpoint(os.path.join(VERDICTS_DIR, "label_map.json"), label_map)

    rendered_dir = os.path.join(HERE, "judge-prompts", "rendered")
    os.makedirs(rendered_dir, exist_ok=True)
    workdir = tempfile.mkdtemp(prefix="b1-judge-")
    infra_counter = [0]
    records = []
    for e in sorted(episodes, key=lambda x: x["label"]):
        # Persist the rendered per-episode prompt (rubric deliverable). Prompt
        # construction is deterministic, so this reproduces exactly what the
        # judge saw even on a resume pass that skips the Codex call.
        task_text = open(os.path.join(TASKS_DIR, e["task"] + ".md"),
                         encoding="utf-8").read()
        contract = render_contract(e)
        prompt = template.replace("{{TASK}}", task_text).replace(
            "{{CONTRACT}}", contract)
        with open(os.path.join(rendered_dir, "%s.md" % e["label"]), "w",
                  encoding="utf-8", newline="") as f:
            f.write(prompt)

        cp_path = os.path.join(VERDICTS_DIR, "%s.json" % e["label"])
        existing = judge.load_checkpoint(cp_path)
        if (isinstance(existing, dict) and existing.get("status") in
                ("ok", "judge_error")):
            print("%s (%s/%s) SKIP (checkpoint)" % (e["label"], e["rep"], e["task"]))
            records.append(existing)
            continue

        corpus_norm = judge._norm(task_text + "\n" + contract)

        try:
            result = judge.run_job("b1", prompt,
                                   lambda v: validate_b1(v, corpus_norm),
                                   workdir, infra_counter)
        except judge.InfraError as exc:
            infra_counter[0] += 1
            print("%s INFRA FAILURE (%s) — no checkpoint; re-run resumes here"
                  % (e["label"], exc))
            if infra_counter[0] >= MAX_CONSECUTIVE_INFRA:
                raise SystemExit(
                    "ABORT: %d consecutive Codex infrastructure failures"
                    % infra_counter[0])
            continue

        record = {"label": e["label"], "rep": e["rep"], "task": e["task"],
                  "class": e["class"], "job": "b1_veto_readability",
                  "status": result["status"], "attempts": result["attempts"]}
        if result["status"] == "ok":
            record["verdict"] = result["verdict"]
            print("%s (%s/%s) accept=%s flags=%d (attempt %d)"
                  % (e["label"], e["rep"], e["task"],
                     result["verdict"]["accept"],
                     len(result["verdict"]["risk_flags"]), result["attempts"]))
        else:
            record["error"] = result["error"]
            record["raw_output"] = result.get("raw", "")
            print("%s JUDGE_ERROR: %s" % (e["label"], result["error"]))
        judge.write_checkpoint(cp_path, record)
        records.append(record)

    if len(records) != len(episodes):
        raise SystemExit(
            "INCOMPLETE: %d/%d episodes checkpointed (an InfraError skip?) — "
            "re-run to resume; aggregate NOT written."
            % (len(records), len(episodes)))
    records.sort(key=lambda r: r["label"])
    judge.write_checkpoint(os.path.join(VERDICTS_DIR, "verdicts.json"),
                           {"instrument": "b1_veto_readability", "seed": SEED,
                            "verdicts": records})
    n_ok = sum(1 for r in records if r["status"] == "ok")
    print("\nB1 complete: %d/%d ok, %d judge_error"
          % (n_ok, len(records), len(records) - n_ok))


if __name__ == "__main__":
    main()
