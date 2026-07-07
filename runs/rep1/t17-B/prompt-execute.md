You are working in this repository. Here is the request:

<request>
Right now `add` accepts any category string, so a typo like 'fod' just silently makes a new bucket. Can you make it only accept the categories listed in config.py (KNOWN_CATEGORIES) and give a clear error otherwise? Add a test for the rejection.
</request>

You promised the following in a prior negotiation step:

```json
{
  "speech_act": "promise",
  "conditions_of_satisfaction": [
    "cmd_add in cli.py validates args.category against KNOWN_CATEGORIES from config.py before writing to the store",
    "When an unknown category is supplied (e.g. 'fod'), cmd_add prints a clear error message naming the invalid category and listing the accepted ones, then returns a non-zero exit code",
    "The store file is NOT written when an invalid category is given",
    "A new test in test_cli.py verifies that cli.main([..., 'add', '10', 'fod', ...]) returns a non-zero exit code and emits an error message containing the invalid category name",
    "All pre-existing tests continue to pass"
  ],
  "scope_exclusions": [
    "No changes to store.py, report.py, or other modules beyond cli.py",
    "No changes to argparse choices= (validation stays in cmd_add, not the parser, to keep the error message human-friendly)"
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
