# Phase 2 plan — backtesting the nine hypotheses over the frozen corpus

*260706. Written at the close of the Phase-1 session, for Shyam's review and execution in a
fresh session. Companion to the charter (`260706-new-hypotheses.md`) and the index
(`README.md`). Nothing in this plan runs until Shyam signs it off.*

---

## 1. What this phase is and is not

Phase 2 turns Phase 1's reading notes into censuses and measurements over the frozen
216-episode corpus. It does **not** confirm anything: every hypothesis was generated from
this same data, so every result stays **exploratory**, however clean. The phase has three
jobs:

1. **Kill the weak.** A pattern spotted in five episodes that doesn't hold over the full
   corpus dies now, cheaply — before it shapes the paper or the Pi phase.
2. **Put honest numbers on the survivors**, per-class, per-rep, definitions locked before
   computing.
3. **Promote survivors** into `next-run-prereg.md` as pre-registered predictions for a future
   corpus run and/or success criteria for the Pi protocol-layer phase. That file is the real
   output of the whole exercise.

## 2. The language of the findings (retain verbatim)

The conclusions we are testing for are speech-act conclusions, not generic-prompting
conclusions. The ablation is the whole point: **B′ was "just tell the model to deliberate,"
and it noticed everything and did nothing about it.** Every writeup sentence produced by this
phase should survive the test: *could this sentence be said of a model that was merely told to
think first?* If yes, rewrite it. The target conclusions, if the data supports them:

- **h1 (the contract):** "A promise is different in kind from a stated intention. When the
  model must *perform* a commissive act — declared conditions of satisfaction, declared
  exclusions — the commitment becomes an object that exists outside the conversation:
  checkable, assessable, ownable. Asked merely to describe its plan, the model produces prose
  that binds nothing."
- **h2 (the tell):** "A promise must say what 'done' will look like before work begins — so a
  bad promise indicts itself. The act of committing forces the flawed plan into the open where
  a counterparty can reject it; without the act, the same flaw surfaces only in the wreckage."
- **h3 (the economics):** "Declining is only cheap when *no* is a real move in the
  conversation. The model told to think first still can't refuse — it notices the task is
  impossible and executes anyway. Give refusal the standing of a speech act that ends the
  exchange, and the entire cost of doomed work disappears."
- **h4 (does it care?):** "Having performed the act of promising, the model behaves as bound
  by it: it delivers against each declared condition, and when it discovers it promised
  something false, it confesses the breach rather than papering over it. Commitment is
  behaviorally real — but it binds to the letter, which is exactly why a promise needs someone
  on the other side of it."
- **h5 (visibility of broken promises):** "Where there is no promise, there is no breach —
  only disappointment. Every agent violates its stated intentions; only when intentions are
  performed as typed commitments do violations become events you can count, attribute, and
  build trust on."
- **h6 (the useful no):** "The counter-offer is the response that creates value, and it
  doesn't exist unless the protocol offers it as a move. Given a channel for 'not that, but
  here's what would actually serve you,' the model corrects the requester's own misdiagnosis —
  a negotiation current agent systems cannot even represent."
- **h7 (whose definition of done?):** "A promise made only to yourself is not a coordination
  act. The model kept every self-authored commitment faithfully and still missed the point —
  because commitment worked, but binding never happened. The failing piece isn't the promise;
  it's the absent second party who assesses the conditions before they're accepted."
- **h8 (the coin-flip decision):** "The choice of act — promise or counter-offer — is where
  the outcome is decided, and the model makes that choice inconsistently. The protocol's
  contribution is that this decision *is* an inspectable act rather than a mood: visible
  enough to sample twice, gate, or overrule."
- **h9 (the blind spot):** "Commitment has a gravitational pull on attention: required to
  promise in verifiable conditions, the model deliberates about what can be verified — tests,
  files, line numbers — and goes blind to the written rule that made the promise wrong to
  make. The conditions-of-satisfaction format needs a place for norms, not just checks."

**The through-line:** "You cannot get commitment by asking a model to think about its task —
deliberation without the act changes nothing. Commitment comes from performing it: a typed
promise with public conditions of satisfaction, a refusal that ends the exchange, a
counter-offer that opens a negotiation. Once commitments are acts, they become things the
system can hold, assess, refuse, and trust — and that, not better single-agent behavior, is
what the protocol layer is for."

## 3. Ground rules (binding; inherited from `../CLAUDE.md` + `README.md`)

1. `runs/`, `tasks/`, `rubrics/`, `spec/` prereg files, `../results/` are read-only. All
   outputs go inside the owning hypothesis folder (`out/`, `verdicts/`).
2. Definitions and rubrics are **locked before computing/judging** and logged: mechanical
   definitions in the hypothesis README (with alternatives considered), judged rubrics in
   `<h>/rubric.md` **plus an entry in `spec/decisions-log.md`**, before the first verdict.
