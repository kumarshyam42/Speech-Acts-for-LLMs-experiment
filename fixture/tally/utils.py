"""Small helpers: date parsing and money rounding."""

import datetime
from typing import Union

Dateish = Union[str, datetime.date]


def parse_date(text):
    """Parse a date written as YYYY-MM-DD or YYYY-MM.

    A bare YYYY-MM is treated as the first day of that month. Raises ValueError
    on anything else.
    """
    text = text.strip()
    for fmt in ("%Y-%m-%d", "%Y-%m"):
        try:
            return datetime.datetime.strptime(text, fmt).date()
        except ValueError:
            continue
    raise ValueError("unrecognized date {!r}; use YYYY-MM-DD or YYYY-MM".format(text))


def month_key(d):
    """Return the YYYY-MM string for a date."""
    if isinstance(d, str):
        d = parse_date(d)
    return "{:04d}-{:02d}".format(d.year, d.month)


def round_money(amount):
    """Round a money amount to 2 decimal places, rounding halves up.

    Python's built-in round() rounds halves to even, which surprises people who
    expect 2.675 -> 2.68. The small nudge below makes the behaviour half-up so
    reported totals match what a hand calculator would show.
    """
    return round(amount + 1e-9, 2)
