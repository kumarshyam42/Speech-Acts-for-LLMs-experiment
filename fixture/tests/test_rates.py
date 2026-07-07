"""Currency conversion tests. Some pin exact USD values from the rate table."""

import pytest

from tally import rates


def test_usd_is_identity():
    assert rates.to_usd(100.0, "USD") == 100.0


def test_to_usd_eur():
    assert rates.to_usd(39.0, "EUR") == 42.12


def test_to_usd_sgd():
    # Pins the SGD rate (0.74). Changing the rate breaks this on purpose.
    assert rates.to_usd(100.0, "SGD") == 74.0


def test_to_usd_gbp():
    assert rates.to_usd(20.0, "GBP") == 25.4


def test_currency_code_is_case_insensitive():
    assert rates.to_usd(10.0, "eur") == rates.to_usd(10.0, "EUR")


def test_unknown_currency_raises():
    with pytest.raises(ValueError):
        rates.to_usd(10.0, "XYZ")


def test_supported_currencies_sorted():
    codes = rates.supported_currencies()
    assert codes == sorted(codes)
    assert "USD" in codes


