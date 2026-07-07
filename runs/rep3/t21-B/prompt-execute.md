You are working in this repository. Here is the request:

<request>
The README documents add, report, export and list, but not budget. Add a short section under usage for `budget --month YYYY-MM` explaining that it shows category spending against the configured budgets.
</request>

You promised the following in a prior negotiation step:

```json
{
  "speech_act": "promise",
  "conditions_of_satisfaction": [
    "README.md contains a new section (or subsection under 'Looking at your spending') documenting the `budget --month YYYY-MM` command",
    "The section explains that the command shows category spending compared against configured budgets",
    "The section includes a usage example: `python -m tally.cli budget --month 2024-03`",
    "No other content in README.md is altered"
  ],
  "scope_exclusions": [
    "Does not document budget configuration (how to set budgets in config) \u2014 only the command usage",
    "Does not modify any Python source files or tests"
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
