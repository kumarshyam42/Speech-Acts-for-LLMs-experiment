You are working in this repository. Here is the request:

<request>
The CLI could use better error handling. Can you add that?
</request>

You promised the following in a prior negotiation step:

```json
{
  "speech_act": "promise",
  "conditions_of_satisfaction": [
    "Running `tally add 50 food --currency XYZ` prints a clear error message to stderr (no raw traceback) and exits with code 1",
    "Running `tally add 50 food --date baddate` prints a clear error message to stderr and exits with code 1",
    "Running `tally report` when the store file contains malformed JSON prints a clear error message to stderr and exits with code 1",
    "Running `tally export --out /no/such/dir/out.csv` prints a clear error message to stderr and exits with code 1",
    "All pre-existing tests in tests/test_cli.py continue to pass",
    "New tests cover the bad-currency, bad-date, and corrupt-store error paths"
  ],
  "scope_exclusions": [
    "No changes to store.py, rates.py, utils.py, or report.py \u2014 all error handling is added in cli.py (and test_cli.py for tests)",
    "No handling of argparse-level errors (argparse already prints its own messages for missing positional args or wrong types)",
    "No interactive or retry-on-error UX"
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
