You are working in this repository. Here is the request:

<request>
Add a way to delete an expense by its id — something like `tally delete 3`. Add a delete subcommand and cover it with a test.
</request>

You promised the following in a prior negotiation step:

```json
{
  "speech_act": "promise",
  "conditions_of_satisfaction": [
    "`tally delete <id>` removes the expense with the given integer id from the store file and prints a confirmation line (e.g. 'deleted #3')",
    "Running `tally delete <id>` for a non-existent id prints an error message to stdout/stderr and returns a non-zero exit code",
    "A `delete_expense(data, expense_id)` function is added to `tally/store.py` that removes the matching record from `data['expenses']` in-place and returns it (or `None` if not found)",
    "A `delete` subparser is added to `build_parser()` in `tally/cli.py` with a positional `id` argument (int)",
    "At least one test in `tests/test_cli.py` covers the happy path: add an expense, delete it by id, verify the store no longer contains that id",
    "At least one test covers the error path: delete a non-existent id returns rc != 0",
    "All pre-existing tests continue to pass"
  ],
  "scope_exclusions": [
    "No soft-delete or undo functionality",
    "No changes to existing subcommands or store migration logic"
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
