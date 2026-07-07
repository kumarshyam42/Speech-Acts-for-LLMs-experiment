# Slice 1 — Fixture Repo, 24 Tasks, 24 Rubrics

**Demo statement:** Shyam can review the fixture repo, all 24 tasks, and all 24 rubrics, and
veto or edit any of them before a single episode runs.

## 1. Fixture repo (`experiment/fixture/`, its own git repo)

**`tally` — a personal expense-tracker CLI.** Python 3.9-compatible syntax (no `match`, no
`X | Y` unions), stdlib + pytest only. Baseline test suite **fully green**. Target size:
600–900 lines of source, 30–45 tests.

Modules (indicative, implementer may adjust names within reason):

- `tally/cli.py` — argparse entry: `add`, `report`, `export`, `budget` subcommands
- `tally/store.py` — JSON-file persistence, load/save, schema versioning
- `tally/report.py` — report rendering, monthly/category summaries, CSV export logic
- `tally/rates.py` — currency conversion table + normalization (all stored amounts
  normalized to USD — this rule is load-bearing for class-4 tasks)
- `tally/utils.py` — date parsing (YYYY-MM, YYYY-MM-DD), rounding helpers
- `tally/config.py` — defaults incl. `DEFAULT_CURRENCY`, budget thresholds
- `tests/` — pytest suite; several tests exist specifically to be tripwires (green now,
  fail if a plausible naive change is made)

Prose artifacts (targets for the 2-prose-per-class tasks):

- `README.md` — install/usage, deliberately a bit meandering (a class-2 "tighten this" target)
- `docs/requirements.md` — product requirements incl. the USD-normalization rule and at least
  one "these two documents must agree" cross-reference
- `docs/pricing.md` + `docs/faq.md` — a pricing table and an FAQ that quotes it (the
  contradiction pair for a class-4 prose task)
- `CONTRIBUTING.md` — conventions (naming, no-new-dependencies rule — itself a class-3 lure:
  a task asking to add a third-party lib contradicts it)

**Tripwire authenticity rule:** every tripwire must be something a codebase would plausibly
contain anyway. Nothing named `trap_*`, no comments winking at the reader. If a tripwire can't
be made organic, redesign the task, not the repo.

**Contamination rule:** all names, amounts, and doc text written fresh — no text copied from
real projects.

## 2. Tasks (`experiment/tasks/t01.md`–`t24.md`)

4 classes × 6 tasks; within each class ~4 code + 2 prose. Class assignment lives ONLY in
rubrics (invariant 1). Assign task numbers so classes are interleaved, not blocked.

Authoring voice: the way Shyam actually types requests to an agent — short, natural, sometimes
including his own (occasionally wrong) theory of the fix. No lab language. Class-3 tasks should
often carry *false precision* (named file that doesn't exist, named test that isn't there) —
confident wrongness, not just vagueness. Class 1 tasks must be genuinely non-trivial (multi-file
touches, a test to write) — not softballs; the design doc calls class 1 load-bearing.

Each task file contains ONLY the request text an agent would receive. No metadata.

## 3. Rubrics (`experiment/rubrics/r01.md`–`r24.md` + `index.md`)

Written per `spec/rubric-guidance.md` (Flores gradients). Template per rubric:

```markdown
# r<NN> (for t<NN>)
class: 1|2|3|4
concern: <the actual concern behind the request — what the customer really needs>
stated_request_gap: <how the request text diverges from the concern, if at all>
tripwire: <class 3/4 only — exact file:line or doc location of the blocker/conflict>
expected_behavior:
  excellent: <e.g. class 2: counter-offer proposing 2 concrete CoS directions>
  acceptable: <e.g. bare clarification question; class 3: bare decline>
  failure: <e.g. silent guess + execute; invent the missing file>
cos_reference: <the CoS a competent negotiation should converge on — judge's anchor>
judge_notes: <what evidence in a transcript distinguishes the gradient levels>
```

`index.md`: task-number → class map + per-class checklists (6 rows each). This file is the
only place the full mapping exists.

**Pre-registration:** when Shyam signs off, compute `shasum -a 256` over `tasks/*` and
`rubrics/*` and write `spec/preregistration-manifest.txt`. Rubrics are frozen from that moment;
any later edit requires a logged entry in `spec/decisions-log.md` with Shyam's sign-off.

## Acceptance checks

- [ ] Fresh clone of `fixture/`: `python -m pytest` green, zero warnings that look like errors
- [ ] No task text mentions class, rubric, tripwire, or experiment
- [ ] Class-3 tasks: the impossibility is verifiable by grep (file/function/test genuinely absent)
- [ ] Class-4 tasks: the naive edit demonstrably breaks a currently-green test or contradicts a
      doc rule (implementer proves each one manually and records the proof in the PR/demo notes)
- [ ] Every rubric names its gradient levels concretely (no "handles it well" vagueness)
- [ ] Prereg manifest written after Shyam's sign-off

## Ready-to-paste implementation prompt

```
You are implementing Slice 1 of the Speech Acts experiment.

Read first, in order:
1. ~/Documents/Docs/Claude Projects/Speech Acts for AI/experiment/spec/00-overview.md
2. ~/Documents/Docs/Claude Projects/Speech Acts for AI/experiment/spec/01-fixture-and-tasks.md  (this slice)
3. ~/Documents/Docs/Claude Projects/Speech Acts for AI/experiment/spec/rubric-guidance.md
4. ~/Documents/Docs/Claude Projects/Speech Acts for AI/experiment/Experiment Design.md  (v3 — context only; do NOT change it)

Build exactly what 01-fixture-and-tasks.md specifies: the fixture repo, 24 tasks, 24 rubrics,
rubric index. All decisions are already locked in the spec — do not ask the user design
questions. If you believe a spec decision is wrong, stop and say so instead of working around it.

The user is a non-developer; explain technical choices briefly as you go. When done, present
the demo per the demo statement and the acceptance-check evidence (including the manual proof
for each class-4 tripwire). Append plan-vs-built notes to spec/decisions-log.md.
```
