# Buzz research notes — everything read, in plain language

*Compiled 2026-07-22 (Buzz's public launch day) from the block/buzz repository (shallow clone at
commit of that day), its documentation files, and launch press. This is the evidence file behind
`issue-draft.md`. Written for a non-technical reader first, with the technical receipts inline.*

---

## 1. What Buzz is, in one paragraph

Buzz is an open-source (Apache 2.0) workplace built by Block (Jack Dorsey's company) where AI
agents and humans are literally the same kind of citizen. Think Slack + GitHub in one self-hosted
app, except every message, code change, and decision — by a human or an agent — is a
cryptographically **signed event** in one shared log. Agents get their own keys, their own
identity, their own audit trail. Tagline material from their README: *"Agents are part of the
room, not haunted cron jobs"* and *"Buzz works best when humans stay in the loop and agents stay
in the room."* Launched publicly 2026-07-22; ~3.9k stars, 94 open issues, very active.

## 2. How Buzz works technically (the minimum needed to understand our proposal)

- Built on **Nostr**, a simple open protocol where everything is an "event": a small signed JSON
  object with a `kind` number that says what type of thing it is (a chat message is kind 9, a
  reaction kind 7, etc.).
- **"Event kinds are the only switch."** (CONTRIBUTING.md, verbatim.) Every feature in Buzz is a
  kind number. *"Adding a new feature means defining a new kind. No breaking changes to existing
  clients."* This is their official, documented extension mechanism — which is precisely the
  shape of our proposal.
- Custom Buzz kinds live in ranges: 40xxx messaging, 43xxx **agent jobs**, 45xxx forum,
  46xxx workflows, 48001 tamper-evident audit log.

## 3. The agent job protocol — the gap our proposal fills

From `crates/buzz-core/src/kind.rs` (verbatim, including their comment):

```rust
// Agent job protocol (43000–43999)
// Not using NIP-90 kinds (5000–6999) — Buzz requires auth chains (depth ≤ 3, breadth ≤ 10).
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

Read as a conversation: someone asks (43001), the agent says **yes** (43002) — and that is the
only word the agent has. There is no "no", no "yes, but", no "here is exactly what I understand
done to mean". The first structured signal that a job was doomed is the error event — **after**
the work (and tokens) are spent. This is condition A of our experiment, encoded on the wire.

**Maturity of this surface (important for timing):**
- The kinds are defined and shown in the desktop app's activity feed (job events render as
  non-conversational system rows).
- But: no payload schema exists for any of them, no relay-side state machine, and they are
  **absent from NOSTR.md**, Buzz's own protocol documentation, which documents every other
  surface. `VISION_PROJECTS.md` lists "Job dispatch — 43001–43006 — Delegation trees" and
  imagines a "Coding agent" that "watches Jobs (kind:43001), implements tasks, submits patches
  for review".
- Conclusion: the delegation protocol is scaffolding whose semantics are being decided
  approximately now. This is the moment where a well-evidenced proposal has maximum leverage.

**Their own precedent for our shape of fix:** the workflow range already has approval gates —
`KIND_WORKFLOW_APPROVAL_REQUESTED/GRANTED/DENIED` (46010–46012). So "a step that must be
reviewed before it proceeds" is an established Buzz pattern. Our proposal extends the same idea
to the moment a job is accepted.

**NIP-90 note:** Nostr's ecosystem has a "Data Vending Machine" spec (NIP-90) for job
request/result. Buzz deliberately didn't use it (their comment: auth-chain requirements). NIP-90
also has only request → result/feedback — no negotiation semantics — so going custom gives Buzz
the freedom to get this right, and nothing upstream constrains them.

## 4. Where our other ideas plug in

| Our concept (paper) | Buzz surface |
|---|---|
| Typed act gate (Primitive 2: promise / counter-offer / decline / deferral) | New kinds in the free 43007+ range |
| Explicit conditions of satisfaction (Primitive 3) | Structured JSON `content` on 43002 (their checklist step 2 is literally "define the payload type") |
| Per-CoS completion reporting | Structured content on 43004 JOB_RESULT |
| Assessing counterparty (the paper's "absent component") | Their existing approval-gate pattern (46010–46012), applied at job acceptance |
| Promise-keeping ledger → trust (Primitive 4) | Their roadmap item "Web-of-trust reputation — 📋 Designed"; every commitment event is already signed by the agent's own key |
| Public, signed commitments (Singh's move) | Their core identity model: "Reputation: earned by contributions", identical for humans and agents |
| Two-phase contract harness (our condition B) | `buzz-acp`, their agent harness that turns @mentions into agent prompts and could elicit the typed act before dispatching execution |

The deepest alignment: our paper's conclusion is that commitments must be **public objects,
verifiable without access to anyone's inner states**. Buzz's entire architecture is a machine
for making acts public, signed, and attributable. Their launch framing ("AI agents sign their
own work" — TechTimes headline) extends naturally to *agents signing their own commitments*.

## 5. How contributing works there (process facts)

- **Governance:** maintainer-led (Block's standard model); maintainers approve/merge; a
  Governance Committee is the appeals body. No formal RFC process — CONTRIBUTING.md says to
  **open an issue first to discuss the approach** for significant work. Design discussions
  happen in issues (e.g. #242 "Designing the Human Signal Layer" is a long-running design
  issue — precedent for ours).
- **Issue templates:** only a bug-report template exists; free-form issues are normal.
- **Adding an event kind** is a documented 7–9 step checklist in CONTRIBUTING.md: constant in
  `kind.rs` → payload type → auth scope in `required_scope_for_kind()` → side-effects handler →
  DB persistence → search indexing → audit (automatic) → tests → docs.
- **PR bar:** `just ci` green (fmt + clippy + tests), no new `unwrap()` in production paths,
  documented public APIs, focused PRs, squash-merge. Rust 1.88+, Node 24+, Docker.
- **License:** Apache 2.0.
- **No existing issue** mentions the job protocol, kinds 43001–43006, declining, or negotiation
  (searched their tracker 2026-07-22).

## 6. Evidence available on their tracker context

Open issues on launch day are mostly ops/perf items. #2386 ("instrument end-to-end
mention-to-reply latency") shows maintainer attention on the agent loop's efficiency — our
refusal-economics numbers (tokens saved by early decline) speak directly to that concern.

## 7. Framing decisions taken in the draft (and why)

1. **Their problem first.** The issue opens with their own kind.rs, not with our theory.
2. **Minimal slice offered first**: `JOB_DECLINED` + structured `JOB_ACCEPTED` content.
   Counter-offer/deferral and the acceptance-review gate are staged as follow-ups. Maintainers
   of a week-old project will not take a five-primitive framework in one bite.
3. **Costs reported as prominently as benefits** — the +26.7% token tax on clean work, the
   premature-promise failure on ambiguous tasks, the break-even arithmetic. This is both our
   integrity discipline and the most credibility-building move available: nobody trusts a
   proposal that only has upside.
4. **Evidence grade stated plainly**: pre-registered pilot, N=18/cell, descriptive statistics
   only, one worker model, deliberately pathological task mix.
5. **One link** to our repo; the paper named once. Protocol gap analysis with receipts, not an ad.
