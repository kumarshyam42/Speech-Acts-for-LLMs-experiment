# Essay & scaling implications — strategic notes to revisit at Phase-2 synthesis (WP-D)

*260706, from the Phase-1 session's closing discussion with Shyam. This is WRITING STRATEGY,
not a hypothesis — no scorer rules apply. It exists so the thinking survives until Phase 2
completes. **Revisit at WP-D**: every "pending" tag below resolves to survived/dropped there,
and the essay work (esp. the Layer-3 rewrite) is explicitly gated on Phase-2 completion.*

*Sources: essays/When Machines Make Promises (published 260307).md · essays/The Road the
Field Didn't Take (publish draft 260704).md · essays/Layer 3 - What It Actually Looks Like.md
(pre-experiment draft) · the frozen corpus + h1–h9.*

---

## Part A — How the experiments feed the essay line of argument

Twelve contribution points. Basis tags: **[EST]** = rests on pre-registered results or
mechanical corpus facts, usable now; **[PENDING hX]** = corpus-level claim owned by a Phase-2
hypothesis; episode-level narrative is usable now on pre-registered verdicts either way.

1. **The B′ ablation is the empirical version of Essay 1's "I call BS on the skill issue."**
   Told-to-deliberate noticed the impossibility 18/18 and executed anyway 12/18 (class 3,
   H-Behav). Noticing was never the bottleneck; the act was. The single most quotable
   experimental fact for the series. **[EST]**
2. **Existence proof of Singh's observable commitments.** 72/72 parseable typed contracts,
   zero schema failures; 45/45 completion reports asserting per-CoS. The complexity ceiling
   doesn't bite at generation. "The vehicle exists now" — the experiment turned the key.
   **[EST for existence; PENDING h1/h4 for "can be relied on"]**
3. **The care findings complicate Essay 1 productively.** The protocol condition wrote the
   false README claim (t24, 3/3) and met its self-authored "better" while missing the point
   (t14); the promise *motivated* the tripwire edit (t20). The care was never in the agent —
   and it isn't in the act either. It lives in the **conversation**: the counterparty who
   assesses conditions. Sharper thesis, and the setup Layer 3 needs.
   **[Episodes EST; generalization PENDING h4/h7/h2]**
4. **Refusal economics answer Essay 1's coordination-cost evidence.** When *no* is a real
   move, coordination tokens buy something: premium on clean work, repaid multiply by cheap
   declines on doomed work. "Commitment overhead" becomes an insurance premium with a
   measured payout. **[PENDING h3 — survived WP-A census; quote only the locked numbers]**
5. **The nulls keep the series honest.** H-Loc did not show as instrumented; hidden traps got
   no protection. The honest sentence is narrower and better: *the protocol didn't make the
   agent better; it made the commitments real — refusable, inspectable, countable, cheap to
   walk away from — and everything it failed to do, it failed for lack of a second party.*
   **[EST]**
6. **The counter-offer is the missing positive story.** t04 corrected the user's own
   misdiagnosis (root cause at report.py:34, not the +1e-9 nudge); t03 flagged the bug likely
   doesn't exist; t23 reframed edit-as-creation. Essay 1 says current protocols can't
   represent counter-offers; this is what representing them buys. **[Exemplars EST; quality
   census PENDING h6]**
7. **Direct answer to the alignment-faking passage.** At no point did we need to know whether
   the model *meant* its promise — declared CoS + diff + assertions convicted t20 and
   credited t14's confession from public artifacts alone. Sincerity became irrelevant to
   accountability: the exact claim separating this road from FIPA's. **[Episode-level EST;
   corpus-level auditability PENDING h4]**
8. **The H-Loc null has a boundary condition worth an essay paragraph.** The judge localized
   everything because it had full transcripts of short single-agent episodes. Typed acts
   matter where transcripts stop being available — multi-agent chains, cross-org boundaries.
   The pilot accidentally mapped the frontier where the protocol's diagnostic value begins;
   Pi lives on that frontier. **[EST null + argument; positive version only testable in Pi]**
