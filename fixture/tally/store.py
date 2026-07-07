"""On-disk persistence for expenses.

The store is a single JSON file: {"schema_version": N, "expenses": [ ... ]}.

Each expense record looks like:
    {
      "id": 1,
      "date": "2024-03-04",
      "amount_usd": 42.31,          # normalized to USD at write time
      "original_amount": 39.0,      # what the user actually typed
      "original_currency": "EUR",
      "category": "food",
      "note": "groceries"
    }
"""

import json
import os
from typing import Dict, List, Optional

from tally.config import SCHEMA_VERSION
from tally.rates import normalize


def empty_store():
    return {"schema_version": SCHEMA_VERSION, "expenses": []}


def migrate(data):
    """Bring an older on-disk store up to the current schema version.

    v1 records stored a single "amount" field already in USD and a "currency"
    field naming the original currency. v2 splits that into amount_usd plus the
    original amount/currency pair.
    """
    version = data.get("schema_version", 1)
    if version == 1:
        for exp in data.get("expenses", []):
            if "amount_usd" not in exp and "amount" in exp:
                exp["amount_usd"] = exp.pop("amount")
            exp.setdefault("original_amount", exp.get("amount_usd"))
            exp.setdefault("original_currency", exp.pop("currency", "USD"))
        version = 2
    data["schema_version"] = SCHEMA_VERSION
    return data


def load(path):
    """Load the store at `path`, or return an empty store if it does not exist."""
    if not os.path.exists(path):
        return empty_store()
    with open(path, "r") as fh:
        data = json.load(fh)
    return migrate(data)


def save(path, data):
    """Write the store to `path` (pretty-printed, stable key order)."""
    directory = os.path.dirname(path)
    if directory and not os.path.isdir(directory):
        os.makedirs(directory)
    with open(path, "w") as fh:
        json.dump(data, fh, indent=2, sort_keys=True)
        fh.write("\n")


def next_id(data):
    ids = [exp.get("id", 0) for exp in data["expenses"]]
    if not ids:
        return 1
    return max(ids) + 1


def add_expense(data, date, amount, currency, category, note=""):
    """Append a new expense and return the created record.

    `amount`/`currency` are what the user supplied; the amount is normalized to
    USD before it is stored. `data` is mutated in place.
    """
    amount_usd = normalize(amount, currency)
    record = {
        "id": next_id(data),
        "date": date,
        "amount_usd": amount_usd,
        "original_amount": amount,
        "original_currency": currency.upper(),
        "category": category,
        "note": note,
    }
    data["expenses"].append(record)
    return record


def find_expense(data, expense_id):
    for exp in data["expenses"]:
        if exp.get("id") == expense_id:
            return exp
    return None


def all_expenses(data):
    return list(data["expenses"])
