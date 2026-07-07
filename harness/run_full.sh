#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# Speech Acts experiment -- Slice 5 full-run driver (rep1 -> rep2 -> rep3).
#
# Runs the WHOLE pipeline unattended and RESUMABLY:
#   for each rep:  run_episodes (harness)  ->  score_tier1  ->  judge  ->  incremental merge
# then a final pooled merge over rep1,rep2,rep3.
#
# INTEGRITY (spec 05):
#   * Every stage uses --resume, so re-running this script from the top NEVER re-runs a
#     completed episode or judge verdict. A death mid-run resumes exactly where it stopped.
#   * Re-runs happen for INFRASTRUCTURE failure ONLY (usage limit / network), detected via the
#     stages' own exit code 3, and backed off. A "weird" result is a result -- never re-run.
#   * Harness exit 2 (fixture/task/model drift) is FATAL: retrying can't fix a config mismatch.
#
# This script is idempotent and safe to launch again after any interruption.
# ---------------------------------------------------------------------------
set -uo pipefail

HARNESS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EXPERIMENT_DIR="$(dirname "$HARNESS_DIR")"
LOG="$EXPERIMENT_DIR/results/run_full.log"
PY=python3
REPS=(rep1 rep2 rep3)

mkdir -p "$EXPERIMENT_DIR/results"
cd "$HARNESS_DIR" || { echo "cannot cd to harness dir"; exit 40; }

ts()  { date "+%Y-%m-%d %H:%M:%S"; }
log() { echo "[$(ts)] $*" | tee -a "$LOG"; }

# Backoff schedule for infrastructure retries (seconds). Escalates, caps ~30 min.
backoff() {
  local try=$1
  case "$try" in
    1) echo 300 ;;
    2) echo 300 ;;
    3) echo 600 ;;
    4) echo 900 ;;
    *) echo 1800 ;;
  esac
}

MAX_INFRA_TRIES=12   # per stage; with the schedule above this spans several hours

# run_stage <human-label> <fatal-on-exit2:yes|no> <cmd...>
# Retries ONLY on exit 3 (infra) with backoff. Exit 0 => success. Exit 2 (if fatal) => abort.
run_stage() {
  local label="$1"; shift
  local fatal2="$1"; shift
  local try=1
  while : ; do
    log ">>> $label  (attempt $try)"
    set +e
    "$@" 2>&1 | tee -a "$LOG"
    local rc=${PIPESTATUS[0]}
    set -e 2>/dev/null || true
    if [ "$rc" -eq 0 ]; then
      log "<<< $label  OK"
      return 0
    fi
    if [ "$rc" -eq 2 ] && [ "$fatal2" = "yes" ]; then
      log "!!! $label  FATAL exit 2 (config/drift mismatch). Not retrying."
      return 2
    fi
    if [ "$rc" -eq 3 ]; then
      if [ "$try" -ge "$MAX_INFRA_TRIES" ]; then
        log "!!! $label  gave up after $try infra retries (exit 3). Surfacing for resume."
        return 3
      fi
      local wait; wait=$(backoff "$try")
      log "... $label  infra failure (exit 3). Backing off ${wait}s then --resume."
      sleep "$wait"
      try=$((try+1))
      continue
    fi
    # Unexpected non-zero: treat cautiously as infra, limited retries.
    if [ "$try" -ge 4 ]; then
      log "!!! $label  unexpected exit $rc after $try tries. Surfacing."
      return "$rc"
    fi
    log "... $label  unexpected exit $rc. Retrying in 120s (--resume)."
    sleep 120
    try=$((try+1))
  done
}

log "==================================================================="
log "FULL RUN START. reps=${REPS[*]}"
log "fixture HEAD: $(git -C "$EXPERIMENT_DIR/fixture" rev-parse HEAD)"
log "==================================================================="

DONE_REPS=()
for rep in "${REPS[@]}"; do
  log "########## REP: $rep ##########"

  run_stage "harness/$rep" yes "$PY" run_episodes.py --run "$rep" --resume
  rc=$?; [ "$rc" -ne 0 ] && { log "STOP: harness/$rep returned $rc"; exit "$rc"; }

  run_stage "tier1/$rep" no "$PY" score_tier1.py "$rep"
  rc=$?; [ "$rc" -ne 0 ] && { log "STOP: tier1/$rep returned $rc"; exit "$rc"; }

  run_stage "judge/$rep" no "$PY" judge.py --run "$rep" --resume
  rc=$?; [ "$rc" -ne 0 ] && { log "STOP: judge/$rep returned $rc"; exit "$rc"; }

  # Non-blocking spotcheck file for this rep (QA aid; gates nothing).
  "$PY" judge.py --spotcheck "$rep" 2>&1 | tee -a "$LOG" || true

  DONE_REPS+=("$rep")
  # Incremental pooled snapshot over reps completed so far.
  joined=$(IFS=,; echo "${DONE_REPS[*]}")
  run_stage "merge-snapshot[$joined]" no "$PY" results.py --runs "$joined" --date 260705
  log "########## REP $rep COMPLETE (snapshot over: $joined) ##########"
done

# Final pooled report over all three reps.
run_stage "final-merge" no "$PY" results.py --runs rep1,rep2,rep3 --date 260705
rc=$?; [ "$rc" -ne 0 ] && { log "STOP: final merge returned $rc"; exit "$rc"; }

log "==================================================================="
log "FULL RUN COMPLETE. All reps done, final report written."
log "==================================================================="
exit 0
