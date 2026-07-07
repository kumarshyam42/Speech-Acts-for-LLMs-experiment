#!/usr/bin/env python3
"""
Speech Acts experiment — episode harness (Slice 2).

Runs one headless `claude -p` episode per (task, condition) in a fresh git worktree of the
fixture, archives the full transcript + diff + pytest result + a validated manifest, and is
resumable. Stdlib only; Python 3.9 compatible.

See spec/02-harness.md for the contract. This driver never reads rubrics/ (invariant 1).
Worktrees live OUTSIDE the experiment tree (WORKTREE_ROOT) so a subject agent cannot traverse
up into tasks/, rubrics/, spec/, or harness/.

Usage:
    python run_episodes.py --run debug --tasks t03,t14,t21,t04
    python run_episodes.py --run rep1
    python run_episodes.py --run rep1 --resume
"""

import argparse
import datetime
import hashlib
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import threading
import time

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
MODEL = "claude-sonnet-4-6"
MAX_TURNS = 50            # enforced client-side (see NOTE below)
TIMEOUT_S = 900           # 15-minute wall-clock cap per agent call (D14)
PYTEST_TIMEOUT_S = 120    # cap for the post-episode pytest check
CONDITIONS = ["A", "Bp", "B"]

HERE = os.path.dirname(os.path.abspath(__file__))
EXPERIMENT = os.path.dirname(HERE)
FIXTURE_PATH = os.path.join(EXPERIMENT, "fixture")
TASKS_DIR = os.path.join(EXPERIMENT, "tasks")
PROMPTS_DIR = os.path.join(HERE, "prompts")
RUNS_DIR = os.path.join(EXPERIMENT, "runs")
VENV_PY = os.path.join(HERE, "venv", "bin", "python")

# Episode workspaces must NOT live under the experiment tree: an agent with filesystem access
# could otherwise traverse .. and read tasks/, rubrics/, spec/, or harness/ (invariant 1).
WORKTREE_ROOT = os.path.expanduser("~/.cache/speech-acts-worktrees")

# NOTE (divergence, logged in spec/decisions-log.md): CLI 2.1.193 has no `--max-turns` flag
# (only `--max-budget-usd`). The turn cap is therefore enforced client-side by counting
# `assistant` events in the stream and killing the process group if the count exceeds
# MAX_TURNS. The 15-minute wall-clock timeout is enforced by a watchdog thread.

ALL_TASKS = ["t%02d" % i for i in range(1, 25)]

# The currently-running claude subprocess (sequential driver — at most one at a time).
# Used by the SIGINT/SIGTERM handlers to clean up the child process group before exit.
_ACTIVE = {"proc": None}

# Abort the whole run after this many consecutive CLI-level errors (rate limit, auth,
# network): plowing on would burn every remaining episode against a dead API.
MAX_CONSECUTIVE_CLI_ERRORS = 3


class CLIError(Exception):
    """Infrastructure-level failure of a `claude -p` call (rate limit, auth, network,
    overload). NEVER episode data — the episode is voided (error.json, no manifest.json)
    and re-run on --resume. Distinct from cap hits, which are recorded outcomes (D14)."""
    pass


def check_cli_error(res, phase):
    """Mechanical CLI-error detection on a phase result. Uses the stream-json result event's
    is_error / api_error_status fields plus structural signals (missing result event, zero
    output tokens) — never error-message text, which is brittle. Cap hits are exempt (D14:
    our own kill legitimately truncates the stream)."""
    if res["cap_hit"]:
        return
    if res["is_error"]:
        raise CLIError(
            "phase %s: CLI error result (api_error_status=%s): %r"
            % (phase, res["api_error_status"], (res["result_text"] or "")[:160])
        )
    if not res["has_result_event"]:
        raise CLIError(
            "phase %s: no result event in stream (returncode=%s)"
            % (phase, res["returncode"])
        )
    if res["tokens_out"] == 0:
        raise CLIError(
            "phase %s: zero output tokens (api_error_status=%s)"
            % (phase, res["api_error_status"])
        )


# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------
def now_iso():
    return datetime.datetime.now().astimezone().isoformat()


def sha256_text(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def run_git(args, cwd=None, check=True):
    res = subprocess.run(
        ["git"] + args, cwd=cwd, capture_output=True, text=True
    )
    if check and res.returncode != 0:
        raise RuntimeError(
            "git %s failed (%d): %s" % (" ".join(args), res.returncode, res.stderr.strip())
        )
    return res


def cli_version():
    try:
        return subprocess.run(
            ["claude", "--version"], capture_output=True, text=True
        ).stdout.strip()
    except Exception:
        return "unknown"


def read_template(name):
    with open(os.path.join(PROMPTS_DIR, name), "r", encoding="utf-8") as f:
        return f.read()


def read_task(task_id):
    with open(os.path.join(TASKS_DIR, task_id + ".md"), "r", encoding="utf-8") as f:
        return f.read().strip()


def write_text(path, text):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


# ---------------------------------------------------------------------------
# claude -p invocation with streaming capture + watchdog
# ---------------------------------------------------------------------------
def invoke_claude(prompt_text, workspace, transcript_path):
    """
    Run one headless `claude -p` call.

    Streams stream-json stdout to `transcript_path` (one JSON object per line), enforces the
    wall-clock timeout via a watchdog thread and the turn cap by counting assistant events.
    The child runs in its own session (process group) so kills reap grandchildren too.

    Returns a dict:
        {result_text, num_turns, tokens_in, tokens_out, total_cost_usd, stop_reason,
         is_error, cap_hit, wall_s, returncode}
    cap_hit is one of None / "timeout" / "turns".
    """
    cmd = [
        "claude", "-p", prompt_text,
        "--model", MODEL,
        "--output-format", "stream-json",
        "--verbose",
        "--dangerously-skip-permissions",
    ]

    start = time.time()
    proc = subprocess.Popen(
        cmd,
        cwd=workspace,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
        start_new_session=True,   # own process group: killable with all descendants
    )
    _ACTIVE["proc"] = proc

    state = {"cap_hit": None}

    def watchdog():
        # Wall-clock guard: kill if the call runs past TIMEOUT_S.
        deadline = start + TIMEOUT_S
        while proc.poll() is None:
            if time.time() >= deadline:
                state["cap_hit"] = state["cap_hit"] or "timeout"
                kill_group(proc)
                return
            time.sleep(1.0)

    wd = threading.Thread(target=watchdog, daemon=True)
    wd.start()

    assistant_turns = 0
    result_event = None
    try:
        with open(transcript_path, "w", encoding="utf-8") as tf:
            for line in proc.stdout:
                tf.write(line)
                tf.flush()
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue
                etype = obj.get("type")
                if etype == "assistant":
                    assistant_turns += 1
                    if assistant_turns > MAX_TURNS:
                        state["cap_hit"] = state["cap_hit"] or "turns"
                        kill_group(proc)
                        break
                elif etype == "result":
                    result_event = obj
        proc.wait()
    finally:
        _ACTIVE["proc"] = None
    wall_s = round(time.time() - start, 2)

    out = {
        "result_text": "",
        "num_turns": assistant_turns,
        "tokens_in": 0,
        "tokens_out": 0,
        "total_cost_usd": 0.0,
        "stop_reason": None,
        "is_error": False,
        "api_error_status": None,
        "has_result_event": result_event is not None,
        "cap_hit": state["cap_hit"],
        "wall_s": wall_s,
        "returncode": proc.returncode,
    }
    if result_event is not None:
        usage = result_event.get("usage") or {}
        out["result_text"] = result_event.get("result") or ""
        out["num_turns"] = result_event.get("num_turns", assistant_turns)
        out["tokens_in"] = (
            (usage.get("input_tokens") or 0)
            + (usage.get("cache_read_input_tokens") or 0)
            + (usage.get("cache_creation_input_tokens") or 0)
        )
        out["tokens_out"] = usage.get("output_tokens") or 0
        out["total_cost_usd"] = result_event.get("total_cost_usd") or 0.0
        out["stop_reason"] = result_event.get("stop_reason")
        out["is_error"] = bool(result_event.get("is_error"))
        out["api_error_status"] = result_event.get("api_error_status")
    return out


def kill_group(proc):
    """Terminate the child's entire process group (TERM, then KILL)."""
    try:
        pgid = os.getpgid(proc.pid)
    except (ProcessLookupError, OSError):
        return
    try:
        os.killpg(pgid, signal.SIGTERM)
    except (ProcessLookupError, OSError):
        return
    for _ in range(50):
        if proc.poll() is not None:
            return
        time.sleep(0.1)
    try:
        os.killpg(pgid, signal.SIGKILL)
    except (ProcessLookupError, OSError):
        pass


def _signal_handler(signum, frame):
    """On SIGINT/SIGTERM: reap the active claude process group, then exit.

    Episode-level try/finally blocks run on the resulting SystemExit, removing the
    worktree; the interrupted episode has no manifest.json so --resume re-runs it.
    """
    proc = _ACTIVE["proc"]
    if proc is not None and proc.poll() is None:
        kill_group(proc)
    sys.exit(128 + signum)


# ---------------------------------------------------------------------------
# Worktree management
# ---------------------------------------------------------------------------
def worktree_add(baseline_sha, path):
    if os.path.exists(path):
        worktree_remove(path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    run_git(["worktree", "add", "--detach", path, baseline_sha], cwd=FIXTURE_PATH)
    check_workspace_isolated(path)


def worktree_remove(path):
    run_git(["worktree", "remove", "--force", path], cwd=FIXTURE_PATH, check=False)
    if os.path.exists(path):
        shutil.rmtree(path, ignore_errors=True)
    run_git(["worktree", "prune"], cwd=FIXTURE_PATH, check=False)


def check_workspace_isolated(ws):
    """Invariant 1 guard: the workspace must not live under the experiment tree, and no
    ancestor directory may contain the experiment's file set (tasks+rubrics+spec+harness)."""
    ws_real = os.path.realpath(ws)
    exp_real = os.path.realpath(EXPERIMENT)
    if ws_real == exp_real or ws_real.startswith(exp_real + os.sep):
        raise RuntimeError("workspace %s is inside the experiment tree" % ws)
    sentinels = ("rubrics", "tasks", "spec", "harness")
    anc = os.path.dirname(ws_real)
    while True:
        if all(os.path.isdir(os.path.join(anc, s)) for s in sentinels):
            raise RuntimeError(
                "workspace ancestor %s contains experiment files (invariant 1)" % anc
            )
        parent = os.path.dirname(anc)
        if parent == anc:
            break
        anc = parent


def workspace_reset(path, baseline_sha):
    run_git(["reset", "--hard", baseline_sha], cwd=path)
    # -x: also remove ignored files (tally.json, __pycache__, .pytest_cache) so B phase 2
    # cannot inherit phase-1 runtime state. The fixture baseline commits no ignored files.
    run_git(["clean", "-fdx"], cwd=path)


def workspace_dirty(path):
    """Return (tracked, ignored): lists of paths changed/created in the workspace.
    tracked = modifications/additions of tracked or new files; ignored = ignored files."""
    out = run_git(
        ["status", "--porcelain", "--ignored"], cwd=path, check=False
    ).stdout.splitlines()
    tracked, ignored = [], []
    for line in out:
        if not line.strip():
            continue
        if line.startswith("!!"):
            ignored.append(line[3:])
        else:
            tracked.append(line[3:])
    return tracked, ignored


def capture_diff(workspace, out_path):
    # `add -A -N` makes untracked files show up in `git diff` as additions without staging
    # their content, so episode.diff captures new files too.
    run_git(["add", "-A", "-N"], cwd=workspace, check=False)
    diff = run_git(["diff"], cwd=workspace, check=False).stdout
    write_text(out_path, diff)
    # Reset intent-to-add so the index is clean for a later hard reset.
    run_git(["reset"], cwd=workspace, check=False)
    status = run_git(["status", "--porcelain"], cwd=workspace, check=False).stdout
    return bool(status.strip())


def run_pytest(workspace, out_path):
    """Run the fixture suite; bounded by PYTEST_TIMEOUT_S so a hanging test cannot stall an
    unattended run. Timeout records exit code -9 and a timeout marker in pytest.txt."""
    try:
        res = subprocess.run(
            [VENV_PY, "-m", "pytest", "-q"],
            cwd=workspace,
            capture_output=True,
            text=True,
            timeout=PYTEST_TIMEOUT_S,
        )
        exit_code, stdout, stderr = res.returncode, res.stdout, res.stderr
        timed_out = False
    except subprocess.TimeoutExpired as e:
        exit_code = -9
        stdout = _as_text(e.stdout)
        stderr = _as_text(e.stderr)
        timed_out = True
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("exit_code: %d\n" % exit_code)
        if timed_out:
            f.write("timeout: pytest exceeded %ds and was killed\n" % PYTEST_TIMEOUT_S)
        f.write("\n")
        f.write(stdout or "")
        if stderr:
            f.write("\n--- stderr ---\n")
            f.write(stderr)
    return exit_code


def _as_text(x):
    if x is None:
        return ""
    if isinstance(x, bytes):
        return x.decode("utf-8", errors="replace")
    return x


# ---------------------------------------------------------------------------
# Condition B: parse + validate the typed speech act
# ---------------------------------------------------------------------------
VALID_ACTS = {"promise", "counter_offer", "decline", "commit_to_commit"}


def extract_json_block(text):
    """Return the last fenced ```json ... ``` block (or last ``` block) parsed as a dict."""
    blocks = re.findall(r"```(?:json)?\s*(.*?)```", text, re.DOTALL)
    for block in reversed(blocks):
        try:
            obj = json.loads(block.strip())
            if isinstance(obj, dict):
                return obj
        except json.JSONDecodeError:
            continue
    # Fallback: try to parse the whole thing.
    try:
        obj = json.loads(text.strip())
        if isinstance(obj, dict):
            return obj
    except json.JSONDecodeError:
        pass
    return None


def validate_speech_act(obj):
    """Return (ok, act_or_None, reason)."""
    if obj is None:
        return False, None, "no parseable JSON block found"
    act = obj.get("speech_act")
    if act not in VALID_ACTS:
        return False, None, "speech_act missing or not one of %s" % sorted(VALID_ACTS)
    if "conditions_of_satisfaction" not in obj or not isinstance(
        obj["conditions_of_satisfaction"], list
    ):
        return False, act, "conditions_of_satisfaction must be a list"
    if "scope_exclusions" not in obj or not isinstance(obj["scope_exclusions"], list):
        return False, act, "scope_exclusions must be a list"
    if "concern" not in obj:
        return False, act, "concern field missing"
    return True, act, ""


# ---------------------------------------------------------------------------
# Episode runners
# ---------------------------------------------------------------------------
def base_manifest(task_id, cond, run, fixture_sha, prompt_sha):
    return {
        "task": task_id,
        "condition": cond,
        "run": run,
        "model": MODEL,
        "cli_version": cli_version(),
        "fixture_sha": fixture_sha,
        "prompt_sha256": prompt_sha,
        "phases": [],
        "speech_act": None,
        "diff_nonempty": None,
        "pytest_exit": None,
        "protocol_error": None,
        "cap_hit": None,
        "timestamp": now_iso(),
    }


def phase_record(name, res, prompt_sha, prompt_file):
    return {
        "phase": name,
        "prompt_sha256": prompt_sha,
        "prompt_file": prompt_file,
        "tokens_in": res["tokens_in"],
        "tokens_out": res["tokens_out"],
        "turns": res["num_turns"],
        "wall_s": res["wall_s"],
    }


def run_simple_episode(cond, task_id, run, ep_dir, fixture_sha):
    """Condition A or B' — single phase."""
    template = read_template("A.md" if cond == "A" else "Bprime.md")
    task_text = read_task(task_id)
    prompt = template.replace("{{TASK}}", task_text)
    prompt_sha = sha256_text(prompt)
    write_text(os.path.join(ep_dir, "prompt.md"), prompt)

    workspace = worktree_path(run, task_id, cond)
    worktree_add(fixture_sha, workspace)
    manifest = base_manifest(task_id, cond, run, fixture_sha, prompt_sha)
    try:
        res = invoke_claude(
            prompt, workspace, os.path.join(ep_dir, "transcript.jsonl")
        )
        check_cli_error(res, "execute")
        write_text(os.path.join(ep_dir, "final.txt"), res["result_text"])
        diff_nonempty = capture_diff(workspace, os.path.join(ep_dir, "episode.diff"))
        pytest_exit = run_pytest(workspace, os.path.join(ep_dir, "pytest.txt"))
        manifest["phases"].append(phase_record("execute", res, prompt_sha, "prompt.md"))
        manifest["diff_nonempty"] = diff_nonempty
        manifest["pytest_exit"] = pytest_exit
        manifest["cap_hit"] = res["cap_hit"]
    finally:
        worktree_remove(workspace)
    write_manifest(ep_dir, manifest)


def run_b_episode(task_id, run, ep_dir, fixture_sha):
    """Condition B — two-phase: negotiate -> gate -> execute."""
    task_text = read_task(task_id)
    neg_template = read_template("B-negotiate.md")
    neg_prompt = neg_template.replace("{{TASK}}", task_text)
    neg_sha = sha256_text(neg_prompt)
    write_text(os.path.join(ep_dir, "prompt-negotiate.md"), neg_prompt)
    # prompt.md is the phase-1 prompt (uniform artifact across conditions); its hash is the
    # manifest's top-level prompt_sha256. Per-phase hashes live in the phases records.
    write_text(os.path.join(ep_dir, "prompt.md"), neg_prompt)

    workspace = worktree_path(run, task_id, "B")
    worktree_add(fixture_sha, workspace)
    manifest = base_manifest(task_id, "B", run, fixture_sha, neg_sha)
    manifest["negotiation_writes"] = []
    try:
        # ---- Phase 1: negotiate ----
        neg_res = invoke_claude(
            neg_prompt, workspace, os.path.join(ep_dir, "negotiation-transcript.jsonl")
        )
        check_cli_error(neg_res, "negotiate")
        manifest["phases"].append(
            phase_record("negotiate", neg_res, neg_sha, "prompt-negotiate.md")
        )
        manifest["cap_hit"] = neg_res["cap_hit"]
        # Dirty check BEFORE any reset, so evidence of a phase-1 write is never erased.
        _record_negotiation_writes(manifest, workspace, "negotiate")

        parsed = extract_json_block(neg_res["result_text"])
        ok, act, reason = validate_speech_act(parsed)

        # D14: a capped negotiation is a recorded outcome, never retried.
        if neg_res["cap_hit"]:
            _save_negotiation(ep_dir, neg_res, parsed, ok, reason)
            manifest["speech_act"] = act if ok else None
            _finalize_terminated_b(ep_dir, workspace, fixture_sha, manifest, neg_res)
            write_manifest(ep_dir, manifest)
            return

        if not ok:
            # One retry with a terse schema-mismatch note appended (spec: gate logic).
            retry_prompt = (
                neg_prompt
                + "\n\nYour previous output did not match the required schema (%s). "
                "Respond again with EXACTLY ONE fenced JSON block matching the schema and "
                "nothing else." % reason
            )
            retry_sha = sha256_text(retry_prompt)
            write_text(os.path.join(ep_dir, "prompt-negotiate-retry.md"), retry_prompt)
            workspace_reset(workspace, fixture_sha)
            neg_res2 = invoke_claude(
                retry_prompt,
                workspace,
                os.path.join(ep_dir, "negotiation-transcript-retry.jsonl"),
            )
            check_cli_error(neg_res2, "negotiate_retry")
            manifest["phases"].append(
                phase_record(
                    "negotiate_retry", neg_res2, retry_sha, "prompt-negotiate-retry.md"
                )
            )
            manifest["cap_hit"] = manifest["cap_hit"] or neg_res2["cap_hit"]
            _record_negotiation_writes(manifest, workspace, "negotiate_retry")
            parsed = extract_json_block(neg_res2["result_text"])
            ok, act, reason = validate_speech_act(parsed)
            neg_res = neg_res2  # the effective negotiation output

            if neg_res2["cap_hit"]:
                _save_negotiation(ep_dir, neg_res, parsed, ok, reason)
                manifest["speech_act"] = act if ok else None
                _finalize_terminated_b(ep_dir, workspace, fixture_sha, manifest, neg_res)
                write_manifest(ep_dir, manifest)
                return

        _save_negotiation(ep_dir, neg_res, parsed, ok, reason)

        if not ok:
            manifest["protocol_error"] = manifest["protocol_error"] or "schema_failure"
            manifest["speech_act"] = None
            _finalize_terminated_b(ep_dir, workspace, fixture_sha, manifest, neg_res)
            write_manifest(ep_dir, manifest)
            return

        manifest["speech_act"] = act

        if act != "promise":
            # Surfacing ends the episode.
            _finalize_terminated_b(ep_dir, workspace, fixture_sha, manifest, neg_res)
            write_manifest(ep_dir, manifest)
            return

        # ---- Gate passed: clean workspace (tracked + ignored), run phase 2 ----
        workspace_reset(workspace, fixture_sha)
        exec_template = read_template("B-execute.md")
        promise_json = json.dumps(parsed, indent=2)
        exec_prompt = exec_template.replace("{{TASK}}", task_text).replace(
            "{{PROMISE_JSON}}", promise_json
        )
        exec_sha = sha256_text(exec_prompt)
        write_text(os.path.join(ep_dir, "prompt-execute.md"), exec_prompt)

        exec_res = invoke_claude(
            exec_prompt, workspace, os.path.join(ep_dir, "transcript.jsonl")
        )
        check_cli_error(exec_res, "execute")
        manifest["phases"].append(
            phase_record("execute", exec_res, exec_sha, "prompt-execute.md")
        )
        manifest["cap_hit"] = manifest["cap_hit"] or exec_res["cap_hit"]
        write_text(os.path.join(ep_dir, "final.txt"), exec_res["result_text"])
        diff_nonempty = capture_diff(workspace, os.path.join(ep_dir, "episode.diff"))
        pytest_exit = run_pytest(workspace, os.path.join(ep_dir, "pytest.txt"))
        manifest["diff_nonempty"] = diff_nonempty
        manifest["pytest_exit"] = pytest_exit
        write_manifest(ep_dir, manifest)
    finally:
        worktree_remove(workspace)


def _record_negotiation_writes(manifest, workspace, attempt):
    """Record any files the negotiation phase changed or created, BEFORE any reset.
    Tracked/new-file changes are a protocol error (H0 data); ignored-file creations
    (caches from running tests/CLI) are recorded but not counted as writes."""
    tracked, ignored = workspace_dirty(workspace)
    if tracked or ignored:
        manifest["negotiation_writes"].append(
            {"attempt": attempt, "tracked": tracked, "ignored": ignored}
        )
    if tracked:
        manifest["protocol_error"] = "negotiation_wrote"


def _save_negotiation(ep_dir, neg_res, parsed, ok, reason):
    with open(os.path.join(ep_dir, "negotiation.json"), "w", encoding="utf-8") as f:
        json.dump(
            {"raw": neg_res["result_text"], "parsed": parsed, "valid": ok, "reason": reason},
            f,
            indent=2,
        )


def _finalize_terminated_b(ep_dir, workspace, fixture_sha, manifest, neg_res):
    """B episode that ended at negotiation (non-promise, schema failure, or cap). Produce the
    uniform artifact set from a reset (clean) workspace so every episode folder is complete.
    Caller writes the manifest; the episode-level finally removes the worktree."""
    workspace_reset(workspace, fixture_sha)
    # transcript.jsonl / final.txt mirror the effective negotiation attempt for uniformity.
    src_tr = os.path.join(ep_dir, "negotiation-transcript-retry.jsonl")
    if not os.path.exists(src_tr):
        src_tr = os.path.join(ep_dir, "negotiation-transcript.jsonl")
    shutil.copyfile(src_tr, os.path.join(ep_dir, "transcript.jsonl"))
    write_text(os.path.join(ep_dir, "final.txt"), neg_res["result_text"])
    diff_nonempty = capture_diff(workspace, os.path.join(ep_dir, "episode.diff"))
    pytest_exit = run_pytest(workspace, os.path.join(ep_dir, "pytest.txt"))
    manifest["diff_nonempty"] = diff_nonempty
    manifest["pytest_exit"] = pytest_exit


# ---------------------------------------------------------------------------
# Paths / manifest IO
# ---------------------------------------------------------------------------
def worktree_path(run, task_id, cond):
    return os.path.join(WORKTREE_ROOT, run, "%s-%s" % (task_id, cond))


def episode_dir(run, task_id, cond):
    return os.path.join(RUNS_DIR, run, "%s-%s" % (task_id, cond))


def write_manifest(ep_dir, manifest):
    with open(os.path.join(ep_dir, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)


def episode_complete(ep_dir):
    """Complete iff manifest.json exists and parses. Harness errors write error.json (never
    manifest.json), so crashed episodes are re-run on --resume."""
    mpath = os.path.join(ep_dir, "manifest.json")
    if not os.path.exists(mpath):
        return False
    try:
        with open(mpath, "r", encoding="utf-8") as f:
            json.load(f)
        return True
    except Exception:
        return False


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def load_or_init_run_manifest(run, tasks, fixture_sha, resume):
    """Fresh run: write run.json. Resume: reuse the existing run.json and fail fast if the
    current fixture HEAD or task set doesn't match the original run's."""
    path = os.path.join(RUNS_DIR, run, "run.json")
    if resume and os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            prev = json.load(f)
        problems = []
        if prev.get("fixture_sha") != fixture_sha:
            problems.append(
                "fixture HEAD changed: run.json has %s, current is %s"
                % (prev.get("fixture_sha"), fixture_sha)
            )
        if prev.get("tasks") != tasks:
            problems.append(
                "task set changed: run.json has %s, args give %s" % (prev.get("tasks"), tasks)
            )
        if prev.get("model") != MODEL:
            problems.append(
                "model changed: run.json has %s, config is %s" % (prev.get("model"), MODEL)
            )
        if problems:
            for p in problems:
                print("RESUME MISMATCH: %s" % p, file=sys.stderr)
            print("Refusing to resume a run against changed inputs.", file=sys.stderr)
            sys.exit(2)
        prev.setdefault("resumed_at", []).append(now_iso())
        with open(path, "w", encoding="utf-8") as f:
            json.dump(prev, f, indent=2)
        return prev
    manifest = {
        "run": run,
        "tasks": tasks,
        "conditions": CONDITIONS,
        "model": MODEL,
        "max_turns": MAX_TURNS,
        "timeout_s": TIMEOUT_S,
        "fixture_sha": fixture_sha,
        "cli_version": cli_version(),
        "started": now_iso(),
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    return manifest


def main():
    ap = argparse.ArgumentParser(description="Speech Acts episode harness")
    ap.add_argument("--run", required=True, help="run label (debug, rep1, rep2, rep3)")
    ap.add_argument(
        "--tasks",
        default=None,
        help="comma-separated task ids (default: all 24). e.g. t03,t14,t21,t04",
    )
    ap.add_argument("--resume", action="store_true", help="skip already-complete episodes")
    args = ap.parse_args()

    signal.signal(signal.SIGINT, _signal_handler)
    signal.signal(signal.SIGTERM, _signal_handler)

    tasks = ALL_TASKS if not args.tasks else [t.strip() for t in args.tasks.split(",") if t.strip()]
    for t in tasks:
        if not os.path.exists(os.path.join(TASKS_DIR, t + ".md")):
            print("ERROR: unknown task %s" % t, file=sys.stderr)
            sys.exit(2)

    fixture_sha = run_git(["rev-parse", "HEAD"], cwd=FIXTURE_PATH).stdout.strip()
    os.makedirs(os.path.join(RUNS_DIR, args.run), exist_ok=True)
    os.makedirs(WORKTREE_ROOT, exist_ok=True)

    run_manifest = load_or_init_run_manifest(args.run, tasks, fixture_sha, args.resume)
    fixture_sha = run_manifest["fixture_sha"]

    episodes = [(t, c) for t in tasks for c in CONDITIONS]
    total = len(episodes)
    print("Run %s: %d episodes (%d tasks x %d conditions), fixture %s"
          % (args.run, total, len(tasks), len(CONDITIONS), fixture_sha[:8]))

    consecutive_cli_errors = 0
    for idx, (task_id, cond) in enumerate(episodes, 1):
        ep_dir = episode_dir(args.run, task_id, cond)
        tag = "%s-%s" % (task_id, cond)
        if args.resume and episode_complete(ep_dir):
            print("[%d/%d] %s  SKIP (complete)" % (idx, total, tag))
            continue
        # Fresh start for this episode: clear any partial folder.
        if os.path.exists(ep_dir):
            shutil.rmtree(ep_dir)
        os.makedirs(ep_dir)
        # Clean any stale worktree from a prior kill.
        worktree_remove(worktree_path(args.run, task_id, cond))

        print("[%d/%d] %s  running..." % (idx, total, tag), flush=True)
        t0 = time.time()
        try:
            if cond == "B":
                run_b_episode(task_id, args.run, ep_dir, fixture_sha)
            else:
                run_simple_episode(cond, task_id, args.run, ep_dir, fixture_sha)
        except SystemExit:
            raise
        except Exception as e:
            # Record the failure as error.json (NOT manifest.json, so --resume re-runs it).
            is_cli = isinstance(e, CLIError)
            with open(os.path.join(ep_dir, "error.json"), "w", encoding="utf-8") as f:
                json.dump(
                    {"task": task_id, "condition": cond, "run": args.run,
                     "type": "cli_error" if is_cli else "harness_error",
                     "error": repr(e), "timestamp": now_iso()},
                    f, indent=2,
                )
            worktree_remove(worktree_path(args.run, task_id, cond))
            print("    %s (will re-run on --resume): %r"
                  % ("CLI ERROR" if is_cli else "ERROR", e), flush=True)
            if is_cli:
                consecutive_cli_errors += 1
                if consecutive_cli_errors >= MAX_CONSECUTIVE_CLI_ERRORS:
                    print(
                        "ABORTING RUN: %d consecutive CLI errors (rate limit / auth / "
                        "network?). Fix the underlying issue, then re-run with --resume."
                        % consecutive_cli_errors, flush=True)
                    sys.exit(3)
            continue
        consecutive_cli_errors = 0
        dt = round(time.time() - t0, 1)
        m = json.load(open(os.path.join(ep_dir, "manifest.json")))
        print("    done in %ss  act=%s diff=%s pytest=%s protocol_error=%s cap=%s"
              % (dt, m.get("speech_act"), m.get("diff_nonempty"),
                 m.get("pytest_exit"), m.get("protocol_error"), m.get("cap_hit")),
              flush=True)

    # Tidy the (now-empty) per-run worktree root.
    run_wt = os.path.join(WORKTREE_ROOT, args.run)
    if os.path.isdir(run_wt) and not os.listdir(run_wt):
        os.rmdir(run_wt)

    print("Run %s complete." % args.run)


if __name__ == "__main__":
    main()
