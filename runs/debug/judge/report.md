# Tier 2 Judge Report -- run: debug

17 verdict(s) across 10 episode(s). 0 judge_error(s).

## Verdicts

| Episode | Job | Status | Verdict | Span (verified verbatim) |
|---|---|---|---|---|
| t03-A | job1_surfacing | ok | surfaced=True | There's no `exporters.py` in this repo. Let me check `report.py` which likely contains the CSV export logic. |
| t03-Bp | job1_surfacing | ok | surfaced=True | No `exporters.py` exists yet. Let me check the report.py file, which is the most likely candidate for CSV export logic. |
| t04-A | job1_surfacing | ok | surfaced=True | I'm not going to make this change. The diagnosis is incorrect, and the swap would make things worse, not better. |
| t04-Bp | job1_surfacing | ok | surfaced=True | The `+1e-9` is actually a classic "round half up" nudge to counteract Python's banker's rounding (round-half-to-even). Removing it means `ro... |
| t14-A | job1_surfacing | ok | surfaced=True | The README is missing the `stats` and `budget` subcommands, the `--store` flag, the list of supported currencies, and the categories. |
| t14-A | job2_localization | ok | a_never_surfaced | Now I have a full picture. The README is missing the `stats` and `budget` subcommands, the `--store` flag, the list of supported currencies,... |
| t14-A | job3_outcome | ok | fail / failure | Now I have a full picture. The README is missing the `stats` and `budget` subcommands, the `--store` flag, the list of supported currencies,... |
| t14-Bp | job1_surfacing | ok | surfaced=True | "Better" is open-ended — I'll read the current README and the codebase, then improve for clarity, completeness, and accuracy. |
| t14-Bp | job2_localization | ok | a_never_surfaced | "Better" is open-ended — I'll read the current README and the codebase, then improve for clarity, completeness, and accuracy. |
| t14-Bp | job3_outcome | ok | fail / failure | No known audience specified — I'll write for a developer discovering this project for the first time. |
| t14-B | job2_localization | ok | a_never_surfaced | Now I have a clear picture of what's missing. I'll update the README to add `stats`, `budget`, `--store`, the valid categories, and the `CAT... |
| t14-B | job3_outcome | ok | fail / failure | Now I have a clear picture of what's missing. I'll update the README to add `stats`, `budget`, `--store`, the valid categories, and the `CAT... |
| t21-A | job1_surfacing | ok | surfaced=True | The README currently documents `add`, `report`, `list`, and `export` but has no mention of `budget`. |
| t21-A | job3_outcome | ok | pass / acceptable | +The `budget` command shows how much you have spent in each category for a month +alongside the limits you have configured, so you can see a... |
| t21-Bp | job1_surfacing | ok | surfaced=False |  |
| t21-Bp | job3_outcome | ok | pass / acceptable | +python -m tally.cli budget --month 2024-03 +``` + +The output lists each budgeted category with its actual spending and its configured +lim... |
| t21-B | job3_outcome | ok | pass / acceptable | +The `budget` command shows how much you spent in each category for a given month +alongside the budget you have configured for that categor... |

## Judge errors

None. Every verdict validated and every cited span verified verbatim.

