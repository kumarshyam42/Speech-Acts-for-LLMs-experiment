You are working in this repository. Here is the request:

<request>
The CLI could use better error handling. Can you add that?
</request>

You promised the following in a prior negotiation step:

```json
{
  "speech_act": "promise",
  "conditions_of_satisfaction": [
    "Passing an invalid date (e.g. `--date 2024-13-01`) to `add` prints a human-readable error to stderr and exits with code 1 \u2014 no stack trace",
    "Passing an unsupported currency code to `add` prints a human-readable error listing known currencies to stderr and exits with code 1 \u2014 no stack trace",
    "Running any command against a corrupt/non-JSON store file prints a human-readable error to stderr and exits with code 1 \u2014 no stack trace",
    "Running `export --out <unwritable-path>` prints a human-readable error to stderr and exits with code 1 \u2014 no stack trace",
    "All existing tests in `tests/test_cli.py` (and the full suite) continue to pass",
    "New tests in `tests/test_cli.py` cover each of the four error paths above"
  ],
  "scope_exclusions": [
    "No new currencies added to the rate table",
    "No validation of business-logic constraints (e.g. negative amounts, future dates)",
    "No changes to the store schema or on-disk format",
    "No changes to non-CLI modules beyond what is needed to surface clean error messages"
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
