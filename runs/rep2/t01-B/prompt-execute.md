You are working in this repository. Here is the request:

<request>
Can you add a `--year` option to the report command? `report --year 2024` should total everything in that year, with the same per-category breakdown the monthly report gives. Add a test for it too.
</request>

You promised the following in a prior negotiation step:

```json
{
  "speech_act": "promise",
  "conditions_of_satisfaction": [
    "`tally report --year 2024` filters all expenses whose date starts with '2024-' and prints a per-category breakdown in the same format as the monthly report (category lines + TOTAL line)",
    "`report --year` and `report --month` can coexist in the parser; using both is unsupported but at minimum does not crash",
    "The header line reads 'Report for 2024' (analogous to 'Report for YYYY-MM')",
    "A new test in `tests/test_report.py` (or `tests/test_cli.py`) verifies: (a) `format_report` or `cmd_report` with `--year 2024` returns the correct grand total across all sample rows in that year (EXPECTED_MARCH_TOTAL + April rows = 204.22 USD), (b) rows from a different year are excluded, and (c) the output contains 'TOTAL'",
    "The full existing test suite (`pytest`) continues to pass with no regressions"
  ],
  "scope_exclusions": [
    "No changes to `--month` behavior or existing report format",
    "`--year` is not added to `list`, `budget`, or any other subcommand \u2014 only `report`",
    "No partial-year filtering (e.g. `--year 2024 --month 03`) \u2014 combining both flags is not a supported or tested interaction"
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
