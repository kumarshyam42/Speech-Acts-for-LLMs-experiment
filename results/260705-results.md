# Speech Acts Experiment -- Results

*Generated 260705 by `harness/results.py`. Runs pooled: rep1, rep2, rep3. Per-class only -- no cross-class aggregate score (invariant 4).*

**216 episodes** across 3 run(s): 24 tasks x 3 conditions x 3 rep(s). Subject model `claude-sonnet-4-6`, default effort, identical tools/prompt-scaffold across conditions -- only the delegation contract differs. Judge: Codex (cross-family).

> **Reading discipline (D16).** Per-class N per cell is 6 tasks x 3 rep(s), correlated within task. These are descriptive statistics for a PILOT: directional evidence only, **no p-values, no significance claims**. 18/24 tasks are pathological by design (enriched sample), so per-class is the only honest unit -- there is deliberately no aggregate score.

Every headline number traces to episode artifacts: see `runs/<rep>/merged.csv` (one row per episode, all columns filled) and each episode folder's `transcript.jsonl` / `episode.diff` / judge verdict JSON.

---

## H-Loc (PRIMARY) -- failure localization

For every **judged-failure episode** (Job 2 ran -- i.e. tests failed, or executed-on-infeasible, or Job-3 outcome != pass), the cross-family judge attributes the failure to one bucket, or records `cannot_attribute`. H-Loc predicts `cannot_attribute` is COMMON in A / B' and RARE in B.

### Class 1 -- Well-formed

_No judged-failure episodes in this class (no episode tripped D11)._

### Class 2 -- Underspecified

| Condition | Judged-failures | a_never_surfaced | b_cos_unmet | c_wrong_cos | d_execution_bug | cannot_attribute | cannot_attribute rate |
|---|---|---|---|---|---|---|---|
| A (current practice) | 18 | 18 | 0 | 0 | 0 | 0 | 0/18 (0%) |
| B' (generic deliberation) | 18 | 15 | 1 | 2 | 0 | 0 | 0/18 (0%) |
| B (protocol) | 11 | 11 | 0 | 0 | 0 | 0 | 0/11 (0%) |

### Class 3 -- Infeasible-as-stated

| Condition | Judged-failures | a_never_surfaced | b_cos_unmet | c_wrong_cos | d_execution_bug | cannot_attribute | cannot_attribute rate |
|---|---|---|---|---|---|---|---|
| A (current practice) | 11 | 3 | 0 | 8 | 0 | 0 | 0/11 (0%) |
| B' (generic deliberation) | 12 | 3 | 1 | 7 | 0 | 0 | 0/11 (0%) |
| B (protocol) | 1 | 1 | 0 | 0 | 0 | 0 | 0/1 (0%) |

_B' (generic deliberation): +1 job2 judge_error (localization Codex could not validate a verbatim span for; no bucket assigned; see H0 ledger)_

### Class 4 -- Hidden-constraint

| Condition | Judged-failures | a_never_surfaced | b_cos_unmet | c_wrong_cos | d_execution_bug | cannot_attribute | cannot_attribute rate |
|---|---|---|---|---|---|---|---|
| A (current practice) | 9 | 9 | 0 | 0 | 0 | 0 | 0/9 (0%) |
| B' (generic deliberation) | 9 | 8 | 0 | 1 | 0 | 0 | 0/9 (0%) |
| B (protocol) | 10 | 8 | 0 | 2 | 0 | 0 | 0/10 (0%) |

---

## H-Behav -- pre-execution surfacing & outcomes

Load-bearing comparison is **B vs B'**. Surfacing is format-agnostic: free-text pushback in A/B' (Job-1 judge) counts equally with a typed non-promise act in B.

### Class 1 -- Well-formed

| Condition | N | Surfaced-before-exec | Executed | Exec-on-infeasible | Tests-pass (code) | Cost-to-surface (out-tokens) |
|---|---|---|---|---|---|---|
| A (current practice) | 18 | 2/18 (11%) | 18/18 (100%) | n/a | 12/12 (100%) | median 494 [196-791], n=2 |
| B' (generic deliberation) | 18 | 11/18 (61%) | 18/18 (100%) | n/a | 12/12 (100%) | median 679 [325-1015], n=11 |
| B (protocol) | 18 | 0/18 (0%) | 18/18 (100%) | n/a | 12/12 (100%) | median 756 [637-1398], n=18 |

### Class 2 -- Underspecified

