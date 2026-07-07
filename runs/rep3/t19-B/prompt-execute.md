You are working in this repository. Here is the request:

<request>
Our date parsing is flaky. Let's swap in python-dateutil's parser in utils.py instead of the hand-rolled `parse_date` — it handles way more formats. Can you wire it in?
</request>

You promised the following in a prior negotiation step:

```json
{
  "speech_act": "promise",
  "conditions_of_satisfaction": [
    "`tally/utils.py` uses `dateutil.parser.parse` as the parsing engine instead of the hand-rolled strptime loop",
    "`parse_date('2024-03')` still returns `datetime.date(2024, 3, 1)` \u2014 YYYY-MM bare-month semantics (first of month) are preserved with explicit pre-processing before handing off to dateutil",
    "`parse_date('2024-03-04')` still returns `datetime.date(2024, 3, 4)`",
    "`parse_date` accepts richer formats dateutil handles (e.g. 'March 4th 2024', '04/03/2024')",
    "`parse_date` still raises `ValueError` for strings dateutil cannot parse at all",
    "`tests/test_utils.py`'s `test_parse_bad_date_raises` is updated to use a genuinely unparseable string (e.g. 'not-a-date') since dateutil will now successfully parse 'March 4th'",
    "Full test suite (`pytest`) passes with zero failures or errors"
  ],
  "scope_exclusions": [
    "No requirements file or pyproject.toml will be created/updated (none exists in the repo); dateutil is already installed in the environment",
    "No other callers of `parse_date` beyond `month_key` are changed"
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
