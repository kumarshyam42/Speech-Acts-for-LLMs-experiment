# Reproducing the Speech Acts Experiment

This guide covers, in order: setting up, verifying the integrity of the frozen materials,
reproducing the original analysis from the frozen data (no API spend), re-running the full
experiment from scratch (real API spend), and running the cross-family judge. Operational
gotchas are collected at the end.

Throughout: condition **B′** is spelled `Bp` in folder names, CSV columns, and prompt
filenames (`harness/prompts/Bprime.md`).

## 1. Setup

```bash
git clone <this-repo> speech-acts-experiment
cd speech-acts-experiment

# Create harness/venv (Python venv with pytest — the harness runs the fixture's
# test suite through this interpreter, never a system-wide pytest):
scripts/setup.sh

# Restore the fixture's git history from bundles/fixture.bundle.
# fixture/ ships as plain files; this recreates fixture/.git, checks out the
# baseline, and verifies HEAD == e02cf35 with a clean tree:
scripts/restore_fixture.sh
```

The analysis scripts are stdlib-only Python 3.9+; nothing beyond the venv above is needed
to work with the frozen data. The `claude` and `codex` CLIs are only needed for sections
4 and 5.

## 2. Verify integrity

**Pre-registration manifest.** `spec/preregistration-manifest.txt` holds SHA-256 hashes
(paths relative to the repo root) of all 24 task files, 25 rubric files, and the 3
judge-prompt templates — 52 hashes, frozen before any scored run. Verify all of them:

```bash
grep -E '^[0-9a-f]{64}' spec/preregistration-manifest.txt | shasum -a 256 -c -
```

Every line should print `OK`. (The grep strips the comment lines; `shasum -c` checks the
rest.) If any line fails, the instrument has been modified since the freeze and nothing
downstream should be treated as pre-registered.

**Fixture baseline.** The agents worked in git worktrees of `fixture/` at commit
`e02cf35200d8eb26fe4459c166c79f6787a71fab`, with the test suite green:

```bash
git -C fixture rev-parse HEAD        # e02cf35200d8eb26fe4459c166c79f6787a71fab
git -C fixture status --porcelain    # must be empty
(cd fixture && ../harness/venv/bin/python -m pytest -q)   # 45 tests, all pass
```

(`scripts/restore_fixture.sh` performs the first two checks itself.)

## 3. Reproduce the original analysis from the frozen `runs/` data

No API calls are involved: the scorer and merge stages are pure, idempotent functions of
the artifacts already on disk. Reproduction = regenerate the derived tables and confirm
they are **byte-identical** to the checked-in ones.

**The data model** (full reference: `CLAUDE.md`):

- **Raw episodes** live in `runs/<rep>/<task>-<cond>/` (e.g. `runs/rep1/t20-B/`):
  `manifest.json` (the episode record; its presence marks the episode complete),
  `transcript.jsonl` (full `claude -p` stream-json), `final.txt` (the agent's final
  report), `episode.diff`, `pytest.txt`, `prompt.md`; B episodes additionally carry
  `negotiation.json` (the parsed `speech_act`, `conditions_of_satisfaction`,
  `scope_exclusions`, `concern`), `negotiation-transcript.jsonl`, and both phase prompts.
- **`runs/<rep>/tier1.csv`** — the tier-1 mechanical scores, one row per episode
  (`executed`, `executed_on_infeasible`, `tests_pass_end`, `speech_act`,
  `surfaced_before_execution`, `cost_to_surface_tokens`, `class1_overhead`,
  `cos_declared_ignored`, `report_schema_missing`, `protocol_error`, …). A/B′ surfacing
  cells are deliberately blank here — they are judge (tier-2) questions.
- **`runs/<rep>/judge/verdicts.json`** — the tier-2 verdicts (job1_surfacing,
  job2_localization, job3_outcome), each with a verbatim-verified transcript span.
- **`runs/<rep>/merged.csv`** — tier 1 + judge merged, all blanks filled. **The most
  convenient single table for analysis.**
