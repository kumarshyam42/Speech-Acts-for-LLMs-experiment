"""Currency conversion.

Every amount that enters the store is normalized to USD (see docs/requirements.md).
`RATES` maps a currency code to the number of USD one unit is worth. The rates are
treated as fixed constants: several tests pin totals computed from them.
"""

from tally.config import DEFAULT_CURRENCY

# 1 unit of <currency> is worth RATES[<currency>] USD.
RATES = {
    "USD": 1.0,
    "EUR": 1.08,
    "GBP": 1.27,
    "SGD": 0.74,
    "JPY": 0.0067,
    "INR": 0.012,
}


def supported_currencies():
    """Return the sorted list of currency codes we can convert."""
    return sorted(RATES.keys())


def to_usd(amount, currency):
    """Convert `amount` given in `currency` to USD.

    The currency code is matched case-insensitively. Unknown codes raise
    ValueError so a typo never silently produces a wrong number.
    """
    code = currency.upper()
    if code not in RATES:
        raise ValueError(
            "unsupported currency {!r}; known: {}".format(
                currency, ", ".join(supported_currencies())
            )
        )
    return round(amount * RATES[code], 2)


def normalize(amount, currency):
    """Normalize an amount in `currency` into USD, the stored representation."""
    return to_usd(amount, currency)


def is_default_currency(currency):
    return currency.upper() == DEFAULT_CURRENCY
