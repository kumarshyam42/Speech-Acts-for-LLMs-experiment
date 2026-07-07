#!/usr/bin/env python3
"""
Case-file inspector for the Speech Acts experiment (analysis tool, read-only).

Assembles, for any task, everything needed to analyse a failure by hand -- the task text, the
HIDDEN rubric (intent + tripwire + expected behavior), what each condition actually did (speech
act, self-declared conditions of satisfaction, diff, final report), and the cross-family judge's
verdicts (surfacing / localization / outcome) WITH their cited evidence spans -- in one readable
block. It reads only finished artifacts; it never runs an episode, judges anything, or writes to
the run. This is the tool used by hand to produce the t14 / t20 mechanism analyses.

USAGE
-----
    python inspect_episode.py --failures                 # index: every failed/degraded episode
    python inspect_episode.py t20                         # all conditions x reps for one task (compact)
    python inspect_episode.py t20 --cond B --rep rep1     # one episode, deep
    python inspect_episode.py t20 --full                  # include full diffs + final reports
    python inspect_episode.py t20 --rubric                # also print the full hidden rubric file

Notes: rubric/intent/tripwire come from rubrics/ -- this tool is for ANALYSIS after the run, so
seeing the hidden key is the point (agents never saw it). Standard library only, Python 3.9.
"""

import argparse
import csv
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
EXPERIMENT = os.path.dirname(HERE)
RUNS_DIR = os.path.join(EXPERIMENT, "runs")
TASKS_DIR = os.path.join(EXPERIMENT, "tasks")
RUBRICS_DIR = os.path.join(EXPERIMENT, "rubrics")
INDEX_MD = os.path.join(RUBRICS_DIR, "index.md")

CONDITIONS = ["A", "Bp", "B"]
COND_LABEL = {"A": "A (current practice)", "Bp": "B' (generic deliberation)", "B": "B (protocol)"}
CLASS_NAME = {1: "well-formed", 2: "underspecified", 3: "infeasible-as-stated",
              4: "hidden-constraint"}
DEFAULT_REPS = ["rep1", "rep2", "rep3"]


# ---------------------------------------------------------------------------
# rubrics/index.md parsing: class, kind, intent, tripwire, per-task checklist line
# ---------------------------------------------------------------------------
def load_index():
    """Return {task: {class, kind, intent, tripwire, checklist}}."""
    info = {}
    row_re = re.compile(
        r"^\|\s*(t\d{2})\s*\|\s*(\d)\s*\|\s*(code|prose)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|",
        re.IGNORECASE)
    check_re = re.compile(r"^-\s*\[.\]\s*(t\d{2})\s*[—-]\s*(.*)$")
    with open(INDEX_MD, encoding="utf-8") as f:
        for line in f:
            s = line.strip()
            m = row_re.match(s)
            if m:
                info.setdefault(m.group(1), {}).update(
                    {"class": int(m.group(2)), "kind": m.group(3).lower(),
                     "intent": m.group(4), "tripwire": m.group(5)})
                continue
            c = check_re.match(s)
            if c:
                info.setdefault(c.group(1), {})["checklist"] = c.group(2)
    return info


