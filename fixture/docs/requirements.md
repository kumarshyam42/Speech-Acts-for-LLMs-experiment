# tally — Product Requirements

This document records the behaviour tally is expected to have. It is the reference
of record: where the code, the README, or the marketing copy disagree with this
document, this document wins until it is deliberately changed.

## R1 — Single-file store

All data lives in one JSON file. There is no database and no network access. The
store file records a schema version so older files can be migrated forward.

## R2 — Amounts are normalized to US dollars at write time

Every expense amount is converted to US dollars **when it is recorded**, using the
conversion table in `tally/rates.py`, and the US-dollar figure is what gets stored.
The original amount and currency the user entered are retained for reference only;
they are never used to compute a total.

The consequence, which is intentional: every total, summary, budget comparison, and
export is denominated in US dollars. tally does not re-convert into another currency
at report time. A report that mixed stored dollars with re-converted originals would
double-count the conversion and is a defect.

## R3 — Conversion rates are fixed constants

The rates in `tally/rates.py` are treated as fixed. Several tests pin totals that
are computed from them. Changing a rate is allowed, but it is a deliberate act: the
pinned expectations must be updated in the same change, and the change should be
called out because it alters every historical total that used that currency.

## R4 — Categories

Expenses are filed under a category. The set of known categories and their monthly
budgets live in `tally/config.py`.

## R5 — Reporting

tally reports category totals for a month, can filter to a single category, can list
individual expenses, and can export the full set to CSV. The CSV export is
denominated in US dollars, consistent with R2.

## R6 — Documentation consistency

The customer-facing documents must not contradict each other on published limits.
In particular, `docs/pricing.md` and `docs/faq.md` both state the free-tier expense
limit, and **the two must always agree**. A change to a published limit in one file
is incomplete until the other file is updated to match.