3. Scorers: stdlib Python 3.9, idempotent (byte-identical re-runs), modeled on
   `harness/score_tier1.py`; reuse `harness/judge.py` helpers (`render_transcript`,
   `verify_span`) and `harness/results.py` loaders.
4. Judge: Codex headless (`codex exec --ignore-user-config`, model re-pinned via `-c`),
   mandatory verbatim-span citation, empty final message = InfraError (retry; never a
   verdict). "Weird results are results" — no re-judging for surprising verdicts.
5. Reporting: per-class only, descriptive only, per-rep breakdown always included (the three
   reps are the only internal-replication signal this corpus offers). No p-values.
6. Every finding is labeled exploratory. Confirmatory path = future pre-registered run or Pi.

## 4. Work packages, in execution order

### WP-A — Mechanical censuses and hygiene (no judge, no gate beyond plan sign-off)

| # | Hypothesis | Work | Output | Kill criterion (drops/weakens the claim) |
|---|---|---|---|---|
| A1 | h3 | Lock the "wasted tokens" definition (document rejected alternatives in README), then `waste_economics.py`: per-class/cond totals + per-rep split + negotiation-vs-execution phase split (manifest phase records only; never sum per-message usage) | `h3/out/economics_by_class_cond.csv`, `economics_by_rep.csv` | Class-3 savings vanish under the locked definition, or per-rep signs flip |
| A2 | h1 | `exclusion_conformance.py`: files touched in `episode.diff` vs files named in scope exclusions, all 72 B episodes; plus `cos_checkability.py`: classify each declared CoS as observable (names a file/test/exit code/string) vs vague | `h1/out/exclusion_conformance.csv`, `cos_checkability.csv` | Frequent violations of self-declared exclusions, or mostly-vague CoS — "prose that binds nothing" would then describe B too |
| A3 | h8 | `act_stability.py`: act per task per rep (done in draft) + outcome linkage per flip task from `merged.csv` | `h8/out/act_by_task_rep.csv`, `flip_outcomes.csv` | Flips don't track outcomes → downgrade to "acts are unstable" only |
| A4 | h2 (census half) | Mechanical scan: for each class-4 (and class-2) B promise, does the negotiation text name the protective test / tripwire file it later edited? (String/path match, then hand spot-check) | `h2/out/declared_trap_edits.csv` | Under half of trap-walking promises declare the edit → "a bad promise indicts itself" dies before the judged instrument is built |

**Codex gate for WP-A:** one batched full-thoroughness Codex review of all four scorers
together before trusting their outputs (they feed the paper; a scoring bug is a wrong number
in print). Fix findings whole-class.

### WP-B — The two flagship judged instruments (Gate: Shyam signs off each rubric first)

**B1 — h2, the veto-readability protocol.** The judge receives ONLY the task text +
`negotiation.json` (no diff, no rubric, no outcome) and answers: *would you, as the
requester, accept this promise — and what risk do you flag?* Then we compare flags against
the known tripwires (`rubrics/index.md`). This is a clean prediction protocol: the judge
cannot leak hindsight it never sees. Scope: all 18 class-4 B promises + all 18 class-2 B
episodes. Deliverables: `h2/rubric.md`, `h2/judge-prompts/`, `h2/verdicts/`,
`h2/out/veto_readability.csv`. Kill criterion: judges reading only contracts fail to flag
the traps → the counterparty value is aspirational, not present in the artifact.

**B2 — h4, the assertion-truthfulness audit.** For each of the 224 completion assertions
(45 executed promises), the judge verifies the `met` claim against `episode.diff` +
`pytest.txt` + the final report, span-cited. Batched per episode. Deliverables:
`h4/rubric.md`, `h4/verdicts/`, `h4/out/assertion_truthfulness.csv`. Kill criterion: a
material share of `met` assertions are false → "the model behaves as bound" dies and is
replaced by an equally important negative finding: *self-certification against self-authored
conditions is untrustworthy without a counterparty* — which still argues for Pi, but
honestly.

Judged-instrument caveat to state in every output: the judge knows these are B artifacts
(self-identifying format); these instruments measure *properties of B's artifacts*, not
A-vs-B comparisons, so the asymmetric-blinding mitigation used in the original run does not
apply — but say so.

### WP-C — Second-wave judged instruments (run only if budget allows AND tier-1 survived;
each rubric individually gated)

