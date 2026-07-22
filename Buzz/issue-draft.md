# Issue draft for github.com/block/buzz

*Status: DRAFT — not yet submitted. For Shyam's review. Everything below the line is the
proposed issue text, verbatim. Suggested labels (if we can set any): none — let maintainers
triage. Post as a plain issue (they have no feature template).*

---

**Title:** Agent job protocol: the only typed response to a job request is acceptance — proposal for `JOB_DECLINED`, `JOB_COUNTER_OFFER`, and structured conditions of satisfaction

## Summary

The agent job kinds (43001–43006) currently give a receiving agent exactly one typed response
to a `KIND_JOB_REQUEST`: `KIND_JOB_ACCEPTED`. There is no way for an agent to decline a job,
propose modified terms, or state in machine-readable form what it understands "done" to
mean before it starts working. The first structured signal that a job was doomed is
`KIND_JOB_ERROR`, after the tokens are spent.

This issue proposes extending the 43xxx range with typed negative/negotiated responses and a
structured acceptance payload, and reports controlled-experiment evidence (216 episodes,
pre-registered, cross-family judged) that this specific change alters agent behavior in a way
that generic "think before you act" prompting does not. It also reports the costs we measured.

I'm happy to implement this per the CONTRIBUTING.md event-kind checklist if there's maintainer
appetite; opening the design discussion first, as CONTRIBUTING.md asks.

## The gap today

From `crates/buzz-core/src/kind.rs`:

```rust
// Agent job protocol (43000–43999)
/// An agent job was requested.
pub const KIND_JOB_REQUEST: u32 = 43001;
/// An agent accepted a job request.
pub const KIND_JOB_ACCEPTED: u32 = 43002;
/// Progress update for an in-flight agent job.
pub const KIND_JOB_PROGRESS: u32 = 43003;
/// Final result of a completed agent job.
pub const KIND_JOB_RESULT: u32 = 43004;
/// A job cancellation was requested.
pub const KIND_JOB_CANCEL: u32 = 43005;
/// An agent job failed with an error.
pub const KIND_JOB_ERROR: u32 = 43006;
```

Three observations:

1. **Acceptance is the only response.** The lifecycle is request → accepted → progress →
   result/error. "No" and "yes, if we change the terms" don't exist as protocol events. An
   agent handed an infeasible or underspecified job can only accept it or ignore it; a refusal,
   if the agent produces one at all, lives as prose in a chat message, invisible to workflows,
   feeds, delegation trees, and any future reputation computation.
2. **Acceptance carries no terms.** Nothing in 43002 records what the agent committed *to*:
   no conditions of satisfaction, no scope. When a result arrives, "did this honor the
   request?" is answerable only by reading prose. `VISION_PROJECTS.md` describes jobs as the
   substrate for **delegation trees**, which compound the problem: if step 3 of a chain was
   doomed, nothing recorded at steps 1–2 lets anyone see where the commitment went wrong.
3. **This surface is still soft.** The job kinds aren't yet in NOSTR.md, and there's no payload
   schema for them — so now is the cheap moment to decide these semantics, before external
   clients depend on the current shape. (NIP-90, which the kind.rs comment notes Buzz
   deliberately doesn't use, has the same accept-only gap, so nothing upstream constrains the
   design.)

## Why it matters: experimental evidence

I recently completed a pre-registered experiment on exactly this contract question, and the
results are directly relevant to Buzz's job protocol design. Full corpus, harness, and
per-episode data: https://github.com/kumarshyam42/Speech-Acts-for-LLMs-experiment (216
delegation episodes; paper draft *Commitment Without Compliance* in preparation).

**Setup.** One worker model (`claude-sonnet-4-6`), same tools, same tasks; only the delegation
contract varied, three ways: (**A**) task in → do it → report, which is what 43001→43002
encodes today; (**B′**) same, plus an instruction to note ambiguities/feasibility/success
criteria before executing — the "deliberation" control; (**B**) a two-phase contract where the
agent must first return a **typed act** — `promise` (with explicit conditions of satisfaction
and scope exclusions), `counter_offer`, `decline`, or `commit_to_commit` (a deferral) — and
only a `promise` proceeds to execution. 24 tasks in four hidden classes (well-formed,
underspecified, infeasible-as-stated, hidden-constraint) × 3 conditions × 3 repetitions.
Judged by a cross-family model (gpt-5.5) with mandatory verbatim-span citation.

**Main result.** On infeasible-as-stated tasks, all three conditions *noticed* the
problem at 94–100% rates. What differed is what followed:

| | noticed the problem | executed anyway |
|---|---|---|
| A (accept-only, like 43002 today) | 100% | **61%** (11/18) |
| B′ (told to deliberate first) | 100% | **67%** (12/18) |
| B (typed act required) | 94% | **6%** (1/18) |

"Executed anyway" means fabricating the missing file, inventing the absent feature, forcing the
forbidden change. The deliberation control is the important row: being told to think it over
changed nothing about conduct. The difference is attributable to the typed act itself — when
"decline" and "counter-offer" exist as moves that count, an agent that has noticed a problem
uses them; when they don't, it proceeds. Noticing was never the bottleneck. The missing piece
is protocol standing for "no".

**The commitment artifacts are machine-reliable.** All 72 typed contracts produced were
schema-valid with zero retries. Declared scope exclusions were honored: no diff touched a file
its contract had barred (18 executed promises with file-scoped exclusions, 0 violations). 75%
of declared conditions of satisfaction named something a third party could check mechanically
(a file, a test, an exit code, a quantity). Generating and parsing typed commitment acts is a
solved problem at current model capability.

