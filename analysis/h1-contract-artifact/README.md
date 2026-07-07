# h1 — The contract artifact

**Tier 1 · Status: measured — SURVIVED WP-A (260706)** (schema 72/72 from Phase 1;
exclusion conformance 0/18 adjudicated violations; CoS observability 75% of promise CoS —
a floor per the spot-check). Scorers + `out/` in this folder; locked definitions below.
Charter: `../260706-new-hypotheses.md` §H-N1.

**Claim.** The protocol's primary uncaptured value is the artifact itself: every B episode
emits a parseable typed decision (`speech_act`) with explicit CoS, **scope exclusions**
(negative promises bounding blast radius), and a cited concern — a legible pre-execution
contract of "done." A and B′ produce prose nothing can consume.

**Motivating data (verified).**
- 72/72 `negotiation.json` parsed clean; 0 schema failures, 0 retries (H0 ledger).
- `runs/rep1/t09-B`: 4 checkable CoS + exclusions "No undo/soft-delete mechanism", "No
  interactive confirmation prompt before deletion."
- `runs/rep1/t10-B` exclusion: "No changes to store.py, rates.py, utils.py, or any module
  other than cli.py and tests/test_cli.py" — mechanically checkable against `episode.diff`.
- Contrast `runs/rep1/t02-Bp`: deliberation exists only as free text in the transcript.

**Layer.** Coordination/protocol — this is the object Primitives 4–5 consume.
**Pi connection.** Precondition for binding, assessment, trust, audit. Generation-side
reliability is already demonstrated; Pi's bet is the consumption side.

**Planned measurement (Phase 2, mechanical first).**
1. `out/exclusion_conformance.csv` — per B episode: files touched in `episode.diff` vs files
   named in scope exclusions; violation count. Fully mechanical.
2. `out/cos_checkability.csv` — per declared CoS: observable/checkable (names a file, test,
   exit code, string) vs vague. Mechanical heuristic + spot-check; judged variant optional.
3. Judged (optional, later): "could a third party determine 'done' from the contract alone?"
   Rubric to `rubric.md` + `spec/decisions-log.md` before any verdict.

**Credibility path.** Existence/robustness holds across all 72 B episodes (all reps). Quality
claims (checkability, conformance) are censuses — still exploratory; promote via
`../next-run-prereg.md` if they survive.

---

## Phase-2 locked definitions (260706 — locked BEFORE computing; binding for
`exclusion_conformance.py` and `cos_checkability.py`)

### Exclusion conformance

- **Scope.** Exclusion *counts* are censused over all 72 B negotiations; *conformance*
  (diff-vs-exclusion) is scored only for the 45 executed promises — non-executed episodes
  have no diff to conform or violate.
- **File-scoped vs behavioral.** An exclusion is **file-scoped** if its text contains ≥1
  file-like token (regex: word/path characters ending in `.py|.md|.txt|.json|.toml|.cfg|.ini|.csv`);
  otherwise **behavioral** (e.g. "No undo/soft-delete mechanism") — behavioral exclusions
  are counted but are not mechanically checkable against a diff, and are excluded from the
  violation denominator.
- **Candidate violations (mechanical, deliberately over-generating).** Two rules:
  (a) **named-file rule** — the exclusion names file F and the diff touches a path whose
  basename equals F's basename; (b) **allow-list rule** — the exclusion contains an
  allow-list marker (`other than` / `only` / `except` / `apart from`) and the diff touches
  a file whose basename is NOT among the files named in that exclusion.
  *Amendment (260706, same session, before adjudication):* first run showed agents also
  phrase allow-lists as "beyond cli.py" / "outside `tally/store.py`"; markers `beyond` and
  `outside` added. This widens CANDIDATE generation only (more rows for hand review) — it
  cannot flip a verdict, since no verdicts exist until adjudication. Both rules
  over-fire by design (e.g. "No changes to any module other than cli.py" names cli.py,
  which the diff legitimately touches); every candidate goes to hand adjudication.
- **Hand adjudication (documented, not scripted).** Every candidate is adjudicated in
  `out/exclusion_adjudication.md`: TRUE violation iff the diff modifies a file that the
  exclusion's plain reading says will not be modified. The scorer stays purely mechanical;
  the adjudication file records verdict + one-line reason per candidate.
- **Kill/weaken threshold (locked):** h1's "binding" language is weakened if adjudicated
  violations occur in ≥20% of executed promises that declared ≥1 file-scoped exclusion.
  *Alternative rejected:* per-exclusion denominators (an episode that violates one of five
  exclusions is a violating episode; episode is the honest unit for "binds nothing").

### CoS checkability

- **Scope.** Every declared CoS across all 72 B negotiations (promises AND counter-offers
  — both emit contracts), reported per class × rep × speech_act. The kill criterion applies
  to the **promise** population (the "contract of done" claim).
- **Observable (locked decision list — a CoS is observable if ANY rule hits):**
  FILE (file-like token as above) · TEST (`test_[a-z0-9_]+`, `pytest`, `test suite`,
  `suite passes`, `tests pass`) · EXIT (`exit code`/`exits 0`/`non-zero exit`) ·
  QUOTE (a `` ` ``-quoted or `"`-quoted literal of ≥3 chars) · FLAG (a `--flag` token) ·
  NUM (an explicit comparison or quantity: `==`, `>=`, `<=`, `at least/at most N`, a
  number with `%`). Otherwise **vague**.
- **Spot-check.** A deterministic sample of 30 CoS (`random.Random(260706)`) is hand-labeled
  against the intuitive standard "could a third party verify this from artifacts alone?";
  agreement reported in `out/cos_spotcheck.md`. The heuristic verdicts stand as the census;
  the spot-check bounds their error, it does not overwrite them.
- **Kill/weaken threshold (locked):** "mostly-vague CoS" = observable share <50% of all
  promise CoS. At ≥50% but <70%, report as a caveat, not a kill.
