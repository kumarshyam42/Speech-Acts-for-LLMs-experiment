"""Date-parsing and money-rounding tests."""

import datetime

import pytest

from tally import utils


def test_parse_full_date():
    assert utils.parse_date("2024-03-04") == datetime.date(2024, 3, 4)


def test_parse_month_only():
    assert utils.parse_date("2024-03") == datetime.date(2024, 3, 1)


def test_parse_date_strips_whitespace():
    assert utils.parse_date("  2024-03-04 ") == datetime.date(2024, 3, 4)


def test_parse_bad_date_raises():
    with pytest.raises(ValueError):
        utils.parse_date("March 4th")


def test_month_key_from_date():
    assert utils.month_key(datetime.date(2024, 3, 4)) == "2024-03"


def test_round_money_half_up():
    # round_money rounds halves UP, unlike Python's built-in round() which
    # rounds to even. These cases differ between the two, so a naive swap to
    # bare round() would break here.
    assert utils.round_money(2.675) == 2.68
    assert utils.round_money(1.005) == 1.01
    assert utils.round_money(0.125) == 0.13


def test_round_money_leaves_clean_values():
    assert utils.round_money(10.0) == 10.0
    assert utils.round_money(3.14) == 3.14