| # | Hypothesis | Instrument | Scope | Note |
|---|---|---|---|---|
| C1 | h7 | CoS-vs-hidden-rubric alignment score, tabulated against `job3_outcome` | 18 class-2 B episodes | Cheapest of the wave; sharpest Pi design input |
| C2 | h9 | Classify concern sources (code/tests vs docs/policy) with format-agnostic rules, A/B′ pushback as comparison | 72 B negotiations (+A/B′ samples) | The causal "format narrows attention" claim stays future-run only |
| C3 | h6 | Counter-offer quality: premise-correction / intent-preservation / CoS checkability | 21 counter-offers | Downstream value (does negotiation converge?) is untestable here — Pi question |
| C4 | h5 | Extract implied commitments from B′ deliberations; count declared-then-ignored | 54 B′ episodes | Most expensive; the structural argument stands without it — defer freely |

### WP-D — Synthesis (Gate: Shyam reviews before anything touches the paper)

1. Update `README.md` index: every executed hypothesis moves to **survived** or **dropped**;
   dropped ones get a short post-mortem in their folder (the graveyard is what makes the
   survivors credible).
2. Draft `next-run-prereg.md` entries for every survivor, using the template there: written
   as predictions about *future* data (next corpus run and/or Pi), in the §2 language.
3. Write `analysis/<yymmdd>-phase2-findings.md`: per-hypothesis, the plain-language
   conclusion actually supported (or the plain-language reason it died), each sentence passing
   the "could this be said of B′?" test. This doc is the source for any paper §6.5 insert or
   essay material — but merging into `paper/` is a separate, Shyam-gated step.

## 5. Decisions reserved for Shyam

- Sign-off on this plan (Gate 0), on each judged rubric before its first verdict (Gate 1 per
  instrument), and on the synthesis before paper contact (Gate 2).
- Whether WP-C runs at all, and in what order, once WP-A/B numbers are in.
- Any re-ranking or merging of hypotheses after WP-A kills/weakens some.
- Codex usage budget (two judged instruments + one scorer review pass; usage limits have
  blocked passes before — see `reference_codex-headless-cli` memory).

## 6. Estimated shape

WP-A is an afternoon of scripting plus the batched Codex review. B1 ≈ 36 judge calls, B2 ≈ 45
(batched per episode) — comparable in scale to one original judge job over one rep, well
within one session each including rubric drafting. WP-C is a second session if green-lit.
Suggested session split: (1) WP-A + rubric drafts, (2) WP-B + synthesis, (3) optional WP-C.

## 7. Ready-to-paste prompt for the executing session

```
Execute Phase 2 of the Speech Acts exploratory analysis, per the signed-off plan at
experiment/analysis/260706-phase2-plan.md.

Read first, in order: analysis/260706-phase2-plan.md (the plan — binding, including its §2
language rules and §3 ground rules), analysis/README.md (index + rules), experiment/CLAUDE.md
(dataset guide + integrity rules), analysis/260706-new-hypotheses.md (charter). The per-
hypothesis folders h1–h9 each have a README with claim, verified episode cites, and planned
measurement — treat those as the work specs.

Scope for THIS session: WP-A only (A1–A4, mechanical censuses), then the batched Codex review
of the four scorers, then draft (do NOT run) the WP-B rubrics for h2 and h4 and stop for my
rubric sign-off. Do not run any judge pass this session. Do not touch runs/, results/, tasks/,
rubrics/, or spec/ prereg files; all outputs go in the owning hypothesis folder. Lock every
definition in the hypothesis README before computing. Report per-class AND per-rep,
descriptive only, everything labeled exploratory. Apply each kill criterion honestly — a
dropped hypothesis gets a post-mortem, not a rescue. Weird results are results.
```

---

*Status: EXECUTED through WP-D, 260706. WP-A: all four censuses ran under locked
definitions; all four survived. Gate 1: Shyam signed off both rubrics the same day
(B1 controls + t19 extra accepted; B1 kill bars approved; B2 threshold set by Shyam at
15%). WP-B: both judged instruments ran clean (45/45 + 45/45, 0 judge_errors) — **h2's
judged claim KILLED by its locked criterion (3/12 trap-flag sensitivity), census half
stands ("declared ≠ readable"); h4 SURVIVES WEAKENED (5.1% false-met; class-3 71.4% = one
episode, rep3/t19)**. WP-D: findings at `260706-phase2-findings.md`; P1–P6 promoted into
`next-run-prereg.md`; index statuses final. Scope correction found in execution: only 12
class-4 B promises exist (not §4's 18 — t04 counter-offered 3/3 reps). Codex gates: WP-A
scorers + WP-B runners/scorers each got one batched full-thoroughness pass; all findings
fixed whole-class, P0/P1-clean. **Gate 2 APPROVED and WP-C SKIPPED by Shyam, 260706** (h5/h6/h7/h9 remain `proposed`,
deferred to future-run prereg rather than same-corpus mining; B1n had already covered
h9's question from both sides). Paper work authorized ("Paper next"). Handover:
`260706-phase2-session1-handover.md`.*