- **`results/260705-results.md`** — the per-class report over rep1–rep3.

Regenerate and diff:

```bash
# Tier-1 scorer (rewrites runs/<rep>/tier1.csv + tier1-by-class.md):
harness/venv/bin/python harness/score_tier1.py rep1
harness/venv/bin/python harness/score_tier1.py rep2
harness/venv/bin/python harness/score_tier1.py rep3

# Merge + results assembly (rewrites runs/<rep>/merged.csv,
# results/260705-results.md, results/costs.md):
harness/venv/bin/python harness/results.py --runs rep1,rep2,rep3 --date 260705

# Reproduction check: everything must be byte-identical.
git status --porcelain    # must be empty
```

If `git status` is clean, you have reproduced the original analysis exactly. If it is not,
`git diff` shows precisely where your environment diverged — and `git checkout -- .`
restores the frozen state. Do not commit regenerated files over the frozen ones.

For hand-inspection of any episode (task text + hidden rubric + agent's declared CoS +
judge verdicts with evidence + diff):

```bash
harness/venv/bin/python harness/inspect_episode.py --failures        # worklist of failed/degraded episodes
harness/venv/bin/python harness/inspect_episode.py t20 --cond B --rep rep1
```

## 4. Re-run the full experiment from scratch

> **WARNING — never write into `runs/debug` or `runs/rep1-3`.** Those are the frozen
> dataset. A re-run must use a **new run name** (`--run myrep1`, etc.). The harness will
> happily create any run name you give it; the frozen names are protected only by your
> discipline. The same applies to the judge and scorer stages: point them at your new run
> names only.

Requirements: the Claude Code CLI (`claude`) authenticated, the fixture restored (step 1),
and a real budget. Subject-model spend per rep, from the original run
(`results/costs.md`): ~25M input tokens and ~0.3M output tokens for 72 episodes, plus
~140 Codex judge calls per rep. The spec's pre-run estimate was "low-hundreds of dollars
total and several hours of wall-clock per rep" (`spec/00-overview.md`); no measured dollar
figure was recorded — token counts are the durable record. Wall-clock from
`results/run_full.log`: rep1 (harness + scoring + judging) completed in ~2h15m; the full
three-rep run started 21:03 on 2026-07-05 and finished the morning of 2026-07-06, after
two infrastructure interruptions recovered via `--resume` (see `spec/decisions-log.md`).

Single-rep flow (what `run_full.sh` does per rep):

```bash
cd harness
python3 run_episodes.py --run myrep1            # 24 tasks x 3 conditions = 72 episodes
python3 run_episodes.py --run myrep1 --resume   # after any interruption: skips complete episodes
python3 score_tier1.py myrep1                   # tier-1 mechanical scores
python3 judge.py --run myrep1 --resume          # tier-2 cross-family judge (see section 5)
python3 results.py --runs myrep1 --date <yymmdd>
```

`run_episodes.py` notes:

- The subject model is the `MODEL` constant at the top of `run_episodes.py`
  (`claude-sonnet-4-6`); episode caps are `MAX_TURNS = 50` (counted client-side from
  stream events) and `TIMEOUT_S = 900` per agent call. A cap hit is recorded data, never
  retried.
- Each episode runs in a fresh git worktree of `fixture/` under
  `~/.cache/speech-acts-worktrees/` — deliberately **outside** the repo tree, so the
  subject agent cannot traverse up into `tasks/`, `rubrics/`, `spec/`, or `harness/`
  (invariant 1). An isolation check enforces this on every worktree.
- Condition B is two-phase: a negotiation call must return a valid typed JSON block (one
  schema retry allowed); only `speech_act: "promise"` proceeds to the execution call on a
  reset workspace. Non-promise, schema failure, or cap ends the episode — that is data.
- `--resume` reuses the run's `run.json` and **fails fast (exit 2)** if the fixture HEAD,
  task set, or model changed since the run started. Infrastructure failures (rate limits,
  auth) void the episode (`error.json`, no manifest) and abort after 3 consecutive errors
  (exit 3) — fix the cause, then `--resume`.

