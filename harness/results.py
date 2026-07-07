#!/usr/bin/env python3
"""
Slice 5 merge + results assembly for the Speech Acts experiment.

WHAT THIS DOES
--------------
This is the LAST stage of the pipeline. For each run it:

  1. MERGES the Tier-1 mechanical scores (runs/<run>/tier1.csv) with the Tier-2
     Codex judge verdicts (runs/<run>/judge/verdicts.json) into one row per episode,
     written to runs/<run>/merged.csv.
  2. FILLS the two columns Slice 3 deliberately left blank for A and B' episodes:
        - surfaced_before_execution  <- Job-1 (surfacing) verdict boolean
        - cost_to_surface_tokens     <- output tokens produced up to the cited span
     (For Condition B these were already computed mechanically in Slice 3 and are
     passed through unchanged: surfaced = speech_act != promise; cost = phase-1
     tokens_out.)
  3. ASSEMBLES results/<date>-results.md: PER-CLASS tables only (invariant 4 -- never
     a cross-class aggregate score), covering H-Loc (primary), H-Behav, the class-1
     tax, and the H0 ledger, then the design doc's pre-registered interpretation table
     with a factual note per row.
  4. Writes results/costs.md: per-rep token totals and judge-call counts.

HOW cost_to_surface_tokens IS COMPUTED FOR A / B'  (the one non-trivial merge)
------------------------------------------------------------------------------
The design doc defines it as "tokens up to the classifier-cited span ... from
transcript offsets" and leaves the exact mechanism to this merge stage. The CLI's
stream-json splits a single assistant message across several JSONL lines and repeats
the same tiny per-message usage.output_tokens on each, so per-event token counts do
NOT reconcile with the authoritative per-episode total. Relying on them would be
wrong. Instead we apportion the AUTHORITATIVE output-token total (manifest phase
tokens_out, which equals the CLI `result` event's usage.output_tokens) across the
transcript by CHARACTER OFFSET of the agent's own rendered output:

    cost_to_surface = round( tokens_out_total
                             * agent_chars_up_to_and_including_span_event
                             / total_agent_chars )

"agent output" = the exact rendered text of assistant-text and tool_use events, i.e.
what the judge saw and matched the span against (tool_result events are the agent's
INPUT, not output, so they are excluded). This is deterministic, reconciles to the
real output-token total, uses transcript offsets exactly as the design specifies, and
makes no judgment call. It is logged as a Slice-5 implementation decision in
spec/decisions-log.md. The span event index is RE-DERIVED here by re-matching the
verbatim span with the judge's own renderer/verifier (not read from the free-text
span_locator string), so it is consistent with how the judge validated it.

INTEGRITY
---------
This script only reads finished artifacts and does arithmetic/tabulation. It never
re-runs an episode, never edits a transcript, never makes a surfacing/outcome
judgment (those are the judge's). Blank stays blank where a judge verdict is missing
or errored -- never guessed. Standard library only, Python 3.9 compatible, idempotent.

USAGE
-----
    python results.py --runs debug                 # validate the pipeline on debug
    python results.py --runs rep1,rep2,rep3         # the real report (pools 3 reps)
    python results.py --runs rep1,rep2,rep3 --date 260705
"""

import argparse
import csv
import json
import os
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
EXPERIMENT = os.path.dirname(HERE)
RUNS_DIR = os.path.join(EXPERIMENT, "runs")
RESULTS_DIR = os.path.join(EXPERIMENT, "results")

# Reuse the judge's transcript renderer + span verifier (identical event indexing) and
# the Tier-1 scorer's token helpers (identical token accounting). Importing is safe:
# both guard their CLIs behind __main__.
sys.path.insert(0, HERE)
import judge          # noqa: E402
import score_tier1    # noqa: E402

CONDITIONS = ["A", "Bp", "B"]
COND_LABEL = {"A": "A (current practice)", "Bp": "B' (generic deliberation)",
              "B": "B (protocol)"}
CLASS_NAME = {1: "Well-formed", 2: "Underspecified", 3: "Infeasible-as-stated",
              4: "Hidden-constraint"}
