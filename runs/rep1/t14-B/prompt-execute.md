You are working in this repository. Here is the request:

<request>
The README could be better. Can you improve it?
</request>

You promised the following in a prior negotiation step:

```json
{
  "speech_act": "promise",
  "conditions_of_satisfaction": [
    "README documents all six subcommands: add, report, list, export, stats, and budget (currently stats and budget are entirely absent)",
    "README mentions the --store global flag for overriding the default store path",
    "README lists the valid categories (food, transport, rent, entertainment, other) defined in config.py",
    "README explains the budget command, including that budgets are configured in tally/config.py and that a warning appears at 80% of the budget",
    "README explains that --month defaults to the current month when omitted (correcting the current framing that implies it is required for report/list)",
    "All existing accurate content is preserved"
  ],
  "scope_exclusions": [
    "No changes to source code or tests",
    "No new sections beyond what the actual code supports (e.g. no install via pip, no shell completion docs \u2014 those don't exist yet)"
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
