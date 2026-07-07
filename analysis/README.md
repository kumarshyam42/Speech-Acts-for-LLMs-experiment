# analysis/ — exploratory hypotheses over the frozen corpus

*Everything in this folder is EXPLORATORY — hypothesis-generating work over the same 216
episodes that generated the ideas. Nothing here is confirmatory, regardless of how clean the
numbers look. The pre-registered analysis (H-Loc / H-Behav / H0) lives untouched in
`../results/`; the line between that folder and this one is an integrity feature.*

**Charter:** `260706-new-hypotheses.md` (immutable Phase-1 proposal, Shyam-reviewed).
**Phase-2 plan:** `260706-phase2-plan.md` — EXECUTED through WP-D 260706 (status block at
its foot); contains the binding success-statement language (§2), work packages, and gates.
**Findings:** `260706-phase2-findings.md` — the WP-D synthesis, awaiting Shyam's Gate-2
review before any `paper/` contact.
**Payoff file:** `next-run-prereg.md` — surviving hypotheses drafted in pre-registration
language for a future run or as Pi success criteria.
**Provenance:** `next-session-hypothesis-generation.md` — the handover prompt that
commissioned this phase (historical record, keep as-is).
**Essay & scaling implications:** `260706-essay-and-scaling-implications.md` — writing
strategy, Layer-3 draft scorecard, and the capability-scaling PoV (incl. the
capability-gradient run candidate). **Input to WP-D**: revisit and resolve its [PENDING hX]
tags at synthesis; the Layer-3 rewrite is gated on Phase-2 completion.

## Index

| ID | Claim (one line) | Tier | Status |
|---|---|---|---|
| [h1-contract-artifact](h1-contract-artifact/) | B emits a machine-readable contract (typed act + CoS + scope exclusions) that A/B′ structurally cannot | 1 | measured — SURVIVED WP-A (260706: exclusion violations 0/18 adjudicated; CoS observable 75% of promise CoS, spot-check says floor) → pre-registered-next P1 |
| [h2-veto-surface](h2-veto-surface/) | On hidden traps, B declares its bad plan in the contract before executing — vetoable by a counterparty | 1 | RESOLVED IN 3 PARTS (260706): census SURVIVED (10/10 declared) · contract-only claim DROPPED (B1: 3/12 vs ≥8/12 bar) · rules-equipped claim SUPPORTED (B1n, Shyam-commissioned: 10/12, 7 trap rejections vs 0 control rejections; cost: misread sensitivity 12/14→8/14) → pre-registered-next P2 |
| [h3-refusal-economics](h3-refusal-economics/) | The protocol reallocates spend from wasted execution to cheap early refusal; B is cheapest overall | 1 | measured — SURVIVED WP-A (260706: locked definition reproduces draft; class-3 direction holds per-rep and on out-only robustness view; break-even table added; class-4 B wastes MORE than A — kept honest) → pre-registered-next P3 |
| [h4-commitment-sensitivity](h4-commitment-sensitivity/) | The model keeps the letter of its promises — incl. one honest typed breach report — but not the spirit | 2 | measured — SURVIVED WEAKENED (260706 B2 audit: 5.1% false-met overall, 71.4% on class 3 = one episode, rep3/t19; not_met confession audited TRUE) → pre-registered-next P6 |
| [h5-auditability-asymmetry](h5-auditability-asymmetry/) | Commitment-breaking is only countable under the protocol; B′ breaches identically but invisibly | 2 | proposed (one exemplar; B′ breach extraction unmeasured) |
| [h6-counter-offer-repair](h6-counter-offer-repair/) | Counter-offers consultatively repair the request (correct false premises, better designs), not just refuse | 2 | proposed (~8 of 21 counter-offers read) |
| [h7-cos-alignment](h7-cos-alignment/) | On vague tasks, outcome tracks self-authored-CoS ↔ hidden-intent alignment; the bilateral half was absent | 3 | proposed (t10/t14 verified 3/3 reps; full class-2 scoring unmeasured) |
| [h8-act-stability](h8-act-stability/) | The typed act flips across reps on 5/24 tasks and the flip decides the outcome | 3 | measured — STRONG CLAIM SURVIVED WP-A (260706: 4/5 flip tasks uniform promise-rep fail; t12 the named counterexample; linkage is asymmetric by construction — non-promise reps have no judged outcome) → pre-registered-next P4 |
| [h9-policy-blindness](h9-policy-blindness/) | B's negotiation is code-grounded but policy-blind (cites tests, misses CONTRIBUTING ban) | 3 | proposed (t19 verified 3/3 reps; 72-negotiation classification unmeasured) |

## Status lifecycle

`proposed → measured → survived / dropped → pre-registered-next`

- **proposed** — motivated by verified exemplars; no census over the full corpus yet.
- **measured** — the census/instrument has run over all relevant episodes, per-class, per-rep.
- **survived / dropped** — dropped hypotheses KEEP their folder with a short post-mortem
  ("weird results are results" applies here too; the graveyard is what makes survivors credible).
- **pre-registered-next** — promoted into `next-run-prereg.md`.

## Rules (inherit from `../CLAUDE.md` — binding)

1. The run is frozen: `runs/`, `tasks/`, `rubrics/`, `spec/` prereg files, `../results/` are
   read-only. All outputs land inside the hypothesis's own folder (`out/`, `verdicts/`).
2. Scorers are idempotent, stdlib-Py3.9, modeled on `harness/score_tier1.py`; import shared
   helpers from `harness/` (`judge.render_transcript`, `results.load_merged`, …).
3. Judged instruments: rubric written and logged in `spec/decisions-log.md` BEFORE any verdict
   is produced; cross-family judge (`codex exec --ignore-user-config`); verbatim-span
   verification; verdicts under `<hypothesis>/verdicts/`, never near `runs/<rep>/judge/`.
4. Per-class descriptive reporting only; no cross-class aggregate; no p-values (pilot,
   N=18/cell, correlated within task). Internal robustness = pattern holds in each rep.
