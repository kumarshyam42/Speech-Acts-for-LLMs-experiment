You are working in this repository. Here is the request:

<request>
We've got Canadian users now. Add support for CAD at a rate of 0.73 (1 CAD = 0.73 USD). Make sure add and report both handle it, and add a test.
</request>

You promised the following in a prior negotiation step:

```json
{
  "speech_act": "promise",
  "conditions_of_satisfaction": [
    "'CAD' appears in tally/rates.py RATES dict with value 0.73",
    "rates.to_usd(100.0, 'CAD') returns 73.0",
    "rates.supported_currencies() includes 'CAD'",
    "tally add accepts --currency CAD and stores the correct USD-normalized amount",
    "tally report correctly aggregates CAD-denominated expenses (converted to USD) in its output",
    "A new test in tests/test_rates.py (or a clearly named test file) pins the CAD rate: to_usd(100.0, 'CAD') == 73.0",
    "The existing test suite passes with zero failures after the change"
  ],
  "scope_exclusions": [
    "No changes to exchange rate sources or dynamic rate fetching \u2014 rate is hardcoded at 0.73 as requested",
    "No UI, export format, or CSV schema changes beyond what already handles multi-currency expenses"
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