# ---------------------------------------------------------------------------
# per-run artifact loading
# ---------------------------------------------------------------------------
def load_merged(rep):
    path = os.path.join(RUNS_DIR, rep, "merged.csv")
    rows = {}
    if os.path.exists(path):
        with open(path, newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                rows[(r["task"], r["condition"])] = r
    return rows


def load_verdicts(rep):
    path = os.path.join(RUNS_DIR, rep, "judge", "verdicts.json")
    out = {}
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            for v in json.load(f).get("verdicts", []):
                out[(v["task"], v["condition"], v["job"])] = v
    return out


def read_text(path, limit=None):
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as f:
        t = f.read()
    if limit and len(t) > limit:
        return t[:limit] + "\n…[truncated %d chars]…" % (len(t) - limit)
    return t


def diff_files(diff_text):
    """List changed file paths from a unified diff."""
    files = []
    for m in re.finditer(r"^\+\+\+ b/(.+)$", diff_text or "", re.MULTILINE):
        files.append(m.group(1))
    if not files:  # intent-to-add / new files sometimes only show 'diff --git'
        for m in re.finditer(r"^diff --git a/.+ b/(.+)$", diff_text or "", re.MULTILINE):
            files.append(m.group(1))
    return files


def test_hunks(diff_text):
    """Pull '+/-' lines that touch tests/ -- the class-4 tell (editing a tripwire)."""
    out = []
    cur_file = None
    for line in (diff_text or "").splitlines():
        m = re.match(r"^\+\+\+ b/(.+)$", line)
        if m:
            cur_file = m.group(1)
        elif cur_file and "test" in cur_file and re.match(r"^[+-][^+-]", line):
            out.append(line)
    return out


# ---------------------------------------------------------------------------
# rendering
# ---------------------------------------------------------------------------
def fmt_verdict(v, job):
    if v is None:
        return "—"
    if v.get("status") == "judge_error":
        return "JUDGE_ERROR (%s)" % v.get("error", "")[:80]
    vd = v.get("verdict", {})
    if job == "job1_surfacing":
        s = "surfaced=%s" % vd.get("surfaced_before_execution")
        if vd.get("span"):
            s += "\n        span: %s" % vd["span"].strip()[:240]
        return s
    if job == "job2_localization":
        s = "localization=%s" % vd.get("localization")
        if vd.get("reason"):
            s += "\n        reason: %s" % vd["reason"].strip()[:280]
        if vd.get("span"):
            s += "\n        span: %s" % vd["span"].strip()[:240]
        return s
    if job == "job3_outcome":
        s = "%s / %s" % (vd.get("outcome"), vd.get("gradient_level"))
        if vd.get("evidence"):
            s += "\n        evidence: %s" % vd["evidence"].strip()[:240]
        return s
    return str(vd)


def render_episode(task, cond, rep, info, merged, verdicts, full=False):
    key = (task, cond)
    row = merged.get(key)
    ep_dir = os.path.join(RUNS_DIR, rep, "%s-%s" % (task, cond))
    out = []
    out.append("  ── %s — %s ──" % (COND_LABEL[cond], rep))
    if row is None:
        out.append("    (no merged row / episode missing)")
        return "\n".join(out)

    # Mechanical line
    out.append("    executed=%s  tests_pass=%s  exec_on_infeasible=%s"
               % (row["executed"], row["tests_pass_end"], row["executed_on_infeasible"]))
    out.append("    surfaced_before_exec=%s  cost_to_surface=%s  tokens=%s"
               % (row["surfaced_before_execution"] or "—",
                  row["cost_to_surface_tokens"] or "—", row["tokens_total"]))

    # Condition B: the promise + its self-authored CoS, and CoS integrity
    if cond == "B":
        neg = read_text(os.path.join(ep_dir, "negotiation.json"))
        if neg:
            try:
                p = (json.loads(neg).get("parsed") or {})
                out.append("    speech_act=%s   cos_declared_ignored=%s  report_schema_missing=%s"
                           % (p.get("speech_act"), row["cos_declared_ignored"],
                              row["report_schema_missing"]))
                cos = p.get("conditions_of_satisfaction") or []
                if cos:
                    out.append("    conditions of satisfaction it set for itself:")
                    for c in cos:
                        out.append("      - %s" % c)
                if p.get("concern"):
                    out.append("    concern: %s" % p["concern"])
                if p.get("scope_exclusions"):
                    out.append("    scope_exclusions: %s" % p["scope_exclusions"])
            except json.JSONDecodeError:
                pass

    # Judge verdicts
    j1 = verdicts.get((task, cond, "job1_surfacing"))
    j2 = verdicts.get((task, cond, "job2_localization"))
    j3 = verdicts.get((task, cond, "job3_outcome"))
    out.append("    JUDGE:")
    if cond in ("A", "Bp"):
        out.append("      surfacing:    %s" % fmt_verdict(j1, "job1_surfacing"))
    out.append("      outcome:      %s" % fmt_verdict(j3, "job3_outcome"))
    out.append("      localization: %s" % fmt_verdict(j2, "job2_localization"))

    # Diff (what it actually touched) + the test-edit tell
    diff = read_text(os.path.join(ep_dir, "episode.diff"))
    files = diff_files(diff or "")
    out.append("    DIFF files: %s" % (", ".join(files) if files else "(none — empty diff)"))
    hunks = test_hunks(diff or "")
    if hunks:
        out.append("    !! test-file edits (class-4 tripwire tell):")
        for h in hunks[:8]:
            out.append("       %s" % h)

    if full:
        fr = read_text(os.path.join(ep_dir, "final.txt"), limit=1600)
        out.append("    FINAL REPORT:\n" + "\n".join("      " + l for l in (fr or "").splitlines()))
        if diff:
            out.append("    FULL DIFF:\n" + "\n".join("      " + l for l in diff.splitlines()[:120]))
    return "\n".join(out)


def render_task(task, info, reps, conds, full=False, show_rubric=False):
    ti = info.get(task, {})
    out = []
    out.append("=" * 78)
    out.append("### %s — class %s (%s), %s"
               % (task, ti.get("class"), CLASS_NAME.get(ti.get("class"), "?"), ti.get("kind")))
    out.append("INTENT:   %s" % ti.get("intent", "?"))
    if ti.get("tripwire") and ti["tripwire"] not in ("n/a", ""):
        out.append("TRIPWIRE: %s" % ti["tripwire"])
    if ti.get("checklist"):
        out.append("EXPECTED (rubric): %s" % ti["checklist"])
    out.append("TASK TEXT:")
    tt = read_text(os.path.join(TASKS_DIR, task + ".md")) or ""
    out.append("\n".join("  " + l for l in tt.strip().splitlines()))
    if show_rubric:
        rb = read_text(os.path.join(RUBRICS_DIR, "r" + task[1:] + ".md"))
        out.append("\nFULL HIDDEN RUBRIC (r%s.md):" % task[1:])
        out.append("\n".join("  " + l for l in (rb or "").strip().splitlines()))
    out.append("")
    for rep in reps:
        merged = load_merged(rep)
        verdicts = load_verdicts(rep)
        for cond in conds:
            out.append(render_episode(task, cond, rep, info, merged, verdicts, full=full))
            out.append("")
    return "\n".join(out)


# ---------------------------------------------------------------------------
# failure index
# ---------------------------------------------------------------------------
def is_int_pos(x):
    try:
        return int(x) > 0
    except (ValueError, TypeError):
        return False


def failure_flags(row):
    """Return a list of reasons this episode is 'interesting' (failed/degraded/taxed)."""
    flags = []
    klass = int(row["class"])
    if row["job3_outcome"] in ("fail", "partial"):
        flags.append("outcome=%s" % row["job3_outcome"])
    if str(row["executed_on_infeasible"]) == "True":
        flags.append("executed-on-infeasible")
    if row["kind"] == "code" and str(row["tests_pass_end"]) == "False":
        flags.append("tests-fail")
    if is_int_pos(row["cos_declared_ignored"]):
        flags.append("CoS-ignored=%s" % row["cos_declared_ignored"])
    if str(row["report_schema_missing"]) == "True":
        flags.append("report-schema-missing")
    if row["protocol_error"]:
        flags.append("protocol_error=%s" % row["protocol_error"])
    if row["job2_localization"]:
        flags.append("loc=%s" % row["job2_localization"])
    # class-1 tax signals
    if klass == 1:
        if row["condition"] == "B" and row["speech_act"] not in ("promise", "", None):
            flags.append("reflexive-%s" % row["speech_act"])
        if row["condition"] in ("A", "Bp") and str(row["surfaced_before_execution"]) == "True":
            flags.append("unnecessary-concern")
    return flags


def failure_index(reps):
    info = load_index()
    lines = ["# Failure / degradation index — reps: %s" % ", ".join(reps),
             "(one line per interesting episode; drill in with: inspect_episode.py <task> --cond <C> --rep <rep>)",
             ""]
    by_task = {}
    for rep in reps:
        for (task, cond), row in load_merged(rep).items():
            flags = failure_flags(row)
            if flags:
                by_task.setdefault(task, []).append((rep, cond, flags))
    total = 0
    for task in sorted(by_task):
        ti = info.get(task, {})
        lines.append("## %s — class %s (%s): %s"
                     % (task, ti.get("class"), CLASS_NAME.get(ti.get("class"), "?"),
                        ti.get("intent", "")))
        for rep, cond, flags in sorted(by_task[task], key=lambda x: (CONDITIONS.index(x[1]), x[0])):
            lines.append("   %-3s %-5s  %s" % (cond, rep, "; ".join(flags)))
            total += 1
        lines.append("")
    lines.insert(2, "TOTAL flagged episodes: %d\n" % total)
    return "\n".join(lines)


# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description="Speech Acts episode case-file inspector (read-only)")
    ap.add_argument("task", nargs="?", help="task id, e.g. t20")
    ap.add_argument("--cond", choices=CONDITIONS, help="restrict to one condition")
    ap.add_argument("--rep", help="restrict to one rep (rep1/rep2/rep3/debug)")
    ap.add_argument("--full", action="store_true", help="include full diffs + final reports")
    ap.add_argument("--rubric", action="store_true", help="also print the full hidden rubric file")
    ap.add_argument("--failures", action="store_true", help="print the failure/degradation index")
    ap.add_argument("--reps", default=",".join(DEFAULT_REPS), help="comma reps (default rep1,rep2,rep3)")
    args = ap.parse_args()

    reps = [args.rep] if args.rep else [r.strip() for r in args.reps.split(",") if r.strip()]

    if args.failures:
        print(failure_index(reps))
        return
    if not args.task:
        ap.error("give a task id (e.g. t20) or use --failures")

    info = load_index()
    conds = [args.cond] if args.cond else CONDITIONS
    print(render_task(args.task, info, reps, conds, full=args.full, show_rubric=args.rubric))


if __name__ == "__main__":
    main()
