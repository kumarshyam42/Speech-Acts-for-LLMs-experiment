# h6 — Counter-offers as consultative repair

**Tier 2 · Status: proposed** (~8 of 21 counter-offers read closely). Charter:
`../260706-new-hypotheses.md` §H-N6.

**Claim.** B's counter-offers (21 across reps) don't just refuse — they *repair the request*:
naming the real file, correcting the requester's diagnosis, proposing a superior
implementation, or reframing edit-as-creation, each with its own checkable CoS. Bell's "the
response that creates the most value" showing up empirically; the original metrics scored it
only as binary "surfaced."

**Motivating data (verified).**
- `runs/rep3/t04-B` concern: bare `round()` "would fail all three of those assertions and is
  more likely to introduce cent-off errors than fix them. ... The more plausible source of the
  'cent off' issue is `report.py:34`, which applies `round_money` after each incremental
  addition inside a loop, causing compounding rounding drift." — corrects the user's own
  diagnosis, pre-execution.
- `runs/rep2/t04-B`: counter-offers `decimal.Decimal(...ROUND_HALF_UP)` — strictly better than
  the request.
- `runs/rep1/t03-B`: names the real export code (`tally/report.py::to_csv`, line 91) and flags
  that the reported bug likely doesn't exist.
- `t23-B` (3/3 reps): reframes "add to CHANGELOG" as "create CHANGELOG."

**Layer.** Coordination/negotiation quality.
**Pi connection.** The pilot *terminated* episodes at counter-offer by design — whether the
requester accepts and the re-bound task succeeds is exactly the untested half of the CfA
cycle, and a first-class Pi experiment. **The downstream-value claim cannot be tested on this
corpus at all.**

**Planned measurement (Phase 2, judged).**
Rate all 21 counter-offers on: premise-correction (y/n), intent-preservation, CoS
checkability. Symmetric comparison against A/B′ pushback prose needs Job-1-style
format-agnostic rules. Rubric to `rubric.md` + `spec/decisions-log.md` first; verdicts to
`verdicts/`.

**Credibility path.** Pattern present 3/3 reps for t03/t04/t07/t23. Quality scoring is a new
instrument (pre-register the rubric); downstream value needs Pi.
