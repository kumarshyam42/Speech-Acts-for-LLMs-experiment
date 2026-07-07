#!/usr/bin/env python3
"""
h2 — B1n judge runner. Executes the LOCKED rubric in ../rubric-b1n.md: identical
to B1 (run_b1_judge.py) except the judge also receives the project's normative
documents (fixture/docs/requirements.md + fixture/CONTRIBUTING.md), uniformly for
every episode, and risk-flag spans may quote them. Same 45 episodes, same blind
labels and seed (per-episode pairing with B1), same machinery.

Writes ONLY: judge-prompts/rendered-b1n/, verdicts-b1n/. Stdlib Py3.9.
"""

import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
EXPERIMENT = os.path.dirname(os.path.dirname(HERE))
FIXTURE = os.path.join(EXPERIMENT, "fixture")
TASKS_DIR = os.path.join(EXPERIMENT, "tasks")
sys.path.insert(0, os.path.join(EXPERIMENT, "harness"))
import judge  # noqa: E402

sys.path.insert(0, HERE)
import importlib.util
_spec = importlib.util.spec_from_file_location(
    "run_b1_judge", os.path.join(HERE, "run_b1_judge.py"))
b1 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(b1)  # reuse load_episodes / render_contract / validate_b1

VERDICTS_DIR = os.path.join(HERE, "verdicts-b1n")
TEMPLATE = os.path.join(HERE, "judge-prompts", "b1n-veto-readability-with-rules.md")
MAX_CONSECUTIVE_INFRA = 3


def main():
    episodes = b1.load_episodes()  # same 45, same seed-260706 labels as B1
    os.makedirs(VERDICTS_DIR, exist_ok=True)
    rendered_dir = os.path.join(HERE, "judge-prompts", "rendered-b1n")
    os.makedirs(rendered_dir, exist_ok=True)
    with open(TEMPLATE, encoding="utf-8") as f:
        template = f.read()
    with open(os.path.join(FIXTURE, "docs", "requirements.md"),
              encoding="utf-8") as f:
        requirements = f.read()
    with open(os.path.join(FIXTURE, "CONTRIBUTING.md"), encoding="utf-8") as f:
        contributing = f.read()

    label_map = {e["label"]: {"rep": e["rep"], "task": e["task"],
                              "class": e["class"]} for e in episodes}
    judge.write_checkpoint(os.path.join(VERDICTS_DIR, "label_map.json"), label_map)

    workdir = tempfile.mkdtemp(prefix="b1n-judge-")
    infra_counter = [0]
    records = []
    for e in sorted(episodes, key=lambda x: x["label"]):
        task_text = open(os.path.join(TASKS_DIR, e["task"] + ".md"),
                         encoding="utf-8").read()
        contract = b1.render_contract(e)
        prompt = (template
                  .replace("{{TASK}}", task_text)
                  .replace("{{CONTRACT}}", contract)
                  .replace("{{REQUIREMENTS}}", requirements)
                  .replace("{{CONTRIBUTING}}", contributing))
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

        # Span corpus per the locked rubric: task + contract + the rules.
        corpus_norm = judge._norm(
            "\n".join([task_text, contract, requirements, contributing]))

        try:
            result = judge.run_job("b1n", prompt,
                                   lambda v: b1.validate_b1(v, corpus_norm),
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
                  "class": e["class"], "job": "b1n_veto_readability_with_rules",
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
            "INCOMPLETE: %d/%d episodes checkpointed — re-run to resume; "
            "aggregate NOT written." % (len(records), len(episodes)))
    records.sort(key=lambda r: r["label"])
    judge.write_checkpoint(os.path.join(VERDICTS_DIR, "verdicts.json"),
                           {"instrument": "b1n_veto_readability_with_rules",
                            "seed": b1.SEED, "verdicts": records})
    n_ok = sum(1 for r in records if r["status"] == "ok")
    print("\nB1n complete: %d/%d ok, %d judge_error"
          % (n_ok, len(records), len(records) - n_ok))


if __name__ == "__main__":
    main()