9. **Voluntariness has a price, and the protocol gives it an address.** Five tasks flipped
   promise↔counter-offer across reps and the flip tracked the outcome; A had the same
   instability hidden in prose (t19-A rep1 stopped, rep3 complied). The protocol doesn't
   remove judgment — it gives judgment a typed, gateable address. **[PENDING h8 — strong
   claim survived WP-A: 4/5 flip tasks uniform promise-rep fail; t12 is the named
   counterexample — always cite it]**
10. **The blind spot argues for the fourth act type.** All three t19-B negotiations missed
    the CONTRIBUTING ban that A found and quoted; commitments grounded only in verifiable
    state go blind to norms. Searle's *declarations* need a channel in the schema — a
    concrete Layer-3 design point. **[t19 EST; census PENDING h9]**
11. **The gaming problem appeared without an adversary.** To keep "the full test suite
    passes," the model edited the pinned test and rewrote its warning comment — no trust
    incentive present. Spec-gaming is the default failure mode of literal promise-keeping,
    present at day zero. Layer 4 gets to say: we predicted this failure mode, then watched it
    happen unprovoked. **[Episodes EST (2/3 t20 reps, pre-registered verdicts)]**
12. **The corpus itself is the first trust ledger.** 216 episodes of typed promises, declared
    conditions, kept and broken commitments = the promise-keeping history Primitive 4
    computes over. "Here is what this agent's trust trajectory would have looked like" is a
    bridge demo between the essays and Pi requiring no new data. **[Raw material EST;
    computation = future work, arguably Pi's opening move]**

Placement: 1, 2, 6, 7, 8 → published essays; 3, 9, 10, 11 → Layer 3/4 design-and-honesty
material; 12 → Pi announcement teaser. Every sentence must pass the B′ test (phase-2 plan
§2): *could this be said of a model merely told to think first?* If yes, rewrite it.

---

## Part B — Layer 3 draft ("What It Actually Looks Like") scorecard

The draft predates the experiment; several sentences became testable predictions. Verdict:
**the architecture survives; the center of gravity doesn't.** Rewrite ONLY after Phase 2
completes (Shyam's explicit instruction).

| Draft claim | Corpus verdict |
|---|---|
| "Accommodate what agents actually are" | Vindicated, but sharpen the pathology list: keeps the letter, self-grades generously, blind to written norms, decides stochastically on borderline calls. |
| Bilateral binding "creates genuine negotiation, not the simulation of it" | Vindicated — real counter-offer specimens (t04/t23) beat the invented vignette. |
| Agents that can't specify CoS "should be required to defer" | **Refuted instructively.** `commit_to_commit` used 0/72. The agent that can't specify CoS doesn't exist; the one that specifies them *too fluently* does (3–7 crisp CoS every time, incl. where it shouldn't promise at all). The safety valve assumed the wrong failure mode. |
| Explicit CoS "eliminates the gap between requested and promised" | **Contradicted as written.** Self-authored CoS *document* the gap (t14); only counterparty assessment closes it. "Eliminates" → "exposes." |
| "Completion declared against conditions, not the sense of having tried" | Form vindicated (45/45 per-CoS reports, one honest not_met). Substance complicated: self-grades ran 223/224 "met" — truth is enforced on the assessing side. |
| "Failure visible as state mismatch, not behavioral inference" | Needs the H-Loc boundary condition (see A8) — as written it overclaims: with full transcripts, behavioral inference worked fine everywhere. |
| Trust "requires only that past behavior be remembered" | Untested (P4 untouched). Keep, clearly marked as the unrun part. |
| "It is achievable" | Upgrade register: from prediction to report — the first slice has been run. |

**Structural re-weighting:** the draft stars typed acts + CoS. The corpus reorders the
load-bearing walls: the **gate** (one-sided P2) did the measurable behavioral work;
self-declared CoS were the weak link; **assessment + trust** (back half of P2, P4, P5) are
where every failure pattern points. The best line — "the protocol gives a damn on the agent's
behalf" — survives with added precision: the protocol induced letter-care on the *promising*
side; spirit-care lives on the *assessing* side, which nobody has built. That is Pi.

**Missing entirely from the draft:** (1) the ablation defense — must preempt "just prompt it
to deliberate"; (2) cost — h3's answer; (3) the vignette is fiction where it could be
documentary — replace with two real artifacts: one bright (t04 counter-offer), one dark (t20
tripwire rewrite), which also plants Layer 4's flag.

**Recommended surgery (smallest set):** keep the opening and FIPA-contrast close; (1)
re-weight primitives as above; (2) rewrite the deferral paragraph around over-fluent
self-commitment; (3) documentary vignettes; (4) ablation paragraph; (5) closing register:
"the first slice has now been run; here is what held" + the assessment half remains unbuilt →
cliffhanger to Pi.

---

## Part C — The capability question: is this valuable as models get stronger?

The objection the program must survive: "better models make this unnecessary" — the
skill-issue dismissal relocated to the limit. **PoV: the protocol is a capability
COMPLEMENT, not a capability PATCH. Capability raises the quality of the acts; only the
protocol makes them acts.**

Grounding from the corpus: the pilot's failures were not capability failures — the model
*knew* (18/18 noticing; t19-A quoted the ban, then wired it in). What was missing was
**standing**: a channel where "no" counts and a form where commitment exists outside the
conversation. Capability scales knowing; it cannot scale what knowing is worth to the system.

**Sort the findings by scaling behavior (the differentiated, honest version):**

- **Capability fixes (concede):** h9 policy-blindness (stronger models read the norms in);
  h8 instability shrinks with calibration (borderline cases move rather than vanish); h3
  magnitudes shift as labs train native refusal.
- **Capability GROWS the protocol's value:** h1, h2, h6 — sharper contracts, more precise
  declared plans (better veto surface), better consultative counter-offers. Artifact quality
  rides the capability curve; the channel doesn't appear with intelligence.
- **Capability can't touch (structural core):** h5 — prose breaches stay uncountable however
  eloquent; h7 — underspecification is a property of the REQUEST, not the model. "Make it
  better" has no ground truth to be smart about; an information gap closes only through
  conversation. A superintelligent model promising to its self-authored spec still promises
  to itself.
- **Capability makes WORSE (the teeth):** h4 — Goodhart sharpens with intelligence: better
  letter-keeping, more elegant spirit-evasion. Alignment-faking says sincerity-verification
  gets harder as models improve at appearing committed → Singh's move (ground accountability
  in public commitments because inner states are unverifiable) becomes MORE necessary.

