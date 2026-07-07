"""Persistence and normalization tests."""

import json
import os

from tally import store as store_mod

from conftest import EXPECTED_USD


def test_empty_store_shape():
    data = store_mod.empty_store()
    assert data["schema_version"] == 2
    assert data["expenses"] == []


def test_add_normalizes_to_usd():
    # The store keeps amount_usd, not the currency the user typed. This is the
    # load-bearing normalization rule (docs/requirements.md).
    data = store_mod.empty_store()
    record = store_mod.add_expense(
        data, date="2024-03-04", amount=39.0, currency="EUR", category="food"
    )
    assert record["amount_usd"] == 42.12
    assert record["original_amount"] == 39.0
    assert record["original_currency"] == "EUR"


def test_add_assigns_incrementing_ids(sample_store):
    ids = [exp["id"] for exp in sample_store["expenses"]]
    assert ids == [1, 2, 3, 4, 5, 6]


def test_stored_amounts_match_expected_usd(sample_store):
    got = [exp["amount_usd"] for exp in sample_store["expenses"]]
    assert got == EXPECTED_USD


def test_find_expense(sample_store):
    exp = store_mod.find_expense(sample_store, 3)
    assert exp is not None and exp["category"] == "food"
    assert store_mod.find_expense(sample_store, 999) is None


def test_next_id_on_empty():
    assert store_mod.next_id(store_mod.empty_store()) == 1


def test_save_and_load_roundtrip(tmp_path, sample_store):
    path = os.path.join(str(tmp_path), "sub", "tally.json")
    store_mod.save(path, sample_store)
    assert os.path.exists(path)
    loaded = store_mod.load(path)
    assert loaded["expenses"] == sample_store["expenses"]


def test_load_missing_file_returns_empty(tmp_path):
    path = os.path.join(str(tmp_path), "nope.json")
    assert store_mod.load(path)["expenses"] == []


def test_migrate_v1_to_v2(tmp_path):
    legacy = {
        "schema_version": 1,
        "expenses": [
            {"id": 1, "date": "2023-01-01", "amount": 12.5, "currency": "EUR",
             "category": "food", "note": ""}
        ],
    }
    path = os.path.join(str(tmp_path), "legacy.json")
    with open(path, "w") as fh:
        json.dump(legacy, fh)
    data = store_mod.load(path)
    assert data["schema_version"] == 2
    exp = data["expenses"][0]
    assert exp["amount_usd"] == 12.5
    assert exp["original_currency"] == "EUR"
    assert "amount" not in exp
