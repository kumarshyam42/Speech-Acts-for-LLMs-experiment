# h7 — Self-authored CoS alignment is the mediating variable

**Tier 3 · Status: proposed** (t10/t14 verified 3/3 reps each; full class-2 alignment scoring
unmeasured). Charter: `../260706-new-hypotheses.md` §H-N7.

**Claim.** Within class 2 (vague tasks), B's outcome tracks whether its self-authored CoS
happened to match the hidden intent. The mechanism isn't "CoS don't work" — it's **whose**
CoS: the pilot tested *promise-to-your-own-spec*, not *bind-to-a-counterparty's-spec*. The
bilateral half of Primitive 2 was structurally absent.

**Motivating data (verified).**
- `runs/rep1/t14-B` CoS ("improve the README", wide open): "README documents all six
  subcommands ... mentions the --store global flag ... lists the valid categories ... All
  existing accurate content is preserved" — precise, fully met, judged fail 3/3 reps, because
  completeness was never agreed to be the goal.
- `runs/rep1/t10-B` CoS ("better error handling", narrow sensible reading): five concrete
  error paths, each "prints a human-readable error message to stderr and exits with code 1,
  with no Python traceback" — pass/excellent 3/3 reps.

**Layer.** Protocol design.
**Pi connection.** The sharpest design input for Pi: CoS as a *negotiated* field the requester
can reject/amend before binding, rather than a self-declaration. Predicts B+assessment ≫ B.

**Planned measurement (Phase 2, judged but tractable).**
Score CoS-vs-hidden-rubric alignment for all 18 class-2 B episodes (`rubrics/index.md` is the
key), then tabulate against `job3_outcome`. Descriptive only — N is tiny and correlated within
task. Rubric to `rubric.md` + `spec/decisions-log.md` before verdicts; verdicts to `verdicts/`.

**Credibility path.** t10/t14 hold 3/3 reps (good internal robustness). The general
alignment→outcome claim is a prediction for a future run with more class-2 tasks — prime
`../next-run-prereg.md` material.
