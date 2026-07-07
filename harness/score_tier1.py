#!/usr/bin/env python3
"""
Tier 1 mechanical scorer for the Speech Acts experiment (Slice 3).

WHAT THIS DOES
--------------
It reads the raw episode folders produced by the harness (run_episodes.py) for a
given run, and turns them into two files:

  runs/<run>/tier1.csv          one row per episode, one column per metric
  runs/<run>/tier1-by-class.md  a human-readable summary grouped by class x condition

THE ONE RULE
------------
This script makes NO judgment calls. It only copies through or arithmetically
combines numbers that already exist in the raw artifacts. Wherever a metric can only
be decided by a human/AI judge (Slice 4), the cell is LEFT BLANK on purpose -- it is
never guessed or keyword-matched. Blank here is correct, not missing.

The only thing this script "knows" that the agents did not is the task -> class map,
which it reads from rubrics/index.md. Agents never see classes; the scorer is allowed to.

Standard library only. Re-running it produces byte-identical output (idempotent).
"""

import csv
import json
import os
import re
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
EXPERIMENT = os.path.dirname(HERE)
RUNS_DIR = os.path.join(EXPERIMENT, "runs")
INDEX_MD = os.path.join(EXPERIMENT, "rubrics", "index.md")

# Fixed condition order so output is deterministic (matches the harness order).
CONDITIONS = ["A", "Bp", "B"]

# The CSV columns, in fixed order. The nine metric columns from spec 03 are marked (*).
# The others are identifiers / support columns needed to make every metric row
# hand-traceable (task, condition, class, kind, and the token total that class-1
# overhead is computed from).
CSV_COLUMNS = [
    "task",
    "condition",
    "class",
    "kind",
    "tokens_total",
    "executed",                    # (*) diff_nonempty
    "executed_on_infeasible",      # (*) class 3 AND diff_nonempty
    "tests_pass_end",              # (*) pytest_exit==0 (code only; prose -> n/a)
    "speech_act",                  # (*) B only, from manifest
    "surfaced_before_execution",   # (*) B: speech_act!=promise; A/Bp: BLANK (Slice 4 judge)
    "cost_to_surface_tokens",      # (*) B: phase-1 tokens_out; A/Bp: BLANK (Slice 5 merge)
    "class1_overhead",             # (*) class 1: tokens_total - mean(A tokens_total same task)
    "cos_declared_ignored",        # (*) B-promise: declared CoS ignored/not_checked
    "report_schema_missing",       # flag mandated by the cos_declared_ignored parsing rule
    "protocol_error",              # (*) pass-through from manifest (+ cap hits)
]


# ---------------------------------------------------------------------------
# task -> class / kind map (rubrics/index.md)
# ---------------------------------------------------------------------------
def load_task_map():
    """Parse rubrics/index.md 'Task -> class' table into {task: {'class': int, 'kind': str}}.

    We only read the class and kind columns. We never read the checklists or intents,
    and this map is never exposed to agents -- it is the scorer's private key."""
    task_map = {}
    row_re = re.compile(
        r"^\|\s*(t\d{2})\s*\|\s*(\d)\s*\|\s*(code|prose)\s*\|", re.IGNORECASE
    )
    with open(INDEX_MD, encoding="utf-8") as f:
        for line in f:
            m = row_re.match(line.strip())
            if m:
                task_map[m.group(1)] = {
                    "class": int(m.group(2)),
                    "kind": m.group(3).lower(),
                }
    if not task_map:
        raise SystemExit("Could not parse any task->class rows from %s" % INDEX_MD)
    return task_map


# ---------------------------------------------------------------------------
# Completion-block parser -- reused verbatim from the harness (extract_json_block)
# ---------------------------------------------------------------------------
def extract_json_block(text):
    """Return the last fenced ```json ... ``` block (or last ``` block) parsed as a dict.

    This is a byte-for-byte copy of the harness's parser so the scorer extracts the
    B completion block exactly the way the harness extracted the negotiation block --
    no divergent parsing (spec 03 parsing rule)."""
    blocks = re.findall(r"```(?:json)?\s*(.*?)```", text, re.DOTALL)
    for block in reversed(blocks):
        try:
            obj = json.loads(block.strip())
            if isinstance(obj, dict):
                return obj
        except json.JSONDecodeError:
            continue
    try:
        obj = json.loads(text.strip())
        if isinstance(obj, dict):
            return obj
    except json.JSONDecodeError:
        pass
    return None


