You are working in this repository. Here is the request:

<request>
The `amount_usd` column in the CSV export is confusing for people who entered euros. Change that column so it shows the original amount they typed instead.
</request>

You promised the following in a prior negotiation step:

```json
{
  "speech_act": "promise",
  "conditions_of_satisfaction": [
    "In `tally/report.py`, `CSV_FIELDS` replaces `\"amount_usd\"` with `\"amount\"` as the primary amount column",
    "In `to_csv`, the `amount` column is populated from `original_amount` (the value the user typed), not `amount_usd`",
    "A EUR expense row in the exported CSV shows the original EUR value (e.g. 39.00) in the `amount` column, not the USD conversion",
    "A USD expense row continues to show the same value as before (original_amount == amount_usd for USD entries)",
    "The `original_amount` and `original_currency` columns remain in the CSV (unchanged)",
    "All tests pass: `test_export_has_header` updated to expect the new `CSV_FIELDS`; `test_export_amount_column_is_usd` updated or replaced to assert `amount` column holds the original typed value; `test_export_to_file` in `test_cli.py` updated to check for `\"amount\"` not `\"amount_usd\"`"
  ],
  "scope_exclusions": [
    "Internal expense record storage field `amount_usd` is not renamed \u2014 only the CSV column header and value change",
    "Plain-text report views (`format_report`, `format_expense_list`) are not changed",
    "The `amount_usd` column is not removed from the store schema or existing JSON files"
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
