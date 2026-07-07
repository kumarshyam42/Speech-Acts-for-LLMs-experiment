#!/usr/bin/env python3
"""
h1 (contract artifact) — WP-A / A2, part 1: scope-exclusion conformance census.

Implements EXACTLY the locked definitions in this folder's README.md
("Phase-2 locked definitions (260706)"). Mechanical only: it counts exclusions,
classifies file-scoped vs behavioral, and over-generates CANDIDATE violations
via the named-file and allow-list rules. It never decides that a violation is
real — that is the hand-adjudication step documented in
out/exclusion_adjudication.md.

Reads ONLY frozen artifacts: runs/<rep>/merged.csv, negotiation.json,
episode.diff. Writes ONLY out/exclusion_conformance.csv and
out/exclusion_conformance_summary.md.

Standard library only, Python 3.9, idempotent (byte-identical re-runs).
"""

import csv
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
EXPERIMENT = os.path.dirname(os.path.dirname(HERE))
RUNS_DIR = os.path.join(EXPERIMENT, "runs")
OUT_DIR = os.path.join(HERE, "out")

REPS = ["rep1", "rep2", "rep3"]

FILE_TOKEN_RE = re.compile(
    r"[A-Za-z0-9_./-]*[A-Za-z0-9_-]+\.(?:py|md|txt|json|toml|cfg|ini|csv)\b")
ALLOWLIST_RE = re.compile(
    r"\bother than\b|\bonly\b|\bexcept\b|\bapart from\b|\bbeyond\b|\boutside\b",
    re.IGNORECASE)
DIFF_FILE_RE = re.compile(r"^diff --git a/(.+?) b/(.+)$", re.MULTILINE)

CSV_COLUMNS = [
    "rep", "task", "class", "speech_act", "executed", "exclusion_index",
    "exclusion_type", "named_files", "allowlist_marker", "candidate_violation",
    "diff_files_implicated", "exclusion_text",
]


