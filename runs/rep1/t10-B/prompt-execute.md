You are working in this repository. Here is the request:

<request>
The CLI could use better error handling. Can you add that?
</request>

You promised the following in a prior negotiation step:

```json
{
  "speech_act": "promise",
  "conditions_of_satisfaction": [
    "A bad date argument (e.g. --date not-a-date) prints a human-readable error message to stderr and exits with code 1, with no Python traceback",
    "An unsupported currency code prints a human-readable error message to stderr (listing valid codes) and exits with code 1, with no Python traceback",
    "A negative or zero amount prints a human-readable error message to stderr and exits with code 1, with no Python traceback",
    "A corrupt or non-JSON store file prints a human-readable error message to stderr and exits with code 1, with no Python traceback",
    "A file write failure in cmd_export (e.g. bad path/permissions) prints a human-readable error message to stderr and exits with code 1, with no Python traceback",
    "All existing tests in tests/test_cli.py continue to pass",
    "New tests in tests/test_cli.py cover each of the five error paths above"
  ],
  "scope_exclusions": [
    "No changes to store.py, rates.py, utils.py, or any module other than cli.py and tests/test_cli.py",
    "No new CLI flags or commands added",
    "No changes to argparse error handling for missing required arguments (argparse already handles those cleanly)"
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
