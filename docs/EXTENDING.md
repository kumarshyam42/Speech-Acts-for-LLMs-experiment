# Extending the Experiment

How to adapt this repo to your own tasks, models, and hypotheses. Read
`docs/REPRODUCING.md` first — this guide assumes you know the pipeline
(harness → tier-1 scorer → tier-2 judge → merge) and the frozen/pre-registered
boundaries.

## 1. Authoring new tasks

Every task is a **pair**: an agent-visible task file and a hidden rubric.

**Task file** (`tasks/tNN.md`): just the request text, exactly as a requester would write
it — no metadata, no hints. See `tasks/t01.md` for the shape. Two hard rules:

- **The filename must not encode the class** (locked decision D15). Classes are
  interleaved across task numbers; the only class map is `rubrics/index.md`.
- **Agents never see `rubrics/`, class assignments, or judge prompts** (invariant 1).
  In the original run this was enforced structurally: episode worktrees live outside the
  repo tree and contain only the fixture. Keep that property.

**Hidden rubric** (`rubrics/rNN.md`): written *before* any agent sees the task, frozen by
hash. The fields, per `rubrics/r01.md`:

```
class:                1–4
concern:              what the requester actually needs
stated_request_gap:   how the request text diverges from the concern
tripwire:             (class 3/4) the discoverable conflict, or n/a
expected_behavior:    excellent / acceptable / failure — each level naming concrete,
                      observable evidence a judge could quote
cos_reference:        what correct CoS would look like
judge_notes:          what to check, and how to avoid predictable scoring errors
```

**Index entry** (`rubrics/index.md`): one table row —
`| tNN | class | code|prose | one-line intent | tripwire |`. The scorer and judge read
class/kind from this table; it is the analysis key.

**The 4-class taxonomy** (6 tasks each in the original, ~4 code + 2 prose):

1. **Well-formed** — clear, feasible, verifiable. The load-bearing control: does the
   protocol tax clean work (reflexive counter-offers, overhead)?
2. **Underspecified** — "improve readability", "make it faster". Correct behavior:
   surface and propose CoS.
3. **Infeasible-as-stated** — nonexistent file/function, or forbidden by the repo's own
   rules. Correct: decline or counter-offer toward the real target.
4. **Hidden-constraint** — feasible on the surface, but naive execution conflicts with
   something discoverable in the repo (a pinned test, a contradicting requirement).
   Correct: surface the conflict, at negotiation or in the final report.

Read `spec/rubric-guidance.md` before writing any rubric — it encodes the per-class
gradient rules (proposing beats extracting on class 2; the store-clerk gradient on
class 3; "silently editing the tripwire test is the worst outcome in the experiment" on
class 4) and the authoring hygiene (every gradient level must name quotable evidence;
never invent content to fill a template field).

If you build a new fixture repo, note why this one is synthetic (locked decision D2): a
real OSS repo can be memorized from training data, which contaminates class-3/4 tripwires.
Keep the fixture its own git repo with a green test suite at a pinned baseline SHA.

## 2. Different models and runtimes

**Different Claude model, same runtime:** change the `MODEL` constant at the top of
`harness/run_episodes.py` (line ~35, `MODEL = "claude-sonnet-4-6"`). `--resume` will
refuse to mix models within a run (exit 2), so a model change means a new run name.

**Different agent runtime:** exactly one function spawns the subject agent —
`invoke_claude(prompt_text, workspace, transcript_path)` in `run_episodes.py`. Its two
callers, `run_simple_episode` (conditions A/B′) and `run_b_episode` (condition B's
negotiate → gate → execute), contain no CLI specifics beyond that call. To swap runtimes,
replace `invoke_claude` and preserve its return contract (`result_text`, `tokens_in`,
`tokens_out`, `num_turns`, `wall_s`, `cap_hit`, `is_error`, …) plus `check_cli_error`'s
notion of an infrastructure failure.

What assumes the `claude` CLI specifically:

- the argv in `invoke_claude` (`claude -p … --output-format stream-json --verbose
  --dangerously-skip-permissions`) and the stream-json parsing: `assistant` events drive
  the client-side turn cap, the terminal `result` event carries authoritative usage and
  final text;
- **downstream, the transcript format:** `judge.render_transcript` and
  `inspect_episode.py` parse `transcript.jsonl` as claude stream-json (assistant-text /
  tool_use / tool_result blocks). A swapped executor must either emit a compatible
  `transcript.jsonl` or you must adapt the renderer — the judge's span verification and
  the merge's cost-to-surface apportionment both run over those rendered events.

What is model-agnostic and carries over unchanged: worktree lifecycle and isolation
checks, prompt templates (`harness/prompts/`), the condition-B gate logic
(`extract_json_block` / `validate_speech_act` — only a valid `promise` proceeds),
diff/pytest capture, the manifest schema, resume semantics, and the entire tier-1 scorer.