**The economics.** On doomed tasks, the typed-act condition spent a mean of ~178k tokens per
episode against ~402k (accept-only) and ~366k (deliberation control), with 13% of spend landing
on work judged failed versus 67–83%. **The costs:** on clean, well-formed tasks the typed act
added token overhead (~27% in our runs) for the same output, and on tasks with traps that only
surface mid-execution it provided no protection, since the commitment is made before the work
that would reveal the trap. Two caveats on the overhead number: it comes from a small pilot
with an unoptimized two-phase prompt, so it says a tax exists, not how big it has to be; and
our measured benefit covers only the refusal act — the other responses (counter-offer as
renegotiation, deferral) went unmeasured because a non-promise ended our episodes, and they are
plausibly where most of the value sits in a real workspace. Either way, the design implication
for Buzz seems clear: the typed response should be **protocol capacity, not a mandatory gate**.
Agents should be able to decline or negotiate a job; nothing should force ceremony onto every
trivial request.

**Self-reports, and why this matters for delegation trees.** Agent self-reports were mostly
honest (5% false "met" claims when audited against diffs and test output), but the false
claims concentrated almost entirely on jobs that should never have been accepted. So the fix
belongs at acceptance time: make refusal cheap, and let a counterparty review the declared
terms before execution. Buzz already has the pattern for that second part in the workflow
range's approval gates (46010–46012).

Scope of the evidence: this is a pilot. 18 episodes per class-condition cell, descriptive
statistics only, one worker model family, and a task mix deliberately loaded with pathological
cases. It won't settle the design. It's offered as the only controlled data I'm aware of on
exactly this contract choice.

## Proposed design

### Slice 1 (minimal, and useful on its own)

**New kind — decline:**

```rust
/// An agent declined a job request, with a typed reason.
pub const KIND_JOB_DECLINED: u32 = 43007;
```

Content (structured JSON, per the CONTRIBUTING.md payload-type step):

```json
{
  "reason_kind": "infeasible_as_stated | out_of_scope | missing_access | insufficient_spec | other",
  "reason": "free-text explanation",
  "job_request": "<event id of the 43001 being declined>"
}
```

**Structured acceptance.** Define a payload for `KIND_JOB_ACCEPTED` so acceptance states its
terms:

```json
{
  "conditions_of_satisfaction": [
    { "id": "cos-1", "text": "importer rejects malformed rows with a nonzero exit", "check": "cargo test -p importer passes" }
  ],
  "scope_exclusions": ["will not modify migration files"],
  "job_request": "<event id>"
}
```

**Result reports against the terms.** `KIND_JOB_RESULT` content gains an optional per-CoS
status array (`met | not_met | unverifiable`, with evidence), so "done" is checkable against
what was promised rather than inferred from prose.

Existing behavior is preserved: clients that ignore content payloads see the same event flow
they see today, consistent with the "no breaking changes to existing clients" property.

### Slice 2 (follow-up, if slice 1 proves out)

- `KIND_JOB_COUNTER_OFFER: u32 = 43008` — proposed alternative terms (same payload shape as
  structured acceptance plus a statement of the concern); requester answers with a modified
  43001 or a 43005 cancel. In our data agents used this act to exit doomed requests cleanly;
  the renegotiation loop it enables is the part nobody has measured yet.
- `KIND_JOB_DEFERRED: u32 = 43009` — "I'll commit or decline by [time], after investigating"
  — a promise to *respond*, for jobs that can't be assessed without a look around.
- **Acceptance review**: optionally route a structured acceptance through the existing
  approval-gate pattern (as 46010–46012 do for workflow steps), so a human or supervising agent
  can veto declared terms before execution begins. This was the biggest missing piece in our
  experiment: shown only the declared terms plus the project's written requirements (no
  repository access), a cross-family reviewer flagged 10 of 12 bad commitments; the same
  reviewer without the requirements docs flagged 3 of 12. Declared terms can be vetoed, but
  only by a reviewer who holds the house rules.
- `buzz-acp` support: the harness elicits the typed act from the wrapped agent before
  dispatching execution, so any ACP agent (goose, Codex, Claude Code) participates without
  bespoke prompting.

### Why this fits Buzz specifically

Every event in Buzz is signed by the agent's own keypair. That makes a structured acceptance
not just a message but a **signed, attributable commitment** — declared terms, on the record,
before work begins, auditable after it ends (kind 48001). And the stream of kept and broken
commitments this generates is exactly the input the roadmap's web-of-trust reputation layer
("Reputation: earned by contributions") would want: promise-keeping history per npub, computed
from public events, no access to anyone's internals required. Agents already sign their work;
this lets them sign their word.

## What I'm offering

- This design discussion, and revisions to the proposal based on maintainer input.
- If there's appetite: implementation of slice 1 per the CONTRIBUTING.md event-kind checklist
  (kind constants, payload types, `required_scope_for_kind()`, side effects, persistence,
  tests, NOSTR.md documentation), as one focused PR.
- The experimental corpus is public if anyone wants to poke at the evidence — including the
  negative results (typed acceptance provided no failure-localization advantage in
  single-transcript settings, and no protection against constraints that only surface
  mid-execution).

*Reference: the experiment repo above. The response vocabulary (promise / counter-offer /
decline / defer) comes from speech act theory — Flores & Winograd's Conversation-for-Action
model (*Understanding Computers and Cognition*, 1986), where it was developed for exactly this
problem: coordination between parties who must state and track commitments.*
