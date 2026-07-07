"""End-to-end CLI tests driving main() with an isolated store file."""

import json
import os

from tally import cli


def _store_path(tmp_path):
    return os.path.join(str(tmp_path), "tally.json")


def test_add_then_report(tmp_path, capsys):
    store = _store_path(tmp_path)
    rc = cli.main(["--store", store, "add", "39", "food", "--currency", "EUR", "--date", "2024-03-04"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "42.12 USD" in out

    rc = cli.main(["--store", store, "report", "--month", "2024-03"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "food" in out and "42.12" in out


def test_add_persists_normalized_amount(tmp_path, capsys):
    store = _store_path(tmp_path)
    cli.main(["--store", store, "add", "100", "rent", "--currency", "SGD", "--date", "2024-03-01"])
    with open(store) as fh:
        data = json.load(fh)
    assert data["expenses"][0]["amount_usd"] == 74.0


def test_report_category_filter(tmp_path, capsys):
    store = _store_path(tmp_path)
    cli.main(["--store", store, "add", "50", "food", "--date", "2024-03-15"])
    cli.main(["--store", store, "add", "30", "transport", "--date", "2024-03-16"])
    capsys.readouterr()
    cli.main(["--store", store, "report", "--month", "2024-03", "--category", "food"])
    out = capsys.readouterr().out
    assert "food" in out
    assert "transport" not in out


def test_export_to_file(tmp_path, capsys):
    store = _store_path(tmp_path)
    cli.main(["--store", store, "add", "50", "food", "--date", "2024-03-15"])
    capsys.readouterr()
    out_path = os.path.join(str(tmp_path), "out.csv")
    rc = cli.main(["--store", store, "export", "--out", out_path])
    assert rc == 0
    with open(out_path) as fh:
        content = fh.read()
    assert "amount_usd" in content.splitlines()[0]


def test_budget_command(tmp_path, capsys):
    store = _store_path(tmp_path)
    cli.main(["--store", store, "add", "650", "food", "--date", "2024-05-01"])
    capsys.readouterr()
    rc = cli.main(["--store", store, "budget", "--month", "2024-05"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "food" in out and "over" in out


def test_list_command(tmp_path, capsys):
    store = _store_path(tmp_path)
    cli.main(["--store", store, "add", "50", "food", "--date", "2024-03-15", "--note", "dinner"])
    capsys.readouterr()
    rc = cli.main(["--store", store, "list", "--month", "2024-03"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "dinner" in out and "food" in out


def test_no_command_prints_help(capsys):
    rc = cli.main([])
    assert rc == 1
    out = capsys.readouterr().out
    assert "usage" in out.lower()


def test_add_defaults_currency_to_usd(tmp_path, capsys):
    store = _store_path(tmp_path)
    cli.main(["--store", store, "add", "12.5", "other", "--date", "2024-06-01"])
    with open(store) as fh:
        data = json.load(fh)
    assert data["expenses"][0]["original_currency"] == "USD"
    assert data["expenses"][0]["amount_usd"] == 12.5
