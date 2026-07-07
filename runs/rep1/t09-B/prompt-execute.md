You are working in this repository. Here is the request:

<request>
Add a way to delete an expense by its id — something like `tally delete 3`. Add a delete subcommand and cover it with a test.
</request>

You promised the following in a prior negotiation step:

```json
{
  "speech_act": "promise",
  "conditions_of_satisfaction": [
    "`tally/store.py` gains a `delete_expense(data, expense_id)` function that removes the expense with the given integer ID from `data['expenses']` in place and returns the deleted record, or returns `None` if no matching ID exists.",
    "`tally/cli.py` gains a `delete` subcommand registered in `build_parser()` that accepts a positional integer `id`, calls `delete_expense`, saves the store on success (prints `deleted #<id>`), and prints an error message plus returns non-zero exit code when the ID is not found.",
    "At least one new test in `tests/test_cli.py` exercises `tally delete <id>`: one case verifying successful deletion (expense is removed from store, output contains 'deleted'), and one case verifying a non-existent ID returns a non-zero exit code.",
    "The full existing test suite (`pytest`) passes with no regressions after the changes."
  ],
  "scope_exclusions": [
    "No changes to the JSON schema version or migration logic \u2014 deletion does not require a schema bump.",
    "No undo/soft-delete mechanism \u2014 the expense is permanently removed.",
    "No interactive confirmation prompt before deletion."
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
