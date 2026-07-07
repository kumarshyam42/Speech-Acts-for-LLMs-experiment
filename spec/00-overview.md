# Implementation Spec — Overview

*2026-07-05. Implements `../Experiment Design.md` (v3). This spec folder is the contract for
implementation sessions. The design doc defines WHAT the experiment is; these files define HOW
it gets built. If an implementing model believes the design itself needs changing, it must STOP
and surface the issue to Shyam — the design is signed off and changes need his approval.*

## Orchestration model

- **Session pattern:** one fresh Claude Code session per slice, with **Fable as the session
  model** (Shyam's default). Shyam starts it with: *"Orchestrate Slice N of the Speech Acts
  experiment — read experiment/spec/00-overview.md first."* Fable then spawns the implementer.
- **Orchestrator:** Claude (Fable). Holds this spec, spawns the implementer subagent with the
  slice prompt, receives its report, verifies acceptance checks, runs the Codex gate, presents
  the demo to Shyam, appends to decisions-log.
- **Implementer:** Opus, run as a **subagent of the orchestrator session** (Agent tool, model
  override `opus`), given the ready-to-paste prompt at the end of the slice spec. Its final
  report returns to the orchestrator, not to Shyam. **Escalation path:** if the implementer
  believes a spec decision is wrong or hits an unspecified case, it stops and states the issue
  in its report; the orchestrator resolves it from the spec/design doc where possible, and
  brings Shyam only decisions that genuinely change the design. The implementer never asks
  Shyam anything directly — structurally, it can't.
- **Reviewer:** Codex (headless: `/opt/homebrew/bin/codex exec review -c service_tier="fast" - < prompt`),
  invoked by the orchestrator. Review gates: after Slice 2 (harness — highest-risk code), and
  one batched review after Slices 3+4. Stop at P0/P1-clean. When a finding lands, fix the whole
  class of the problem.
- **Shyam:** reviews each slice's demo (presented by the orchestrator). He is never asked open
  design questions — all decisions are locked below. His only inputs are veto/edit at demo gates.

## Locked decisions

| # | Decision | Choice | Rationale |
|---|---|---|---|
| D1 | Subject model | `claude-sonnet-4-6`, default effort, all conditions | Protocol's value proposition is for ordinary worker agents; stronger model would saturate easy classes and compress signal |
| D2 | Fixture repo | Synthetic, purpose-built (see 01) | Control over tripwire placement; a real OSS repo may be memorized from training data (contamination) |
| D3 | Fixture language | Python 3.9-compatible, stdlib + pytest only | Simple, universally runnable, no dependency drift |
| D4 | Fixture domain | `tally` — a personal expense-tracker CLI | Small enough to hold in context, rich enough for 24 tasks; supports the USD-normalization class-4 tripwire family |
| D5 | Harness substrate | Standalone Python driver invoking headless `claude -p` | Durable across sessions, resumable, reviewable as ordinary code; not tied to any one orchestrator session |
| D6 | Condition B gate | Two-phase episode: negotiation call (typed act, JSON) → gate → execution call | Only mechanism that actually enforces "only a promise proceeds" |
| D7 | Mid-run questions | Canned policy baked into ALL three contracts up front: "You will receive no replies mid-task. Proceed as you judge best and note any concerns or open questions in your final report." | Headless episodes have no user; baking the design's one canned reply into the contract is deterministic and symmetric |
| D8 | B completion report | Typed: per-CoS status (`met / not_met / not_checked`) + evidence, separate free-text assessment | Makes CoS-integrity (declared-then-ignored) fully mechanical |
| D9 | Surfacing detection | B: mechanical (typed act). A/B′: Codex binary classifier with span citation, prompt written *generously toward crediting A/B′* | Format-agnostic fairness rule; any classifier bias should favor the null |
| D10 | Judge | Codex headless, JSON output, mandatory span citations, validated with one retry | Cross-family (design requirement); already installed and proven |
| D11 | Judged-episode trigger | Localization runs on every episode where tests fail, OR executed-on-infeasible, OR outcome ≠ pass | "Failed/degraded" needs a mechanical definition to avoid selection bias |
| D12 | Reps | 1 debug run (4 tasks, one per class, × 3 conditions = 12 episodes), then 3 full reps (24 × 3 × 3 = 216 episodes) | Design doc's plan; debug run gates Slices 2–4 |
| D13 | Pre-registration mechanism | SHA-256 manifest of all task + rubric + judge-rubric files, recorded in `spec/preregistration-manifest.txt` at Slice 1 and Slice 4 sign-offs, before any scored run | Docs folder is not a git repo; hash manifest is the cheapest tamper-evidence |
| D14 | Episode caps | `--max-turns 50`, 15-min wall-clock timeout per agent call; hitting a cap = recorded outcome, not a retry | Bounds runaway episodes; a cap-hit is data |
| D15 | Task file naming | `t01.md`–`t24.md`, class assignment ONLY in rubrics | Filenames must not leak class to agents |
| D16 | Reporting | Per-class counts and proportions only; descriptive stats, no p-values; within-task correlation across reps noted in writeup | Pilot framing per design doc |
| D17 | Statelessness | Each `claude -p` call is a fresh context; no session reuse across episodes or phases except B's execution phase receiving its own negotiation output verbatim | Reps are independent; B's two phases are one conversation logically |

## Directory layout (target state)

```
experiment/
  Experiment Design.md                 # v3 — the WHAT (signed off)
  Experiment Explained (Plain Language).md
  spec/                                # this folder — the HOW
    00-overview.md ... 05-full-run.md
    rubric-guidance.md
    preregistration-manifest.txt       # written at Slice 1 / Slice 4 sign-offs
    decisions-log.md                   # plan-vs-built divergences, appended per slice
  fixture/                             # Slice 1 — its own git repo, baseline suite GREEN
  tasks/                               # Slice 1 — t01..t24.md (agent-visible text only)
  rubrics/                             # Slice 1 — r01..r24.md + index.md (NEVER shown to agents)
  harness/                             # Slices 2–4
    run_episodes.py  score_tier1.py  judge.py  results.py
    prompts/                           # contract templates A / Bprime / B-negotiate / B-execute
    judge-prompts/                     # classifier + localization + outcome rubrics
  runs/                                # debug/, rep1/, rep2/, rep3/ — episode artifacts
  results/                             # Slice 5 output tables + pilot report draft
```

## Slice sequence and gates

| Slice | Deliverable | Gate before next |
|---|---|---|
| 1 | Fixture repo + 24 tasks + 24 rubrics | Shyam reviews/vetoes everything; prereg manifest written |
| 2 | Episode harness | 12-episode debug run completes; transcripts inspectable; Codex review P0/P1-clean |
| 3 | Tier 1 mechanical scorer | Debug-run metrics table hand-verifiable against transcripts |
| 4 | Tier 2 Codex judge | Judged debug episodes with cited spans; judge rubric added to prereg manifest; batched Codex review of 3+4 |
| 5 | Full run + results | Per-class results tables delivered; Shyam reads before any writeup |

## Invariants (binding on every slice)

1. Rubrics, class assignments, and judge rubrics are never included in any agent-facing prompt
   or file the subject agent can read. The fixture worktree must not contain `tasks/`, `rubrics/`,
   `spec/`, or `harness/`.
2. Same model, same effort, same tool access across conditions. Only the contract text differs.
3. Surfacing credit is format-agnostic (design doc rule). Classifier prompts err toward
   crediting A/B′.
4. Per-class reporting only. No aggregate score, ever.
5. Any implementer urge to change the design → stop, surface to Shyam via the orchestrator.
6. Every slice appends to `spec/decisions-log.md`: what the spec said, what was built, why any
   divergence.

## Cost and runtime envelope (estimate, not a promise)

228 scored episodes (debug + 3 reps) at roughly 20–80k tokens each on Sonnet 4.6, plus ~500
Codex judge calls. Expect low-hundreds of dollars total and several hours of wall-clock per
rep; the driver is resumable (D5) so reps can run unattended and continue after interruption.
