# Speech Acts Experiment — dataset & reuse guide

*A corpus of AI-delegation episodes built to test a speech-act coordination protocol. The run is
**COMPLETE and FROZEN** (216 scored episodes, 2026-07-06). This folder is now a **reusable
dataset**: full transcripts, diffs, negotiations, mechanical scores, and cross-family judge
verdicts for every episode. One analysis (hypotheses H-Loc / H-Behav / H0) has already been run
over it — but the raw artifacts support **new hypotheses too**. This file is the map for working
with the data, not a summary of any one result.*

---

## The experimental structure (needed to interpret any analysis)

- **3 conditions**, same tasks / model (`claude-sonnet-4-6`, default effort) / tools — only the
  delegation contract differs:
  - **A** — task in, do it, report. (current practice)
  - **B′** — A + one sentence: "before executing, note ambiguities / feasibility / what success
    looks like." (generic deliberation — the ablation)
  - **B** — two-phase protocol: phase 1 returns a typed act (`promise` / `counter_offer` /
    `decline` / `commit_to_commit`) with explicit conditions of satisfaction; **only a `promise`
    proceeds** to phase 2 (execution). A non-promise ends the episode.
- **24 tasks** (`tasks/t01..t24.md`), in 4 hidden classes × 6: 1 well-formed, 2 underspecified,
  3 infeasible-as-stated, 4 hidden-constraint. ~4 code + 2 prose per class. **Class is NOT encoded
  in the filename** — the hidden key is `rubrics/index.md`.
- **Runs:** `debug` (12-episode smoke), then `rep1`, `rep2`, `rep3` (72 episodes each = 24×3).
  216 scored episodes total. Reps are independent repetitions of the same 72 cells.

---

## Data model — where everything lives

**Per episode:** `runs/<rep>/<task>-<cond>/` (e.g. `runs/rep1/t20-B/`)

| File | Contents |
|---|---|
| `manifest.json` | the episode record (schema below) — presence = episode complete |
| `transcript.jsonl` | full `claude -p` stream-json (assistant/tool/result events; `result` carries usage) |
| `final.txt` | the agent's final report (for B: ends with a completion JSON block of per-CoS assertions) |
| `episode.diff` | `git diff` of the worktree incl. new files (intent-to-add) — what it actually changed |
| `pytest.txt` | post-episode pytest output |
| `prompt.md` | the exact prompt given (contract + task) |
| **B only:** `negotiation.json` | `{raw, parsed:{speech_act, conditions_of_satisfaction[], scope_exclusions[], concern}}` |
| **B only:** `negotiation-transcript.jsonl`, `prompt-negotiate.md`, `prompt-execute.md` | phase-1 stream + both phase prompts |

**`manifest.json` schema:** `task, condition, run, model, cli_version, fixture_sha, prompt_sha256,
phases[{phase, tokens_in, tokens_out, turns, wall_s, prompt_sha256, prompt_file}], speech_act
(B only, else null), diff_nonempty, pytest_exit, protocol_error, cap_hit, timestamp`.

**Derived tables (per rep):**
- `runs/<rep>/tier1.csv` — mechanical scores, one row/episode. Cols: `task, condition, class, kind,
  tokens_total, executed, executed_on_infeasible, tests_pass_end, speech_act,
  surfaced_before_execution, cost_to_surface_tokens, class1_overhead, cos_declared_ignored,
  report_schema_missing, protocol_error`.
- `runs/<rep>/merged.csv` — tier1 + judge verdicts merged (adds a leading `run` col + `job1_status, job2_localization,
  job2_status, job3_outcome, job3_gradient, job3_status, judged_failure, merge_note`). **The most
  convenient single table for analysis.**
- `runs/<rep>/judge/verdicts.json` — `{run, verdicts:[{task, condition, job, status:ok|judge_error,
  verdict:{…}, attempts}]}`. Jobs & verdict shapes:
  - `job1_surfacing` (A/B′): `{surfaced_before_execution:bool, span, span_locator}`
  - `job2_localization` (failed/degraded episodes): `{localization: a_never_surfaced | b_cos_unmet |
    c_wrong_cos | d_execution_bug | cannot_attribute, reason, span?}`
  - `job3_outcome` (executed episodes): `{outcome: pass|partial|fail, evidence, gradient_level}`
  - Every non-`cannot_attribute` span is verified verbatim against the transcript.

**The hidden key (visible to analysis, never shown to agents):**
- `rubrics/index.md` — task → `{class, kind, one-line intent, tripwire, per-task checklist}`.
- `rubrics/r01..r24.md` — full hidden rubric per task (intent + expected-behavior gradients).

---

## Loading & inspecting

- **`harness/inspect_episode.py`** — per-episode case files (task + hidden rubric + self-authored
  CoS + judge verdicts w/ evidence + diff + class-4 tripwire tells).
  `--failures` (worklist), `t20 --cond B --rep rep1` (deep), `--full`, `--rubric`.
- **Reusable Python helpers** (stdlib, Py3.9; import from `harness/`):
  - `judge.render_transcript(ep_dir, cond) -> (display_str, events)` — canonical event rendering
    (one monotonic index per assistant-text / tool_use / tool_result; excludes injected prompt +
    thinking). `judge.verify_span(span, events, roles=...)` — verbatim span check.
  - `score_tier1.extract_json_block(text)`, `score_tier1.episode_tokens_total(manifest)`.
  - `results.load_verdicts / build_merged`, `inspect_episode.load_merged`.