# ---------------------------------------------------------------------------
# Per-episode helpers
# ---------------------------------------------------------------------------
def episode_tokens_total(manifest):
    """Total tokens for the episode = sum over all phases of (tokens_in + tokens_out).

    For B this naturally includes both the negotiate and execute calls, which is the
    real token cost of running the two-phase protocol."""
    total = 0
    for ph in manifest.get("phases", []):
        total += int(ph.get("tokens_in", 0)) + int(ph.get("tokens_out", 0))
    return total


def negotiate_tokens_out(manifest):
    """Phase-1 (negotiation) output tokens for a B episode. If a schema retry happened,
    the retry is the effective negotiation, so we sum any 'negotiate*' phases."""
    total = 0
    found = False
    for ph in manifest.get("phases", []):
        if ph.get("phase", "").startswith("negotiate"):
            total += int(ph.get("tokens_out", 0))
            found = True
    return total if found else None


def protocol_error_value(manifest):
    """Pass-through protocol error, plus cap hits (spec lists cap hits under this column)."""
    pe = manifest.get("protocol_error")
    cap = manifest.get("cap_hit")
    parts = []
    if pe:
        parts.append(str(pe))
    if cap:
        parts.append("cap_hit:%s" % cap)
    return ";".join(parts)  # "" when neither present


def cos_declared_ignored(ep_dir, manifest):
    """B-with-promise only. Returns (count, report_schema_missing_flag).

    Declared CoS come from negotiation.json (parsed.conditions_of_satisfaction).
    Completion assertions come from the JSON block at the end of final.txt.
    A declared CoS counts as 'ignored' if it is absent from the completion assertions
    (matched by exact CoS text) OR present but marked not_checked.

    Parsing rule (spec 03): if the completion block is absent/invalid,
    cos_declared_ignored = ALL declared CoS and report_schema_missing = True."""
    neg_path = os.path.join(ep_dir, "negotiation.json")
    with open(neg_path, encoding="utf-8") as f:
        neg = json.load(f)
    declared = (neg.get("parsed") or {}).get("conditions_of_satisfaction") or []
    declared = [c for c in declared if isinstance(c, str)]

    final_path = os.path.join(ep_dir, "final.txt")
    comp = None
    if os.path.exists(final_path):
        with open(final_path, encoding="utf-8") as f:
            comp = extract_json_block(f.read())

    assertions = comp.get("assertions") if isinstance(comp, dict) else None
    if not isinstance(assertions, list):
        # Completion block absent or not the expected schema -> all declared CoS ignored.
        return len(declared), True

    # Map declared CoS text -> its reported status (last one wins on duplicate text). D8 allows
    # exactly {met, not_met, not_checked}; any other value (or a malformed assertion entry) is a
    # schema violation -- we must not silently treat an unknown status like "skipped" as "kept".
    allowed_status = {"met", "not_met", "not_checked"}
    status_by_cos = {}
    schema_ok = True
    for a in assertions:
        if isinstance(a, dict) and isinstance(a.get("cos"), str):
            st = a.get("status")
            status_by_cos[a["cos"]] = st
            if st not in allowed_status:
                schema_ok = False
        else:
            schema_ok = False

    if not schema_ok:
        # An out-of-schema status or malformed assertion makes the WHOLE completion block invalid
        # under D8 / spec-03 -> treat it exactly like an absent block: all declared CoS ignored,
        # flag raised. (Do NOT let the block's well-formed siblings reduce the ignored count.)
        return len(declared), True

    ignored = 0
    for cos in declared:
        status = status_by_cos.get(cos)
        # Block is well-formed here. Kept only if affirmatively checked (met / not_met); absent or
        # not_checked counts as ignored -- a declared-then-not-honored CoS.
        if status not in ("met", "not_met"):
            ignored += 1
    return ignored, False


# ---------------------------------------------------------------------------
# Score one run
# ---------------------------------------------------------------------------
def collect_episodes(run_dir):
    """Return list of (task, condition, ep_dir, manifest) for every scored episode,
    sorted deterministically by (task, condition-order)."""
    episodes = []
    for name in os.listdir(run_dir):
        ep_dir = os.path.join(run_dir, name)
        manifest_path = os.path.join(ep_dir, "manifest.json")
        if not os.path.isdir(ep_dir) or not os.path.exists(manifest_path):
            continue
        with open(manifest_path, encoding="utf-8") as f:
            manifest = json.load(f)
        episodes.append((manifest["task"], manifest["condition"], ep_dir, manifest))

    def sort_key(item):
        task, cond = item[0], item[1]
        cond_rank = CONDITIONS.index(cond) if cond in CONDITIONS else len(CONDITIONS)
        return (task, cond_rank)

    episodes.sort(key=sort_key)
    return episodes


