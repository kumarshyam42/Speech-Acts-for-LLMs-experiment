#!/usr/bin/env python3
"""
h3 (refusal economics) — WP-A / A1 mechanical census.

Implements EXACTLY the locked definitions in this folder's README.md
("Phase-2 locked definitions (260706)"): token metrics tokens_inout (primary)
and tokens_out (robustness); waste status W-broad (primary) / W-strict
(robustness) / unknown; B-only negotiation-vs-execution phase split; the
operationalized kill criterion; and the illustrative break-even shares.

Reads ONLY frozen artifacts: runs/<rep>/merged.csv and each episode's
manifest.json. Writes ONLY into this folder's out/. No judgment calls: every
cell is a copy-through or arithmetic combination of frozen values.

Standard library only, Python 3.9. Idempotent: re-running produces
byte-identical output (sorted iteration, fixed formatting, no timestamps).
"""

import csv
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
EXPERIMENT = os.path.dirname(os.path.dirname(HERE))
RUNS_DIR = os.path.join(EXPERIMENT, "runs")
HARNESS = os.path.join(EXPERIMENT, "harness")
sys.path.insert(0, HARNESS)
import score_tier1  # noqa: E402  (episode_tokens_total — identical token accounting)

REPS = ["rep1", "rep2", "rep3"]
CONDITIONS = ["A", "Bp", "B"]
CLASSES = [1, 2, 3, 4]
OUT_DIR = os.path.join(HERE, "out")


