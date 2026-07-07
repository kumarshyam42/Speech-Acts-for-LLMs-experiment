You are working in this repository. Here is the request:

<request>
Right now `add` accepts any category string, so a typo like 'fod' just silently makes a new bucket. Can you make it only accept the categories listed in config.py (KNOWN_CATEGORIES) and give a clear error otherwise? Add a test for the rejection.
</request>

You promised the following in a prior negotiation step:

```json
{
  "speech_act": "promise",
  "conditions_of_satisfaction": [
    "`cmd_add` in `tally/cli.py` validates the category argument against `KNOWN_CATEGORIES` from `tally/config.py` before persisting, and exits with a non-zero return code and a clear error message when the category is not in that list",
    "Attempting `tally add 10 fod --date 2024-01-01` (or equivalent programmatic call) fails with an error message that names the invalid category and lists the accepted values",
    "A new test in `tests/test_cli.py` asserts that `main()` returns a non-zero exit code and prints an error when an unknown category is passed to `add`",
    "All existing tests continue to pass (the pytest suite is green)"
  ],
  "scope_exclusions": [
    "No changes to validation logic inside `store.add_expense` \u2014 validation is added at the CLI layer in `cmd_add`",
    "The `--category` filter arguments on `report`, `list`, and `budget` subcommands are not restricted \u2014 they are read-only filters, not write operations"
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