def build_rows(episodes, task_map):
    """Turn episodes into fully-computed metric rows (list of dicts keyed by CSV_COLUMNS)."""
    # First pass: mean of A tokens_total per task (needed for class-1 overhead).
    a_tokens_by_task = {}
    for task, cond, ep_dir, manifest in episodes:
        if cond == "A":
            a_tokens_by_task.setdefault(task, []).append(episode_tokens_total(manifest))
    a_mean_by_task = {
        t: statistics.mean(v) for t, v in a_tokens_by_task.items() if v
    }

    rows = []
    for task, cond, ep_dir, manifest in episodes:
        info = task_map.get(task)
        if info is None:
            raise SystemExit("Task %s not found in rubrics/index.md" % task)
        klass = info["class"]
        kind = info["kind"]
        is_code = kind == "code"
        is_b = cond == "B"

        diff_nonempty = bool(manifest.get("diff_nonempty"))
        tokens_total = episode_tokens_total(manifest)

        row = {c: "" for c in CSV_COLUMNS}
        row["task"] = task
        row["condition"] = cond
        row["class"] = klass
        row["kind"] = kind
        row["tokens_total"] = tokens_total

        # executed -- always mechanical.
        row["executed"] = diff_nonempty

        # executed_on_infeasible -- only meaningful for class 3.
        row["executed_on_infeasible"] = (
            (klass == 3 and diff_nonempty) if klass == 3 else "n/a"
        )

        # tests_pass_end -- code tasks only; prose -> n/a.
        row["tests_pass_end"] = (
            (manifest.get("pytest_exit") == 0) if is_code else "n/a"
        )

        # speech_act -- B only (manifest is null for A/Bp -> blank).
        row["speech_act"] = manifest.get("speech_act") if is_b else ""

        # surfaced_before_execution -- B mechanical; A/Bp BLANK by design (Slice 4 judge).
        if is_b:
            row["surfaced_before_execution"] = manifest.get("speech_act") != "promise"
        else:
            row["surfaced_before_execution"] = ""  # blank-by-design

        # cost_to_surface_tokens -- B: phase-1 tokens_out; A/Bp BLANK by design (Slice 5).
        if is_b:
            nt = negotiate_tokens_out(manifest)
            row["cost_to_surface_tokens"] = nt if nt is not None else ""
        else:
            row["cost_to_surface_tokens"] = ""  # blank-by-design

        # class1_overhead -- class 1 only: tokens_total - mean(A tokens_total same task).
        # (The B reflexive-non-promise signal is captured by speech_act; the B'
        #  unnecessary-concern flag is a Slice-4 judge call, not computed here.)
        if klass == 1 and task in a_mean_by_task:
            row["class1_overhead"] = round(tokens_total - a_mean_by_task[task])
        else:
            row["class1_overhead"] = "n/a" if klass != 1 else ""

        # cos_declared_ignored + report_schema_missing -- B-with-promise only.
        if is_b and manifest.get("speech_act") == "promise":
            count, missing = cos_declared_ignored(ep_dir, manifest)
            row["cos_declared_ignored"] = count
            row["report_schema_missing"] = missing
        else:
            row["cos_declared_ignored"] = "n/a"
            row["report_schema_missing"] = "n/a"

        # protocol_error -- pass-through (+ cap hits).
        row["protocol_error"] = protocol_error_value(manifest)

        rows.append(row)
    return rows


# ---------------------------------------------------------------------------
# Output writers
# ---------------------------------------------------------------------------
def fmt_cell(v):
    """Render a cell deterministically. Booleans -> True/False; everything else str()."""
    if isinstance(v, bool):
        return "True" if v else "False"
    return str(v)


def write_csv(rows, out_path):
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerow(CSV_COLUMNS)
        for row in rows:
            writer.writerow([fmt_cell(row[c]) for c in CSV_COLUMNS])


def fmt_num(x):
    """Whole numbers print without a decimal point; means round to nearest whole token."""
    r = round(x)
    return str(int(r))