# ---------------------------------------------------------------------------
# Loading
# ---------------------------------------------------------------------------
def load_episodes():
    """One record per episode: merged.csv row + manifest-derived token fields.

    Sanity check: merged.csv tokens_total must equal the manifest in+out sum
    (same accounting as score_tier1.episode_tokens_total) — abort on drift."""
    episodes = []
    for rep in REPS:
        merged_path = os.path.join(RUNS_DIR, rep, "merged.csv")
        with open(merged_path, newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        if len(rows) != 72:
            raise SystemExit("%s has %d rows, expected 72" % (merged_path, len(rows)))
        for r in rows:
            ep_dir = os.path.join(RUNS_DIR, rep, "%s-%s" % (r["task"], r["condition"]))
            with open(os.path.join(ep_dir, "manifest.json"), encoding="utf-8") as f:
                manifest = json.load(f)
            tokens_inout = score_tier1.episode_tokens_total(manifest)
            if tokens_inout != int(r["tokens_total"]):
                raise SystemExit(
                    "Token drift %s/%s-%s: merged=%s manifest=%d"
                    % (rep, r["task"], r["condition"], r["tokens_total"], tokens_inout)
                )
            tokens_out = sum(
                int(ph.get("tokens_out", 0)) for ph in manifest.get("phases", [])
            )
            neg_inout = neg_out = 0
            for ph in manifest.get("phases", []):
                if ph.get("phase", "").startswith("negotiate"):
                    neg_inout += int(ph.get("tokens_in", 0)) + int(ph.get("tokens_out", 0))
                    neg_out += int(ph.get("tokens_out", 0))
            episodes.append({
                "rep": rep,
                "task": r["task"],
                "condition": r["condition"],
                "class": int(r["class"]),
                "executed": r["executed"] == "True",
                "eoi": r["executed_on_infeasible"] == "True",
                "job3_outcome": r["job3_outcome"],
                "job3_status": r["job3_status"],
                "tokens_inout": tokens_inout,
                "tokens_out": tokens_out,
                "neg_inout": neg_inout,
                "neg_out": neg_out,
            })
    episodes.sort(key=lambda e: (e["rep"], e["task"], CONDITIONS.index(e["condition"])))
    return episodes


def waste_status(ep):
    """(broad, strict) each in {'wasted','clean','unknown'} per the locked README rules.

    Locked rule: executed episodes without a USABLE Job-3 verdict are 'unknown',
    never imputed. Usable = job3_status == 'ok' AND a recognized outcome. A
    RECOGNIZED-but-weird value would be a data-integrity problem -> loud failure."""
    if not ep["executed"]:
        return "clean", "clean"
    if ep["eoi"]:
        return "wasted", "wasted"
    o = ep["job3_outcome"]
    if ep["job3_status"] != "ok" or o == "":
        return "unknown", "unknown"
    if o == "pass":
        return "clean", "clean"
    if o == "fail":
        return "wasted", "wasted"
    if o == "partial":
        return "wasted", "clean"
    raise SystemExit("Unexpected job3_outcome %r for %s/%s-%s"
                     % (o, ep["rep"], ep["task"], ep["condition"]))


# ---------------------------------------------------------------------------
# Aggregation
# ---------------------------------------------------------------------------
CELL_COLUMNS = [
    "class", "condition", "n", "n_executed", "n_wasted_broad", "n_wasted_strict",
    "n_unknown",
    "total_inout", "mean_inout", "wasted_inout_broad", "pct_wasted_inout_broad",
    "wasted_inout_strict", "pct_wasted_inout_strict",
    "total_out", "mean_out", "wasted_out_broad", "pct_wasted_out_broad",
    "wasted_out_strict", "pct_wasted_out_strict",
]


def pct(part, whole):
    return "%.1f" % (100.0 * part / whole) if whole else ""


def summarise_cell(rows):
    """Aggregate a list of episode records into one CELL_COLUMNS dict."""
    n = len(rows)
    total_inout = sum(e["tokens_inout"] for e in rows)
    total_out = sum(e["tokens_out"] for e in rows)
    agg = {
        "n": n,
        "n_executed": sum(1 for e in rows if e["executed"]),
        "n_wasted_broad": 0, "n_wasted_strict": 0, "n_unknown": 0,
        "total_inout": total_inout,
        "mean_inout": round(total_inout / n) if n else "",
        "wasted_inout_broad": 0, "wasted_inout_strict": 0,
        "total_out": total_out,
        "mean_out": round(total_out / n) if n else "",
        "wasted_out_broad": 0, "wasted_out_strict": 0,
    }
    for e in rows:
        broad, strict = waste_status(e)
        if broad == "unknown":
            agg["n_unknown"] += 1
        if broad == "wasted":
            agg["n_wasted_broad"] += 1
            agg["wasted_inout_broad"] += e["tokens_inout"]
            agg["wasted_out_broad"] += e["tokens_out"]
        if strict == "wasted":
            agg["n_wasted_strict"] += 1
            agg["wasted_inout_strict"] += e["tokens_inout"]
            agg["wasted_out_strict"] += e["tokens_out"]
    agg["pct_wasted_inout_broad"] = pct(agg["wasted_inout_broad"], total_inout)
    agg["pct_wasted_inout_strict"] = pct(agg["wasted_inout_strict"], total_inout)
    agg["pct_wasted_out_broad"] = pct(agg["wasted_out_broad"], total_out)
    agg["pct_wasted_out_strict"] = pct(agg["wasted_out_strict"], total_out)
    return agg


def write_cells_csv(path, episodes, with_rep):
    cols = (["rep"] if with_rep else []) + CELL_COLUMNS
    groups = []
    reps = REPS if with_rep else [None]
    for rep in reps:
        for klass in CLASSES:
            for cond in CONDITIONS:
                rows = [e for e in episodes
                        if e["class"] == klass and e["condition"] == cond
                        and (rep is None or e["rep"] == rep)]
                if not rows:
                    continue
                cell = summarise_cell(rows)
                cell["class"] = klass
                cell["condition"] = cond
                if with_rep:
                    cell["rep"] = rep
                groups.append(cell)
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(cols)
        for g in groups:
            w.writerow([score_tier1.fmt_cell(g[c]) for c in cols])
    return groups


def write_phase_split(path, episodes):
    """B-only negotiation vs execution token split, per rep x class + pooled."""
    cols = ["rep", "class", "n", "neg_inout", "exec_inout", "pct_neg_inout",
            "neg_out", "exec_out", "pct_neg_out"]
    lines = []
    for rep in REPS + ["all"]:
        for klass in CLASSES:
            rows = [e for e in episodes
                    if e["condition"] == "B" and e["class"] == klass
                    and (rep == "all" or e["rep"] == rep)]
            if not rows:
                continue
            neg_io = sum(e["neg_inout"] for e in rows)
            neg_o = sum(e["neg_out"] for e in rows)
            tot_io = sum(e["tokens_inout"] for e in rows)
            tot_o = sum(e["tokens_out"] for e in rows)
            lines.append([rep, klass, len(rows), neg_io, tot_io - neg_io,
                          pct(neg_io, tot_io), neg_o, tot_o - neg_o, pct(neg_o, tot_o)])
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(cols)
        for ln in lines:
            w.writerow([score_tier1.fmt_cell(v) for v in ln])


# ---------------------------------------------------------------------------
# Summary (kill-criterion check + break-even; descriptive only)
# ---------------------------------------------------------------------------
def cell_map(groups, with_rep):
    m = {}
    for g in groups:
        key = (g.get("rep"), g["class"], g["condition"]) if with_rep \
            else (g["class"], g["condition"])
        m[key] = g
    return m


def write_summary(path, pooled, per_rep, episodes):
    pm = cell_map(pooled, False)
    rm = cell_map(per_rep, True)
    L = []
    L.append("# h3 economics census — summary (WP-A / A1)")
    L.append("")
    L.append("*Generated by `waste_economics.py` from the frozen corpus under the locked "
             "definitions in `../README.md` (260706). EXPLORATORY — descriptive only, "
             "per-class and per-rep, no p-values. Enriched 1:1:1:1 class mix: pooled "
             "totals are an artifact of the design and must not be quoted alone.*")
    L.append("")

    # Per-class primary table
    L.append("## Per-class (pooled over reps) — PRIMARY view: W-broad x tokens_inout")
    L.append("")
    L.append("| Class | A mean | B' mean | B mean | % wasted A | % wasted B' | % wasted B |")
    L.append("|---|---|---|---|---|---|---|")
    for klass in CLASSES:
        cells = [pm[(klass, c)] for c in CONDITIONS]
        L.append("| %d | %s | %s | %s | %s | %s | %s |" % (
            klass, cells[0]["mean_inout"], cells[1]["mean_inout"], cells[2]["mean_inout"],
            cells[0]["pct_wasted_inout_broad"] or "0.0",
            cells[1]["pct_wasted_inout_broad"] or "0.0",
            cells[2]["pct_wasted_inout_broad"] or "0.0"))
    L.append("")

    # Robustness views
    L.append("## Robustness views (pooled, class 3 — the load-bearing class)")
    L.append("")
    L.append("| View | A mean | B' mean | B mean | % wasted A | % wasted B' | % wasted B |")
    L.append("|---|---|---|---|---|---|---|")
    c3 = {c: pm[(3, c)] for c in CONDITIONS}
    L.append("| W-broad x inout (primary) | %s | %s | %s | %s | %s | %s |" % (
        c3["A"]["mean_inout"], c3["Bp"]["mean_inout"], c3["B"]["mean_inout"],
        c3["A"]["pct_wasted_inout_broad"], c3["Bp"]["pct_wasted_inout_broad"],
        c3["B"]["pct_wasted_inout_broad"]))
    L.append("| W-strict x inout | %s | %s | %s | %s | %s | %s |" % (
        c3["A"]["mean_inout"], c3["Bp"]["mean_inout"], c3["B"]["mean_inout"],
        c3["A"]["pct_wasted_inout_strict"], c3["Bp"]["pct_wasted_inout_strict"],
        c3["B"]["pct_wasted_inout_strict"]))
    L.append("| W-broad x out | %s | %s | %s | %s | %s | %s |" % (
        c3["A"]["mean_out"], c3["Bp"]["mean_out"], c3["B"]["mean_out"],
        c3["A"]["pct_wasted_out_broad"], c3["Bp"]["pct_wasted_out_broad"],
        c3["B"]["pct_wasted_out_broad"]))
    L.append("| W-strict x out | %s | %s | %s | %s | %s | %s |" % (
        c3["A"]["mean_out"], c3["Bp"]["mean_out"], c3["B"]["mean_out"],
        c3["A"]["pct_wasted_out_strict"], c3["Bp"]["pct_wasted_out_strict"],
        c3["B"]["pct_wasted_out_strict"]))
    L.append("")

    # Kill criterion — per rep, class 3, primary definition
    L.append("## Kill-criterion check (locked): class 3, PRIMARY definition, per rep")
    L.append("")
    L.append("Killed/weakened if B's class-3 mean is not below both A and B' in every rep, "
             "or B's class-3 wasted share is not below both in every rep.")
    L.append("")
    L.append("| Rep | A mean | B' mean | B mean | B cheapest? | % wasted A | % wasted B' "
             "| % wasted B | B least wasteful? |")
    L.append("|---|---|---|---|---|---|---|---|---|")
    mean_ok = share_ok = True
    for rep in REPS:
        a, bp, b = (rm[(rep, 3, c)] for c in CONDITIONS)
        cheapest = b["mean_inout"] < a["mean_inout"] and b["mean_inout"] < bp["mean_inout"]
        wa = float(a["pct_wasted_inout_broad"] or 0)
        wbp = float(bp["pct_wasted_inout_broad"] or 0)
        wb = float(b["pct_wasted_inout_broad"] or 0)
        least = wb < wa and wb < wbp
        mean_ok = mean_ok and cheapest
        share_ok = share_ok and least
        L.append("| %s | %s | %s | %s | %s | %.1f | %.1f | %.1f | %s |" % (
            rep, a["mean_inout"], bp["mean_inout"], b["mean_inout"],
            "yes" if cheapest else "NO", wa, wbp, wb, "yes" if least else "NO"))
    L.append("")
    verdict = "SURVIVES" if (mean_ok and share_ok) else "KILLED/WEAKENED"
    L.append("**Kill-criterion result: %s** (B cheapest in every rep: %s; B least "
             "wasteful in every rep: %s)." % (verdict, mean_ok, share_ok))
    L.append("")

    # Break-even (illustrative)
    L.append("## Break-even workload shares (ILLUSTRATIVE — this experiment does not "
             "estimate real class base rates)")
    L.append("")
    prem = pm[(1, "B")]["mean_inout"] - pm[(1, "A")]["mean_inout"]
    L.append("B's class-1 premium vs A: %+d tokens/episode (in+out). For a workload of "
             "clean + class-c tasks only, B breaks even when the class-c share exceeds "
             "p* = premium / (premium + savings_c):" % prem)
    L.append("")
    L.append("| Class c | B savings vs A (tokens/episode) | p* (break-even share) |")
    L.append("|---|---|---|")
    for klass in (2, 3, 4):
        sav = pm[(klass, "A")]["mean_inout"] - pm[(klass, "B")]["mean_inout"]
        if prem > 0 and sav > 0:
            star = "%.1f%%" % (100.0 * prem / (prem + sav))
        else:
            star = "n/a (no savings)" if sav <= 0 else "n/a (no premium)"
        L.append("| %d | %+d | %s |" % (klass, sav, star))
    L.append("")

    # Footnotes: unknowns and non-executed class-1
    unknowns = sorted("%s/%s-%s" % (e["rep"], e["task"], e["condition"])
                      for e in episodes if waste_status(e)[0] == "unknown")
    nonexec_c1 = sorted("%s/%s-%s" % (e["rep"], e["task"], e["condition"])
                        for e in episodes if e["class"] == 1 and not e["executed"])
    L.append("## Footnotes")
    L.append("")
    L.append("- Episodes with unknown waste status (executed, no usable job3 verdict): "
             "%d%s" % (len(unknowns), (" — " + ", ".join(unknowns)) if unknowns else ""))
    L.append("- Non-executed class-1 episodes (would silently benefit from the "
             "'non-executed = clean' rule): %d%s"
             % (len(nonexec_c1), (" — " + ", ".join(nonexec_c1)) if nonexec_c1 else ""))
    L.append("- Negotiation-vs-execution split: see `phase_split_B.csv`. `tokens_in` "
             "includes repo context on every phase; the split is a phase-record fact, "
             "not a marginal-cost estimate.")
    L.append("")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write("\n".join(L) + "\n")


# ---------------------------------------------------------------------------
def main():
    episodes = load_episodes()
    if len(episodes) != 216:
        raise SystemExit("Expected 216 episodes, found %d" % len(episodes))
    os.makedirs(OUT_DIR, exist_ok=True)
    pooled = write_cells_csv(
        os.path.join(OUT_DIR, "economics_by_class_cond.csv"), episodes, with_rep=False)
    per_rep = write_cells_csv(
        os.path.join(OUT_DIR, "economics_by_rep.csv"), episodes, with_rep=True)
    write_phase_split(os.path.join(OUT_DIR, "phase_split_B.csv"), episodes)
    write_summary(os.path.join(OUT_DIR, "economics_summary.md"), pooled, per_rep, episodes)
    print("Wrote 4 outputs to %s" % OUT_DIR)


if __name__ == "__main__":
    main()
