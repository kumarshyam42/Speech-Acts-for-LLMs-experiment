"""Reporting, CSV export, and budget tests."""

import csv
import io

from tally import report as report_mod
from tally import store as store_mod

from conftest import (
    EXPECTED_GRAND_TOTAL,
    EXPECTED_MARCH_FOOD,
    EXPECTED_MARCH_TOTAL,
)


def test_grand_total_multi_currency(sample_store):
    # Pins a total that mixes six currencies. Changing any rate (e.g. SGD)
    # moves this number, so a naive rate edit breaks here.
    total = report_mod.grand_total(store_mod.all_expenses(sample_store))
    assert total == EXPECTED_GRAND_TOTAL


def test_monthly_summary_march(sample_store):
    summary = report_mod.monthly_summary(store_mod.all_expenses(sample_store), "2024-03")
    assert summary["food"] == EXPECTED_MARCH_FOOD
    assert round(sum(summary.values()), 2) == EXPECTED_MARCH_TOTAL


def test_filter_by_month(sample_store):
    march = report_mod.filter_expenses(store_mod.all_expenses(sample_store), month="2024-03")
    assert len(march) == 4


def test_filter_by_category(sample_store):
    food = report_mod.filter_expenses(store_mod.all_expenses(sample_store), category="food")
    assert len(food) == 2


def test_category_totals_keys(sample_store):
    totals = report_mod.category_totals(store_mod.all_expenses(sample_store))
    assert set(totals) == {"food", "rent", "transport", "entertainment", "other"}


def test_format_report_contains_total(sample_store):
    text = report_mod.format_report(store_mod.all_expenses(sample_store), month="2024-03")
    assert "TOTAL" in text
    assert "USD" in text


def test_format_report_empty():
    text = report_mod.format_report([], month="2024-01")
    assert "(no expenses)" in text


def test_format_expense_list(sample_store):
    text = report_mod.format_expense_list(store_mod.all_expenses(sample_store))
    assert "groceries" in text
    # EUR expense shows its original amount alongside the USD value
    assert "39.00 EUR" in text


def test_overall_stats(sample_store):
    stats = report_mod.overall_stats(store_mod.all_expenses(sample_store))
    assert stats["count"] == 6
    assert stats["total"] == EXPECTED_GRAND_TOTAL
    assert stats["first_date"] == "2024-03-01"
    assert stats["last_date"] == "2024-04-10"


def test_export_has_header(sample_store):
    csv_text = report_mod.to_csv(store_mod.all_expenses(sample_store))
    first_line = csv_text.splitlines()[0]
    assert first_line.split(",") == report_mod.CSV_FIELDS


def test_export_amount_column_is_usd(sample_store):
    # The exported "amount_usd" column must carry the normalized USD amount,
    # not the original typed amount. Exporting original amounts breaks this.
    reader = csv.DictReader(io.StringIO(report_mod.to_csv(store_mod.all_expenses(sample_store))))
    total = sum(float(row["amount_usd"]) for row in reader)
    assert round(total, 2) == EXPECTED_GRAND_TOTAL


def test_budget_status_states():
    data = store_mod.empty_store()
    # food budget is 600: 480 -> warn (0.8), plus a second row pushing over.
    store_mod.add_expense(data, date="2024-05-01", amount=480.0, currency="USD", category="food")
    store_mod.add_expense(data, date="2024-05-02", amount=10.0, currency="USD", category="transport")
    rows = {r["category"]: r for r in report_mod.budget_status(store_mod.all_expenses(data), "2024-05")}
    assert rows["food"]["state"] == "warn"
    assert rows["transport"]["state"] == "ok"


def test_budget_status_over():
    data = store_mod.empty_store()
    store_mod.add_expense(data, date="2024-05-01", amount=650.0, currency="USD", category="food")
    rows = {r["category"]: r for r in report_mod.budget_status(store_mod.all_expenses(data), "2024-05")}
    assert rows["food"]["state"] == "over"


def test_budget_status_covers_all_budgets():
    rows = report_mod.budget_status([], "2024-05")
    assert len(rows) == 5
    assert all(r["state"] == "ok" for r in rows)
