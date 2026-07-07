#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# Restore fixture/.git from bundles/fixture.bundle.
#
# The fixture is its own git repo (baseline commit e02cf35...); its .git dir
# was stripped for packaging and preserved as a git bundle. This script puts
# it back and verifies the checked-in fixture files byte-match the baseline.
#
# Idempotent: if fixture/.git already exists at the baseline commit with a
# clean status, prints OK and exits 0.
# ---------------------------------------------------------------------------
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
FIXTURE_DIR="$REPO_ROOT/fixture"
BUNDLE="$REPO_ROOT/bundles/fixture.bundle"
BASELINE_SHA="e02cf35200d8eb26fe4459c166c79f6787a71fab"

fail() {
  echo "ERROR: $*" >&2
  exit 1
}

[ -d "$FIXTURE_DIR" ] || fail "fixture directory not found: $FIXTURE_DIR"
[ -f "$BUNDLE" ]      || fail "bundle not found: $BUNDLE"

# --- Idempotency check: already restored and clean? -------------------------
if [ -e "$FIXTURE_DIR/.git" ]; then
  head_sha="$(git -C "$FIXTURE_DIR" rev-parse HEAD 2>/dev/null || echo '')"
  status_out="$(git -C "$FIXTURE_DIR" status --porcelain 2>/dev/null || echo 'STATUS-FAILED')"
  if [ "$head_sha" = "$BASELINE_SHA" ] && [ -z "$status_out" ]; then
    echo "OK: fixture/.git already restored (HEAD=$BASELINE_SHA, status clean). Nothing to do."
    exit 0
  fi
  fail "fixture/.git exists but is not at a clean baseline state.
  HEAD:   ${head_sha:-<unreadable>}   (expected $BASELINE_SHA)
  status: $(printf '%s' "$status_out" | head -5)
Remove or inspect fixture/.git manually before re-running."
fi

# --- Restore from bundle -----------------------------------------------------
TMP_DIR="$(mktemp -d)"
cleanup_tmp() { rm -rf "$TMP_DIR"; }
trap cleanup_tmp EXIT

echo "Cloning bundle (no checkout) ..."
git clone --quiet --no-checkout "$BUNDLE" "$TMP_DIR/fixture-clone"
mv "$TMP_DIR/fixture-clone/.git" "$FIXTURE_DIR/.git"

# The clone's index is empty (--no-checkout); reset it to HEAD so status
# compares the on-disk fixture files against the baseline tree.
git -C "$FIXTURE_DIR" reset --quiet

# --- Verify ------------------------------------------------------------------
head_sha="$(git -C "$FIXTURE_DIR" rev-parse HEAD 2>/dev/null || echo '')"
if [ "$head_sha" != "$BASELINE_SHA" ]; then
  rm -rf "$FIXTURE_DIR/.git"
  fail "restored HEAD is $head_sha, expected $BASELINE_SHA. Removed fixture/.git; state left clean."
fi

status_out="$(git -C "$FIXTURE_DIR" status --porcelain)"
if [ -n "$status_out" ]; then
  rm -rf "$FIXTURE_DIR/.git"
  fail "fixture files do not byte-match baseline $BASELINE_SHA. Differences:
$status_out
Removed fixture/.git; state left clean."
fi

echo "OK: fixture/.git restored from bundle."
echo "  HEAD:   $BASELINE_SHA"
echo "  status: clean (fixture files byte-match the baseline)"
