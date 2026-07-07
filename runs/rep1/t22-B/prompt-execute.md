You are working in this repository. Here is the request:

<request>
docs/faq.md feels thin. Can you make it more helpful?
</request>

You promised the following in a prior negotiation step:

```json
{
  "speech_act": "promise",
  "conditions_of_satisfaction": [
    "docs/faq.md retains all four existing Q&A entries, unchanged in meaning",
    "docs/faq.md gains at least 6 new Q&A entries covering topics visible in the README and CLI but absent from the FAQ (e.g. installation, the list/export/report commands, data file format, how currency conversion works, scope/limitations, what Python version is required)",
    "All added content is grounded in the repository (README.md, tally/cli.py, tally/rates.py, docs/) \u2014 no invented features or plans",
    "The file remains plain Markdown with no new dependencies or tooling"
  ],
  "scope_exclusions": [
    "No changes to any file other than docs/faq.md",
    "No rewriting of the pricing model \u2014 that content lives in docs/pricing.md and is not duplicated",
    "No UI, tests, or source-code changes"
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
