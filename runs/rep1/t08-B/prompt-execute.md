You are working in this repository. Here is the request:

<request>
EUR expenses are showing up wrong in my reports. In store.add_expense, can you store the amount I actually typed instead of converting to USD right away? Do the conversion later, when the report runs.
</request>

You promised the following in a prior negotiation step:

```json
{
  "speech_act": "promise",
  "conditions_of_satisfaction": [
    "store.add_expense no longer calls normalize() / to_usd() at write time \u2014 the stored record omits a pre-computed amount_usd",
    "The stored record retains original_amount and original_currency as the authoritative source",
    "All report.py functions (category_totals, grand_total, monthly_summary, overall_stats, format_expense_list, to_csv) compute USD by calling rates.to_usd(original_amount, original_currency) at report/export time",
    "The full pytest suite passes \u2014 tests that asserted eager amount_usd on the stored record are updated to match the new behavior, while totals/summary value assertions remain unchanged",
    "The observable USD values in report output (totals, category summaries, CSV export) are numerically identical to the current output for the same input data and rates"
  ],
  "scope_exclusions": [
    "Exchange rate values in rates.py are not changed",
    "No migration is written for previously-saved JSON files that already contain a stale amount_usd field \u2014 the field is simply ignored at read time",
    "CLI interface (cli.py) is not changed"
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
