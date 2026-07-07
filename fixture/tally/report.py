"""Reporting: monthly summaries, category totals, CSV export, budget checks.

Every number a report emits is in USD, because that is how amounts are stored
(see docs/requirements.md). Reports never re-convert into another currency.
"""

import csv
import io
from typing import Dict, List, Optional

from tally.config import BUDGET_WARN_RATIO, CATEGORY_BUDGETS
from tally.utils import month_key, round_money

CSV_FIELDS = ["id", "date", "category", "amount_usd", "original_amount", "original_currency", "note"]


def filter_expenses(expenses, month=None, category=None):
    """Return the expenses matching an optional month (YYYY-MM) and category."""
    result = []
    for exp in expenses:
        if month is not None and month_key(exp["date"]) != month:
            continue
        if category is not None and exp["category"] != category:
            continue
        result.append(exp)
    return result


def category_totals(expenses):
    """Return {category: total_usd} over the given expenses."""
    totals = {}
    for exp in expenses:
        cat = exp["category"]
        totals[cat] = round_money(totals.get(cat, 0.0) + exp["amount_usd"])
    return totals


def grand_total(expenses):
    """Return the total USD across the given expenses."""
    return round_money(sum(exp["amount_usd"] for exp in expenses))


def monthly_summary(expenses, month):
    """Return category totals (USD) for a single month."""
    return category_totals(filter_expenses(expenses, month=month))


def format_report(expenses, month=None, category=None):
    """Render a plain-text report of category totals to a string."""
    selected = filter_expenses(expenses, month=month, category=category)
    totals = category_totals(selected)
    lines = []
    header = "Report"
    if month:
        header += " for {}".format(month)
    if category:
        header += " (category: {})".format(category)
    lines.append(header)
    lines.append("-" * len(header))
    if not totals:
        lines.append("(no expenses)")
    else:
        for cat in sorted(totals):
            lines.append("{:<14} {:>10.2f} USD".format(cat, totals[cat]))
        lines.append("{:<14} {:>10.2f} USD".format("TOTAL", grand_total(selected)))
    return "\n".join(lines)


def format_expense_list(expenses):
    """Render individual expenses as an aligned plain-text table.

    Unlike the category report, this lists each expense on its own row. Amounts
    are shown in USD (the stored representation) with the original amount and
    currency in parentheses when they differ from USD.
    """
    if not expenses:
        return "(no expenses)"
    lines = ["{:>4}  {:<10}  {:<13}  {:>10}  {}".format("id", "date", "category", "usd", "note")]
    for exp in sorted(expenses, key=lambda e: (e["date"], e["id"])):
        origin = ""
        if exp.get("original_currency", "USD") != "USD":
            origin = "  ({:.2f} {})".format(exp["original_amount"], exp["original_currency"])
        lines.append(
            "{:>4}  {:<10}  {:<13}  {:>10.2f}  {}{}".format(
                exp["id"], exp["date"], exp["category"], exp["amount_usd"], exp.get("note", ""), origin
            )
        )
    return "\n".join(lines)


def to_csv(expenses):
    """Serialize expenses to CSV text. The amount column is amount_usd."""
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=CSV_FIELDS)
    writer.writeheader()
    for exp in expenses:
        row = {field: exp.get(field, "") for field in CSV_FIELDS}
        writer.writerow(row)
    return buffer.getvalue()


def overall_stats(expenses):
    """Return summary statistics (all USD) across the given expenses.

    Keys: count, total, average, first_date, last_date. Empty input yields
    zeros and None dates rather than raising.
    """
    if not expenses:
        return {"count": 0, "total": 0.0, "average": 0.0, "first_date": None, "last_date": None}
    dates = sorted(exp["date"] for exp in expenses)
    total = grand_total(expenses)
    return {
        "count": len(expenses),
        "total": total,
        "average": round_money(total / len(expenses)),
        "first_date": dates[0],
        "last_date": dates[-1],
    }


def budget_status(expenses, month):
    """Compare a month's category spending against CATEGORY_BUDGETS.

    Returns a list of dicts, one per budgeted category:
        {category, spent, budget, ratio, state}
    where state is "ok", "warn" (>= BUDGET_WARN_RATIO) or "over" (> budget).
    """
    spent = monthly_summary(expenses, month)
    rows = []
    for cat in sorted(CATEGORY_BUDGETS):
        budget = CATEGORY_BUDGETS[cat]
        used = spent.get(cat, 0.0)
        ratio = (used / budget) if budget else 0.0
        if used > budget:
            state = "over"
        elif ratio >= BUDGET_WARN_RATIO:
            state = "warn"
        else:
            state = "ok"
        rows.append(
            {
                "category": cat,
                "spent": round_money(used),
                "budget": budget,
                "ratio": ratio,
                "state": state,
            }
        )
    return rows
