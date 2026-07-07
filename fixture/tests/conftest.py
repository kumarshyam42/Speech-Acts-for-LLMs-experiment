"""Shared pytest fixtures for the tally suite."""

import pytest

from tally import store as store_mod


# Amounts here are what a user would type (original currency); add_expense
# normalizes each into USD when it builds the record.
SAMPLE_ROWS = [
    # date,        amount, currency, category,        note
    ("2024-03-04", 39.0, "EUR", "food", "groceries"),
    ("2024-03-01", 100.0, "SGD", "rent", "room share"),
    ("2024-03-15", 50.0, "USD", "food", "dinner"),
    ("2024-04-02", 20.0, "GBP", "transport", "train"),
    ("2024-03-20", 1000.0, "JPY", "entertainment", "concert"),
    ("2024-04-10", 500.0, "INR", "other", "gift"),
]

# Expected USD values for the rows above, under the shipped RATES table.
EXPECTED_USD = [42.12, 74.0, 50.0, 25.4, 6.7, 6.0]
EXPECTED_GRAND_TOTAL = 204.22
EXPECTED_MARCH_TOTAL = 172.82  # rows 0,1,2,4
EXPECTED_MARCH_FOOD = 92.12  # rows 0,2


@pytest.fixture
def sample_store():
    data = store_mod.empty_store()
    for date, amount, currency, category, note in SAMPLE_ROWS:
        store_mod.add_expense(
            data,
            date=date,
            amount=amount,
            currency=currency,
            category=category,
            note=note,
        )
    return data
