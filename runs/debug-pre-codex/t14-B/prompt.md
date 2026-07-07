You are working in this repository. Here is the request:

<request>
The README could be better. Can you improve it?
</request>

You promised the following in a prior negotiation step:

```json
{
  "speech_act": "promise",
  "conditions_of_satisfaction": [
    "All six subcommands (add, report, list, export, stats, budget) are documented with examples in the README",
    "The global --store flag is documented",
    "The budget command's required --month flag is shown in the example",
    "The stats command output format is described or illustrated",
    "No existing accurate content is removed or degraded"
  ],
  "scope_exclusions": [
    "Will not change the prose tone/voice \u2014 the conversational style is intentional and good",
    "Will not add a full flag reference table for every argument",
    "Will not restructure the document into a different format (e.g. man page style)"
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
