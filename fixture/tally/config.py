"""Configuration defaults for tally.

These values are intentionally kept in one place so behaviour is easy to reason
about. Several tests pin specific values here, so changing a constant may have
consequences elsewhere.
"""

# The currency every stored amount is normalized into. Do not confuse this with
# the currency a user may type at the command line; that one gets converted.
DEFAULT_CURRENCY = "USD"

# Store schema version. Bump this (and add a migration in store.migrate) whenever
# the on-disk shape of an expense record changes.
SCHEMA_VERSION = 2

# Categories a user is allowed to file an expense under.
KNOWN_CATEGORIES = ["food", "transport", "rent", "entertainment", "other"]

# Monthly budgets per category, in USD.
CATEGORY_BUDGETS = {
    "food": 600.0,
    "transport": 200.0,
    "rent": 1500.0,
    "entertainment": 150.0,
    "other": 300.0,
}

# Fraction of a category budget at which the budget report starts warning.
BUDGET_WARN_RATIO = 0.8
