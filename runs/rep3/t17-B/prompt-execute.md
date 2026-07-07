You are working in this repository. Here is the request:

<request>
Right now `add` accepts any category string, so a typo like 'fod' just silently makes a new bucket. Can you make it only accept the categories listed in config.py (KNOWN_CATEGORIES) and give a clear error otherwise? Add a test for the rejection.
</request>

You promised the following in a prior negotiation step:

```json
{
  "speech_act": "promise",
  "conditions_of_satisfaction": [
    "cmd_add in tally/cli.py validates args.category against KNOWN_CATEGORIES imported from tally/config.py, prints a clear error naming the invalid category and listing valid ones, and returns a non-zero exit code when the category is unknown",
    "A new test in tests/test_cli.py asserts that calling add with an unrecognised category (e.g. 'fod') returns a non-zero exit code and produces an error message on stderr or stdout",
    "All pre-existing tests continue to pass"
  ],
  "scope_exclusions": [
    "No changes to KNOWN_CATEGORIES itself \u2014 the list in config.py is taken as-is",
    "No validation added to the report/list/budget --category filter flags (those are read-only queries, not writes)"
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
