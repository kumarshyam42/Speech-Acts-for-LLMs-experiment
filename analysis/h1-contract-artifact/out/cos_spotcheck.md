# h1 CoS checkability — hand spot-check of the seeded 30-CoS sample (WP-A / A2)

*260706. Hand labels for the deterministic sample (seed 260706) listed in
`cos_checkability_summary.md`. Standard (locked in `../README.md`): could two independent
third parties verify the condition from artifacts alone and agree without interpretation?
Hand labels bound the heuristic's error; they never overwrite the census. Labeled by the
executing session (Claude).*

| # | rep | task | idx | heuristic | hand label | agree? | note |
|---|---|---|---|---|---|---|---|
| 1 | rep1 | t01 | 1 | observable | observable | yes | Names `build_parser()`, `--year`, default. |
| 2 | rep1 | t01 | 4 | observable | observable | yes | Suite-green is mechanically checkable. |
| 3 | rep1 | t04 | 0 | vague | vague | yes | "actual source ... identified" is a judgment. |
| 4 | rep1 | t05 | 0 | observable | observable | yes | Literal dict entry. |
| 5 | rep1 | t05 | 5 | observable | observable | yes | Pinned assertion value. |
| 6 | rep1 | t07 | 3 | observable | observable | yes | Named helper + file + anchor rule. |
| 7 | rep1 | t14 | 3 | observable | observable | yes | Named file + 80% figure. |
| 8 | rep1 | t20 | 0 | observable | observable | yes | Literal `"SGD": 0.75`. |
| 9 | rep1 | t20 | 3 | observable | observable | yes | Suite-green. |
| 10 | rep1 | t21 | 1 | vague | vague | yes | Whether prose "explains" X needs interpretation. |
| 11 | rep1 | t21 | 3 | vague | vague | yes | Borderline: "usage/looking-at-your-spending area" is not a literal heading; placement judgment. |
| 12 | rep1 | t22 | 3 | vague | vague | yes | Borderline: "plain Markdown, no new tooling" needs interpretation at the margins. |
| 13 | rep2 | t03 | 2 | vague | observable | NO — heuristic false negative | Underlying property (rows end after final field) is concretely checkable; "CSV" carried no file-extension token. |
| 14 | rep2 | t12 | 0 | observable | observable | yes | Literal table-cell text in a named file. |
| 15 | rep2 | t14 | 2 | observable | observable | yes | Named file anchors it. |
| 16 | rep2 | t17 | 1 | observable | observable | yes | Concrete command + required error content. |
| 17 | rep2 | t17 | 3 | observable | observable | yes | Suite-green. |
| 18 | rep2 | t18 | 2 | vague | observable | NO — heuristic false negative | "At least one new test covers (percentage present, budget annotation present)" is checkable; "at least one" is spelled out, so the NUM digit rule missed it. |
| 19 | rep2 | t19 | 0 | observable | observable | yes | Named file + named API. |
| 20 | rep2 | t19 | 6 | observable | observable | yes | pytest exit 0. |
| 21 | rep2 | t21 | 1 | vague | vague | yes | Same shape as #10. |
| 22 | rep2 | t22 | 1 | vague | observable | NO — heuristic false negative | Enumerates the six subcommands to cover; presence per subcommand is checkable ("missing or only partially covered today" adds fuzz but the core is enumerable). |
| 23 | rep2 | t22 | 4 | observable | vague | NO — heuristic false positive | "No information is invented that contradicts the codebase/README/pricing.md" is a global judgment over all content; the pricing.md token triggered FILE. |
| 24 | rep2 | t24 | 1 | vague | observable | NO — heuristic false negative | Pins a specific propositional claim the section must state; presence of that claim is checkable. |
| 25 | rep3 | t09 | 6 | vague | observable | NO — heuristic false negative | "All pre-existing tests continue to pass" ≡ suite-green; phrasing dodges the literal "tests pass" pattern. |
| 26 | rep3 | t14 | 1 | observable | observable | yes | Named flag in README. |
| 27 | rep3 | t20 | 1 | observable | observable | yes | Pinned assertion. |
| 28 | rep3 | t21 | 2 | observable | observable | yes | Literal usage example. |
| 29 | rep3 | t22 | 1 | observable | observable | yes | Five entries, enumerated topics. |
| 30 | rep3 | t23 | 2 | observable | observable | yes | Named section + named files. |

## Result

- **Agreement: 24/30 (80%).** Disagreements: 5 false negatives (heuristic said vague,
  hand says observable: #13, #18, #22, #24, #25) vs 1 false positive (#23).
- **Error direction: the heuristic UNDER-counts observable.** The census's 75% observable
  share among promise CoS is therefore best read as a floor; the hand standard puts the
  true share several points higher. Since the kill criterion fires on *low* observability,
  the census is conservative in exactly the direction that protects against a false
  survival.
- Recurring miss patterns (for any future heuristic revision, NOT applied retroactively):
  suite-green phrasings without the literal tokens ("continue to pass"), spelled-out
  quantities ("at least one/five"), and propositional-content conditions ("states that X").
- Borderlines recorded: #11, #12 (kept vague — both need interpretation at the margins).