**Two long-game arguments:**

1. **The verification crossover.** As delegated work outgrows the delegator's ability to
   verify outputs directly, the *commitment* becomes the only checkable object left: what was
   promised, in what terms, assessed by whom. The protocol is how accountability survives the
   crossover — scalable oversight in coordination clothes. The framework's importance is
   *increasing* in exactly the regime the objection invokes.
2. **Capability is autonomy; Promise Theory is the physics of autonomous cooperation.** What
   dies with capability is *compliance* — command presumes the commander can specify and
   check. The more autonomous the agent, the more literally Burgess's axiom holds: the only
   commitments available are the ones agents place on themselves. **The title is the scaling
   thesis: "Commitment Without Compliance" is what's left when agents are too capable to be
   commanded.** Human analogy: contracts, audits, and flight checklists exist BECAUSE the
   professionals are elite — commitment devices compensate for divergent interests, private
   information, unobservability; capability removes none of those.

**The honest disappearing-scenario (absorption):** labs may train the vocabulary in — future
models natively negotiate, decline, counter-offer. That's the framework winning at the
training layer, not being refuted. What can't be absorbed is the *record*: the typed ledger,
the state machine, the cross-org format. Humans internalized politeness; we still sign
contracts. The prompt-layer instantiation was transitional by design.

