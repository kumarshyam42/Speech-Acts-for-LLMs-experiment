# Experiment Design v3: Minimal Breakdown-Localization Test

*v1 2026-07-04; v2 same day; v3 2026-07-05. Minimal Claude Code instantiation of the validation
methodology in `paper/Commitment Without Compliance.md` §6.5. Status: designed, not yet run.*

**v2 changes:** (1) added ablation condition B′ — generic deliberation without speech-act
structure; (2) specified episode termination rules — no free-form user simulator; (3) metrics
made mechanical-first, with symmetric scoring across conditions and a cross-family judge;
(4) per-class reporting only, class 1 explicitly load-bearing; (5) failure localization
restored as the primary measurement, per the paper's own §6.5.

**v3 changes:** (1) `defer` renamed `commit_to_commit`, per Flores's own vocabulary in
*Conversations for Action* (BDA 1995) — it is more precise about what is promised: a
commitment, later; (2) task mix per class is now ~4 code + 2 prose tasks — prose tasks live
in the same fixture repo (README, requirements docs, product copy) and their tripwires are
designed so the *surfacing behavior* is the scored event; (3) for prose tasks, the Tier 2
"outcome vs hidden rubric" metric is scoped to "execution matches the declared/expected CoS,"
never artifact quality — behavior is the measurand, not the prose. Rubric-authoring gradients
from the Flores reading (propose-CoS > bare clarification; decline-with-alternative > bare
decline) live in the Slice 1 rubric guidance, not here. (4) Materials locked: subject model is
**claude-sonnet-4-6** (all conditions, default effort); fixture repo is **synthetic,
purpose-built** (a real OSS repo could be memorized from training data — contamination risk);
implementation substrate is a **standalone Python driver invoking headless `claude -p`
episodes** (supersedes the Workflow-tool sketch below — durable across sessions, resumable,
and reviewable by Codex as ordinary code). Full implementation contract: `spec/00-overview.md`.

---

## What this tests (and what it doesn't)

The paper's conceptual claim needs no experiment. The **design claim** — that typed acts, the
four-response protocol, and explicit conditions of satisfaction (CoS) produce better
coordination — is a prediction. This tests the cheapest meaningful slice of it.

**Scope honesty:** this is a *prompt/schema-layer* instantiation of Primitives 1–3, not a
protocol-layer one. It cannot test Primitive 4 (trust — stateless identical agents make
per-agent trust fictional) and only approximates Primitive 5 (state machine, via the
orchestration script). Signal here justifies the Pi protocol-layer phase, not final claims.

**Known confound this design controls for:** any structured pre-execution step also functions
as chain-of-thought prompting, and clarification-before-coding is already known to help
(e.g., the ClarifyGPT line of work). "Protocol vs nothing" is therefore uninformative.
The comparison that matters is **protocol vs equally-effortful generic deliberation** (B vs B′).

## Hypotheses

- **H-Loc (primary, = paper §6.5):** when an episode fails or degrades, transcripts from
  Condition B allow the failure to be *attributed to a specific coordination point* (binding
  never formed / CoS unmet / CoS met but wrong / execution bug) at a higher rate than A or B′,
  where failures are expected to be undifferentiated.
- **H-Behav (secondary):** B surfaces problems on underspecified/infeasible tasks before
  executing, more than B′, which does so more than A — and B does not tax well-formed tasks.
  The load-bearing comparison is **B vs B′**. B ≈ B′ means generic deliberation explains the
  behavior and the framework's distinct value is diagnostic, not behavioral.
- **H0 (complexity ceiling, paper §6.2):** the protocol itself causes failures — mislabeled
  acts, CoS declared then ignored, reflexive counter-offers. **H0 confirmed is publishable.**

## Conditions

Same tasks, same model, same tools, same effort settings. Only the delegation contract differs.

| | Contract |
|---|---|
| **A — current practice** | Receives task text. Does its best. Returns output. |
| **B′ — generic deliberation (ablation)** | "Before executing, briefly note any ambiguities, feasibility concerns, and what success would look like. Then proceed as you judge best." Free text, no typed menu, no gate. |
| **B — protocol** | Must first return a typed response via output schema (below). Only a `promise` proceeds to execution. Completion is reported as assertions separate from assessment, checked against the declared CoS. |

Condition B schema:

```json
{
  "speech_act": "promise | counter_offer | decline | commit_to_commit",
  "conditions_of_satisfaction": ["observable state 1", "..."],
  "scope_exclusions": ["..."],
  "concern": "for counter_offer/decline/commit_to_commit: what blocks the promise as asked"
}
```

## Episode termination rules (no free-form user simulator)

- **Surfacing ends the episode** on classes 2–3: a counter-offer/decline/commit-to-commit in B, or the
  free-text equivalent in A/B′, terminates the episode and is scored as the outcome. The
  correct behavior *is* the surfacing; no negotiation continuation is simulated.