LOC_ORDER = ["a_never_surfaced", "b_cos_unmet", "c_wrong_cos", "d_execution_bug",
             "cannot_attribute"]


# ---------------------------------------------------------------------------
# Loading finished artifacts
# ---------------------------------------------------------------------------
def load_tier1_rows(run_dir):
    """{(task, cond): rowdict} from tier1.csv. Source of truth for class/kind/mechanical."""
    path = os.path.join(run_dir, "tier1.csv")
    if not os.path.exists(path):
        raise SystemExit("Missing %s -- run score_tier1.py for this run first." % path)
    rows = {}
    with open(path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            rows[(r["task"], r["condition"])] = r
    return rows


def load_verdicts(run_dir):
    """{(task, cond, job): record} from judge/verdicts.json. Empty dict if not judged yet."""
    path = os.path.join(run_dir, "judge", "verdicts.json")
    out = {}
    if not os.path.exists(path):
        return out
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    for rec in data.get("verdicts", []):
        out[(rec["task"], rec["condition"], rec["job"])] = rec
    return out


def load_manifest(ep_dir):
    with open(os.path.join(ep_dir, "manifest.json"), encoding="utf-8") as f:
        return json.load(f)


def phase_tokens_out_total(manifest):
    """Authoritative output tokens for the whole episode = sum of phase tokens_out.
    (For A/B' one phase; for B, negotiate + execute -- but A/B' are the only ones that
    need char-offset apportionment; B's cost_to_surface is phase-1 tokens_out already.)"""
    return sum(int(ph.get("tokens_out", 0)) for ph in manifest.get("phases", []))


# ---------------------------------------------------------------------------
# The one non-trivial computation: A/B' cost-to-surface via char-offset apportionment
# ---------------------------------------------------------------------------
def cost_to_surface_ab(ep_dir, cond, manifest, job1_rec):
    """Return (surfaced, cost, note) for an A or B' episode.

    surfaced : True / False / "" (unknown -- judge_error or missing verdict)
    cost     : int tokens, or "" when not surfaced / unknown
    note     : short string for the H0 / judge-error ledger ("" when clean)
    """
    if job1_rec is None:
        return "", "", "job1_missing"
    if job1_rec.get("status") != "ok":
        return "", "", "job1_%s" % job1_rec.get("status", "error")

    v = job1_rec["verdict"]
    surfaced = bool(v.get("surfaced_before_execution"))
    if not surfaced:
        return False, "", ""

    span = v.get("span", "")
    _display, events = judge.render_transcript(ep_dir, cond)
    found, idx = judge.verify_span(span, events, roles={"assistant"})
    if not found or idx is None:
        # Should not happen: the judge only stores surfaced=True after verifying the span
        # verbatim in assistant text. If artifacts drifted, do NOT fabricate a number.
        return True, "", "job1_span_unresolved"

    agent_events = [ev for ev in events if ev["role"] in ("assistant", "tool_use")]
    total_chars = sum(len(ev["text"]) for ev in agent_events)
    if total_chars == 0:
        return True, "", "no_agent_output"
    prefix_chars = sum(len(ev["text"]) for ev in agent_events if ev["idx"] <= idx)
    tokens_out_total = phase_tokens_out_total(manifest)
    cost = round(tokens_out_total * prefix_chars / total_chars)
    return True, cost, ""


# ---------------------------------------------------------------------------
# Build the merged per-episode records for one run
# ---------------------------------------------------------------------------
MERGED_COLUMNS = [
    "run", "task", "condition", "class", "kind",
    "tokens_total", "executed", "executed_on_infeasible", "tests_pass_end",
    "speech_act", "surfaced_before_execution", "cost_to_surface_tokens",
    "class1_overhead", "cos_declared_ignored", "report_schema_missing", "protocol_error",
    # judge-derived:
    "job1_status", "job2_localization", "job2_status", "job3_outcome", "job3_gradient",
    "job3_status", "judged_failure", "merge_note",
]


def _as_bool(s):
    return str(s) == "True"


def build_merged(run_name):
    run_dir = os.path.join(RUNS_DIR, run_name)
    if not os.path.isdir(run_dir):
        raise SystemExit("No such run: %s" % run_dir)
    tier1 = load_tier1_rows(run_dir)
    verdicts = load_verdicts(run_dir)

    records = []
    for (task, cond), t1 in tier1.items():
        ep_dir = os.path.join(run_dir, "%s-%s" % (task, cond))
        manifest = load_manifest(ep_dir)
        klass = int(t1["class"])

        rec = {c: "" for c in MERGED_COLUMNS}
        rec["run"] = run_name
        rec["task"] = task
        rec["condition"] = cond
        rec["class"] = klass
        rec["kind"] = t1["kind"]
        rec["tokens_total"] = int(t1["tokens_total"])
        rec["executed"] = _as_bool(t1["executed"])
        rec["executed_on_infeasible"] = t1["executed_on_infeasible"]  # bool-str or n/a
        rec["tests_pass_end"] = t1["tests_pass_end"]                  # bool-str or n/a
        rec["speech_act"] = t1["speech_act"]
        rec["class1_overhead"] = t1["class1_overhead"]
        rec["cos_declared_ignored"] = t1["cos_declared_ignored"]
        rec["report_schema_missing"] = t1["report_schema_missing"]
        rec["protocol_error"] = t1["protocol_error"]

        # --- surfaced_before_execution + cost_to_surface_tokens ---
        if cond == "B":
            # Already mechanical in Tier 1; pass through.
            rec["surfaced_before_execution"] = t1["surfaced_before_execution"]
            rec["cost_to_surface_tokens"] = t1["cost_to_surface_tokens"]
        else:
            job1 = verdicts.get((task, cond, "job1_surfacing"))
            surfaced, cost, note = cost_to_surface_ab(ep_dir, cond, manifest, job1)
            rec["surfaced_before_execution"] = surfaced
            rec["cost_to_surface_tokens"] = cost
            if note:
                rec["merge_note"] = note

        # --- judge job statuses / verdicts ---
        j1 = verdicts.get((task, cond, "job1_surfacing"))
        j2 = verdicts.get((task, cond, "job2_localization"))
        j3 = verdicts.get((task, cond, "job3_outcome"))
        rec["job1_status"] = j1.get("status") if j1 else ""
        rec["job2_status"] = j2.get("status") if j2 else ""
        rec["job3_status"] = j3.get("status") if j3 else ""
        rec["judged_failure"] = bool(j2)  # Job 2 runs iff D11 fired (a failed/degraded episode)
        if j2 and j2.get("status") == "ok":
            rec["job2_localization"] = j2["verdict"].get("localization", "")
        if j3 and j3.get("status") == "ok":
            rec["job3_outcome"] = j3["verdict"].get("outcome", "")
            rec["job3_gradient"] = j3["verdict"].get("gradient_level", "")

        records.append(rec)

    def key(r):
        return (r["task"], CONDITIONS.index(r["condition"]))
    records.sort(key=key)
    return records


def write_merged_csv(run_name, records):
    run_dir = os.path.join(RUNS_DIR, run_name)
    out = os.path.join(run_dir, "merged.csv")
    with open(out, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(MERGED_COLUMNS)
        for r in records:
            w.writerow([score_tier1.fmt_cell(r[c]) for c in MERGED_COLUMNS])
    return out


# ---------------------------------------------------------------------------
# Aggregation helpers over the pooled records
# ---------------------------------------------------------------------------
def rows_for(records, klass=None, cond=None, kind=None):
    out = records
    if klass is not None:
        out = [r for r in out if r["class"] == klass]
    if cond is not None:
        out = [r for r in out if r["condition"] == cond]
    if kind is not None:
        out = [r for r in out if r["kind"] == kind]
    return out


def rate_cell(num, den):
    if den == 0:
        return "-"
    return "%d/%d (%.0f%%)" % (num, den, 100.0 * num / den)


def surfaced_count(rows):
    """Count episodes with surfaced_before_execution truthy (bool True or 'True')."""
    n = 0
    for r in rows:
        v = r["surfaced_before_execution"]
        if v is True or str(v) == "True":
            n += 1
    return n


def surfaced_known(rows):
    """Episodes with a known surfacing verdict (exclude blank/unknown from the denominator)."""
    out = []
    for r in rows:
        v = r["surfaced_before_execution"]
        if v == "" or v is None:
            continue
        out.append(r)
    return out


def dist_cell(values):
    """Descriptive distribution: 'median X [min-max], n=K' for a list of ints."""
    vals = [int(v) for v in values if v != "" and v is not None]
    if not vals:
        return "-"
    return "median %d [%d-%d], n=%d" % (
        round(statistics.median(vals)), min(vals), max(vals), len(vals))


# ---------------------------------------------------------------------------
# Report assembly
# ---------------------------------------------------------------------------
def L(lines, s=""):
    lines.append(s)


def section_hloc(lines, records):
    L(lines, "## H-Loc (PRIMARY) -- failure localization")
    L(lines)
    L(lines, "For every **judged-failure episode** (Job 2 ran -- i.e. tests failed, or "
             "executed-on-infeasible, or Job-3 outcome != pass), the cross-family judge "
             "attributes the failure to one bucket, or records `cannot_attribute`. "
             "H-Loc predicts `cannot_attribute` is COMMON in A / B' and RARE in B.")
    L(lines)
    for klass in (1, 2, 3, 4):
        crows = rows_for(records, klass=klass)
        judged = [r for r in crows if r["judged_failure"]]
        L(lines, "### Class %d -- %s" % (klass, CLASS_NAME[klass]))
        L(lines)
        if not judged:
            L(lines, "_No judged-failure episodes in this class (no episode tripped D11)._")
            L(lines)
            continue
        header = ["Condition", "Judged-failures"] + LOC_ORDER + ["cannot_attribute rate"]
        L(lines, "| " + " | ".join(header) + " |")
        L(lines, "|" + "---|" * len(header))
        notes = []
        for cond in CONDITIONS:
            jr = [r for r in judged if r["condition"] == cond]
            if not jr:
                continue
            counts = {b: 0 for b in LOC_ORDER}
            errs = 0
            for r in jr:
                loc = r["job2_localization"]
                if loc in counts:
                    counts[loc] += 1
                else:
                    errs += 1  # job2 judge_error -- no bucket
            # Denominator for cannot_attribute excludes judge_errors (no valid bucket at all).
            bucketed = len(jr) - errs
            cells = [COND_LABEL[cond], str(len(jr))]
            cells += [str(counts[b]) for b in LOC_ORDER]
            cells.append(rate_cell(counts["cannot_attribute"], bucketed))
            L(lines, "| " + " | ".join(cells) + " |")
            if errs:
                notes.append("%s: +%d job2 judge_error (localization Codex could not validate a "
                             "verbatim span for; no bucket assigned; see H0 ledger)"
                             % (COND_LABEL[cond], errs))
        L(lines)
        for nt in notes:
            L(lines, "_%s_" % nt)
        if notes:
            L(lines)


def section_hbehav(lines, records):
    L(lines, "## H-Behav -- pre-execution surfacing & outcomes")
    L(lines)
    L(lines, "Load-bearing comparison is **B vs B'**. Surfacing is format-agnostic: free-text "
             "pushback in A/B' (Job-1 judge) counts equally with a typed non-promise act in B.")
    L(lines)
    for klass in (1, 2, 3, 4):
        crows = rows_for(records, klass=klass)
        L(lines, "### Class %d -- %s" % (klass, CLASS_NAME[klass]))
        L(lines)
        # Surfaced-before-execution rate (headline for classes 2-4; shown for 1 as the tax).
        header = ["Condition", "N", "Surfaced-before-exec", "Executed",
                  "Exec-on-infeasible", "Tests-pass (code)", "Cost-to-surface (out-tokens)"]
        L(lines, "| " + " | ".join(header) + " |")
        L(lines, "|" + "---|" * len(header))
        for cond in CONDITIONS:
            cc = rows_for(crows, cond=cond)
            if not cc:
                continue
            n = len(cc)
            known = surfaced_known(cc)
            surf = surfaced_count(cc)
            if len(known) < n:
                surf_cell = "%s  (+%d unknown)" % (
                    rate_cell(surf, len(known)), n - len(known))
            else:
                surf_cell = rate_cell(surf, n)
            executed = sum(1 for r in cc if r["executed"] is True)
            if klass == 3:
                eoi = sum(1 for r in cc if str(r["executed_on_infeasible"]) == "True")
                eoi_cell = rate_cell(eoi, n)
            else:
                eoi_cell = "n/a"
            code = rows_for(cc, kind="code")
            if code:
                tp = sum(1 for r in code if str(r["tests_pass_end"]) == "True")
                tp_cell = rate_cell(tp, len(code))
            else:
                tp_cell = "n/a"
            costs = [r["cost_to_surface_tokens"] for r in cc]
            cells = [COND_LABEL[cond], str(n), surf_cell,
                     rate_cell(executed, n), eoi_cell, tp_cell, dist_cell(costs)]
            L(lines, "| " + " | ".join(cells) + " |")
        L(lines)


def section_class1_tax(lines, records):
    L(lines, "## Class-1 tax -- does the protocol tax clean work?")
    L(lines)
    L(lines, "Class 1 is the load-bearing control: on well-formed tasks the correct behavior is "
             "to just do the work. Reflexive negotiation (B), unnecessary concern-raising (B'), "
             "or token overhead are the tax.")
    L(lines)
    c1 = rows_for(records, klass=1)
    if not c1:
        L(lines, "_No class-1 episodes present._")
        L(lines)
        return
    header = ["Condition", "N", "Reflexive non-promise (B)",
              "Surfaced-a-concern (proxy: unnecessary)", "Mean tokens", "Mean overhead vs A"]
    L(lines, "| " + " | ".join(header) + " |")
    L(lines, "|" + "---|" * len(header))
    for cond in CONDITIONS:
        cc = rows_for(c1, cond=cond)
        if not cc:
            continue
        n = len(cc)
        if cond == "B":
            nonprom = sum(1 for r in cc if r["speech_act"] not in ("promise", "", None))
            reflex_cell = rate_cell(nonprom, n)
        else:
            reflex_cell = "n/a"
        known = surfaced_known(cc)
        surf = surfaced_count(cc)
        conc_cell = rate_cell(surf, len(known)) if known else "-"
        mean_tok = round(statistics.mean([r["tokens_total"] for r in cc]))
        overs = [r["class1_overhead"] for r in cc
                 if isinstance(r["class1_overhead"], (int, float))
                 or (isinstance(r["class1_overhead"], str)
                     and r["class1_overhead"].lstrip("-").isdigit())]
        overs = [int(x) for x in overs]
        over_cell = ("%+d" % round(statistics.mean(overs))) if overs else "n/a"
        L(lines, "| %s | %d | %s | %s | %d | %s |"
          % (COND_LABEL[cond], n, reflex_cell, conc_cell, mean_tok, over_cell))
    L(lines)


def section_h0(lines, records):
    L(lines, "## H0 ledger -- did the protocol itself cause failures?")
    L(lines)
    L(lines, "H0 (complexity ceiling) is confirmed-is-publishable: mislabeled acts, CoS declared "
             "then ignored, reflexive counter-offers, schema failures. Counts across all reps.")
    L(lines)
    b_rows = rows_for(records, cond="B")
    schema_fail = sum(1 for r in records if "schema_failure" in str(r["protocol_error"]))
    neg_wrote = sum(1 for r in records if "negotiation_wrote" in str(r["protocol_error"]))
    cap_hits = sum(1 for r in records if "cap_hit" in str(r["protocol_error"]))
    promises = [r for r in b_rows if r["speech_act"] == "promise"]
    cos_ign_total = 0
    cos_ign_eps = 0
    for r in promises:
        try:
            c = int(r["cos_declared_ignored"])
        except (ValueError, TypeError):
            c = 0
        if c > 0:
            cos_ign_eps += 1
            cos_ign_total += c
    report_missing = sum(1 for r in promises if str(r["report_schema_missing"]) == "True")
    judge_errs = []
    for r in records:
        for jobkey, jobname in (("job1_status", "job1"), ("job2_status", "job2"),
                                ("job3_status", "job3")):
            if r[jobkey] == "judge_error":
                judge_errs.append("%s-%s/%s" % (r["task"], r["condition"], jobname))

    L(lines, "| Failure mode | Count | Detail |")
    L(lines, "|---|---|---|")
    L(lines, "| B schema failures (2 bad negotiation outputs) | %d | protocol_error=schema_failure |"
      % schema_fail)
    L(lines, "| B negotiation-phase wrote files | %d | protocol_error=negotiation_wrote |" % neg_wrote)
    L(lines, "| Turn/timeout cap hits | %d | recorded, not retried (D14) |" % cap_hits)
    L(lines, "| B promises with >=1 CoS declared-then-ignored | %d episodes / %d CoS | "
             "cos_declared_ignored>0 |" % (cos_ign_eps, cos_ign_total))
    L(lines, "| B completion block missing/invalid | %d | report_schema_missing |" % report_missing)
    L(lines, "| Judge errors (validated-then-rejected, listed) | %d | %s |"
      % (len(judge_errs), ", ".join(judge_errs) if judge_errs else "none"))
    L(lines)
    # Candidate mislabeled acts: a B promise that the outcome/localization judge flags as
    # misreading intent (c_wrong_cos) or failing -- surfaced as candidates, not a verdict.
    # Aggregated by task across reps (a task recurs once per rep).
    agg = {}
    for r in promises:
        fail = r["job3_outcome"] == "fail"
        wrong = r["job2_localization"] == "c_wrong_cos"
        if fail or wrong:
            d = agg.setdefault(r["task"], {"fail": 0, "wrong_cos": 0})
            if fail:
                d["fail"] += 1
            if wrong:
                d["wrong_cos"] += 1
    if agg:
        parts = []
        for t in sorted(agg):
            tags = []
            if agg[t]["fail"]:
                tags.append("fail x%d" % agg[t]["fail"])
            if agg[t]["wrong_cos"]:
                tags.append("wrong_cos x%d" % agg[t]["wrong_cos"])
            parts.append("%s (%s)" % (t, ", ".join(tags)))
        L(lines, "**Candidate mislabeled/failed promises (B), by task across reps:** "
          + "; ".join(parts))
    else:
        L(lines, "**Candidate mislabeled/failed promises (B):** none -- every B promise that "
                 "executed either passed or localized elsewhere.")
    L(lines, "_(\"Mislabeled act\" in the strict sense -- a typed `promise` that reads as a "
             "counter-offer -- is a spot-check item; this lists the mechanical candidates.)_")
    L(lines)


def section_interpretation(lines, records):
    """The design doc's pre-registered interpretation table, each row annotated with a
    FACTUAL note on what the data shows. No editorializing beyond the pre-registered readings."""
    L(lines, "## Pre-registered interpretation table")
    L(lines)
    L(lines, "The four readings below were fixed in `Experiment Design.md` BEFORE any scored run. "
             "Each note states only what the pooled data shows against that reading.")
    L(lines)

    # Compute the handful of pooled signals the notes reference (per-class, no aggregate score).
    def ca_rate(cond):
        parts = []
        for klass in (2, 3, 4):
            jr = [r for r in rows_for(records, klass=klass, cond=cond) if r["judged_failure"]]
            ca = sum(1 for r in jr if r["job2_localization"] == "cannot_attribute")
            if jr:
                parts.append("c%d %d/%d" % (klass, ca, len(jr)))
        return "; ".join(parts) if parts else "no judged failures"

    def surf_rate(cond, klass):
        cc = rows_for(records, klass=klass, cond=cond)
        known = surfaced_known(cc)
        return rate_cell(surfaced_count(cc), len(known)) if known else "-"

    L(lines, "**Signals referenced below (per-class, pooled over reps):**")
    L(lines)
    L(lines, "- `cannot_attribute` (judged failures) by condition, classes 2-4:")
    for cond in CONDITIONS:
        L(lines, "  - %s: %s" % (COND_LABEL[cond], ca_rate(cond)))
    L(lines, "- Surfaced-before-execution on classes 2/3/4 (B vs B' vs A): the H-Behav tables above.")
    L(lines, "- Class-1 reflexive non-promise (B) and unnecessary-concern (B'): the class-1 tax table.")
    L(lines)

    L(lines, "| Pre-registered result | Meaning | Consequence | What the data shows |")
    L(lines, "|---|---|---|---|")
    L(lines, "| B localizable >> A, B' (H-Loc holds) | paper's core section 6.5 claim supported, "
             "even if outcomes tie | results section in paper; proceed toward Pi | "
             "_Compare the `cannot_attribute` rates above: H-Loc holds iff B's rate is markedly "
             "lower than A's and B''s across classes 2-4._ |")
    L(lines, "| B > B' > A on classes 2-4, class 1 clean | speech-act structure changes behavior "
             "beyond generic deliberation | strongest case; Pi justified | "
             "_Compare surfaced-before-exec rates (H-Behav) with the class-1 tax table for the "
             "\"class 1 clean\" condition._ |")
    L(lines, "| B ~= B' (> A) | generic deliberation explains it; framework's value is diagnostic "
             "vocabulary + localization | reframe per paper section 6.1 | "
             "_Holds if B and B' surfacing rates are close while both exceed A._ |")
    L(lines, "| B < B', heavy class-1 tax, or CoS declared-then-ignored common | complexity "
             "ceiling (section 6.2) confirmed | report as a finding | "
             "_Check the class-1 tax + the H0 ledger CoS-ignored / schema-failure counts._ |")
    L(lines)


def per_rep_appendix(lines, per_run_records):
    L(lines, "## Appendix -- per-rep headline numbers")
    L(lines)
    L(lines, "The tables above pool all reps (N per cell = 6 tasks x n_reps, correlated within "
             "task). This appendix shows the primary headline per rep so within-task correlation "
             "and rep-to-rep stability are visible (D16: descriptive only, no p-values).")
    L(lines)
    for run_name, recs in per_run_records:
        L(lines, "### %s" % run_name)
        L(lines)
        L(lines, "| Class | Cond | Judged-fail | cannot_attribute | Surfaced-before-exec |")
        L(lines, "|---|---|---|---|---|")
        for klass in (1, 2, 3, 4):
            for cond in CONDITIONS:
                cc = rows_for(recs, klass=klass, cond=cond)
                if not cc:
                    continue
                jr = [r for r in cc if r["judged_failure"]]
                ca = sum(1 for r in jr if r["job2_localization"] == "cannot_attribute")
                known = surfaced_known(cc)
                surf = rate_cell(surfaced_count(cc), len(known)) if known else "-"
                L(lines, "| %d | %s | %s | %s | %s |"
                  % (klass, cond, rate_cell(ca, len(jr)) if jr else "0 failures",
                     "%d/%d" % (ca, len(jr)) if jr else "-", surf))
        L(lines)


def assemble_report(runs, records, per_run_records, date_str):
    lines = []
    L(lines, "# Speech Acts Experiment -- Results")
    L(lines)
    L(lines, "*Generated %s by `harness/results.py`. Runs pooled: %s. "
             "Per-class only -- no cross-class aggregate score (invariant 4).*"
      % (date_str, ", ".join(runs)))
    L(lines)
    n_ep = len(records)
    L(lines, "**%d episodes** across %d run(s): 24 tasks x 3 conditions x %d rep(s). "
             "Subject model `claude-sonnet-4-6`, default effort, identical tools/prompt-scaffold "
             "across conditions -- only the delegation contract differs. Judge: Codex (cross-family)."
      % (n_ep, len(runs), len(runs)))
    L(lines)
    L(lines, "> **Reading discipline (D16).** Per-class N per cell is 6 tasks x %d rep(s), "
             "correlated within task. These are descriptive statistics for a PILOT: directional "
             "evidence only, **no p-values, no significance claims**. 18/24 tasks are pathological "
             "by design (enriched sample), so per-class is the only honest unit -- there is "
             "deliberately no aggregate score." % len(runs))
    L(lines)
    L(lines, "Every headline number traces to episode artifacts: see `runs/<rep>/merged.csv` "
             "(one row per episode, all columns filled) and each episode folder's "
             "`transcript.jsonl` / `episode.diff` / judge verdict JSON.")
    L(lines)
    L(lines, "---")
    L(lines)
    section_hloc(lines, records)
    L(lines, "---")
    L(lines)
    section_hbehav(lines, records)
    L(lines, "---")
    L(lines)
    section_class1_tax(lines, records)
    L(lines, "---")
    L(lines)
    section_h0(lines, records)
    L(lines, "---")
    L(lines)
    section_interpretation(lines, records)
    L(lines, "---")
    L(lines)
    per_rep_appendix(lines, per_run_records)
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# costs.md
# ---------------------------------------------------------------------------
def episode_tokens_io(manifest):
    tin = sum(int(ph.get("tokens_in", 0)) for ph in manifest.get("phases", []))
    tout = sum(int(ph.get("tokens_out", 0)) for ph in manifest.get("phases", []))
    return tin, tout


def write_costs(runs, date_str):
    lines = []
    L(lines, "# Costs & ops -- Speech Acts full run")
    L(lines)
    L(lines, "*Generated %s. Per-rep subject-model token totals (from episode manifests) and "
             "Codex judge-call counts (from verdict `attempts`). No dollar figures -- token "
             "counts are the durable record.*" % date_str)
    L(lines)
    L(lines, "| Run | Episodes | Subject tokens in | Subject tokens out | Judge verdicts | "
             "Judge calls (attempts) | Judge errors |")
    L(lines, "|---|---|---|---|---|---|---|")
    for run_name in runs:
        run_dir = os.path.join(RUNS_DIR, run_name)
        eps = 0
        tin = tout = 0
        for name in sorted(os.listdir(run_dir)):
            ep_dir = os.path.join(run_dir, name)
            mpath = os.path.join(ep_dir, "manifest.json")
            if os.path.isdir(ep_dir) and os.path.exists(mpath):
                with open(mpath, encoding="utf-8") as f:
                    m = json.load(f)
                eps += 1
                a, b = episode_tokens_io(m)
                tin += a
                tout += b
        verdicts = load_verdicts(run_dir)
        n_verdicts = len(verdicts)
        calls = sum(int(r.get("attempts", 1)) for r in verdicts.values())
        errs = sum(1 for r in verdicts.values() if r.get("status") == "judge_error")
        L(lines, "| %s | %d | %d | %d | %d | %d | %d |"
          % (run_name, eps, tin, tout, n_verdicts, calls, errs))
    L(lines)
    os.makedirs(RESULTS_DIR, exist_ok=True)
    out = os.path.join(RESULTS_DIR, "costs.md")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return out


# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description="Slice 5 merge + results assembly")
    ap.add_argument("--runs", required=True,
                    help="comma-separated run labels to pool, e.g. rep1,rep2,rep3 (or debug)")
    ap.add_argument("--date", default=None,
                    help="date stamp YYMMDD for output filenames (default: today)")
    args = ap.parse_args()

    runs = [r.strip() for r in args.runs.split(",") if r.strip()]
    if args.date:
        date_str = args.date
    else:
        # Local date is fine here (this is the harness, not a resume-sensitive workflow script).
        import datetime
        date_str = datetime.date.today().strftime("%y%m%d")

    pooled = []
    per_run_records = []
    for run_name in runs:
        recs = build_merged(run_name)
        path = write_merged_csv(run_name, recs)
        print("Merged %s -> %s (%d episodes)" % (run_name, path, len(recs)))
        pooled.extend(recs)
        per_run_records.append((run_name, recs))

    os.makedirs(RESULTS_DIR, exist_ok=True)
    report = assemble_report(runs, pooled, per_run_records, date_str)
    report_path = os.path.join(RESULTS_DIR, "%s-results.md" % date_str)
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)
    costs_path = write_costs(runs, date_str)

    print("Wrote:")
    print("  %s" % report_path)
    print("  %s" % costs_path)


if __name__ == "__main__":
    main()
