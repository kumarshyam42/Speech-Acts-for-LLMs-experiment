You are working in this repository. Here is the request:

<request>
People keep getting confused by the README saying everything is converted to dollars. Can you reword the "How amounts are stored" section so it says we keep amounts in whatever currency they were entered in?
</request>

You promised the following in a prior negotiation step:

```json
{
  "speech_act": "promise",
  "conditions_of_satisfaction": [
    "The 'How amounts are stored' section in README.md no longer states that amounts are converted to US dollars",
    "The section instead states that amounts are stored in whatever currency they were entered in",
    "No other sections of the README are modified",
    "The section remains coherent and readable"
  ],
  "scope_exclusions": [
    "No changes to the actual code (tally/rates.py or any other source files)",
    "No changes to other README sections (e.g. the 'add' command description at line 31-32 which also mentions dollar conversion)"
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
