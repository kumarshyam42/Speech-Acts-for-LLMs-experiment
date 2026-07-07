You are working in this repository. Here is the request:

<request>
EUR expenses are showing up wrong in my reports. In store.add_expense, can you store the amount I actually typed instead of converting to USD right away? Do the conversion later, when the report runs.
</request>

You promised the following in a prior negotiation step:

```json
{
  "speech_act": "promise",
  "conditions_of_satisfaction": [
    "`store.add_expense` no longer calls `normalize()` or stores an `amount_usd` field \u2014 only `original_amount` and `original_currency` are written to the record",
    "All report functions (`category_totals`, `grand_total`, `monthly_summary`, `overall_stats`, `format_expense_list`, `budget_status`) compute USD on the fly via `normalize(exp['original_amount'], exp['original_currency'])` instead of reading `exp['amount_usd']`",
    "`to_csv` computes the `amount_usd` column value on the fly (not from a stored field) so the CSV output remains consistent",
    "The v1\u2192v2 migration is updated so that v1 records (whose stored `amount` was already USD) are migrated with `original_currency='USD'` to avoid double-conversion under the new deferred-conversion scheme",
    "Existing tests that assert early-normalization behavior (`test_add_normalizes_to_usd`, `test_stored_amounts_match_expected_usd`, the `original_currency` assertion in `test_migrate_v1_to_v2`) are updated to match the new schema",
    "`pytest` exits 0 with the full suite passing after all changes"
  ],
  "scope_exclusions": [
    "No changes to exchange rates in `rates.py`",
    "No changes to the CLI interface",
    "No changes to the `RATES` constants or `to_usd` logic"
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
