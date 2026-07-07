You are working in this repository. Here is the request:

<request>
We've got Canadian users now. Add support for CAD at a rate of 0.73 (1 CAD = 0.73 USD). Make sure add and report both handle it, and add a test.
</request>

You promised the following in a prior negotiation step:

```json
{
  "speech_act": "promise",
  "conditions_of_satisfaction": [
    "`tally/rates.py` contains `\"CAD\": 0.73` in the `RATES` dict",
    "`rates.to_usd(100.0, \"CAD\")` returns `73.0`",
    "`rates.supported_currencies()` includes `\"CAD\"` in sorted position",
    "`tally add 50 food --currency CAD` records `amount_usd` of `36.5` in the store",
    "`tally report` sums CAD-sourced expenses in USD (no code change needed beyond the rates entry, since report already uses `amount_usd`)",
    "A new test in `tests/test_rates.py` asserts `rates.to_usd(100.0, \"CAD\") == 73.0`",
    "The full existing test suite passes (`pytest` exits 0)"
  ],
  "scope_exclusions": [
    "No changes to report display format \u2014 reports already emit USD and work with any supported currency",
    "No live exchange-rate fetching \u2014 rate is hardcoded as 0.73 per the request",
    "No changes to docs unless they explicitly list supported currencies"
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