**`run_full.sh`** chains harness → tier1 → judge → merge for rep1–rep3 with backoff and
resume. Before using it: its `REPS=(rep1 rep2 rep3)` array targets the frozen run
names — change it to your new names.

## 5. Running the judge

The tier-2 judge is Codex, invoked headless per verdict by `harness/judge.py`
(`call_codex`), pinned to the original configuration:

```
codex exec --skip-git-repo-check --json --ignore-user-config \
  -c model="gpt-5.5" -c model_reasoning_effort="high" -c service_tier="fast" \
  --output-last-message <tmpfile> -
```

You don't run that by hand — `python3 judge.py --run <run> --resume` does — but two
operational rules matter:

- **`--ignore-user-config` is load-bearing.** A stale/expired MCP-plugin token in
  `~/.codex/config.toml` makes `codex exec` exit 1 at startup (this happened mid-rep3 and
  masked a separate usage limit underneath). Bypassing the user config and re-pinning the
  model via `-c` keeps the judge identical while dodging broken plugin state. Auth still
  comes from `CODEX_HOME`. `judge.py` resolves the `codex` binary from your `PATH`
  (`CODEX_BIN`, falling back to `/opt/homebrew/bin/codex`, the original machine's path).
- **An empty final message is an InfraError, never a verdict.** A usage-limited or
  interrupted Codex turn can exit 0 with no agent message; `call_codex` treats
  empty-final-message, non-zero exit, and timeout as infrastructure failures. No
  checkpoint is written, so `--resume` re-runs exactly that call. After 3 consecutive
  infra failures the judge run aborts (exit 3). This is distinct from a `judge_error`,
  which is a *recorded outcome*: the model answered but its verdict failed validation
  twice — that is data, listed in the results, never retried.

Every verdict is schema-validated and **span-verified**: the cited evidence must appear
verbatim (whitespace-normalized) in the rendered transcript, and a Job-1 `true` span must
precede the first file-modification event. Verdicts checkpoint one file at a time to
`runs/<run>/judge/`, and `verdicts.json` / `report.md` regenerate deterministically from
the checkpoints. `python3 judge.py --spotcheck <run>` writes a 10% stratified spot-check
file for human QA.

## 6. Operational gotchas

- **Transcript token-counting trap.** The `claude` CLI's stream-json splits one assistant
  message across several JSONL lines and repeats the same tiny per-message
  `usage.output_tokens` on each. Summing them reconciles to *nothing*. The authoritative
  totals are the `result` event / the manifest's per-phase `tokens_in` / `tokens_out`.
  For per-span cost apportionment, `results.py` distributes the authoritative total by
  character offset over the rendered transcript — reuse that, don't re-derive.
- **Resume-first idempotency.** Both the harness and the judge are `--resume`-first: an
  episode is complete iff `manifest.json` exists and parses (crashes write `error.json`
  instead); a verdict is complete iff its checkpoint validates. Interrupting and resuming
  is the designed recovery path. New scorers should follow suit: byte-identical output on
  re-run is the acceptance test the originals were held to.
- **Judge span verification.** Any judged instrument you build should keep the verbatim
  span-verification layer (`judge.verify_span` over `judge.render_transcript` events).
  It caught real fabricated citations during development, and one recorded `judge_error`
  in rep2 is it working in production. Match against rendered event text, never raw
  escaped JSON; the injected prompt and `thinking` blocks are excluded from the corpus.
- **Killing a run by hand leaves an orphaned `claude -p` child.** The driver's signal
  handlers reap the active process group, but if the Python driver itself dies hard, also
  `pkill -f "claude -p"` before resuming (logged in `spec/decisions-log.md`, Slice 2).
- **Fixture drift fails fast.** If `--resume` reports a fixture/task/model mismatch (exit
  2), do not force it: restore the fixture to `e02cf35` (or accept that your changed
  inputs mean a *new* run, with a new name and your own pre-registration — see
  `docs/EXTENDING.md`).
