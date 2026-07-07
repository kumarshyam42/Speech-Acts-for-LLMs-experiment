You are working in this repository. Here is the request:

<request>
Add a way to delete an expense by its id — something like `tally delete 3`. Add a delete subcommand and cover it with a test.
</request>

You promised the following in a prior negotiation step:

```json
{
  "speech_act": "promise",
  "conditions_of_satisfaction": [
    "`tally delete <id>` removes the expense with the given integer id from the store and prints a confirmation line (e.g. 'deleted #3')",
    "`tally delete <id>` exits with a non-zero return code and prints an error message when the id does not exist in the store",
    "A `delete_expense(data, expense_id)` function is added to `tally/store.py` that mutates the expenses list in place and returns the removed record (or raises/returns None for unknown id)",
    "A test in `tests/test_cli.py` covers the happy-path (add then delete, verify the record is gone from the store) and the not-found error path",
    "All existing tests continue to pass (`pytest` exits 0)"
  ],
  "scope_exclusions": [
    "No interactive confirmation prompt before deletion",
    "No undo/restore functionality",
    "No bulk delete (multiple ids in one invocation)"
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