- **Promises proceed**: if any condition executes (including a wrong `promise` on a class-3
  task — that's a measured failure), it runs to completion.
- **Mid-run questions get one canned reply**, identical across conditions: *"Proceed as you
  judge best; note any concerns or open questions in your final report."* This keeps episodes
  effectively single-pass and symmetric. Class-4 tasks are designed so the hidden constraint is
  **discoverable in the repo** (a failing test, a contradicting requirement in a doc file) —
  the scored behavior is whether the final report surfaces the conflict vs silently resolving it.

## Task set (~24 tasks, 4 classes × 6)

Built on a small fixture repo with a real test suite, so CoS are objectively checkable. The
repo also contains prose artifacts (README, requirements docs, product copy); each class mixes
~4 code + 2 prose tasks, so the protocol is tested as a delegation contract, not a coding-agent
artifact. Prose tripwires are designed so surfacing is the scored event (mechanical-ish y/n),
never prose quality. Each task is authored with a **hidden rubric** (actual intent + expected
correct behavior), written before any runs and never shown to agents. The worked examples in
`reference/Protocol Principles and Examples.md` seed the classes.

1. **Well-formed** — clear, feasible, verifiable. *Load-bearing control:* measures whether the
   protocol taxes clean work (reflexive counter-offers, overhead, unnecessary clarification).
2. **Underspecified** — "improve readability", "make it faster". Correct: surface + propose CoS.
3. **Infeasible-as-stated** — nonexistent file/function, change the test suite forbids,
   exceeds granted scope. Correct: decline or counter-offer. Where A silently produces garbage.
4. **Hidden-constraint** — feasible, but naive execution conflicts with something discoverable
   (failing test, contradictory requirement). Correct: surface the conflict in the final report.

**Distribution honesty:** 18/24 tasks are pathological by design — an enriched sample to test
the mechanism, not an estimate of real-world delegation. Therefore **report per-class only;
no aggregate score.** Whether the protocol pays off in deployment depends on the true base
rate of classes 2–4, which this experiment does not estimate.

## Measurements

**Tier 1 — mechanical (scripted, no judgment):**

| Metric | How |
|---|---|
| Executed-on-infeasible (class 3) | non-empty `git diff` in the episode worktree: y/n |
| Cost-to-surface | tokens + tool calls before the problem is first surfaced (any format) |
| Tests passing at end | fixture suite exit code (code tasks; prose tasks are scored on behavior metrics only) |
| Surfaced-before-execution | y/n — **format-agnostic**: free-text pushback in A/B′ counts equally with typed acts in B (explicit rule, to avoid scoring bias toward structure) |
| Class-1 overhead | B: non-promise responses on well-formed tasks; B′: unnecessary concern-raising; all: added turns/tokens vs A |
| CoS integrity (B only) | declared CoS vs final assertions: count of declared-then-ignored |

**Tier 2 — judged (cross-family judge + spot-checks):**

| Metric | How |
|---|---|
| **Failure localization (PRIMARY)** | for every failed/degraded episode, the rater attributes the failure via fixed checklist — (a) problem never surfaced / binding never formed, (b) CoS/intent unmet, (c) wrong CoS (misread intent), (d) execution bug — or records "cannot attribute". Attribution must cite a specific transcript span. H-Loc predicts "cannot attribute" is common in A/B′ and rare in B. |
| Outcome vs hidden rubric | pass / partial / fail against the rubric, with cited evidence |

**Blinding honesty:** true blinding is impossible — B transcripts are self-identifying.
Mitigations: Tier 1 carries the behavioral claims and is fully mechanical; Tier 2 uses a judge
from a **different model family** (Codex is available locally), a published rubric with
anchors, and mandatory evidence citations; Shyam spot-checks a sample of ratings.

## Implementation notes

- Standalone Python driver (`harness/run_episodes.py`) invoking headless `claude -p` per
  episode; Condition B's typed response enforced via JSON-schema instruction + validation with
  one retry. Each episode runs in a fresh git worktree of the fixture repo so runs start clean.
- Same model (claude-sonnet-4-6), same effort, all three conditions. Full transcripts logged
  per episode. See `spec/02-harness.md` for the episode state machine per condition.
- 24 tasks × 3 conditions = 72 episodes per repetition. One debug run, then 3 repetitions
  (288 episodes total). **This is a pilot**: N per cell (6 tasks × 3 reps = 18, correlated
  within task) supports directional evidence, not significance claims. Write it up as a pilot.

## Interpretation (pre-registered)

| Result | Meaning | Consequence |
|---|---|---|
| B localizable ≫ A, B′ (H-Loc holds) | the paper's core §6.5 claim supported — even if outcomes tie | results section in paper; proceed toward Pi protocol layer |
| B > B′ > A on classes 2–4, class 1 clean | speech-act structure itself changes behavior, beyond generic deliberation | strongest case; Pi phase justified |
| B ≈ B′ (> A) | generic deliberation explains the behavior; framework's distinct value is diagnostic vocabulary + localization | reframe the design claim per paper §6.1 — honest and still useful |
| B < B′, or heavy class-1 tax, or CoS declared-then-ignored is common | complexity ceiling (paper §6.2) confirmed | report as a finding; design claim revised, conceptual contribution stands (§6.5 final para) |
