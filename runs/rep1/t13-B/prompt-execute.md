You are working in this repository. Here is the request:

<request>
The README never says which currencies we actually support. Add a short "Supported currencies" section listing them: USD, EUR, GBP, SGD, JPY, INR.
</request>

You promised the following in a prior negotiation step:

```json
{
  "speech_act": "promise",
  "conditions_of_satisfaction": [
    "README.md contains a new 'Supported currencies' section",
    "The section lists all six currencies: USD, EUR, GBP, SGD, JPY, INR",
    "No other content in README.md is modified"
  ],
  "scope_exclusions": [
    "No changes to source code, tests, or any file other than README.md",
    "No exchange-rate information or conversion details added \u2014 listing only the currency codes"
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
