# Goal: A protocol contribution to block/buzz grounded in the speech-acts experiment

**Owner:** Shyam Kumar · **Started:** 2026-07-22 (Buzz's public launch day) · **Status:** SUBMITTED — awaiting maintainer response

**The issue is live: https://github.com/block/buzz/issues/2426** (posted 2026-07-22, same day
as Buzz's public launch; verified rendering correctly — table, code blocks, links all good).

## The one-sentence goal

Get Buzz's agent-job protocol (Nostr kinds 43001–43006) extended with typed commitment
semantics — decline, counter-offer, and explicit conditions of satisfaction — by contributing
a well-argued design issue (and, if maintainers engage, the implementation), using the
216-episode speech-acts experiment and *Commitment Without Compliance* as the evidence base.

## Why Buzz, why now

- Buzz launched publicly on 2026-07-22 (today). Early protocol decisions in young projects
  have long tails; the job-response vocabulary is not yet ossified.
- Buzz's stated extension mechanism is *exactly* new event kinds: "adding a new feature means
  defining a new kind number." Our proposal fits their architecture natively.
- Their job lifecycle today: `JOB_REQUEST (43001) → JOB_ACCEPTED (43002) → JOB_PROGRESS →
  JOB_RESULT / JOB_ERROR / JOB_CANCEL`. The **only** response an agent can give to a job
  request is acceptance. This is condition A of our experiment, wire-encoded.
- Every event in Buzz is cryptographically signed by the agent's own keypair. A promise with
  declared conditions of satisfaction becomes a **signed, auditable commitment** — the
  public-commitment semantics (Singh) our paper argues for, plus the identity layer it lacked.
- Their signed-event log is a promise-keeping ledger waiting to happen — the substrate for
  Primitive 4 (locally computed trust) that no other production system has.

## What we are proposing to them (the ask, in their vocabulary)

1. New kinds: `KIND_JOB_DECLINED`, `KIND_JOB_COUNTER_OFFER` (and optionally
   `KIND_JOB_DEFERRED` for commit-to-commit).
2. Structured content on `KIND_JOB_ACCEPTED`: `conditions_of_satisfaction[]`,
   `scope_exclusions[]`, `concern` — turning acceptance into a promise in the
   Winograd/Flores sense.
3. `KIND_JOB_RESULT` reports per-CoS status, so results are checkable against the declared
   contract instead of read as prose.
4. (Later / optional) harness support in `buzz-acp`: elicit the typed act before dispatching
   execution — the two-phase contract from our condition B.

## Evidence we bring (honestly framed)

- 216 pre-registered episodes, one worker model, contract-only variation, cross-family judge.
- Headline: on infeasible-as-stated tasks, accept-only contracts executed anyway ~61–67% of
  episodes despite noticing the problem; the typed-act gate cut that to 6%. The deliberation
  ablation (B′) proves the *typed act*, not extra thinking, carries the effect.
- Contracts are machine-reliable: 72/72 schema-valid, zero violations of file-scoped
  exclusions, 75% of CoS observable/checkable.
- Refusal economics: ~178k vs ~402k tokens per episode on doomed tasks; 13% vs 67–83% of
  spend landing on failed work. Break-even ≈ 25% infeasible-share of workload; a ~27% token
  tax on clean tasks. We report the tax as prominently as the dividend.
- Known limits stated up front: pilot scale (N=18/cell), descriptive stats only,
  self-identifying transcripts, enriched task mix, single model family as worker.

## Sequence

1. ✅ Evaluate fit (done — see conversation of 2026-07-22).
2. ✅ Read Buzz docs end to end → `Buzz/buzz-docs-notes.md`.
3. ✅ Draft the design issue → `Buzz/issue-draft.md`. Reviewed by Shyam (4 revision rounds:
   cost claim softened, Promise Theory removed, phrasing de-AI'd, essay linked).
4. ✅ Posted 2026-07-22 by Shyam (session couldn't authenticate to third-party repos):
   **https://github.com/block/buzz/issues/2426**
5. ⬜ Engage with maintainer responses (treat as negotiation; expect them to want the
   minimal slice first — likely `DECLINED` + structured `ACCEPTED` content). Their
   CONTRIBUTING.md promises review within a few business days. Anticipated pushback and
   our answer: "why not just prompt for this in buzz-acp?" → the B′ ablation row —
   prompted deliberation didn't change conduct (67% executed anyway); the typed act did (6%).
   NOTE: this session cannot watch block/buzz issues automatically — Shyam brings
   maintainer replies into the session, we draft responses here.
6. ⬜ If receptive: fork, implement kinds per their 9-step CONTRIBUTING checklist, `just ci`,
   focused PR. Rust (buzz-core) + possibly buzz-acp changes.
7. ⬜ Separately: consider a short companion note linking the paper once it has a public home.

## Framing rules (binding on any drafting in this folder)

- Lead with **their** problem (accept-only job protocol), not our paper.
- Evidence grade stated honestly: pilot, descriptive, enriched sample. No p-values, no
  aggregate score, per-class numbers only.
- Report costs as prominently as benefits (the class-1 token tax, the underspecified-task
  premature-promise failure, the hidden-constraint non-protection).
- Link the repo/paper once. This is a protocol gap analysis with receipts, not an ad.
- Match their vocabulary: kinds, relay, events, ACP harness, signed events, `kind.rs`.
