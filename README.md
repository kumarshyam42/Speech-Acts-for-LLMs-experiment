# Speech Acts Experiment

A completed, frozen pilot experiment testing whether a speech-act coordination protocol
changes how AI agents handle delegation — plus everything needed to reproduce the analysis
or re-run the whole experiment on your own tasks, models, and hypotheses.

## The experiment in one paragraph

An AI agent (`claude-sonnet-4-6`, via the headless `claude -p` CLI) ran 24 tasks against a
small synthetic Python codebase under three delegation contracts: **A** (plain delegation:
do the task, report), **B′** (A plus one sentence of generic pre-execution deliberation —
the ablation), and **B** (a two-phase protocol: the agent first returns a typed speech act —
`promise` / `counter_offer` / `decline` / `commit_to_commit` — with explicit conditions of
satisfaction (CoS), and **only a `promise` proceeds** to execution). The 24 tasks fall into
4 hidden classes (well-formed / underspecified / infeasible-as-stated / hidden-constraint);
agents never see the classes or rubrics. Three repetitions of all 72 task×condition cells
produced **216 scored episodes**, scored mechanically (tier 1) and by a cross-family judge
(Codex / `gpt-5.5`) with mandatory verbatim-span citations (tier 2). Pre-registered
hypotheses, per-class-only reporting, no p-values — this is a pilot. Results:
`results/260705-results.md`.

## What's in the repo

```
Experiment Design.md              # the pre-registered design (v3): hypotheses, conditions, interpretation table
Experiment Explained (Plain Language).md
spec/                             # implementation contract: 00-overview (locked decisions D1–D17) … 05-full-run,
                                  #   rubric-guidance.md, preregistration-manifest.txt, decisions-log.md
fixture/                          # the synthetic `tally` CLI the agents worked on (own git repo, baseline e02cf35)
bundles/fixture.bundle            # git bundle to restore fixture/.git (see docs/REPRODUCING.md)
tasks/                            # t01..t24.md — the agent-visible task text (SHA-256 pre-registered)
rubrics/                          # r01..r24.md + index.md — the HIDDEN class map & rubrics (pre-registered)
harness/                          # run_episodes.py, score_tier1.py, judge.py, results.py, inspect_episode.py,
                                  #   run_full.sh, prompts/ (the three contracts), judge-prompts/ (pre-registered)
runs/                             # debug/, rep1/, rep2/, rep3/ — the FROZEN dataset (full transcripts, diffs,
                                  #   negotiations, manifests, tier1.csv, judge verdicts, merged.csv per rep)
results/                          # the original pre-registered analysis: 260705-results.md, costs.md, casebook
analysis/                         # exploratory follow-up hypotheses (h1–h9), one folder each — see analysis/README.md
docs/                             # REPRODUCING.md and EXTENDING.md (start here)
scripts/                          # setup.sh (harness venv), restore_fixture.sh (fixture git restore)
CLAUDE.md                         # the dataset & reuse map — the deepest single reference for the data model
```

## Three things you can do with this

1. **Reproduce the analysis** over the frozen dataset — re-run the tier-1 scorer, the merge,
   and the results assembly and verify byte-identical output against the checked-in files.
2. **Re-run the experiment** end to end — same tasks, prompts, and pipeline, your own API
   spend — into a **new** run name (never overwriting `runs/rep1-3`).
3. **Test new hypotheses** — either new mechanical metrics or new judged questions over the
   existing 216 episodes, or a fresh pre-registered run with your own tasks, models, and
   rubrics.

**Quickstart:** setup, integrity checks, and the full reproduction walkthrough are in
[`docs/REPRODUCING.md`](docs/REPRODUCING.md). Adapting the harness to your own tasks,
models, or hypotheses is in [`docs/EXTENDING.md`](docs/EXTENDING.md).

## Integrity model

- **Pre-registration.** `spec/preregistration-manifest.txt` records SHA-256 hashes of all
  24 task files, 25 rubric files, and the 3 judge-prompt templates, frozen before any scored
  run. All 52 hashes still verify. Any edit to those files breaks the manifest by design.
- **Frozen runs.** Everything under `runs/` and `results/` is the dataset and the original
  analysis. Nothing there is ever re-run, re-judged, or edited; new work writes new files
  under `analysis/` or a new run name.
- **Fixture baseline.** The agents' workspace was a git worktree of `fixture/` at commit
  `e02cf35` (test suite green). `scripts/restore_fixture.sh` restores and verifies it.
- **Decisions log.** Every plan-vs-built divergence and infrastructure fix is a logged row
  in `spec/decisions-log.md`. "Weird results are results" — no episode was ever re-run
  because its result looked wrong.

## Requirements

| Requirement | Used for |
|---|---|
| Python 3.9+ | all harness/analysis scripts (stdlib only); `scripts/setup.sh` creates `harness/venv` with pytest, which the harness uses to run the fixture's test suite |
| git | fixture worktrees, restoring `fixture/.git` from the bundle |
| Claude Code CLI (`claude`) | running subject episodes (`claude -p`) — only needed to **re-run** the experiment, not to reproduce the analysis. Original run: CLI 2.1.193 |
| Codex CLI (`codex`) | the cross-family tier-2 judge (`codex exec`) — only needed to judge new episodes or ask new judged questions. Original run: codex 0.142.5, model `gpt-5.5` |

## License

MIT — see [`LICENSE`](LICENSE). The dataset (episode transcripts under `runs/`) is included
under the same terms.

## Provenance & citation

The experiment was designed, run, and analyzed 2026-07-04 → 2026-07-06 by **Shyam Kumar**,
with Claude (Anthropic) as orchestrator/implementer and Codex (OpenAI) as the cross-family
judge and code reviewer. Subject model: `claude-sonnet-4-6`. The full run executed overnight
2026-07-05/06 (`results/run_full.log`). The paper this corpus was built to validate,
*Commitment Without Compliance*, lives outside this repo. If you use the dataset or harness,
cite this repository and the run date.
