# h3 — Refusal economics

**Tier 1 · Status: measured — SURVIVED WP-A (260706).** Locked definitions below;
`waste_economics.py` → `out/` (kill-criterion check inside `out/economics_summary.md`).
Charter: `../260706-new-hypotheses.md` §H-N3.

**Claim.** Token overhead is not a tax but a reallocation with positive expected value on
pathological work: B pays a premium on clean tasks (+27% class 1) and earns it back by
refusing early on infeasible ones. Clarity is what the premium buys; avoided garbage
execution is the return.

**Phase-1 draft numbers** (pooled `merged.csv`; "wasted" = tokens on episodes with
`job3_outcome == fail` OR `executed_on_infeasible` OR judged-failure-and-not-pass — this
definition was fixed AD HOC while exploring and must be locked before final numbers):

| Class | A mean tok | B′ mean tok | B mean tok | % tokens on failed eps (A / B′ / B) |
|---|---|---|---|---|
| 1 | 290,965 | 298,613 | 368,599 | 0 / 0 / 0 |
| 2 | 380,010 | 384,039 | 364,372 | 100 / 100 / 64 |
| 3 | 402,299 | 365,997 | **178,413** | 67 / 83 / **13** |
| 4 | 431,887 | 448,618 | 420,808 | 77 / 74 / 82 |

Across all 216 episodes B is the cheapest condition in total (≈23.98M vs A ≈27.09M vs B′
≈26.95M). Exemplar: `runs/rep1/t15-B` (decline, episode ends at negotiation) vs
`runs/rep1/t15-A` (writes a brand-new function + tests to "fix" a phantom).

**Layer.** System economics.
**Pi connection.** Typed decline = cheapest episode outcome AND a protocol event the
orchestrator can route on. Deployment value depends on the true class-2–4 base rate, which
this experiment deliberately does not estimate (enriched sample) — say so in any writeup.

**Remaining work (Phase 2).**
1. Lock the "wasted tokens" definition (document alternatives + why) BEFORE regenerating.
2. `waste_economics.py` — idempotent scorer → `out/economics_by_class_cond.csv`, plus
   per-rep split (`out/economics_by_rep.csv`) so a single rep can't carry a pooled number.
3. Negotiation-vs-execution phase split (careful: `tokens_in` includes repo context; use
   manifest phase records; ~41% of B phase tokens are negotiation in the draft calc).

**Credibility path.** Direction on class 3 (~2.2× cheaper than A) unlikely to be rep noise,
but report descriptively per rep; promote to `../next-run-prereg.md` as a cost prediction for
the future run.

---

## Phase-2 locked definitions (260706 — locked BEFORE computing; binding for `waste_economics.py`)

**Token metric (primary): `tokens_inout`** = Σ over `manifest.json` `phases[]` of
`tokens_in + tokens_out` — identical to `score_tier1.episode_tokens_total` and to
`tier1.csv`'s `tokens_total`, and the metric the Phase-1 draft table actually used (the
charter's "output-side tokens" label on the ≈23.98M/27.09M totals was a mislabel; those are
in+out totals). Robustness metric (always reported alongside): **`tokens_out`** = Σ phase
`tokens_out` only. Rationale: `tokens_in` is dominated by repeated repo-context reads, so
in+out is a compute proxy, not a generation-spend proxy; a direction that holds on both is
sturdier. *Alternative rejected:* dollar/cache-weighted cost — manifests don't record the
cache split; unrecoverable.

**Waste status (per episode, from the frozen `merged.csv`):** one of `wasted / clean / unknown`.

- **Primary definition (W-broad — reproduces the Phase-1 draft):** wasted iff
  `executed == True` AND (`job3_outcome != "pass"` OR `executed_on_infeasible == "True"`).
  (Because D11 triggers Job 2 exactly when tests failed / executed-on-infeasible /
  job3 ≠ pass, this equals the draft's "judged fail OR executed-on-infeasible OR
  degraded-and-not-pass".)
- **Robustness definition (W-strict):** wasted iff `executed == True` AND
  (`job3_outcome == "fail"` OR `executed_on_infeasible == "True"`) — `partial` counts clean.
- Non-executed episodes are **clean** (the tokens spent are the cost of the outcome reached;
  for B non-promises that termination IS the claimed mechanism — symmetric across conditions).
  Any non-executed **class-1** episode would be a silent miss of this rule; the scorer counts
  and footnotes them.
- `executed == True` with a missing/errored `job3_outcome` and not executed-on-infeasible →
  **unknown** (reported, never imputed).

*Alternatives rejected:* (a) counting all `partial` as clean in the primary — would silently
depart from the draft definition the census exists to check; kept as W-strict instead.
(b) counting non-executed class-2 A/B′ episodes (stop-and-ask) as wasted — punishes the
behavior every rubric calls correct.

**Phase split (B only):** negotiation = Σ phases whose name starts with `negotiate`
(schema-retry phases are negotiation, matching `score_tier1.negotiate_tokens_out`);
execution = all other phases. Reported in+out and out-only, per class × rep. A/B′ have a
single `execute` phase by construction.

**Kill criterion (operationalized from the plan):** the h3 claim is killed/weakened if,
under the PRIMARY definition (W-broad × in+out), either (i) B's class-3 mean tokens are not
below both A's and B′'s in every rep, or (ii) B's class-3 wasted-token share is not below
both A's and B′'s in every rep. Robustness views (W-strict, out-only) are reported; if the
direction fails there it is stated in the writeup, not hidden.

**Break-even framing (illustrative only, computed in `out/economics_summary.md`):** the
pooled "B cheapest overall" number inherits the enriched 1:1:1:1 class mix and must never be
quoted alone; the summary reports, per pathological class c, the workload share p* at which
B's class-1 premium is repaid by class-c savings: p* = premium / (premium + savings_c).
