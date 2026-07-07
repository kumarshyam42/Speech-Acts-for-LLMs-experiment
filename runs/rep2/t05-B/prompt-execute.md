You are working in this repository. Here is the request:

<request>
We've got Canadian users now. Add support for CAD at a rate of 0.73 (1 CAD = 0.73 USD). Make sure add and report both handle it, and add a test.
</request>

You promised the following in a prior negotiation step:

```json
{
  "speech_act": "promise",
  "conditions_of_satisfaction": [
    "tally/rates.py RATES dict contains 'CAD': 0.73",
    "rates.to_usd(100.0, 'CAD') returns 73.0",
    "tally add --currency CAD accepts a CAD amount and stores it converted to USD (amount_usd = amount * 0.73)",
    "tally report displays the correct USD total for expenses entered in CAD",
    "tests/test_rates.py contains a test that pins the CAD rate (e.g. to_usd(100.0, 'CAD') == 73.0)",
    "the full test suite (pytest) passes with zero failures"
  ],
  "scope_exclusions": [
    "No changes to report formatting or output labels \u2014 reports already emit USD and the existing format is sufficient",
    "No changes to CLI argument handling beyond accepting 'CAD' as a valid --currency value (which already works once the rate is registered)"
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
