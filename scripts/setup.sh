#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# One-time environment setup for the speech-acts-experiment repo.
#
# Creates harness/venv (python3 -m venv) and installs harness/requirements.txt
# into it. Idempotent: safe to re-run; an existing venv is reused and pip
# install is a no-op when requirements are already satisfied.
# ---------------------------------------------------------------------------
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
VENV_DIR="$REPO_ROOT/harness/venv"
REQUIREMENTS="$REPO_ROOT/harness/requirements.txt"

if ! command -v python3 >/dev/null 2>&1; then
  echo "ERROR: python3 not found on PATH. Install Python 3.9+ and re-run." >&2
  exit 1
fi

if [ -x "$VENV_DIR/bin/python" ]; then
  echo "Reusing existing venv at $VENV_DIR"
else
  echo "Creating venv at $VENV_DIR"
  python3 -m venv "$VENV_DIR"
fi

echo "Installing requirements from $REQUIREMENTS"
"$VENV_DIR/bin/pip" install --quiet --upgrade pip
"$VENV_DIR/bin/pip" install --quiet -r "$REQUIREMENTS"

echo
echo "Setup complete."
echo "  venv:   $VENV_DIR"
echo "  pytest: $("$VENV_DIR/bin/pytest" --version)"
echo
echo "Next steps:"
echo "  1. Restore the fixture's git history:  scripts/restore_fixture.sh"
# Use `python -m pytest` (not the pytest console script): -m puts the cwd on
# sys.path so the fixture's `tally` package is importable, matching how the
# harness invokes the suite (run_episodes.py).
echo "  2. Sanity-check the fixture suite:     cd fixture && ../harness/venv/bin/python -m pytest -q"
