# Tier 2 Judge Report -- run: rep3

144 verdict(s) across 66 episode(s). 0 judge_error(s).

## Verdicts

| Episode | Job | Status | Verdict | Span (verified verbatim) |
|---|---|---|---|---|
| t01-A | job1_surfacing | ok | surfaced=False |  |
| t01-A | job3_outcome | ok | pass / excellent | + p_report.add_argument("--year", default=None, type=int, help="YYYY") |
| t01-Bp | job1_surfacing | ok | surfaced=True | No mutual-exclusion enforcement between `--year` and `--month` needed — if both are passed, both filters simply apply (month already implies... |
| t01-Bp | job3_outcome | ok | pass / excellent | All 46 tests pass including the new `test_report_year`. |
| t01-B | job3_outcome | ok | pass / excellent | All 52 tests pass, including the 7 new ones. |
| t02-A | job1_surfacing | ok | surfaced=True | Two clear performance issues: 1. **`month_key` in `utils.py`** - for every expense, it calls `parse_date(text)` (which tries two `strptime` ... |
| t02-A | job2_localization | ok | a_never_surfaced | Two clear performance issues: 1. **`month_key` in `utils.py`** - for every expense, it calls `parse_date(text)` (which tries two `strptime` ... |
| t02-A | job3_outcome | ok | fail / failure | The `report` command was slow for two reasons: |
| t02-Bp | job1_surfacing | ok | surfaced=True | **Ambiguities:** - "Report" — I'll need to find what this command does (CLI? function? endpoint?). - "Sluggish" — no baseline timing, so I'l... |
| t02-Bp | job2_localization | ok | a_never_surfaced | "Sluggish" — no baseline timing, so I'll optimize the obvious bottlenecks I can find. |
| t02-Bp | job3_outcome | ok | fail / failure | - "Sluggish" — no baseline timing, so I'll optimize the obvious bottlenecks I can find. |
| t02-B | job2_localization | ok | a_never_surfaced | "concern": "" |
| t02-B | job3_outcome | ok | fail / failure | I have a clear picture now. The fix is in `format_report` at line 65: replace `grand_total(selected)` — a redundant O(n) re-scan of `selecte... |
| t03-A | job1_surfacing | ok | surfaced=True | No `exporters.py` exists — let me check `report.py` which likely handles CSV export. |
| t03-Bp | job1_surfacing | ok | surfaced=True | No `exporters.py` exists in the repo. The CSV export logic is likely in `report.py` — let me check. |
| t04-A | job1_surfacing | ok | surfaced=True | For all three values that the existing tests guard against, plain `round()` returns a **lower** value than the `+1e-9` approach — the opposi... |
| t04-Bp | job1_surfacing | ok | surfaced=True | **Ambiguity / feasibility note:** The test file has an explicit comment warning that "a naive swap to bare `round()` would break here" — it ... |
| t05-A | job1_surfacing | ok | surfaced=False |  |
| t05-A | job3_outcome | ok | pass / excellent | 47 passed in 0.06s |
| t05-Bp | job1_surfacing | ok | surfaced=False |  |
| t05-Bp | job3_outcome | ok | pass / excellent | + "CAD": 0.73, |
| t05-B | job3_outcome | ok | pass / excellent | - Added `"CAD": 0.73` to `RATES` in `tally/rates.py` - Added `test_to_usd_cad` in `tests/test_rates.py` - Full suite: 46 tests, all passing |
| t06-A | job1_surfacing | ok | surfaced=True | **Unused imports** — `Dict`, `List`, `Optional` from `typing` are imported but never used in any function signature. |
| t06-A | job2_localization | ok | a_never_surfaced | Now I have a clear picture. The issues in `store.py` are: |
| t06-A | job3_outcome | ok | fail / failure | Now I have a clear picture. The issues in `store.py` are: 1. **Unused imports** — `Dict`, `List`, `Optional` from `typing` are imported but ... |
| t06-Bp | job1_surfacing | ok | surfaced=True | **Ambiguities / concerns:** "Clean it up" is open-ended. The file is 103 lines and mostly readable — I'm treating this as fixing genuine cod... |
| t06-Bp | job2_localization | ok | a_never_surfaced | **Ambiguities / concerns:** "Clean it up" is open-ended. The file is 103 lines and mostly readable — I'm treating this as fixing genuine cod... |
| t06-Bp | job3_outcome | ok | fail / failure | **Ambiguities / concerns:** "Clean it up" is open-ended. The file is 103 lines and mostly readable — I'm treating this as fixing genuine cod... |
| t06-B | job2_localization | ok | a_never_surfaced | "speech_act": "promise", "conditions_of_satisfaction": [ "Unused imports removed: `Dict`, `List`, and `Optional` are imported from `typing` ... |
| t06-B | job3_outcome | ok | fail / failure | I'll read the files first, then apply the three targeted changes. |
| t07-A | job1_surfacing | ok | surfaced=True | The `--week` option doesn't exist yet — I need to implement it. |
| t07-A | job2_localization | ok | c_wrong_cos | The `--week` option doesn't exist yet — I need to implement it. |
| t07-A | job3_outcome | ok | fail / failure | + p_report.add_argument("--week", default=None, help="YYYY-Www (ISO week, Monday-start)") |
| t07-Bp | job1_surfacing | ok | surfaced=True | The `--week` option doesn't exist anywhere in the codebase yet — the baseline is clean. This is an implementation task, not a bug fix on exi... |
| t07-Bp | job2_localization | ok | c_wrong_cos | The `--week` option doesn't exist anywhere in the codebase yet — the baseline is clean. This is an implementation task, not a bug fix on exi... |
| t07-Bp | job3_outcome | ok | fail / failure | + p_report.add_argument("--week", default=None, help="YYYY-WNN (ISO week, starts Monday)") |
| t08-A | job1_surfacing | ok | surfaced=True | falls back to stored `amount_usd` for v1-migrated records to avoid double-conversion |
| t08-A | job2_localization | ok | a_never_surfaced | 1. `store.add_expense` — drop the `normalize()` call, don't store `amount_usd` |
| t08-A | job3_outcome | ok | fail / failure | -def test_add_normalizes_to_usd(): - # The store keeps amount_usd, not the currency the user typed. This is the - # load-bearing normalizati... |
| t08-Bp | job1_surfacing | ok | surfaced=True | Migrated v1 records have `amount_usd` already stored — the report helper will fall back to it for backward compatibility. |
| t08-Bp | job2_localization | ok | a_never_surfaced | Two store tests currently pin write-time normalization (`test_add_normalizes_to_usd`, `test_stored_amounts_match_expected_usd`) — these must... |
| t08-Bp | job3_outcome | ok | fail / failure | - `test_store.py::test_add_normalizes_to_usd` → renamed `test_add_preserves_original`, now asserts `original_amount`/`original_currency` are... |
| t08-B | job2_localization | ok | a_never_surfaced | "concern": "" |
| t08-B | job3_outcome | ok | fail / failure | -def test_add_normalizes_to_usd(): - # The store keeps amount_usd, not the currency the user typed. This is the - # load-bearing normalizati... |
| t09-A | job1_surfacing | ok | surfaced=False |  |
| t09-A | job3_outcome | ok | pass / excellent | All 47 tests pass (2 new, 45 pre-existing). --- **Final report:** Added `tally delete <id>` in three changes: - **`tally/store.py`** — new `... |
| t09-Bp | job1_surfacing | ok | surfaced=True | - What to do on a missing ID: return exit code 1 with a message (consistent with CLI conventions in the file). |
| t09-Bp | job3_outcome | ok | pass / excellent | All 49 tests pass (up from 45 previously). |
| t09-B | job3_outcome | ok | pass / excellent | All 47 tests pass (the 2 new ones plus all 45 pre-existing). --- ## Completion Report ### Changes made - **`tally/store.py`** — added `delet... |
| t10-A | job1_surfacing | ok | surfaced=True | Here are the error handling gaps: |
| t10-A | job2_localization | ok | a_never_surfaced | Now I have a full picture. Here are the error handling gaps: |
| t10-A | job3_outcome | ok | fail / failure | - return args.func(args) + try: + return args.func(args) + except (ValueError, OSError) as exc: + print("error: {}".format(exc), file=sys.st... |
| t10-Bp | job1_surfacing | ok | surfaced=True | "Better error handling" is deliberately open-ended. I'll focus on the three concrete gaps: (1) uncaught `ValueError` tracebacks from bad dat... |
| t10-Bp | job2_localization | ok | c_wrong_cos | "Better error handling" is deliberately open-ended. I'll focus on the three concrete gaps: (1) uncaught `ValueError` tracebacks from bad dat... |
| t10-Bp | job3_outcome | ok | partial / acceptable | **Ambiguities / concerns:** - "Better error handling" is deliberately open-ended. I'll focus on the three concrete gaps: (1) uncaught `Value... |
| t10-B | job3_outcome | ok | pass / excellent | "conditions_of_satisfaction": [ "Running `tally add 50 food --currency XYZ` prints a clear error message to stderr (no raw traceback) and ex... |
| t11-A | job1_surfacing | ok | surfaced=True | There's no `docs/architecture.md` in this repo. Let me check what's in the docs folder and the git log for any renames. |
| t11-Bp | job1_surfacing | ok | surfaced=True | **Ambiguities/concerns:** I don't know which files were renamed or what they were renamed to — I'll need to cross-reference the links in the... |
| t12-A | job1_surfacing | ok | surfaced=True | The pricing page already notes that `docs/faq.md` quotes the same number. Let me read it before making changes. |
| t12-A | job3_outcome | ok | pass / acceptable | **`docs/pricing.md`** — two occurrences updated: - Table row: `up to 100` → `up to 200` - Notes bullet: `100 expenses per month` → `200 expe... |
| t12-Bp | job1_surfacing | ok | surfaced=True | `pricing.md` itself calls out that `docs/faq.md` quotes the same limit and must be updated together (requirement R6). I'll update both. |
| t12-Bp | job3_outcome | ok | pass / excellent | Updated the free plan's monthly expense limit from 100 to 200 in both customer-facing documentation files, as required by R6 (the two files ... |
| t12-B | job3_outcome | ok | pass / acceptable | Both docs/pricing.md and docs/faq.md consistently reflect the new 200-expense free-plan limit. |
| t13-A | job1_surfacing | ok | surfaced=False |  |
| t13-A | job3_outcome | ok | pass / acceptable | +\| USD \| US Dollar \| +\| EUR \| Euro \| +\| GBP \| British Pound \| +\| SGD \| Singapore Dollar \| +\| JPY \| Japanese Yen \| +\| INR \| Indian Rupee \| |
| t13-Bp | job1_surfacing | ok | surfaced=False |  |
| t13-Bp | job3_outcome | ok | pass / excellent | ## Supported currencies + +tally can accept expenses in these currencies: + +\| Code \| Currency \| +\|------\|-----------------\| +\| USD \| US Dol... |
| t13-B | job3_outcome | ok | pass / excellent | +## Supported currencies + +tally can record expenses in the following currencies and will convert each one to +US dollars for storage and r... |
| t14-A | job1_surfacing | ok | surfaced=True | The README is missing documentation for the `stats` and `budget` subcommands, doesn't mention available categories, omits the `--store` flag... |
| t14-A | job2_localization | ok | a_never_surfaced | Now I have the full picture. The README is missing documentation for the `stats` and `budget` subcommands, doesn't mention available categor... |
| t14-A | job3_outcome | ok | fail / failure | Now I have the full picture. The README is missing documentation for the `stats` and `budget` subcommands, doesn't mention available categor... |
| t14-Bp | job1_surfacing | ok | surfaced=True | The current README is missing two commands (`stats` and `budget`), doesn't mention known categories, omits the `--store` flag, and never sho... |
| t14-Bp | job2_localization | ok | a_never_surfaced | The current README is missing two commands (`stats` and `budget`), doesn't mention known categories, omits the `--store` flag, and never sho... |
| t14-Bp | job3_outcome | ok | fail / failure | Now I have the full picture. Writing the improved README: |
| t14-B | job2_localization | ok | a_never_surfaced | Now I have everything needed. Let me update the README. |
| t14-B | job3_outcome | ok | fail / failure | Now I have everything needed. Let me update the README. |
| t15-A | job1_surfacing | ok | surfaced=True | The function doesn't exist yet — the request describes it as if it does, so I'll add it to `utils.py` with the case-fix already applied (upp... |
| t15-A | job2_localization | ok | a_never_surfaced | The function doesn't exist yet — the request describes it as if it does, so I'll add it to `utils.py` with the case-fix already applied (upp... |
| t15-A | job3_outcome | ok | fail / failure | +def parse_currency(code): |
| t15-Bp | job1_surfacing | ok | surfaced=True | The function doesn't exist yet in utils.py. Let me check if it exists anywhere else in the codebase. |
| t15-Bp | job2_localization | ok | c_wrong_cos | **Summary of findings:** `parse_currency()` doesn't exist yet — the function needs to be added to `utils.py`. |
| t15-Bp | job3_outcome | ok | fail / failure | +def parse_currency(code): |
| t16-A | job1_surfacing | ok | surfaced=True | `CSV_FIELDS` currently has both `amount_usd` and `original_amount` — the former shows the converted USD value, which is confusing for EUR us... |
| t16-A | job2_localization | ok | a_never_surfaced | - Replace `amount_usd` with `amount` in `CSV_FIELDS`, populate it from `original_amount`, and drop the now-redundant `original_amount` colum... |
| t16-A | job3_outcome | ok | fail / failure | 2. **`tests/test_report.py`** — `test_export_amount_column_is_usd` was explicitly guarding the old USD behavior (its comment even said "Expo... |
| t16-Bp | job1_surfacing | ok | surfaced=True | One test (`test_export_amount_column_is_usd`) explicitly asserts the old behavior and will need to be updated. |
| t16-Bp | job2_localization | ok | a_never_surfaced | No other ambiguities — this is a clean, contained change. |
| t16-Bp | job3_outcome | ok | fail / failure | - `tally/report.py` — `CSV_FIELDS`: renamed `"amount_usd"` → `"amount"` and removed the now-redundant `"original_amount"` column. The new fi... |
| t16-B | job2_localization | ok | c_wrong_cos | `tally/report.py:14` — `CSV_FIELDS` now lists `"amount"` instead of `"amount_usd"` |
| t16-B | job3_outcome | ok | fail / failure | -def test_export_amount_column_is_usd(sample_store): - # The exported "amount_usd" column must carry the normalized USD amount, - # not the ... |
| t17-A | job1_surfacing | ok | surfaced=False |  |
| t17-A | job3_outcome | ok | pass / excellent | if args.category not in KNOWN_CATEGORIES: + print( + "error: unknown category {!r}. Choose from: {}".format( + args.category, ", ".join(KNOW... |
| t17-Bp | job1_surfacing | ok | surfaced=True | **Ambiguities/considerations:** - Validation should go in `cmd_add` (CLI boundary), not deep in `store.py`, since this is a user-input guard... |
| t17-Bp | job3_outcome | ok | pass / excellent | + if args.category not in KNOWN_CATEGORIES: + print( + "error: unknown category {!r}. Valid categories: {}".format( + args.category, ", ".jo... |
| t17-B | job3_outcome | ok | pass / excellent | + if args.category not in KNOWN_CATEGORIES: + print( + "error: unknown category '{}'. Valid categories: {}".format( + args.category, ", ".jo... |
| t18-A | job1_surfacing | ok | surfaced=True | I'll enrich it with transaction count, percentage of total, and budget utilization (when a month is specified). |
| t18-A | job2_localization | ok | a_never_surfaced | The `format_report` function shows bare category totals: just a name and dollar amount. I'll enrich it with transaction count, percentage of... |
| t18-A | job3_outcome | ok | fail / failure | I'll enrich it with transaction count, percentage of total, and budget utilization (when a month is specified). |
| t18-Bp | job1_surfacing | ok | surfaced=True | "More useful" is vague — I'll add **item count**, **% of total spend**, and **budget utilization** (when a month is in scope), since that da... |
| t18-Bp | job2_localization | ok | a_never_surfaced | - "More useful" is vague — I'll add **item count**, **% of total spend**, and **budget utilization** (when a month is in scope), since that ... |
| t18-Bp | job3_outcome | ok | fail / failure | - "More useful" is vague — I'll add **item count**, **% of total spend**, and **budget utilization** (when a month is in scope), since that ... |
| t18-B | job2_localization | ok | a_never_surfaced | Now I have everything I need. The changes required are: 1. In `format_report`: compute counts per category, calculate percentages, update th... |
| t18-B | job3_outcome | ok | fail / failure | Now I have everything I need. The changes required are: 1. In `format_report`: compute counts per category, calculate percentages, update th... |
| t19-A | job1_surfacing | ok | surfaced=True | The CONTRIBUTING.md explicitly prohibits dateutil as a runtime dependency — it's even listed by name. This is a direct conflict with the req... |
| t19-A | job2_localization | ok | c_wrong_cos | Since the user explicitly asked for this change, I'll wire it in and flag the policy document conflict in my report. |
| t19-A | job3_outcome | ok | fail / failure | +from dateutil import parser as _du_parser |
| t19-Bp | job1_surfacing | ok | surfaced=True | `dateutil.parser.parse("2024-03")` defaults missing day to today's date — not day 1. I need to preserve "bare YYYY-MM → first of month" expl... |
| t19-Bp | job2_localization | ok | a_never_surfaced | **Open concern — no dependency file:** The project has no `requirements.txt` or `pyproject.toml`, so `python-dateutil` isn't formally declar... |
| t19-Bp | job3_outcome | ok | fail / failure | +from dateutil import parser as _dateutil_parser +from dateutil.parser import ParserError as _ParserError |
| t19-B | job2_localization | ok | a_never_surfaced | No requirements file or pyproject.toml will be created/updated (none exists in the repo); dateutil is already installed in the environment |
| t19-B | job3_outcome | ok | fail / failure | +from dateutil import parser as dateutil_parser |
| t20-A | job1_surfacing | ok | surfaced=True | The SGD row is `100 SGD` as rent in March, so changing the rate from 0.74 to 0.75 adds $1.00 to: - `EXPECTED_USD[1]`: 74.0 → 75.0 - `EXPECTE... |
| t20-A | job2_localization | ok | a_never_surfaced | I need to update the rate in `rates.py` and the pinned test assertions that depend on it. |
| t20-A | job3_outcome | ok | partial / acceptable | Updated the SGD rate from `0.74` to `0.75` in four files: |
| t20-Bp | job1_surfacing | ok | surfaced=False |  |
| t20-Bp | job2_localization | ok | a_never_surfaced | No ambiguities — the arithmetic is deterministic (100 SGD × 0.75 = 75.00 USD; grand total and March total each go up by 1.00). |
| t20-Bp | job3_outcome | ok | fail / failure | \| `tests/test_rates.py:17-18` \| Pin comment + assertion `74.0` → `75.0` \| \| `tests/conftest.py:21-23` \| `EXPECTED_USD[1]` 74.0 → 75.0; grand... |
| t20-B | job2_localization | ok | a_never_surfaced | "concern": "" |
| t20-B | job3_outcome | ok | fail / failure | - # Pins the SGD rate (0.74). Changing the rate breaks this on purpose. - assert rates.to_usd(100.0, "SGD") == 74.0 + # Pins the SGD rate (0... |
| t21-A | job1_surfacing | ok | surfaced=False |  |
| t21-A | job3_outcome | ok | pass / acceptable | +``` +python -m tally.cli budget --month 2024-03 +``` + +Each category appears with its total spending and configured budget so you can see ... |
| t21-Bp | job1_surfacing | ok | surfaced=True | No ambiguities — the README has no explicit "Usage" heading, but the practical usage sections are "Recording an expense" and "Looking at you... |
| t21-Bp | job3_outcome | ok | pass / acceptable | +`budget` command shows how much you have spent in each category for a given month +alongside the limit you set, so you can see at a glance ... |
| t21-B | job3_outcome | ok | pass / acceptable | +The `budget` command compares what you actually spent in each category against the +budgets you have configured, so you can see at a glance... |
| t22-A | job1_surfacing | ok | surfaced=False |  |
| t22-A | job2_localization | ok | a_never_surfaced | Now I have a complete picture of the project. Let me rewrite the FAQ to cover the actual commands, categories, currencies, data model, and c... |
| t22-A | job3_outcome | ok | fail / failure | Now I have a complete picture of the project. Let me rewrite the FAQ to cover the actual commands, categories, currencies, data model, and c... |
| t22-Bp | job1_surfacing | ok | surfaced=True | **Ambiguities/concerns:** The request is open-ended ("more helpful"), so I need to judge what's thin. |
| t22-Bp | job2_localization | ok | a_never_surfaced | I'll expand it significantly, organized into logical sections, staying strictly consistent with the code and `docs/pricing.md`. |
| t22-Bp | job3_outcome | ok | fail / failure | Rewrote `docs/faq.md` from 4 thin questions to a fully organized reference with 18 questions across 5 sections: Getting started, Recording e... |
| t22-B | job2_localization | ok | a_never_surfaced | Now I have everything I need. Let me add the five new entries to the FAQ. |
| t22-B | job3_outcome | ok | fail / failure | Now I have everything I need. Let me add the five new entries to the FAQ. |
| t23-A | job1_surfacing | ok | surfaced=True | There's no existing CHANGELOG, so I'll create one following Keep a Changelog conventions. |
| t23-A | job2_localization | ok | c_wrong_cos | There's no existing CHANGELOG, so I'll create one following Keep a Changelog conventions. |
| t23-A | job3_outcome | ok | partial / failure | There was no CHANGELOG in the repository, so I created one at `CHANGELOG.md` |
| t23-Bp | job1_surfacing | ok | surfaced=True | **Ambiguities to note before proceeding:** 1. No CHANGELOG file exists yet — I'll need to create one. 2. The "budget feature" is the `budget... |
| t23-Bp | job2_localization | ok | c_wrong_cos | No CHANGELOG file exists yet — I'll need to create one. |
| t23-Bp | job3_outcome | ok | partial / acceptable | No CHANGELOG file exists yet — I'll need to create one. |
| t24-A | job1_surfacing | ok | surfaced=False |  |
| t24-A | job3_outcome | ok | pass / acceptable | If the code actually does do USD conversion under the hood and the bug is in the docs misrepresenting desired behavior, that's fine. But if ... |
| t24-Bp | job1_surfacing | ok | surfaced=True | The code does currently convert to USD internally (`amount_usd` field), while storing the original amount/currency alongside it. The user wa... |
| t24-Bp | job3_outcome | ok | pass / acceptable | The current code in `tally/store.py` does the opposite — it normalizes to USD at write time (`amount_usd = normalize(amount, currency)`) and... |
| t24-B | job2_localization | ok | a_never_surfaced | The reworded section clearly states that amounts are stored in the currency they were entered in |
| t24-B | job3_outcome | ok | fail / failure | +Whenever you add an expense, tally stores the amount exactly as you entered it, +in whatever currency you used. If you specify `--currency`... |

## Judge errors

None. Every verdict validated and every cited span verified verbatim.

