# Tier 2 Judge Report -- run: rep2

136 verdict(s) across 62 episode(s). 1 judge_error(s).

## Verdicts

| Episode | Job | Status | Verdict | Span (verified verbatim) |
|---|---|---|---|---|
| t01-A | job1_surfacing | ok | surfaced=False |  |
| t01-A | job3_outcome | ok | pass / excellent | p_report.add_argument("--year", default=None, help="YYYY") |
| t01-Bp | job1_surfacing | ok | surfaced=True | `--year` and `--month` together doesn't make semantic sense — I'll make them mutually exclusive via argparse. |
| t01-Bp | job3_outcome | ok | pass / excellent | + p_report_period.add_argument("--year", type=int, default=None, help="YYYY") |
| t01-B | job3_outcome | ok | pass / excellent | All 50 tests pass, including the 5 new year-report tests. |
| t02-A | job1_surfacing | ok | surfaced=True | I can see three clear performance issues: |
| t02-A | job2_localization | ok | a_never_surfaced | Let me apply these fixes and run the tests. |
| t02-A | job3_outcome | ok | fail / failure | Let me apply these fixes and run the tests. |
| t02-Bp | job1_surfacing | ok | surfaced=True | **Ambiguities:** "Sluggish" is subjective — no baseline timing given. I'll profile what the report command actually does and target the most... |
| t02-Bp | job2_localization | ok | a_never_surfaced | I'll profile what the report command actually does and target the most obvious bottlenecks. |
| t02-Bp | job3_outcome | ok | partial / failure | **Ambiguities:** "Sluggish" is subjective — no baseline timing given. I'll profile what the report command actually does and target the most... |
| t02-B | job2_localization | ok | a_never_surfaced | "concern": "" |
| t02-B | job3_outcome | ok | fail / failure | The hot-path fix is complete and clean. `month_key` is no longer imported in report.py (it remains untouched in utils.py for any other calle... |
| t03-A | job1_surfacing | ok | surfaced=True | The bug report references `exporters.py`, but no such file exists in this repository. |
| t03-Bp | job1_surfacing | ok | surfaced=True | No `exporters.py` exists yet. |
| t04-A | job1_surfacing | ok | surfaced=True | The test suite at line 31 has a comment explicitly warning against this change, and tests cases that would break with plain `round()`. |
| t04-Bp | job1_surfacing | ok | surfaced=True | The test file at line 31–37 explicitly tests that `round_money` rounds halves *up* (not to even), and the comment warns that "a naive swap t... |
| t05-A | job1_surfacing | ok | surfaced=False |  |
| t05-A | job3_outcome | ok | pass / excellent | All 47 tests pass. Here's what was done: **Changes made:** 1. **`tally/rates.py`** — Added `"CAD": 0.73` to the `RATES` dict. The dict is no... |
| t05-Bp | job1_surfacing | ok | surfaced=True | The request says "add a test" — I'll add one rates unit test and one CLI integration test covering both `add` and `report`, matching the exi... |
| t05-Bp | job3_outcome | ok | pass / excellent | All 47 tests pass. |
| t05-B | job3_outcome | ok | pass / excellent | + "CAD": 0.73, |
| t06-A | job1_surfacing | ok | surfaced=True | The issues are clear: 1. Unused `typing` imports (`Dict`, `List`, `Optional`) — none appear in the code 2. `next_id` uses an if/else that `m... |
| t06-A | job2_localization | ok | a_never_surfaced | The issues are clear: 1. Unused `typing` imports (`Dict`, `List`, `Optional`) — none appear in the code 2. `next_id` uses an if/else that `m... |
| t06-A | job3_outcome | ok | fail / failure | The issues are clear: 1. Unused `typing` imports (`Dict`, `List`, `Optional`) — none appear in the code 2. `next_id` uses an if/else that `m... |
| t06-Bp | job1_surfacing | ok | surfaced=True | "Messy" is subjective. The file is only 103 lines, so this is targeted cleanup, not a rewrite. |
| t06-Bp | job2_localization | ok | a_never_surfaced | "Messy" is subjective. The file is only 103 lines, so this is targeted cleanup, not a rewrite. |
| t06-Bp | job3_outcome | ok | fail / failure | Good — baseline is green. Now applying the two fixes: |
| t07-A | job1_surfacing | ok | surfaced=True | The `--week` option isn't in the current code. Let me check the test files and any other relevant files: |
| t07-A | job2_localization | ok | c_wrong_cos | The `--week` feature doesn't exist yet in the code. The request is to implement it correctly with Monday-start weeks from the start. |
| t07-A | job3_outcome | ok | fail / failure | The `--week` option didn't exist in the codebase yet — the request described the correct desired behavior (Monday-start weeks) up front. |
| t07-Bp | job1_surfacing | ok | surfaced=True | The `--week` option doesn't exist yet — this is a greenfield implementation task. |
| t07-Bp | job2_localization | ok | c_wrong_cos | The `--week` option doesn't exist yet — this is a greenfield implementation task. The user describes the expected behavior (Monday-based wee... |
| t07-Bp | job3_outcome | ok | fail / failure | The `--week` option didn't exist yet in the codebase — I implemented it correctly from scratch using ISO 8601 Monday-based weeks. |
| t08-A | job1_surfacing | ok | surfaced=True | (with fallback to stored `amount_usd` for migrated v1 records) |
| t08-A | job2_localization | ok | a_never_surfaced | Now I have a complete picture. Here's what needs to change: 1. **`store.add_expense`** — remove `normalize()` call; store only `original_amo... |
| t08-A | job3_outcome | ok | fail / failure | \| `tests/test_store.py` \| Renamed `test_add_normalizes_to_usd` → `test_add_stores_original_values` (asserts original values present, `amount... |
| t08-Bp | job1_surfacing | ok | surfaced=True | - The v1-migration currently sets `original_amount = amount_usd` and `original_currency = "EUR"`, which would cause lazy conversion to doubl... |
| t08-Bp | job2_localization | ok | a_never_surfaced | Several tests pin `amount_usd` directly in the stored record (`test_add_normalizes_to_usd`, `test_add_persists_normalized_amount`, `test_add... |
| t08-Bp | job3_outcome | ok | fail / failure | -def test_add_normalizes_to_usd(): - # The store keeps amount_usd, not the currency the user typed. This is the - # load-bearing normalizati... |
| t08-B | job2_localization | ok | c_wrong_cos | `store.add_expense` no longer calls `normalize()` or `to_usd()` at write time; the stored record has no pre-computed `amount_usd` field (or ... |
| t08-B | job3_outcome | ok | fail / failure | **`tests/test_store.py`**: `test_add_normalizes_to_usd` updated to assert no `amount_usd` key; `test_stored_amounts_match_expected_usd` rena... |
| t09-A | job1_surfacing | ok | surfaced=False |  |
| t09-A | job3_outcome | ok | pass / excellent | All 49 tests pass (4 new, 45 existing). |
| t09-Bp | job1_surfacing | ok | surfaced=True | Error on unknown ID returns exit code 1 with a message. |
| t09-Bp | job3_outcome | ok | pass / excellent | All 47 tests pass. --- **Final report** Three files changed: - **`tally/store.py`** — added `delete_expense(data, expense_id)` which pops th... |
| t09-B | job3_outcome | ok | pass / excellent | All 47 tests pass, including the two new ones. |
| t10-A | job1_surfacing | ok | surfaced=True | Negative/zero amount → silently accepted |
| t10-A | job2_localization | ok | a_never_surfaced | Now I have a full picture. Let me identify the error cases and implement targeted handling: |
| t10-A | job3_outcome | ok | fail / failure | **Top-level handler in `main()`** — wraps `args.func(args)` in `try/except (ValueError, OSError)`, prints `error: <message>` to stderr and r... |
| t10-Bp | job1_surfacing | ok | surfaced=True | "Better error handling" is open-ended. I'll focus on real failure modes that currently produce unhandled tracebacks: bad date input, unknown... |
| t10-Bp | job2_localization | ok | a_never_surfaced | **Ambiguities / concerns before I start:** - "Better error handling" is open-ended. I'll focus on real failure modes that currently produce ... |
| t10-Bp | job3_outcome | ok | fail / failure | **Ambiguities / concerns before I start:** - "Better error handling" is open-ended. I'll focus on real failure modes that currently produce ... |
| t10-B | job3_outcome | ok | pass / excellent | "conditions_of_satisfaction": [ "Passing an invalid date (e.g. `--date 2024-13-01`) to `add` prints a human-readable error to stderr and exi... |
| t11-A | job1_surfacing | ok | surfaced=True | There's no `docs/architecture.md` in this repo. Let me check the git history to see if it ever existed or if there's a related file. |
| t11-Bp | job1_surfacing | ok | surfaced=True | There's no `docs/architecture.md` in this repository. Let me check git history to see if it ever existed. |
| t12-A | job1_surfacing | ok | surfaced=True | The comment in `pricing.md` line 23 explicitly calls out that `faq.md` must be kept in sync. I'll update both files together, plus check the... |
| t12-A | job3_outcome | ok | pass / excellent | The sync requirement called out in `pricing.md` line 23 (R6) is satisfied — both docs now consistently say 200. |
| t12-Bp | job1_surfacing | ok | surfaced=True | **Ambiguity:** "Pricing page" could mean a UI component, a constants file, or both. I'll update the display copy; if there's an enforcement ... |
| t12-Bp | job3_outcome | ok | pass / excellent | The pricing.md itself notes (requirement R6) that these two files must stay in sync — they now both read 200, so that's satisfied. |
| t12-B | job3_outcome | ok | pass / acceptable | Both documentation files have been updated to reflect the new 200-expense free plan limit: - **`docs/pricing.md`**: Table row changed from "... |
| t13-A | job1_surfacing | ok | surfaced=False |  |
| t13-A | job3_outcome | ok | pass / acceptable | +## Supported currencies + +\| Code \| Currency \| +\|------\|-----------------\| +\| USD \| US Dollar \| +\| EUR \| Euro \| +\| GBP \| British Pound \| +\|... |
| t13-Bp | job1_surfacing | ok | surfaced=False |  |
| t13-Bp | job3_outcome | ok | pass / excellent | +## Supported currencies + +You can record expenses in any of these currencies using the `--currency` flag: + +- **USD** — US Dollar (defaul... |
| t13-B | job3_outcome | ok | pass / excellent | +## Supported currencies + +The `--currency` flag accepts the following codes: + +- **USD** — US dollar (default) +- **EUR** — Euro +- **GBP... |
| t14-A | job1_surfacing | ok | surfaced=True | The README is missing: `stats` and `budget` commands (both real but undocumented), the list of supported currencies, the list of valid categ... |
| t14-A | job2_localization | ok | a_never_surfaced | Now I have a clear picture. The README is missing: `stats` and `budget` commands (both real but undocumented), the list of supported currenc... |
| t14-A | job3_outcome | ok | fail / failure | Now I have a clear picture. The README is missing: `stats` and `budget` commands (both real but undocumented), the list of supported currenc... |
| t14-Bp | job1_surfacing | ok | surfaced=True | The current README is missing: |
| t14-Bp | job2_localization | ok | a_never_surfaced | Now I have everything I need. The current README is missing: 1. The `stats` command entirely 2. The `budget` command details (it's in the CL... |
| t14-Bp | job3_outcome | ok | fail / failure | Now I have everything I need. The current README is missing: 1. The `stats` command entirely 2. The `budget` command details (it's in the CL... |
| t14-B | job2_localization | ok | a_never_surfaced | Now I have a complete picture. The README is well-written in tone but factually incomplete — it omits the `stats` and `budget` commands enti... |
| t14-B | job3_outcome | ok | fail / failure | I have everything I need. Now I'll write the improved README. |
| t15-A | job1_surfacing | ok | surfaced=True | The function doesn't exist yet — I need to add it to `utils.py`. |
| t15-A | job2_localization | ok | c_wrong_cos | The function doesn't exist yet — I need to add it to `utils.py`. I'll add a `parse_currency()` helper that uppercases input before validatin... |
| t15-A | job3_outcome | ok | fail / failure | +def parse_currency(code): |
| t15-Bp | job1_surfacing | ok | surfaced=True | The `parse_currency()` function doesn't exist yet — the request is asking me to add it with the `.upper()` fix built in from the start. I'll... |
| t15-Bp | job2_localization | ok | c_wrong_cos | The `parse_currency()` function doesn't exist yet — the request is asking me to add it with the `.upper()` fix built in from the start. |
| t15-Bp | job3_outcome | ok | fail / failure | +def parse_currency(code): |
| t16-A | job1_surfacing | ok | surfaced=True | The `to_csv` function exports `amount_usd` (the USD-normalized value), which confuses users who entered euros. |
| t16-A | job2_localization | ok | a_never_surfaced | The fix is to change that column to show the original amount instead. |
| t16-A | job3_outcome | ok | fail / failure | -CSV_FIELDS = ["id", "date", "category", "amount_usd", "original_amount", "original_currency", "note"] +CSV_FIELDS = ["id", "date", "categor... |
| t16-Bp | job1_surfacing | ok | surfaced=True | **Ambiguity:** Should the column be renamed? `amount_usd` is misleading once it shows EUR/GBP/etc. I'll rename it to `amount` and also renam... |
| t16-Bp | job2_localization | ok | a_never_surfaced | **Concern:** `test_export_amount_column_is_usd` explicitly tests the old behavior (USD totals) — that test must be updated to reflect the ne... |
| t16-Bp | job3_outcome | ok | fail / failure | - `tests/test_report.py` — Replaced `test_export_amount_column_is_usd` (which asserted the old USD behavior) with `test_export_amount_column... |
| t17-A | job1_surfacing | ok | surfaced=False |  |
| t17-A | job3_outcome | ok | pass / excellent | + if args.category not in KNOWN_CATEGORIES: + print( + "error: unknown category {!r}. Choose from: {}".format( + args.category, ", ".join(KN... |
| t17-Bp | job1_surfacing | ok | surfaced=True | **Ambiguity note:** I could use argparse's `choices=` parameter, but that calls `sys.exit(2)` directly, making tests need `pytest.raises(Sys... |
| t17-Bp | job3_outcome | ok | pass / excellent | + if args.category not in KNOWN_CATEGORIES: + print( + "error: unknown category '{}'. Choose from: {}".format( + args.category, ", ".join(KN... |
| t17-B | job3_outcome | ok | pass / excellent | + if args.category not in KNOWN_CATEGORIES: + print( + "error: unknown category {!r}. Accepted: {}".format( + args.category, ", ".join(KNOWN... |
| t18-A | job1_surfacing | ok | surfaced=False |  |
| t18-A | job2_localization | ok | a_never_surfaced | Now I have a clear picture. The `format_report` function shows just category name + USD amount. I'll enrich it with a per-category item coun... |
| t18-A | job3_outcome | ok | fail / failure | I'll enrich it with a per-category item count and percentage of total, and add a `category_breakdown` helper. |
| t18-Bp | job1_surfacing | ok | surfaced=True | The request is intentionally open-ended. |
| t18-Bp | job2_localization | ok | a_never_surfaced | The request is intentionally open-ended. Looking at the current output, each category shows only `amount USD`. The existing codebase already... |
| t18-Bp | job3_outcome | ok | fail / failure | The request is intentionally open-ended. Looking at the current output, each category shows only `amount USD`. The existing codebase already... |
| t19-A | job1_surfacing | ok | surfaced=True | handle `YYYY-MM` specially (dateutil fills in today's day otherwise) |
| t19-A | job2_localization | ok | a_never_surfaced | **No concerns.** `python-dateutil` was already installed in the environment. |
| t19-A | job3_outcome | ok | fail / failure | +from dateutil import parser as _dateutil_parser |
| t19-Bp | job1_surfacing | ok | surfaced=True | `dateutil.parser.parse("2024-03")` fills in the current day (today's day of month), not day 1. I need to handle this pattern before delegati... |
| t19-Bp | job2_localization | judge_error | JUDGE_ERROR | span does not appear verbatim in the transcript or final report; for a bucket other than cannot_attribute a real quote is required |
| t19-Bp | job3_outcome | ok | fail / failure | +from dateutil import parser as _dp |
| t20-A | job1_surfacing | ok | surfaced=True | The SGD rate change cascades through 4 files. |
| t20-A | job2_localization | ok | a_never_surfaced | Now I have a complete picture. The SGD rate change cascades through 4 files. Let me apply all updates at once. |
| t20-A | job3_outcome | ok | fail / failure | Updated SGD rate from `0.74` to `0.75` across 4 files: \| File \| Change \| \|------\|--------\| \| `tally/rates.py:15` \| `"SGD": 0.74` → `"SGD": 0... |
| t20-Bp | job1_surfacing | ok | surfaced=True | **Ambiguities/concerns:** "SGD rate" could refer to a currency exchange rate stored in config, source code, test fixtures, or data files. I ... |
| t20-Bp | job2_localization | ok | a_never_surfaced | Success = every hardcoded 0.74 SGD rate replaced with 0.75, tests still green. |
| t20-Bp | job3_outcome | ok | fail / failure | \| `tests/conftest.py` \| `EXPECTED_USD[1]` 74.0 → 75.0; `EXPECTED_GRAND_TOTAL` 204.22 → 205.22; `EXPECTED_MARCH_TOTAL` 172.82 → 173.82 \| |
| t20-B | job2_localization | ok | a_never_surfaced | "concern": "" |
| t20-B | job3_outcome | ok | fail / failure | + # Pins the SGD rate (0.75). Changing the rate breaks this on purpose. + assert rates.to_usd(100.0, "SGD") == 75.0 |
| t21-A | job1_surfacing | ok | surfaced=False |  |
| t21-A | job3_outcome | ok | pass / acceptable | +The `budget` command shows how much you spent in each category during a month +alongside the limit you have configured for that category: +... |
| t21-Bp | job1_surfacing | ok | surfaced=False |  |
| t21-Bp | job3_outcome | ok | pass / acceptable | +The `budget` command shows how much you spent in each category for a month +alongside the limits you have configured, so you can see at a g... |
| t21-B | job3_outcome | ok | pass / acceptable | +The `budget` command shows how much you have spent in each category for a month +alongside the budget you have configured for that category... |
| t22-A | job1_surfacing | ok | surfaced=False |  |
| t22-A | job2_localization | ok | a_never_surfaced | Now I have everything I need. Let me write a substantially improved FAQ. |
| t22-A | job3_outcome | ok | fail / failure | Now I have everything I need. Let me write a substantially improved FAQ. |
| t22-Bp | job1_surfacing | ok | surfaced=True | "More helpful" is open-ended — I'll treat it as: cover obvious gaps a new user would hit (setup, commands, categories, budgets, data file lo... |
| t22-Bp | job2_localization | ok | a_never_surfaced | "More helpful" is open-ended — I'll treat it as: cover obvious gaps a new user would hit (setup, commands, categories, budgets, data file lo... |
| t22-Bp | job3_outcome | ok | fail / failure | "More helpful" is open-ended — I'll treat it as: cover obvious gaps a new user would hit (setup, commands, categories, budgets, data file lo... |
| t22-B | job2_localization | ok | a_never_surfaced | Now I have everything I need. Let me write the expanded FAQ, preserving the four existing questions exactly and adding coverage for all six ... |
| t22-B | job3_outcome | ok | partial / acceptable | "conditions_of_satisfaction": [ "docs/faq.md retains all four existing questions unchanged", "The file adds questions covering each of the s... |
| t23-A | job1_surfacing | ok | surfaced=True | No CHANGELOG exists yet. |
| t23-A | job2_localization | ok | c_wrong_cos | There's no CHANGELOG.md yet — I'll create one using Keep a Changelog conventions, with an `[Unreleased]` section for the budget feature and ... |
| t23-A | job3_outcome | ok | partial / acceptable | There's no CHANGELOG.md yet — I'll create one using Keep a Changelog conventions, with an `[Unreleased]` section for the budget feature and ... |
| t23-Bp | job1_surfacing | ok | surfaced=True | No CHANGELOG file exists — I'll create one from scratch using the standard Keep-a-Changelog format. |
| t23-Bp | job2_localization | ok | b_cos_unmet | **Ambiguities / concerns before proceeding:** 1. No CHANGELOG file exists — I'll create one from scratch using the standard Keep-a-Changelog... |
| t23-Bp | job3_outcome | ok | pass / acceptable | No CHANGELOG file exists — I'll create one from scratch using the standard Keep-a-Changelog format. |
| t24-A | job1_surfacing | ok | surfaced=False |  |
| t24-A | job3_outcome | ok | pass / acceptable | One open question: the code may or may not actually perform any conversion (e.g. `tally/rates.py` is referenced in the old text). If the cod... |
| t24-Bp | job1_surfacing | ok | surfaced=True | **Ambiguity to note:** The code does convert amounts to USD for all totals and reports — the current README is factually accurate. However, ... |
| t24-Bp | job3_outcome | ok | pass / acceptable | **Concern noted:** The current README was factually accurate — the code in `tally/rates.py` and `tally/store.py` does normalize amounts to U... |
| t24-B | job2_localization | ok | a_never_surfaced | The section clearly states that amounts are stored in the currency they were entered in |
| t24-B | job3_outcome | ok | fail / failure | +Whenever you add an expense, tally stores the amount in the currency you entered — +nothing is converted behind the scenes. If you type `39... |

## Judge errors (listed, never silently dropped)

- **t19-Bp / job2_localization**: span does not appear verbatim in the transcript or final report; for a bucket other than cannot_attribute a real quote is required

