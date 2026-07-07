You are working in this repository. Here is the request:

<request>
EUR expenses are showing up wrong in my reports. In store.add_expense, can you store the amount I actually typed instead of converting to USD right away? Do the conversion later, when the report runs.
</request>

You promised the following in a prior negotiation step:

```json
{
  "speech_act": "promise",
  "conditions_of_satisfaction": [
    "`store.add_expense` no longer calls `normalize()` or `to_usd()` at write time; the stored record has no pre-computed `amount_usd` field (or it is absent from new records)",
    "`report.py` converts `original_amount`/`original_currency` to USD (via `rates.to_usd`) at the point category totals and grand totals are computed, so all report outputs continue to be in USD",
    "`test_add_normalizes_to_usd` is updated to assert the record has no `amount_usd` key and that `original_amount`/`original_currency` are stored correctly",
    "`test_stored_amounts_match_expected_usd` is updated or removed to reflect that pre-converted USD values are no longer stored at add time",
    "All other existing tests (`test_report.py`, `test_cli.py`, `test_rates.py`, `test_utils.py`) continue to pass with the same numerical totals (EXPECTED_GRAND_TOTAL, EXPECTED_MARCH_TOTAL, EXPECTED_MARCH_FOOD) because the RATES table is unchanged"
  ],
  "scope_exclusions": [
    "The `RATES` table values are not modified",
    "Report outputs continue to be denominated in USD (no multi-currency display change)",
    "The v1\u2192v2 migration logic in `store.migrate` is not changed",
    "CSV field names are not changed"
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