def load_b_rows():
    rows = []
    for rep in REPS:
        with open(os.path.join(RUNS_DIR, rep, "merged.csv"),
                  newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                if r["condition"] == "B":
                    r["rep"] = rep
                    rows.append(r)
    rows.sort(key=lambda r: (r["rep"], r["task"]))
    return rows


def diff_paths(ep_dir):
    path = os.path.join(ep_dir, "episode.diff")
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8", errors="replace") as f:
        text = f.read()
    files = set()
    for m in DIFF_FILE_RE.finditer(text):
        files.add(m.group(2))
    return sorted(files)


def main():
    b_rows = load_b_rows()
    if len(b_rows) != 72:
        raise SystemExit("Expected 72 B episodes, found %d" % len(b_rows))
    os.makedirs(OUT_DIR, exist_ok=True)

    out_rows = []
    candidates = []
    for r in b_rows:
        ep_dir = os.path.join(RUNS_DIR, r["rep"], "%s-B" % r["task"])
        with open(os.path.join(ep_dir, "negotiation.json"), encoding="utf-8") as f:
            neg = json.load(f)
        exclusions = (neg.get("parsed") or {}).get("scope_exclusions") or []
        exclusions = [e for e in exclusions if isinstance(e, str)]
        executed = r["executed"] == "True"
        touched = diff_paths(ep_dir) if executed else []
        touched_basenames = {os.path.basename(p): p for p in touched}

        for i, exc in enumerate(exclusions):
            named = sorted(set(m.group(0).lstrip("./") for m in
                               FILE_TOKEN_RE.finditer(exc)))
            named_basenames = {os.path.basename(n) for n in named}
            file_scoped = bool(named)
            allowlist = bool(ALLOWLIST_RE.search(exc))

            cand = []
            implicated = []
            if executed and file_scoped:
                # named-file rule
                hits = sorted(touched_basenames[b] for b in named_basenames
                              if b in touched_basenames)
                if hits:
                    cand.append("named_file")
                    implicated.extend(hits)
                # allow-list rule
                if allowlist:
                    extras = sorted(p for b, p in touched_basenames.items()
                                    if b not in named_basenames)
                    if extras:
                        cand.append("allowlist")
                        implicated.extend(x for x in extras if x not in implicated)

            row = {
                "rep": r["rep"], "task": r["task"], "class": r["class"],
                "speech_act": r["speech_act"], "executed": executed,
                "exclusion_index": i,
                "exclusion_type": "file_scoped" if file_scoped else "behavioral",
                "named_files": ";".join(named),
                "allowlist_marker": allowlist,
                "candidate_violation": "+".join(cand) if cand else "none",
                "diff_files_implicated": ";".join(implicated),
                "exclusion_text": exc,
            }
            out_rows.append(row)
            if cand:
                candidates.append(row)

    with open(os.path.join(OUT_DIR, "exclusion_conformance.csv"), "w",
              encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(CSV_COLUMNS)
        for row in out_rows:
            w.writerow([str(row[c]) for c in CSV_COLUMNS])

    # ---- summary ----
    L = []
    L.append("# h1 exclusion-conformance census — summary (WP-A / A2)")
    L.append("")
    L.append("*Generated by `exclusion_conformance.py` under the locked definitions in "
             "`../README.md` (260706). EXPLORATORY, descriptive only. Candidate "
             "violations are OVER-GENERATED by design; the truth call per candidate "
             "lives in `exclusion_adjudication.md` (hand-adjudicated, documented).*")
    L.append("")
    n_eps_with = len({(r["rep"], r["task"]) for r in out_rows})
    L.append("- B episodes with >=1 declared exclusion: %d / 72" % n_eps_with)
    L.append("- Total exclusions: %d (file-scoped %d, behavioral %d)" % (
        len(out_rows),
        sum(1 for r in out_rows if r["exclusion_type"] == "file_scoped"),
        sum(1 for r in out_rows if r["exclusion_type"] == "behavioral")))
    exec_promise_eps = {(r["rep"], r["task"]) for r in out_rows
                        if r["executed"] and r["speech_act"] == "promise"}
    fs_exec_eps = {(r["rep"], r["task"]) for r in out_rows
                   if r["executed"] and r["speech_act"] == "promise"
                   and r["exclusion_type"] == "file_scoped"}
    L.append("- Executed promises with >=1 exclusion: %d; with >=1 FILE-SCOPED "
             "exclusion (kill-criterion denominator): %d"
             % (len(exec_promise_eps), len(fs_exec_eps)))
    L.append("")
    L.append("## Per class x rep: exclusions declared (file-scoped / behavioral)")
    L.append("")
    L.append("| Class | rep1 | rep2 | rep3 |")
    L.append("|---|---|---|---|")
    for klass in ("1", "2", "3", "4"):
        cells = []
        for rep in REPS:
            fs = sum(1 for r in out_rows if r["class"] == klass and r["rep"] == rep
                     and r["exclusion_type"] == "file_scoped")
            bh = sum(1 for r in out_rows if r["class"] == klass and r["rep"] == rep
                     and r["exclusion_type"] == "behavioral")
            cells.append("%d / %d" % (fs, bh))
        L.append("| %s | %s |" % (klass, " | ".join(cells)))
    L.append("")
    L.append("## Candidate violations awaiting adjudication: %d" % len(candidates))
    L.append("")
    if candidates:
        L.append("| rep | task | rule | files implicated | exclusion |")
        L.append("|---|---|---|---|---|")
        for c in candidates:
            L.append("| %s | %s | %s | %s | %s |" % (
                c["rep"], c["task"], c["candidate_violation"],
                c["diff_files_implicated"],
                c["exclusion_text"].replace("|", "\\|")))
    L.append("")
    with open(os.path.join(OUT_DIR, "exclusion_conformance_summary.md"), "w",
              encoding="utf-8", newline="") as f:
        f.write("\n".join(L) + "\n")
    print("Wrote %d exclusion rows, %d candidates to %s"
          % (len(out_rows), len(candidates), OUT_DIR))


if __name__ == "__main__":
    main()
