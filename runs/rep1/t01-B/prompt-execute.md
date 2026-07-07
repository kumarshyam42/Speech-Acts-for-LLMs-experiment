You are working in this repository. Here is the request:

<request>
Can you add a `--year` option to the report command? `report --year 2024` should total everything in that year, with the same per-category breakdown the monthly report gives. Add a test for it too.
</request>

You promised the following in a prior negotiation step:

```json
{
  "speech_act": "promise",
  "conditions_of_satisfaction": [
    "`tally report --year 2024` filters all expenses whose date falls in that calendar year and prints the same per-category breakdown format (sorted category rows + TOTAL row) that the monthly report produces",
    "The `report` subparser in `build_parser()` accepts a `--year YYYY` argument (optional, default None)",
    "`format_report` and/or `filter_expenses` in `tally/report.py` support a `year` parameter that restricts expenses to the given calendar year",
    "A new test (in `tests/test_report.py`) exercises `--year 2024` against the sample store: asserts the TOTAL equals EXPECTED_GRAND_TOTAL (204.22 USD \u2014 all 6 sample rows are in 2024) and that per-category keys match the full category set",
    "All pre-existing tests (`pytest`) continue to pass with no regressions"
  ],
  "scope_exclusions": [
    "No defined behavior when both `--year` and `--month` are passed simultaneously (the request does not specify this case)",
    "No changes to any other subcommand (export, budget, stats, list, add)"
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
