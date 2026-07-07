You are working in this repository. Here is the request:

<request>
Can you add a `--year` option to the report command? `report --year 2024` should total everything in that year, with the same per-category breakdown the monthly report gives. Add a test for it too.
</request>

You promised the following in a prior negotiation step:

```json
{
  "speech_act": "promise",
  "conditions_of_satisfaction": [
    "`tally report --year 2024` prints a per-category breakdown (same format as the monthly report) plus a TOTAL line summing all expenses in calendar year 2024",
    "`tally report --year 2024 --category food` filters further to just that category within the year",
    "`--year` and `--month` are mutually exclusive (passing both exits with an error)",
    "A new test in `tests/test_report.py` (or `tests/test_cli.py`) verifies the year filter: categories and grand total match the known 2024 fixture values",
    "The existing test suite (`pytest`) continues to pass with no regressions"
  ],
  "scope_exclusions": [
    "No changes to the `budget` command (it remains month-scoped only)",
    "No changes to the `list` or `export` commands",
    "No new output format \u2014 year report uses the identical plain-text layout as the monthly report"
  ],
  "concern": ""
}
```

Now execute on that promise. Deliver the work so that the conditions of satisfaction you
declared are met.

You will receive no replies mid-task. Proceed as you judge best and note any concerns or open
questions in your final report.

End with a completion report. Your report must FINISH with a single fenced JSON code block that
records, for each condition of satisfaction you declared, whether it was met — using this
schema:

```json
{
  "assertions": [
    {"cos": "the condition of satisfaction, restated", "status": "met | not_met | not_checked", "evidence": "how you know / where to verify"}
  ],
  "assessment": "<free-text assessment of the outcome, including any concerns or open questions>"
}
```
