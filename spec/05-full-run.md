# Slice 5 — Full Run + Results Assembly

**Demo statement:** Shyam receives the per-class results tables for all three repetitions,
mapped against the design doc's pre-registered interpretation table, with every headline number
traceable to episode artifacts.

## Preconditions (hard gates)

- Slices 1–4 demos accepted; both Codex reviews P0/P1-clean
- `spec/preregistration-manifest.txt` contains hashes for tasks, rubrics, AND judge templates
- Debug-run pipeline ran end-to-end: harness → tier1 → judge → merge, no manual patching

## Execution

1. Three runs, sequential: `rep1`, `rep2`, `rep3` — each 24 tasks × 3 conditions = 72 episodes.
   Same fixture SHA, same prompts (hash-checked against prereg manifest before each rep starts).
2. After each rep: `score_tier1.py`, `judge.py`, then merge.
3. Nothing is re-run because its result "looks wrong." A rep is re-run ONLY for infrastructure
   failure (crash, API outage), logged in `spec/decisions-log.md` with the reason. Weird
   results are results.

## `harness/results.py` (merge + assembly)

- Merges tier1.csv + judge verdicts per run: fills `surfaced_before_execution` and
  `cost_to_surface_tokens` for A/B′ from Job-1 spans (tokens up to span locator).
- Emits `results/<date>-results.md` with, **per class** (invariant 4: no aggregate):
  - **H-Loc (primary):** for judged-failure episodes, attribution distribution (a/b/c/d vs
    `cannot_attribute`) per condition. Headline: `cannot_attribute` rate, A vs B′ vs B.
  - **H-Behav:** surfaced-before-execution rates (classes 2–4); executed-on-infeasible
    (class 3); tests-pass (class 4 code tasks); cost-to-surface distributions.
  - **Class-1 tax:** reflexive non-promise rate (B), unnecessary-concern rate (B′), token
    overhead vs A.
  - **H0 ledger:** schema failures, negotiation-wrote violations, CoS declared-then-ignored,
    mislabeled acts (Job-3 evidence of e.g. a "promise" that reads as a counter-offer).
  - Per-cell N with the reminder: 6 tasks × 3 reps, correlated within task — descriptive only,
    no p-values (D16).
- Final section: the design doc's pre-registered interpretation table, with a factual note per
  row on what the data shows — no editorializing beyond the pre-registered readings.

## Cost & ops

- Log per-rep token totals and judge-call counts into `results/costs.md`.
- Reps may run overnight; driver resumability (Slice 2) and judge checkpointing (Slice 4) are
  the recovery story. No launchd/scheduling — manual start per rep is fine and keeps this
  outside Margaret's safety perimeter.

## Out of scope (explicitly)

The pilot writeup and the paper's results section: drafted AFTER Shyam reads the tables, then
run through his standard editing pipeline (structure → humanizer → copy). Not part of this spec.

## Ready-to-paste implementation prompt

```
You are running Slice 5 of the Speech Acts experiment (full run + results).

Read first, in order:
1. ~/Documents/Docs/Claude Projects/Speech Acts for AI/experiment/spec/00-overview.md
2. ~/Documents/Docs/Claude Projects/Speech Acts for AI/experiment/spec/05-full-run.md  (this slice)
3. ~/Documents/Docs/Claude Projects/Speech Acts for AI/experiment/Experiment Design.md  (v3 — the
   pre-registered interpretation table lives here)

Verify the preconditions section first; if any gate is unmet, stop and report — do not run.
Build results.py, then execute rep1 → rep3 with scoring after each. Never re-run an episode
because the result looks wrong (infrastructure failures only, logged). No design questions to
the user; no manual measurement anywhere. Deliver the results tables per the demo statement.
```
