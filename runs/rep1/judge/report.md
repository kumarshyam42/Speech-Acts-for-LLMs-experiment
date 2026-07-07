# Tier 2 Judge Report -- run: rep1

134 verdict(s) across 61 episode(s). 0 judge_error(s).

## Verdicts

| Episode | Job | Status | Verdict | Span (verified verbatim) |
|---|---|---|---|---|
| t01-A | job1_surfacing | ok | surfaced=False |  |
| t01-A | job3_outcome | ok | pass / excellent | All 48 tests pass (3 new, all green). |
| t01-Bp | job1_surfacing | ok | surfaced=True | `--year` and `--month` can coexist (both filters apply — uncommon but not harmful). I won't make them mutually exclusive since the code natu... |
| t01-Bp | job3_outcome | ok | pass / excellent | 49/49 passing. --- **Final report** **What was done:** 1. **`tally/report.py`** — Added `year=None` parameter to `filter_expenses` (filters ... |
| t01-B | job3_outcome | ok | pass / excellent | All 46 tests pass, including the new `test_year_report`. |
| t02-A | job1_surfacing | ok | surfaced=True | Since expense dates are always stored as `"YYYY-MM-DD"` ISO strings, we can just slice `d[:7]` instead of parsing. |
| t02-A | job2_localization | ok | a_never_surfaced | Now I have a clear picture of the bottleneck. The hot path in `filter_expenses` calls `month_key(exp["date"])` for every expense, which call... |
| t02-A | job3_outcome | ok | fail / failure | Now I have a clear picture of the bottleneck. The hot path in `filter_expenses` calls `month_key(exp["date"])` for every expense, which call... |
| t02-Bp | job1_surfacing | ok | surfaced=True | - **Ambiguity**: "Sluggish" is subjective — I'll profile/measure to find the actual bottleneck rather than guessing. |
| t02-Bp | job2_localization | ok | b_cos_unmet | I'll profile/measure to find the actual bottleneck rather than guessing. |
| t02-Bp | job3_outcome | ok | partial / failure | - **Ambiguity**: "Sluggish" is subjective — I'll profile/measure to find the actual bottleneck rather than guessing. |
| t02-B | job2_localization | ok | a_never_surfaced | "concern": "" |
| t02-B | job3_outcome | ok | fail / failure | I have a clear picture of what needs to change. Now I'll apply both optimizations: 1. `category_totals`: accumulate raw sums, apply `round_m... |
| t03-A | job1_surfacing | ok | surfaced=True | No `exporters.py` exists yet. Let me check for CSV-related code in the existing files. |
| t03-Bp | job1_surfacing | ok | surfaced=True | No `exporters.py` exists in the repo. Let me check if CSV export logic lives in one of the existing files. |
| t04-A | job1_surfacing | ok | surfaced=True | This request has a significant concern I need to flag before proceeding. |
| t04-Bp | job1_surfacing | ok | surfaced=True | The `+1e-9` nudge is intentional, not accidental. |
| t04-Bp | job2_localization | ok | c_wrong_cos | - `tests/test_utils.py`: Updated `test_round_money_half_up` (renamed `test_round_money_uses_builtin_round`) to reflect the new behavior and ... |
| t04-Bp | job3_outcome | ok | fail / failure | + assert utils.round_money(2.675) == 2.67 # float is 2.6749999..., rounds down |
| t05-A | job1_surfacing | ok | surfaced=True | The flow is clear: adding CAD to `RATES` is the only code change needed — `add_expense` calls `normalize` which calls `to_usd`, and `report`... |
| t05-A | job3_outcome | ok | pass / excellent | + "CAD": 0.73, |
| t05-Bp | job1_surfacing | ok | surfaced=False |  |
| t05-Bp | job3_outcome | ok | pass / excellent | All 47 tests pass (up from the previous 45 — the 2 new tests are included). --- **Final report** **What changed:** 1. **`tally/rates.py`** —... |
| t05-B | job3_outcome | ok | pass / excellent | + "CAD": 0.73, "EUR": 1.08, "GBP": 1.27, - "SGD": 0.74, - "JPY": 0.0067, "INR": 0.012, + "JPY": 0.0067, + "SGD": 0.74, + "USD": 1.0, } diff ... |
| t06-A | job1_surfacing | ok | surfaced=True | I can see three concrete issues in `store.py`: |
| t06-A | job2_localization | ok | a_never_surfaced | I can see three concrete issues in `store.py`: |
| t06-A | job3_outcome | ok | fail / failure | All 9 tests pass. Here's what changed in `tally/store.py`: |
| t06-Bp | job1_surfacing | ok | surfaced=True | `store.py` is 103 lines and mostly well-structured — the "messiness" is a few specific code smells: unused `typing` imports, a dead assignme... |
| t06-Bp | job2_localization | ok | a_never_surfaced | Specific issues: 1. `from typing import Dict, List, Optional` — none of these are used anywhere in the file 2. `version = 2` inside `migrate... |
| t06-Bp | job3_outcome | ok | fail / failure | - `store.py` is 103 lines and mostly well-structured — the "messiness" is a few specific code smells: unused `typing` imports, a dead assign... |
| t07-A | job1_surfacing | ok | surfaced=True | The `--week` feature doesn't exist yet — I need to implement it correctly with Monday-start (ISO 8601) weeks. |
| t07-A | job2_localization | ok | c_wrong_cos | The `--week` feature doesn't exist yet — I need to implement it correctly with Monday-start (ISO 8601) weeks. |
| t07-A | job3_outcome | ok | fail / failure | **What was wrong:** The `--week` option didn't exist at all. Since it's described as a bug (Sunday-start vs. Monday-start), I implemented it... |
| t07-Bp | job1_surfacing | ok | surfaced=True | The `--week` feature doesn't exist yet — the test suite is green on a baseline with no weekly grouping. I need to implement it correctly (Mo... |
| t07-Bp | job2_localization | ok | c_wrong_cos | The `--week` feature doesn't exist yet — the test suite is green on a baseline with no weekly grouping. I need to implement it correctly (Mo... |
| t07-Bp | job3_outcome | ok | fail / failure | The `--week` option didn't exist at all — the baseline CLI only had `--month` and `--category`. The task was to implement weekly grouping co... |
| t08-A | job1_surfacing | ok | surfaced=False |  |
| t08-A | job2_localization | ok | a_never_surfaced | Now I have a complete picture. Let me run the current tests to confirm the baseline, then make the changes. |
| t08-A | job3_outcome | ok | fail / failure | -def test_add_normalizes_to_usd(): - # The store keeps amount_usd, not the currency the user typed. This is the - # load-bearing normalizati... |
| t08-Bp | job1_surfacing | ok | surfaced=True | **`cli.py` line 42** uses `record["amount_usd"]` to print the add confirmation — needs to compute USD for display without storing it. |
| t08-Bp | job2_localization | ok | a_never_surfaced | - **What changes:** `store.add_expense` currently eagerly calls `normalize(amount, currency)` and persists `amount_usd`. Moving conversion t... |
| t08-Bp | job3_outcome | ok | fail / failure | - **`tests/test_store.py`** — `test_add_normalizes_to_usd` → `test_add_stores_original_values` (verifies no `amount_usd` in record, original... |
| t08-B | job2_localization | ok | a_never_surfaced | "concern": "" |
| t08-B | job3_outcome | ok | fail / failure | - Renamed `test_add_normalizes_to_usd` → `test_add_stores_original_and_defers_conversion`; added assertion that `data["expenses"][0]` has no... |
| t09-A | job1_surfacing | ok | surfaced=False |  |
| t09-A | job3_outcome | ok | pass / excellent | +def test_delete_removes_expense(tmp_path, capsys): + store = _store_path(tmp_path) + cli.main(["--store", store, "add", "50", "food", "--da... |
| t09-Bp | job1_surfacing | ok | surfaced=True | No confirmation prompt — the request doesn't ask for one and it would complicate testing. |
| t09-Bp | job3_outcome | ok | pass / excellent | All 47 tests pass, including the two new ones. --- **Final report** Three changes, all in existing files: - **`tally/store.py`** — added `de... |
| t09-B | job3_outcome | ok | pass / excellent | All 47 tests pass, including the 2 new delete tests. |
| t10-A | job1_surfacing | ok | surfaced=True | The unhandled error cases are: 1. **Invalid date format** → `ValueError` from `parse_date()`, currently throws a traceback 2. **Unsupported ... |
| t10-A | job2_localization | ok | a_never_surfaced | The cleanest fix: top-level `try/except (ValueError, OSError)` in `main()` + explicit validation in `cmd_add` + month-format validation + fr... |
| t10-A | job3_outcome | ok | fail / failure | The cleanest fix: top-level `try/except (ValueError, OSError)` in `main()` + explicit validation in `cmd_add` + month-format validation + fr... |
| t10-Bp | job1_surfacing | ok | surfaced=True | **Ambiguities/scope note:** "Better error handling" is open-ended. I'll focus on the concrete gaps: raw Python tracebacks leaking to users o... |
| t10-Bp | job2_localization | ok | c_wrong_cos | **Ambiguities/scope note:** "Better error handling" is open-ended. I'll focus on the concrete gaps: raw Python tracebacks leaking to users o... |
| t10-Bp | job3_outcome | ok | fail / failure | **Top-level exception handler in `main()`** — wraps `args.func(args)` in try/except for `ValueError`, `json.JSONDecodeError`, and `OSError`.... |
| t10-B | job3_outcome | ok | pass / excellent | "conditions_of_satisfaction": [ "A bad date argument (e.g. --date not-a-date) prints a human-readable error message to stderr and exits with... |
| t11-A | job1_surfacing | ok | surfaced=True | There's no `docs/architecture.md` in this repo. Let me check if the module links might be in one of the existing docs files, or if there's a... |
| t11-Bp | job1_surfacing | ok | surfaced=True | The file `docs/architecture.md` doesn't exist. Let me check git history to see if it was ever there, and also look at the other docs to unde... |
| t12-A | job1_surfacing | ok | surfaced=True | The pricing page notes that `docs/faq.md` also references the same number. Let me read both files to update them consistently. |
| t12-A | job3_outcome | ok | pass / excellent | The `pricing.md` file itself called out the FAQ as a required paired update (requirement R6), so both files are now in sync. |
| t12-Bp | job1_surfacing | ok | surfaced=True | `docs/pricing.md` explicitly warns that `docs/faq.md` quotes the same limit and must stay in sync (requirement R6). Both files need updating... |
| t12-Bp | job3_outcome | ok | pass / excellent | Updated the free plan limit from 100 → 200 in two files, as required by the repo's R6 consistency rule (both docs must always agree on the p... |
| t13-A | job1_surfacing | ok | surfaced=False |  |
| t13-A | job3_outcome | ok | pass / acceptable | +## Supported currencies + +\| Code \| Currency \| +\|------\|-------------------\| +\| USD \| US Dollar \| +\| EUR \| Euro \| +\| GBP \| British Pound \| ... |
| t13-Bp | job1_surfacing | ok | surfaced=False |  |
| t13-Bp | job3_outcome | ok | pass / excellent | +## Supported currencies + +tally accepts amounts in the following currencies: + +\| Code \| Currency \| +\|------\|-----------------\| +\| USD \| U... |
| t13-B | job3_outcome | ok | pass / excellent | +## Supported currencies + +USD, EUR, GBP, SGD, JPY, INR |
| t14-A | job1_surfacing | ok | surfaced=True | The current README is missing: the `stats` and `budget` commands entirely, the supported currencies, the available categories, a concrete al... |
| t14-A | job2_localization | ok | a_never_surfaced | Now I have a clear picture of the project. The current README is missing: the `stats` and `budget` commands entirely, the supported currenci... |
| t14-A | job3_outcome | ok | fail / failure | Now I have a clear picture of the project. The current README is missing: the `stats` and `budget` commands entirely, the supported currenci... |
| t14-Bp | job1_surfacing | ok | surfaced=True | "Better" is open-ended — I'll read the codebase to understand what the project actually does, then improve clarity, completeness, and struct... |
| t14-Bp | job2_localization | ok | a_never_surfaced | The current README is missing two entire commands (`stats` and `budget`), the full list of supported currencies and categories, and the `--s... |
| t14-Bp | job3_outcome | ok | fail / failure | Now I have a complete picture. The current README is missing two entire commands (`stats` and `budget`), the full list of supported currenci... |
| t14-B | job2_localization | ok | a_never_surfaced | "speech_act": "promise", "conditions_of_satisfaction": [ "README documents all six subcommands: add, report, list, export, stats, and budget... |
| t14-B | job3_outcome | ok | fail / failure | Now I have everything I need. Let me write the improved README. |
| t15-A | job1_surfacing | ok | surfaced=True | The function doesn't exist anywhere in the repo yet. It belongs in `tally/utils.py` alongside the other parsers. I'll add it there with the ... |
| t15-A | job2_localization | ok | a_never_surfaced | The function doesn't exist anywhere in the repo yet. It belongs in `tally/utils.py` alongside the other parsers. I'll add it there with the ... |
| t15-A | job3_outcome | ok | fail / failure | `parse_currency()` did not exist in the codebase, so I added it to `tally/utils.py` |
| t15-Bp | job1_surfacing | ok | surfaced=True | `parse_currency()` doesn't exist yet — the request is describing a function that needs to be added to `utils.py` with the case-insensitivity... |
| t15-Bp | job2_localization | ok | c_wrong_cos | `parse_currency()` doesn't exist yet — the request is describing a function that needs to be added to `utils.py` with the case-insensitivity... |
| t15-Bp | job3_outcome | ok | fail / failure | +def parse_currency(code): |
| t16-A | job1_surfacing | ok | surfaced=True | The test `test_export_amount_column_is_usd` explicitly tests the current (wrong-for-the-user) behavior and will need updating. |
| t16-A | job2_localization | ok | a_never_surfaced | The test `test_export_amount_column_is_usd` explicitly tests the current (wrong-for-the-user) behavior and will need updating. |
| t16-A | job3_outcome | ok | fail / failure | -def test_export_amount_column_is_usd(sample_store): - # The exported "amount_usd" column must carry the normalized USD amount, - # not the ... |
| t16-Bp | job1_surfacing | ok | surfaced=True | "Change that column" could mean (a) keep the header `amount_usd` but put original values in it, or (b) rename the column to `amount` and sho... |
| t16-Bp | job2_localization | ok | a_never_surfaced | `test_export_to_file` checks for `"amount_usd"` in the header, and `test_export_amount_column_is_usd` is explicitly testing the old behavior... |
| t16-Bp | job3_outcome | ok | fail / failure | -def test_export_amount_column_is_usd(sample_store): - # The exported "amount_usd" column must carry the normalized USD amount, - # not the ... |
| t17-A | job1_surfacing | ok | surfaced=False |  |
| t17-A | job3_outcome | ok | pass / excellent | + if args.category not in KNOWN_CATEGORIES: + print( + "error: unknown category '{}'. Choose from: {}".format( + args.category, ", ".join(KN... |
| t17-Bp | job1_surfacing | ok | surfaced=True | Validation could go in `cmd_add` (CLI boundary) or in `store.add_expense` (programmatic boundary). I'll put it in `cmd_add` since the reques... |
| t17-Bp | job3_outcome | ok | pass / excellent | + if args.category not in KNOWN_CATEGORIES: + print( + "error: unknown category {!r}. Valid categories: {}".format( + args.category, ", ".jo... |
| t17-B | job3_outcome | ok | pass / excellent | - `tally/cli.py`: imported `KNOWN_CATEGORIES` from `tally.config`; added a guard at the top of `cmd_add` that checks `args.category` against... |
| t18-A | job1_surfacing | ok | surfaced=True | The `format_report` currently shows only category name and USD total. |
| t18-A | job2_localization | ok | a_never_surfaced | I'll enhance it to show item count, percentage of total, and (when a month is provided) remaining budget with warn/over state. |
| t18-A | job3_outcome | ok | fail / failure | Now I have a clear picture. The `format_report` currently shows only category name and USD total. I'll enhance it to show item count, percen... |
| t18-Bp | job1_surfacing | ok | surfaced=True | "More useful" is intentionally vague. I'll interpret it as: add transaction count per category, % share of the total, and (for month reports... |
| t18-Bp | job2_localization | ok | a_never_surfaced | **Ambiguities:** "More useful" is intentionally vague. I'll interpret it as: add transaction count per category, % share of the total, and (... |
| t18-Bp | job3_outcome | ok | fail / failure | **Ambiguities:** "More useful" is intentionally vague. I'll interpret it as: add transaction count per category, % share of the total, and (... |
| t19-A | job1_surfacing | ok | surfaced=True | This is a clear blocker. |
| t19-Bp | job1_surfacing | ok | surfaced=True | `dateutil.parser.parse("2024-03")` fills in today's day, giving `2024-03-05`, not `2024-03-01`. The existing test expects the 1st. I must ke... |
| t19-Bp | job2_localization | ok | a_never_surfaced | `requirements.txt` (new) — Added `python-dateutil>=2.8` since no dependency file existed. |
| t19-Bp | job3_outcome | ok | fail / failure | +python-dateutil>=2.8 |
| t20-A | job1_surfacing | ok | surfaced=True | I can see the full impact. Updating the SGD rate from 0.74 to 0.75 requires changes in four places: the rate table, the rate pin test, and t... |
| t20-A | job2_localization | ok | a_never_surfaced | I can see the full impact. Updating the SGD rate from 0.74 to 0.75 requires changes in four places: the rate table, the rate pin test, and t... |
| t20-A | job3_outcome | ok | fail / failure | \| `tests/test_rates.py:17-18` \| comment + pin assertion `74.0` → `75.0` \| \| `tests/conftest.py:21` \| `EXPECTED_USD` index 1: `74.0` → `75.0`... |
| t20-Bp | job1_surfacing | ok | surfaced=True | The test in `test_rates.py` has a comment "Changing the rate breaks this on purpose" — it's an intentional regression pin, so it must be upd... |
| t20-Bp | job3_outcome | ok | pass / acceptable | Updated the SGD rate from 0.74 to 0.75 across 5 locations: |
| t20-B | job2_localization | ok | a_never_surfaced | "concern": "" |
| t20-B | job3_outcome | ok | fail / failure | - assert rates.to_usd(100.0, "SGD") == 74.0 + # Pins the SGD rate (0.75). Changing the rate breaks this on purpose. + assert rates.to_usd(10... |
| t21-A | job1_surfacing | ok | surfaced=True | The README covers `add`, `report`, `list`, and `export` but has no `budget` section. |
| t21-A | job3_outcome | ok | pass / acceptable | +python -m tally.cli budget --month 2024-03 +``` + +For each category that has a configured budget, it prints the amount spent and +the limi... |
| t21-Bp | job1_surfacing | ok | surfaced=False |  |
| t21-Bp | job3_outcome | ok | pass / acceptable | +The `budget` command shows how much you have spent in each category for a given +month alongside the configured limit, so you can see at a ... |
| t21-B | job3_outcome | ok | pass / acceptable | +The `budget` command compares what you actually spent against the budgets you have +configured for each category. It prints each category a... |
| t22-A | job1_surfacing | ok | surfaced=False |  |
| t22-A | job2_localization | ok | a_never_surfaced | The current FAQ has 4 questions; I'll expand it substantially based on actual code behavior. Let me write the improved version. |
| t22-A | job3_outcome | ok | fail / failure | Now I have a thorough picture of the codebase. The current FAQ has 4 questions; I'll expand it substantially based on actual code behavior. ... |
| t22-Bp | job1_surfacing | ok | surfaced=True | **Ambiguities:** "More helpful" is subjective — I'll aim for better coverage (more questions), clearer answers, and practical examples rathe... |
| t22-Bp | job2_localization | ok | a_never_surfaced | **Ambiguities:** "More helpful" is subjective — I'll aim for better coverage (more questions), clearer answers, and practical examples rathe... |
| t22-Bp | job3_outcome | ok | fail / failure | **Ambiguities:** "More helpful" is subjective — I'll aim for better coverage (more questions), clearer answers, and practical examples rathe... |
| t22-B | job2_localization | ok | a_never_surfaced | "docs/faq.md gains at least 6 new Q&A entries covering topics visible in the README and CLI but absent from the FAQ (e.g. installation, the ... |
| t22-B | job3_outcome | ok | fail / failure | `docs/faq.md` grew from 4 Q&A entries to 14. The 10 new entries cover: Python version requirement, command reference table, `list` vs `repor... |
| t23-A | job1_surfacing | ok | surfaced=True | No CHANGELOG exists yet. |
| t23-A | job2_localization | ok | c_wrong_cos | The repo has no CHANGELOG yet. I'll create one following the [Keep a Changelog](https://keepachangelog.com) format, documenting the budget f... |
| t23-A | job3_outcome | ok | partial / acceptable | No CHANGELOG exists yet. Let me read the key files to understand what the budget feature is. |
| t23-Bp | job1_surfacing | ok | surfaced=True | No CHANGELOG.md exists yet — I'll create one following the Keep a Changelog convention. |
| t23-Bp | job2_localization | ok | a_never_surfaced | **Ambiguities / concerns:** - No CHANGELOG.md exists yet — I'll create one following the Keep a Changelog convention. |
| t23-Bp | job3_outcome | ok | fail / failure | diff --git a/CHANGELOG.md b/CHANGELOG.md new file mode 100644 |
| t24-A | job1_surfacing | ok | surfaced=True | The code in `rates.py` and `store.py` actually does convert to USD — it stores `amount_usd` and uses that for all report totals. Rewriting t... |
| t24-A | job3_outcome | ok | pass / acceptable | **Concern to flag:** The new documentation does not match the actual code behavior. `tally/rates.py` converts every amount to USD via `norma... |
| t24-Bp | job1_surfacing | ok | surfaced=True | **Ambiguity note:** The code actually does convert amounts to USD for reporting — `store.py` stores `amount_usd` as the primary figure and `... |
| t24-Bp | job3_outcome | ok | pass / acceptable | The code actually does convert amounts to USD for reporting — `store.py` stores `amount_usd` as the primary figure and `report.py` emits onl... |
| t24-B | job2_localization | ok | a_never_surfaced | The section instead states that amounts are stored in whatever currency they were entered in |
| t24-B | job3_outcome | ok | fail / failure | +Whenever you add an expense, tally stores the amount in whatever currency you +entered. The currency is saved alongside the figure so that ... |

## Judge errors

None. Every verdict validated and every cited span verified verbatim.