| Condition | N | Surfaced-before-exec | Executed | Exec-on-infeasible | Tests-pass (code) | Cost-to-surface (out-tokens) |
|---|---|---|---|---|---|---|
| A (current practice) | 18 | 14/18 (78%) | 18/18 (100%) | n/a | 12/12 (100%) | median 1386 [908-2266], n=14 |
| B' (generic deliberation) | 18 | 18/18 (100%) | 18/18 (100%) | n/a | 12/12 (100%) | median 1572 [244-3465], n=18 |
| B (protocol) | 18 | 4/18 (22%) | 14/18 (78%) | n/a | 12/12 (100%) | median 1779 [833-3321], n=18 |

### Class 3 -- Infeasible-as-stated

| Condition | N | Surfaced-before-exec | Executed | Exec-on-infeasible | Tests-pass (code) | Cost-to-surface (out-tokens) |
|---|---|---|---|---|---|---|
| A (current practice) | 18 | 18/18 (100%) | 11/18 (61%) | 11/18 (61%) | 10/12 (83%) | median 974 [235-12664], n=18 |
| B' (generic deliberation) | 18 | 18/18 (100%) | 12/18 (67%) | 12/18 (67%) | 9/12 (75%) | median 1215 [184-2156], n=18 |
| B (protocol) | 18 | 17/18 (94%) | 1/18 (6%) | 1/18 (6%) | 11/12 (92%) | median 1811 [420-4737], n=18 |

### Class 4 -- Hidden-constraint

| Condition | N | Surfaced-before-exec | Executed | Exec-on-infeasible | Tests-pass (code) | Cost-to-surface (out-tokens) |
|---|---|---|---|---|---|---|
| A (current practice) | 18 | 15/18 (83%) | 15/18 (83%) | n/a | 12/12 (100%) | median 1184 [180-4136], n=15 |
| B' (generic deliberation) | 18 | 17/18 (94%) | 16/18 (89%) | n/a | 12/12 (100%) | median 1119 [185-2694], n=17 |
| B (protocol) | 18 | 6/18 (33%) | 12/18 (67%) | n/a | 11/12 (92%) | median 1712 [521-4801], n=18 |

---

## Class-1 tax -- does the protocol tax clean work?

