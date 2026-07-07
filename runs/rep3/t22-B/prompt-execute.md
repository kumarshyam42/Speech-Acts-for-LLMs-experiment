You are working in this repository. Here is the request:

<request>
docs/faq.md feels thin. Can you make it more helpful?
</request>

You promised the following in a prior negotiation step:

```json
{
  "speech_act": "promise",
  "conditions_of_satisfaction": [
    "docs/faq.md retains all four existing entries unchanged",
    "At least five new Q&A entries are added covering CLI usage topics absent from the current FAQ: the budget command, the stats command, the list command, the export command, and the --store flag for changing the data file location",
    "Every factual claim in the new entries is verifiable against the actual code (cli.py, report.py, rates.py, config.py) or existing docs \u2014 nothing invented",
    "No pricing or plan details are added beyond what pricing.md already documents"
  ],
  "scope_exclusions": [
    "No changes to README.md, pricing.md, or any source file",
    "No new hosted-backup or account-management Q&As (feature not implemented in the codebase)"
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