**Swapping the judge:** one function calls the judge — `call_codex(prompt, workdir)` in
`harness/judge.py` (plus the `CODEX_BIN` constant and the `-c model="gpt-5.5"` pins). Keep
its contract: return the final message text, raise `InfraError` on non-zero exit, timeout,
or empty final message. Everything else (scheduling, schema validation, span verification,
checkpointing) is judge-model-agnostic.

**Why cross-family judging matters:** B transcripts self-identify — the typed JSON
negotiation blocks are right there in the transcript, so true blinding is impossible.
This is a named limitation of the design, and the mitigations are: a judge from a
*different model family* than the subject (a same-family judge tends to favor its
sibling's work), mandatory verbatim-span citations for every verdict, and format-agnostic
scoring rules written to err toward the null (free-text pushback in A/B′ earns the same
surfacing credit as a typed act in B — locked decision D9). If you change the subject
model family, change the judge family accordingly. Prefer mechanical (tier-1) metrics
wherever possible: they need no judge and carry no blinding problem.

## 3. New hypotheses over the frozen data

The 216 episodes are a fixed sample; you can compute **new mechanical metrics** or ask
**new judged questions** over the same transcripts without re-running anything. The
conventions (in force, with nine worked examples) are in `analysis/README.md`.

- One folder per hypothesis: `analysis/h<n>-<slug>/`, plus an index row in
  `analysis/README.md`. Each folder is self-contained: `README.md` (claim + motivating
  episodes + planned measurement), scorer scripts, `out/` for generated tables, and — for
  judged instruments — `rubric.md`, `judge-prompts/`, `verdicts/`.
- **Mechanical metric:** write a scorer that reads `manifest.json` + episode artifacts,
  modeled on `harness/score_tier1.py` (stdlib, Py3.9, idempotent — byte-identical on
  re-run). Import the shared helpers from `harness/`: `judge.render_transcript`,
  `judge.verify_span`, `score_tier1.extract_json_block`, `inspect_episode.load_merged`.
- **Judged question:** write a new job prompt modeled on `harness/judge-prompts/*.md` and
  drive it with `judge.py`'s machinery (span verification + checkpointing +
  `--ignore-user-config`). Verdicts go in your hypothesis's `verdicts/` dir — **never**
  overwrite the pre-registered job1/2/3 verdicts under `runs/<rep>/judge/`. A new judged
  question is a new measurement instrument: fix its rubric *before* looking at outcomes,
  and log it in `spec/decisions-log.md`.

**The honesty discipline** (binding in the original, and what makes results credible):

- Decide the analysis — metric definitions, thresholds, kill criteria — before peeking at
  outcomes.
- Report **per-class only**; never a cross-class aggregate (18/24 tasks are pathological
  by design; an aggregate is meaningless).
- Descriptive statistics only at this N (18 per cell, correlated within task) — no
  p-values, no significance claims.
- **Weird results are results.** Nothing gets re-run because it looks wrong; dropped
  hypotheses keep their folders with a post-mortem — the graveyard is what makes the
  survivors credible.
- Everything in `analysis/` is exploratory (hypothesis-generating over the same data that
  generated the ideas). Confirmatory claims need a fresh pre-registered run — see below.

## 4. Pre-registration discipline for a new run

If you run new episodes — new tasks, new models, or a confirmatory pass on a surviving
hypothesis — reproduce the tamper-evidence, not just the pipeline:

1. **Freeze the instrument before any scored episode.** Hash every task file, every
   rubric, every judge-prompt template, and (recommended) the contract prompts:

   ```bash
   shasum -a 256 tasks/*.md rubrics/*.md harness/judge-prompts/*.md harness/prompts/*.md \
     > spec/my-preregistration-manifest.txt
   ```

   Write your manifest to a **new file** — never edit
   `spec/preregistration-manifest.txt`, which certifies the original run.

2. **Pre-register the interpretation.** The original wrote down, before running, what
   every possible outcome would mean (the interpretation table in
   `Experiment Design.md`). Do the same for your hypotheses — including what a null or
   embarrassing result means. "H0 confirmed is publishable" was a design principle here,
   not a slogan.

3. **Log decisions.** Every plan-vs-built divergence and every infrastructure fix gets an
   append-only log entry (see `spec/decisions-log.md` for the format: date, slice, what
   the spec said, what was built, why). Infra fixes may change the invocation but never
   the hashed instrument; an instrument change after the freeze needs a logged entry and
   invalidates the "pre-registered" label for affected measurements.

4. **New run names, always.** Your episodes go to `runs/<your-run-name>/`; the frozen
   `debug`/`rep1-3` are never written to. Pin your fixture baseline SHA in the run
   manifest (the harness does this) and report it with your results.
