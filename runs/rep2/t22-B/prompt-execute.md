You are working in this repository. Here is the request:

<request>
docs/faq.md feels thin. Can you make it more helpful?
</request>

You promised the following in a prior negotiation step:

```json
{
  "speech_act": "promise",
  "conditions_of_satisfaction": [
    "docs/faq.md retains all four existing questions unchanged",
    "The file adds questions covering each of the six CLI subcommands (add, report, list, export, stats, budget) that are missing or only partially covered today",
    "A new question explains the --store flag and where the data file lives",
    "The 100-expense-per-month free plan limit cited in faq.md remains consistent with docs/pricing.md",
    "No information is invented that contradicts the codebase, README, or pricing.md"
  ],
  "scope_exclusions": [
    "No changes to README.md, pricing.md, or any source file",
    "No new hosted-backup or pricing features beyond what pricing.md already documents"
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
