# Next session — hypothesis generation from the frozen corpus

*Purpose: mine the completed Speech Acts experiment for value the protocol added that the original
hypotheses (H-Loc / H-Behav / H0) did not capture. Two-phase; phase 1 (understand → question list)
is the whole ask until Shyam signs off the list. Paste the block below into a fresh session.*

---

```
Goal: mine the completed Speech Acts experiment for VALUE THE PROTOCOL ADDED THAT THE ORIGINAL
HYPOTHESES DID NOT CAPTURE. This is a two-phase job, and phase 1 is the whole ask for now:

  PHASE 1 (now): understand the experiment and the actual episode data deeply, then produce a
  FINALIZED, PRIORITIZED LIST OF NEW QUESTIONS / HYPOTHESES, developed with me and tied to my
  overall thesis and goals.
  PHASE 2 (later, gated on my sign-off of that list): design how to backtest each question over
  the frozen data. DO NOT design backtests or run any analysis yet.

Why: the original study pre-registered three hypotheses — H-Loc (failure localization), H-Behav
(pre-execution surfacing), H0 (complexity ceiling). H-Loc (the primary) did not hold; the rest
were mixed. But my strong intuition is that the protocol added real value that those three
metrics were simply the wrong instruments to detect. I want to discover what those value
dimensions are — grounded in what the models actually did, not invented.

STEP 1 — Understand the study and my thesis.
- Read experiment/CLAUDE.md (dataset guide), Experiment Design.md (v3: the 3 conditions,
  hypotheses, pre-registered interpretation), and results/260705-results.md (the one analysis
  already done — so you don't re-derive it).
- Read paper/Commitment Without Compliance.md, especially §5 (the five primitives: typed acts,
  four-response protocol, explicit conditions of satisfaction, trust, state machine) and §6
  (validation + failure modes). The thesis lives here. The next planned phase is a protocol-layer
  ("Pi") instantiation — value that shows up at the coordination/system layer, not the
  single-agent-outcome layer, is especially relevant.
- Then TELL ME back, in a few sentences, what you understand my thesis and goals to be, and ASK
  me to confirm or correct before you finalize any questions. Consider the essays/ and reference/
  folders if they sharpen it.

STEP 2 — Understand what the models actually DID (not just the aggregate scores).
- Use harness/inspect_episode.py to read real episodes across all conditions and all four task
  classes. Read the B negotiations specifically (negotiation.json): the promises and their
  self-authored conditions of satisfaction, the declines, the counter-offers, and the completion
  reports. Compare against what A and B′ produced on the same task.
- The question to hold throughout: what did Condition B PRODUCE or DO that A and B′ structurally
  could not — regardless of whether it changed the pass/fail outcome? (e.g. a legible declared
  contract of "done"; a machine-readable typed decision; a cited reason for declining; a
  separated up-front deliberation artifact; front-loaded refusal that avoids wasted execution.)
  These are starting provocations, NOT conclusions — derive your own from the episodes.

STEP 3 — Produce the finalized question list (the deliverable).
  For each candidate hypothesis/question:
  - the claim/intuition in one line;
  - the specific thing IN THE DATA that motivates it (cite ≥1 real episode via inspect_episode.py
    with a verbatim quote/diff — no ungrounded speculation);
  - which layer it lives at (single-agent outcome vs coordination/protocol/system);
  - how it connects to my thesis and the Pi next phase;
  - a PRELIMINARY note on whether it's testable over the existing 216-episode corpus and whether
    it'd be mechanical or judged (don't design the test — just flag feasibility).
  Prioritize the list against my thesis/goals. Group near-duplicates. Aim for the ~6-12 questions
  that actually matter, not a long tail.

METHOD & INTEGRITY (important):
- Anything discovered in THIS data is EXPLORATORY / hypothesis-generating, not confirmatory — you
  cannot pre-register against the same data that generated the idea. Say so plainly. For each
  candidate, note the honest path to credibility: (a) does the pattern hold across ALL THREE reps
  (internal robustness), or (b) is it best treated as a hypothesis to pre-register for a FUTURE
  run? Do not present post-hoc patterns as established results.
- No fabrication: every motivating observation must name a real episode reproducible via the tool
  and quote actual text/diff/verdict. If an intuition doesn't survive contact with the episodes,
  drop it and say why.
- The run is FROZEN and read-only. Do not modify runs/, results/, tasks/, rubrics/, judge prompts,
  or any artifact. This phase writes at most a proposal doc (e.g. analysis/new-hypotheses.md).
- Descriptive, per-class thinking; it's a pilot (N=18/cell, correlated within task).

A structured brainstorming pass is appropriate here — if you want to use a brainstorming/shaping
skill for the hypothesis-generation step, propose it to me first and explain what changes.

Deliver Phase 1 as: (1) your read of my thesis/goals for me to confirm, then (2) the prioritized
question list. STOP there and get my sign-off before any backtest design.
```

---

## Why it's shaped this way (for whoever opens this file)

- **The Phase-1 gate is methodological, not bureaucratic.** Hypotheses discovered in this corpus
  are exploratory; testing them on the same data that suggested them is overfitting. The honest
  reuse is *hypothesis generation*, with **cross-rep robustness (holds in all 3 reps)** as the
  cheap internal check and a **future pre-registered run** as real confirmation.
- **The search is pointed at "what B produced/did that A/B′ structurally couldn't,"** not "where
  B scored higher." The original metrics measured outcomes and surfacing *rates*; the protocol's
  distinctive output is *artifacts* — a declared checkable contract of "done", a typed routable
  decision, a cited refusal. Those are coordination-layer / legibility / auditability properties a
  single-agent pass/fail rubric is structurally blind to. That is the likely home of the
  uncaptured value.
- **It reflects the thesis back before generating questions** so the list stays anchored to what
  Shyam is actually trying to establish (the Pi protocol-layer case), not a generic "is the
  protocol good" hunt.
```
