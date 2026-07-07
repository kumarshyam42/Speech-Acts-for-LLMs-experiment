# Slice 2 — Episode Harness

**Demo statement:** a 12-episode debug run (one task per class × 3 conditions) completes
unattended; Shyam can open any episode folder and read the full transcript, the diff, and the
manifest, and see exactly what happened.

## Driver: `harness/run_episodes.py`

Plain Python 3.9-compatible script, stdlib only. CLI:

```
python run_episodes.py --run debug --tasks t03,t07,t14,t21        # debug run
python run_episodes.py --run rep1                                  # full 24×3
python run_episodes.py --run rep1 --resume                         # skip completed episodes
```

Config constants at top of file: MODEL = "claude-sonnet-4-6", MAX_TURNS = 50,
TIMEOUT_S = 900, FIXTURE_PATH, CONDITIONS = ["A", "Bp", "B"].

## Episode lifecycle (all conditions)

1. `git worktree add` a fresh worktree of `fixture/` at its pinned baseline SHA (recorded in
   the run manifest) → episode workspace. The workspace contains ONLY the fixture (invariant 1).
2. Compose the prompt: contract template (`harness/prompts/<condition>.md`) + task text.
3. Invoke `claude -p` headless:
   `claude -p --model claude-sonnet-4-6 --output-format json --max-turns 50 --dangerously-skip-permissions`
   with `cwd` = episode workspace. Capture the JSON result (usage, turns, final text) and the
   session transcript (`--output-format stream-json` teed to `transcript.jsonl`).
4. Post-episode, mechanically record: `git -C <workspace> diff` (saved as `episode.diff`),
   `python -m pytest` exit code in the workspace, wall-clock, tokens, turns.
5. Write `manifest.json`; `git worktree remove` (workspace contents already archived).

Episode folder: `runs/<run>/<taskid>-<cond>/` (reps are separate runs: rep1, rep2, rep3)
containing `prompt.md`, `transcript.jsonl`, `final.txt`, `episode.diff`, `pytest.txt`,
`manifest.json`, and for B: `negotiation.json`, `negotiation-transcript.jsonl`.

## Per-condition contracts (`harness/prompts/`)

All three share verbatim: the task framing ("You are working in this repository. Here is the
request:"), the no-replies policy (D7), and the instruction to end with a final report. Only
the delegation contract differs:

- **A.md** — nothing else. Do the task, report.
- **Bprime.md** — adds exactly: "Before executing, briefly note any ambiguities, feasibility
  concerns, and what success would look like. Then proceed as you judge best." (Design doc
  wording; do not embellish — B′ must stay generic, no typed menu, no gate.)
- **B-negotiate.md** — phase 1. Explains the four acts (promise / counter_offer / decline /
  commit_to_commit) and CoS. Output MUST be a single fenced JSON block matching the design
  doc's Condition B schema. Explore the repo as needed, but make no changes.
- **B-execute.md** — phase 2, only if phase 1 returned `promise`. Includes the phase-1 JSON
  verbatim ("You promised the following…"). Completion report MUST end with a fenced JSON
  block: `{"assertions": [{"cos": "...", "status": "met|not_met|not_checked", "evidence": "..."}],
  "assessment": "<free text>"}` (D8).

## Condition B gate logic

- Parse phase-1 output for the JSON block; validate fields. Invalid → one retry with a terse
  "output did not match the required schema" message appended. Second failure → episode ends,
  recorded `protocol_error: schema_failure` (this is DATA for H0, not a bug to hide).
- `counter_offer` / `decline` / `commit_to_commit` → episode ends (surfacing ends the episode).
- `promise` → `git reset --hard && git clean -fd` the workspace first; if phase 1 made changes,
  record `protocol_error: negotiation_wrote` (also H0 data). Then run phase 2 in the same
  workspace, fresh `claude -p` call carrying the phase-1 JSON in its prompt (D17).

## manifest.json (per episode)

```json
{
  "task": "t07", "condition": "B", "run": "rep1",
  "model": "claude-sonnet-4-6", "cli_version": "<claude --version>",
  "fixture_sha": "<baseline commit>", "prompt_sha256": "...",
  "phases": [{"phase": "negotiate", "tokens_in": 0, "tokens_out": 0, "turns": 0, "wall_s": 0}],
  "speech_act": "promise|counter_offer|decline|commit_to_commit|null",
  "diff_nonempty": true, "pytest_exit": 0,
  "protocol_error": null, "cap_hit": null, "timestamp": "..."
}
```

## Resumability & hygiene

- `--resume`: an episode is complete iff `manifest.json` exists and parses; otherwise its
  folder is deleted and re-run.
- Episodes run sequentially (no parallelism in v1 — simpler, and avoids worktree races).
  If a rep's wall-clock proves painful, parallelize by task in a later pass, never within task.
- The driver never reads `rubrics/` (invariant 1). Scoring is Slices 3–4.

## Acceptance checks

- [ ] Debug run (12 episodes) completes end-to-end unattended, including at least one B
      non-promise termination (pick debug tasks so this is likely: t-class3 is in the set)
- [ ] Every episode folder has all listed artifacts; manifests validate against the shape above
- [ ] B phase-1 explored but wrote nothing (or violation was caught and recorded)
- [ ] Kill the driver mid-run, `--resume` completes without duplicating episodes
- [ ] Codex review to P0/P1-clean (this is the gate for Slices 3+)

## Ready-to-paste implementation prompt

```
You are implementing Slice 2 of the Speech Acts experiment (the episode harness).

Read first, in order:
1. ~/Documents/Docs/Claude Projects/Speech Acts for AI/experiment/spec/00-overview.md
2. ~/Documents/Docs/Claude Projects/Speech Acts for AI/experiment/spec/02-harness.md  (this slice)
3. ~/Documents/Docs/Claude Projects/Speech Acts for AI/experiment/Experiment Design.md  (v3 — context; do NOT change it)

Slice 1 artifacts (fixture/, tasks/) already exist — use them, don't modify them. NEVER read
rubrics/ — that's a hard invariant. All decisions are locked in the spec; don't ask the user
design questions. Verify the exact `claude -p` flags against `claude --help` on this machine
before assuming them (especially stream-json capture); if a flag doesn't exist, achieve the
same artifact another way and log the divergence in spec/decisions-log.md.

The user is a non-developer; explain choices briefly. Finish by running the 12-episode debug
run and presenting the demo + acceptance-check evidence.
```