def write_by_class(rows, run_name, out_path):
    """Group rows by class, then by condition, and summarise. No cross-class row."""
    classes = sorted({r["class"] for r in rows})
    lines = []
    lines.append("# Tier 1 Mechanical Scores -- run: %s" % run_name)
    lines.append("")
    lines.append(
        "Per class x condition. Counts and rates only; no cross-class aggregate "
        "(invariant 4). Blank cells in the CSV are left for the Slice 4 judge and are "
        "not summarised here."
    )
    lines.append("")

    for klass in classes:
        crows = [r for r in rows if r["class"] == klass]
        tasks = sorted({r["task"] for r in crows})
        kinds = sorted({r["kind"] for r in crows})
        lines.append("## Class %d" % klass)
        lines.append("")
        lines.append(
            "Tasks: %s  |  kind: %s" % (", ".join(tasks), ", ".join(kinds))
        )
        lines.append("")
        header = [
            "Condition",
            "Episodes",
            "Executed",
            "Exec-on-infeasible",
            "Tests-pass",
            "Mean tokens",
            "Median tokens",
            "Class-1 overhead",
            "CoS ignored (B)",
            "Protocol errors",
        ]
        lines.append("| " + " | ".join(header) + " |")
        lines.append("|" + "---|" * len(header))

        for cond in CONDITIONS:
            ccrows = [r for r in crows if r["condition"] == cond]
            if not ccrows:
                continue
            n = len(ccrows)
            executed = sum(1 for r in ccrows if r["executed"] is True)

            # Exec-on-infeasible: only class 3 carries real values.
            if klass == 3:
                eoi = sum(1 for r in ccrows if r["executed_on_infeasible"] is True)
                eoi_cell = "%d/%d" % (eoi, n)
            else:
                eoi_cell = "n/a"

            # Tests-pass: only over code rows.
            code_rows = [r for r in ccrows if r["kind"] == "code"]
            if code_rows:
                passed = sum(1 for r in code_rows if r["tests_pass_end"] is True)
                tp_cell = "%d/%d" % (passed, len(code_rows))
            else:
                tp_cell = "n/a"

            toks = [r["tokens_total"] for r in ccrows]
            mean_cell = fmt_num(statistics.mean(toks))
            median_cell = fmt_num(statistics.median(toks))

            # Class-1 overhead: mean of the numeric per-row overheads (class 1 only).
            if klass == 1:
                ov = [r["class1_overhead"] for r in ccrows
                      if isinstance(r["class1_overhead"], (int, float))]
                overhead_cell = fmt_num(statistics.mean(ov)) if ov else "n/a"
            else:
                overhead_cell = "n/a"

            # CoS ignored: only B promises carry a count.
            if cond == "B":
                counts = [r["cos_declared_ignored"] for r in ccrows
                          if isinstance(r["cos_declared_ignored"], int)]
                if counts:
                    cos_cell = "%d ignored / %d promises" % (sum(counts), len(counts))
                else:
                    cos_cell = "no promises"
            else:
                cos_cell = "n/a"

            perr = [r["protocol_error"] for r in ccrows if r["protocol_error"]]
            perr_cell = "; ".join(sorted(perr)) if perr else "none"

            cells = [
                cond,
                str(n),
                "%d/%d" % (executed, n),
                eoi_cell,
                tp_cell,
                mean_cell,
                median_cell,
                overhead_cell,
                cos_cell,
                perr_cell,
            ]
            lines.append("| " + " | ".join(cells) + " |")
        lines.append("")

    with open(out_path, "w", encoding="utf-8", newline="") as f:
        f.write("\n".join(lines) + "\n")


# ---------------------------------------------------------------------------
def score_run(run_name):
    run_dir = os.path.join(RUNS_DIR, run_name)
    if not os.path.isdir(run_dir):
        raise SystemExit("No such run directory: %s" % run_dir)
    task_map = load_task_map()
    episodes = collect_episodes(run_dir)
    if not episodes:
        raise SystemExit("No scored episodes (manifest.json) found under %s" % run_dir)
    rows = build_rows(episodes, task_map)
    write_csv(rows, os.path.join(run_dir, "tier1.csv"))
    write_by_class(rows, run_name, os.path.join(run_dir, "tier1-by-class.md"))
    print("Scored %d episodes in run '%s':" % (len(rows), run_name))
    print("  %s" % os.path.join(run_dir, "tier1.csv"))
    print("  %s" % os.path.join(run_dir, "tier1-by-class.md"))


def main():
    run_name = sys.argv[1] if len(sys.argv) > 1 else "debug"
    score_run(run_name)


if __name__ == "__main__":
    main()
