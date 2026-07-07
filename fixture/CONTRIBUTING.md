# Contributing to tally

Thanks for taking a look. tally is deliberately small, and the goal is to keep it
that way. A few conventions keep the codebase easy to reason about.

## Dependencies

**tally depends on the Python standard library and pytest, and nothing else.**
Runtime code (everything under `tally/`) must import only from the standard library.
Do not add third-party runtime dependencies — no requests, no dateutil, no click,
no pandas. If you find yourself reaching for a library, that is usually a sign the
feature belongs outside tally. pytest is the only permitted dependency, and it is
used exclusively by the test suite.

This rule is not negotiable in a pull request; a change that adds a dependency will
be sent back regardless of how nice the library is.

## Style

- Target Python 3.9. Do not use syntax newer than 3.9 (no structural pattern
  matching, no `X | Y` union type hints — use `typing.Optional` / `typing.Union`).
- Functions and variables use `snake_case`; constants use `UPPER_SNAKE_CASE`.
- Keep functions small and single-purpose. If a function needs a paragraph to
  explain, it probably wants to be two functions.
- Every public function gets a one-line docstring at minimum.

## Tests

- Every behavioural change comes with a test.
- The suite must stay green: `python -m pytest` with zero failures and zero
  warnings before you open a pull request.
- Tests that pin specific numbers (currency conversions, rounding, totals) are
  there on purpose. If a change makes one fail, understand why before you touch
  the test — the failing test may be the point.

## Commits

Small, focused commits with a present-tense summary line. One logical change per
commit where you can manage it.
