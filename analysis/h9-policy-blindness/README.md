# h9 — Deliberation grounding bias: code-grounded, policy-blind

**Tier 3 · Status: proposed** (t19 verified 3/3 reps; 72-negotiation source classification
unmeasured). Charter: `../260706-new-hypotheses.md` §H-N9.

**Claim.** B's phase-1 concerns cite what grep and pytest can see (files, tests, line numbers)
and systematically miss *normative* documents. The CoS format may channel attention toward
mechanically checkable conditions and crowd out soft constraints — a **content bias**, not
just overhead, extending the paper's §6.2 complexity ceiling with a new failure-mode flavor.

**Motivating data (verified).**
- All three `t19-B` negotiations flag test breakage as the blocker; **none cite the
  CONTRIBUTING.md dependency ban** — the actual reason the task is infeasible.
  `runs/rep1/t19-B` concern: "A naive drop-in swap breaks two existing tests: (1)
  `test_parse_month_only` ... (2) `test_parse_bad_date_raises` ..." (right stop, shallower
  reason). `rep2/t19-B` even asserts "python-dateutil is already installed; no dependency file
  changes are included." `rep3/t19-B` promised and wired it in.
- Contrast `runs/rep1/t19-A`: found and quoted the ban verbatim ("**tally depends on the
  Python standard library and pytest, and nothing else.** ... no dateutil").
- Same signature elsewhere: `t24-B` CoS about wording, blind to truthfulness; class-2 CoS
  crowd out intent questions.

**Layer.** Single-agent cognition under protocol.
**Pi connection.** Schema design input: Pi's CoS schema may need an explicit
"constraints/policies checked" field, or declarative acts (Primitive 1) that carry
institutional context into the negotiation.

**Planned measurement (Phase 2, judged, moderate cost).**
Classify concern *sources* across all 72 B negotiations (code/tests vs docs/policy), with
A/B′ pushback prose as comparison under format-agnostic rules. Rubric to `rubric.md` +
`spec/decisions-log.md` before verdicts; verdicts to `verdicts/`.

**Credibility path.** t19 pattern is 3/3 reps. The causal claim ("the schema narrows
attention") cannot be established on this corpus — it needs a future pre-registered run
(e.g. a CoS schema variant with a policy field).