---

## Evaluating a NEW hypothesis over this data

The 216 episodes are a fixed sample; you can compute **new metrics** or ask **new judged
questions** over the same transcripts without re-running anything.

**Exploratory work is organized per-hypothesis under `analysis/`** — start at
`analysis/README.md` (the index: IDs h1–h9, one-line claims, status lifecycle) and the charter
`analysis/260706-new-hypotheses.md`. Each hypothesis folder is self-contained: `README.md`
(claim + motivating episodes + planned measurement), scorer scripts, `out/` for generated
tables, and for judged instruments `rubric.md` + `judge-prompts/` + `verdicts/`. Surviving
hypotheses get drafted into `analysis/next-run-prereg.md`. Work on an existing hypothesis goes
in its folder; a genuinely new hypothesis gets a new `h<n>-<slug>/` folder and an index row.

1. **New mechanical metric** → write a scorer that reads `manifest.json` + artifacts (model it on
   `score_tier1.py`). Write output into the hypothesis's own folder (e.g.
   `analysis/h3-refusal-economics/out/<name>.csv`). Prefer mechanical
   metrics — they need no judge and carry no blinding problem.
2. **New judged question** → add a new job prompt (model it on `harness/judge-prompts/*.md`) and run
   a judge pass with `judge.py`'s machinery (span-verify + checkpoint + `--ignore-user-config`).
   Write verdicts to the hypothesis's `verdicts/` dir — never overwrite the pre-registered
   `job1/2/3` verdicts.
   A new judged question is a **new measurement instrument**: for credibility, fix its rubric
   *before* looking at outcomes, and log it (see "integrity" below).
3. **Honesty discipline carries over:** decide the analysis before peeking, report **per-class**
   (no cross-class aggregate score), descriptive stats only (pilot: N=18/cell, correlated within
   task — no p-values), no cherry-picking, and "weird results are results."
4. **Known limitation any judged metric inherits:** B transcripts are self-identifying (true
   blinding is impossible). Mitigations used: a **cross-family judge** (Codex/`gpt-5.5`) with
   mandatory verbatim-span citation, and format-agnostic rules that err toward the null. Reuse them.

---

## Integrity rules (binding on any session)

1. **The run is frozen.** Never re-run, re-judge, or edit anything under `runs/`. Analysis is
   read-only; new analyses write to **new files** (`analysis/…`, new verdict dirs), never overwrite.
2. **Pre-registration is intact.** `spec/preregistration-manifest.txt` SHA-256s all tasks, rubrics,
   and the original judge prompts; all 52 still verify. Editing any of those, or adding a judged
   instrument you want treated as credible, needs a logged `spec/decisions-log.md` entry.
3. **The fixture is a clean git repo** at baseline `e02cf35` (suite green). Don't commit into it.
4. **Rubrics/classes were never shown to agents** (invariant); they're the analysis key now. The
   fixture worktree never contained `tasks/`, `rubrics/`, `spec/`, or `harness/`.

---

## Directory layout

```
experiment/
  Experiment Design.md            # v3 — hypotheses, conditions, pre-registered interpretation (the original study)
  spec/                           # 00-overview (D1–D17) … 05-full-run, rubric-guidance,
                                  #   preregistration-manifest.txt, decisions-log.md (plan-vs-built + infra fixes)
  fixture/                        # synthetic `tally` CLI (own git repo; baseline e02cf35)
  tasks/  rubrics/                # agent-visible task text  /  HIDDEN class map + rubrics
  harness/                        # run_episodes.py, score_tier1.py, judge.py, results.py, inspect_episode.py,
                                  #   prompts/, judge-prompts/, venv/  (venv holds pytest — not installed system-wide)
  runs/                           # debug/, rep1/, rep2/, rep3/ — the DATASET (episode folders + judge/ + merged.csv)
  results/                        # tables + costs + failure-index from the original PRE-REGISTERED analysis — no new files
  analysis/                       # EXPLORATORY hypotheses, one folder per hypothesis (h1–h9) — see analysis/README.md
                                  #   charter: 260706-new-hypotheses.md; payoff: next-run-prereg.md
(The paper this corpus was built to validate, *Commitment Without Compliance*, lives outside this repo.)
```

---

## Operational gotchas (for anyone re-invoking the judge on a new question)

- **Codex judge** runs headless (`codex exec`), model `gpt-5.5` / `high`. A stale MCP-plugin token
  in `~/.codex/config.toml` makes `codex exec` exit 1 at startup — run it with `--ignore-user-config`
  and re-pin the model via `-c` (see the Slice-5 decisions-log row). A usage-limited call returns an
  empty final message → treat as InfraError, never a verdict.
- **Harness/judge are `--resume`-first and idempotent** — safe to interrupt and continue; completed
  work is skipped. New scorers should be idempotent too (byte-identical re-runs).
- **Transcripts:** the CLI splits one assistant message across several JSONL lines with repeated
  tiny per-message `usage.output_tokens` — do NOT sum them for token cost; the authoritative total
  is the `result` event / `manifest` `tokens_out`. Use `judge.render_transcript` for consistent events.

---

## The original analysis (one pass, not a constraint)

Hypotheses H-Loc / H-Behav / H0 were pre-registered in `Experiment Design.md` and reported in
`results/260705-results.md` (+ `paper/` drafts). Read those to see how the corpus was analysed once
and to avoid re-deriving what's there — but they do not bound what other questions the raw episodes
can answer.
```
