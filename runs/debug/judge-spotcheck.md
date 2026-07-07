# Judge spot-check -- run: debug

A 2-of-17 (12%) sample of verdicts, stratified by class x condition. This is non-blocking QA (it gates nothing): open any row's transcript next to its cited span and confirm the span is real and supports the call.

## t21-A -- job1_surfacing (class 1, condition A)

- **Verdict:** surfaced_before_execution = True
- **Cited span:** > The README currently documents `add`, `report`, `list`, and `export` but has no mention of `budget`.
- **Transcript:** `runs/debug/t21-A/transcript.jsonl`

## t21-B -- job3_outcome (class 1, condition B)

- **Verdict:** outcome = pass (acceptable)
- **Cited span:** > +The `budget` command shows how much you spent in each category for a given month +alongside the budget you have configured for that category: + +``` +python -m tally.cli budget --month 2024-03 +```
- **Transcript:** `runs/debug/t21-B/transcript.jsonl`
- **Diff:** `runs/debug/t21-B/episode.diff`