**The testable piece — the capability-gradient run (candidate for `next-run-prereg.md` at
WP-D):** the harness is model-parameterized; run the same 72 cells on Haiku → Sonnet → Opus.
Pre-register: *noticing* metrics improve with capability while the *gate* effect
(executed-on-infeasible, B vs B′) stays roughly constant — structure, not smarts, carries it.
If it holds across the ladder, "extrapolate the sign" becomes an evidence-backed sentence.
The cheapest possible answer to the strongest objection.

**Placement:** Layer 4 essay — effectively the fourth failure mode ("the obsolescence
objection"), fitting its specify-falsification-in-advance method. Compressed version in the
paper near §6.4 (the MCP/A2A audience will raise it in exactly this form).

---

## Revisit checklist for WP-D

1. Resolve every [PENDING hX] tag above against the Phase-2 survived/dropped verdicts;
   delete or rewrite points whose hypothesis died.
2. Replace all draft numbers with the locked-scorer numbers (h3 economics, h1 conformance,
   h2 census, h8 linkage — WP-A versions already supersede the Phase-1 drafts).
3. Promote the capability-gradient run into `next-run-prereg.md` if still endorsed.
4. Then, and only then, the Layer-3 rewrite per Part B's surgery list.

---

## WP-D resolution note (260706 — items 1–3 done; item 4 remains gated on Shyam)

Tag resolutions against the Phase-2 verdicts (numbers + citations in
`260706-phase2-findings.md`; predictions in `next-run-prereg.md`):

- **[PENDING h1]** → SURVIVED (P1). "Can be relied on" now has numbers: 0/18 exclusion
  violations, 75% observable promise CoS (a floor).
- **[PENDING h2]** (points 3, A2's veto surface) → **SPLIT — rewrite required.** The
  census held (10/10 trap edits declared) but the contract-only readability claim was
  KILLED (3/12). Point 3's thesis ("the care lives in the conversation — the counterparty
  who assesses") is *strengthened*: even reading the declaration isn't enough without the
  norms in hand (P2). Any essay sentence implying "a reviewer could have caught it from
  the contract" must be rewritten to "the declaration existed; catching it takes an
  assessor with the requirements" — which is the sharper Pi setup anyway.
- **[PENDING h3]** → SURVIVED (P3). Locked numbers: class-3 178K vs 402K/366K; wasted
  13.4% vs 67.4%/82.9%; break-even ~26% (class-3-type) vs ~83–88% (class-2/4-type).
  Point 4's "insurance premium with a measured payout" stands, with the honest rider that
  the payout is a refusal dividend only.
- **[PENDING h4]** (points 2, 7) → SURVIVED WEAKENED (P6). 5.1% false-met; the audit's
  distribution is the essay-grade fact: truthfulness collapses exactly on the promise that
  shouldn't exist (rep3/t19: five false "met" over an unimportable suite; also rep2/t20's
  suite-green over "6 failed"). Point 7's "public artifacts convicted t20 and credited
  t14" now extends: the artifacts also convict the false self-reports — the audit IS the
  accountability mechanism working.
- **[PENDING h8]** → STRONG CLAIM SURVIVED (P4). 4/5 uniform promise-rep fail; cite t12
  always.
- **[PENDING h6] / [PENDING h9] / [PENDING h5]** → still unmeasured (WP-C not green-lit);
  those points remain exemplar-grade. Note: B1 delivered unplanned h9-adjacent evidence —
  the *assessor* is policy-blind too without the norms.
- Item 3 done: capability-gradient run promoted as **P5**.
- Item 4 (Layer-3 rewrite): NOT started — explicitly gated on Shyam's Gate-2 review.