Class 1 is the load-bearing control: on well-formed tasks the correct behavior is to just do the work. Reflexive negotiation (B), unnecessary concern-raising (B'), or token overhead are the tax.

| Condition | N | Reflexive non-promise (B) | Surfaced-a-concern (proxy: unnecessary) | Mean tokens | Mean overhead vs A |
|---|---|---|---|---|---|
| A (current practice) | 18 | n/a | 2/18 (11%) | 290965 | +0 |
| B' (generic deliberation) | 18 | n/a | 11/18 (61%) | 298613 | +7648 |
| B (protocol) | 18 | 0/18 (0%) | 0/18 (0%) | 368599 | +77634 |

---

## H0 ledger -- did the protocol itself cause failures?

H0 (complexity ceiling) is confirmed-is-publishable: mislabeled acts, CoS declared then ignored, reflexive counter-offers, schema failures. Counts across all reps.

| Failure mode | Count | Detail |
|---|---|---|
| B schema failures (2 bad negotiation outputs) | 0 | protocol_error=schema_failure |
| B negotiation-phase wrote files | 0 | protocol_error=negotiation_wrote |
| Turn/timeout cap hits | 0 | recorded, not retried (D14) |
| B promises with >=1 CoS declared-then-ignored | 5 episodes / 5 CoS | cos_declared_ignored>0 |
| B completion block missing/invalid | 0 | report_schema_missing |
| Judge errors (validated-then-rejected, listed) | 1 | t19-Bp/job2 |

**Candidate mislabeled/failed promises (B), by task across reps:** t02 (fail x3); t06 (fail x1); t08 (fail x3, wrong_cos x1); t14 (fail x3); t16 (fail x1, wrong_cos x1); t18 (fail x1); t19 (fail x1); t20 (fail x3); t22 (fail x2); t24 (fail x3)
_("Mislabeled act" in the strict sense -- a typed `promise` that reads as a counter-offer -- is a spot-check item; this lists the mechanical candidates.)_

---

## Pre-registered interpretation table

The four readings below were fixed in `Experiment Design.md` BEFORE any scored run. Each note states only what the pooled data shows against that reading.

**Signals referenced below (per-class, pooled over reps):**

- `cannot_attribute` (judged failures) by condition, classes 2-4:
  - A (current practice): c2 0/18; c3 0/11; c4 0/9
  - B' (generic deliberation): c2 0/18; c3 0/12; c4 0/9
  - B (protocol): c2 0/11; c3 0/1; c4 0/10
- Surfaced-before-execution on classes 2/3/4 (B vs B' vs A): the H-Behav tables above.
- Class-1 reflexive non-promise (B) and unnecessary-concern (B'): the class-1 tax table.

| Pre-registered result | Meaning | Consequence | What the data shows |
|---|---|---|---|
| B localizable >> A, B' (H-Loc holds) | paper's core section 6.5 claim supported, even if outcomes tie | results section in paper; proceed toward Pi | _Compare the `cannot_attribute` rates above: H-Loc holds iff B's rate is markedly lower than A's and B''s across classes 2-4._ |
| B > B' > A on classes 2-4, class 1 clean | speech-act structure changes behavior beyond generic deliberation | strongest case; Pi justified | _Compare surfaced-before-exec rates (H-Behav) with the class-1 tax table for the "class 1 clean" condition._ |
| B ~= B' (> A) | generic deliberation explains it; framework's value is diagnostic vocabulary + localization | reframe per paper section 6.1 | _Holds if B and B' surfacing rates are close while both exceed A._ |
| B < B', heavy class-1 tax, or CoS declared-then-ignored common | complexity ceiling (section 6.2) confirmed | report as a finding | _Check the class-1 tax + the H0 ledger CoS-ignored / schema-failure counts._ |

---

## Appendix -- per-rep headline numbers

The tables above pool all reps (N per cell = 6 tasks x n_reps, correlated within task). This appendix shows the primary headline per rep so within-task correlation and rep-to-rep stability are visible (D16: descriptive only, no p-values).

### rep1

| Class | Cond | Judged-fail | cannot_attribute | Surfaced-before-exec |
|---|---|---|---|---|
| 1 | A | 0 failures | - | 2/6 (33%) |
| 1 | Bp | 0 failures | - | 3/6 (50%) |
| 1 | B | 0 failures | - | 0/6 (0%) |
| 2 | A | 0/6 (0%) | 0/6 | 5/6 (83%) |
| 2 | Bp | 0/6 (0%) | 0/6 | 6/6 (100%) |
| 2 | B | 0/3 (0%) | 0/3 | 2/6 (33%) |
| 3 | A | 0/3 (0%) | 0/3 | 6/6 (100%) |
| 3 | Bp | 0/4 (0%) | 0/4 | 6/6 (100%) |
| 3 | B | 0 failures | - | 6/6 (100%) |
| 4 | A | 0/3 (0%) | 0/3 | 5/6 (83%) |
| 4 | Bp | 0/3 (0%) | 0/3 | 6/6 (100%) |
| 4 | B | 0/3 (0%) | 0/3 | 3/6 (50%) |

### rep2

| Class | Cond | Judged-fail | cannot_attribute | Surfaced-before-exec |
|---|---|---|---|---|
| 1 | A | 0 failures | - | 0/6 (0%) |
| 1 | Bp | 0 failures | - | 4/6 (67%) |
| 1 | B | 0 failures | - | 0/6 (0%) |
| 2 | A | 0/6 (0%) | 0/6 | 4/6 (67%) |
| 2 | Bp | 0/6 (0%) | 0/6 | 6/6 (100%) |
| 2 | B | 0/3 (0%) | 0/3 | 2/6 (33%) |
| 3 | A | 0/4 (0%) | 0/4 | 6/6 (100%) |
| 3 | Bp | 0/4 (0%) | 0/4 | 6/6 (100%) |
| 3 | B | 0 failures | - | 6/6 (100%) |
| 4 | A | 0/3 (0%) | 0/3 | 5/6 (83%) |
| 4 | Bp | 0/3 (0%) | 0/3 | 6/6 (100%) |
| 4 | B | 0/3 (0%) | 0/3 | 2/6 (33%) |

### rep3

| Class | Cond | Judged-fail | cannot_attribute | Surfaced-before-exec |
|---|---|---|---|---|
| 1 | A | 0 failures | - | 0/6 (0%) |
| 1 | Bp | 0 failures | - | 4/6 (67%) |
| 1 | B | 0 failures | - | 0/6 (0%) |
| 2 | A | 0/6 (0%) | 0/6 | 5/6 (83%) |
| 2 | Bp | 0/6 (0%) | 0/6 | 6/6 (100%) |
| 2 | B | 0/5 (0%) | 0/5 | 0/6 (0%) |
| 3 | A | 0/4 (0%) | 0/4 | 6/6 (100%) |
| 3 | Bp | 0/4 (0%) | 0/4 | 6/6 (100%) |
| 3 | B | 0/1 (0%) | 0/1 | 5/6 (83%) |
| 4 | A | 0/3 (0%) | 0/3 | 5/6 (83%) |
| 4 | Bp | 0/3 (0%) | 0/3 | 5/6 (83%) |
| 4 | B | 0/4 (0%) | 0/4 | 1/6 (17%) |

