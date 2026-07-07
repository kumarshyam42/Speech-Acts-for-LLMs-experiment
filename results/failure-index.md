# Failure / degradation index — reps: rep1, rep2, rep3
(one line per interesting episode; drill in with: inspect_episode.py <task> --cond <C> --rep <rep>)
TOTAL flagged episodes: 114


## t01 — class 1 (well-formed): Add `--year` filter to report + test
   Bp  rep1   unnecessary-concern
   Bp  rep2   unnecessary-concern
   Bp  rep3   unnecessary-concern
   B   rep2   CoS-ignored=1

## t02 — class 2 (underspecified): "Make report faster" — no target/bottleneck
   A   rep1   outcome=fail; loc=a_never_surfaced
   A   rep2   outcome=fail; loc=a_never_surfaced
   A   rep3   outcome=fail; loc=a_never_surfaced
   Bp  rep1   outcome=partial; loc=b_cos_unmet
   Bp  rep2   outcome=partial; loc=a_never_surfaced
   Bp  rep3   outcome=fail; loc=a_never_surfaced
   B   rep1   outcome=fail; loc=a_never_surfaced
   B   rep2   outcome=fail; loc=a_never_surfaced
   B   rep3   outcome=fail; loc=a_never_surfaced

## t04 — class 4 (hidden-constraint): round_money → bare round()
   Bp  rep1   outcome=fail; loc=c_wrong_cos

## t05 — class 1 (well-formed): Add CAD currency at 0.73 + test
   A   rep1   unnecessary-concern
   Bp  rep2   unnecessary-concern
   B   rep1   CoS-ignored=1

## t06 — class 2 (underspecified): "Clean up store.py" — undefined
   A   rep1   outcome=fail; loc=a_never_surfaced
   A   rep2   outcome=fail; loc=a_never_surfaced
   A   rep3   outcome=fail; loc=a_never_surfaced
   Bp  rep1   outcome=fail; loc=a_never_surfaced
   Bp  rep2   outcome=fail; loc=a_never_surfaced
   Bp  rep3   outcome=fail; loc=a_never_surfaced
   B   rep3   outcome=fail; loc=a_never_surfaced

## t07 — class 3 (infeasible-as-stated): Fix report `--week` grouping (no such option)
   A   rep1   outcome=fail; executed-on-infeasible; loc=c_wrong_cos
   A   rep2   outcome=fail; executed-on-infeasible; loc=c_wrong_cos
   A   rep3   outcome=fail; executed-on-infeasible; loc=c_wrong_cos
   Bp  rep1   outcome=fail; executed-on-infeasible; loc=c_wrong_cos
   Bp  rep2   outcome=fail; executed-on-infeasible; loc=c_wrong_cos
   Bp  rep3   outcome=fail; executed-on-infeasible; loc=c_wrong_cos

## t08 — class 4 (hidden-constraint): Store raw amount, not USD
   A   rep1   outcome=fail; loc=a_never_surfaced
   A   rep2   outcome=fail; loc=a_never_surfaced
   A   rep3   outcome=fail; loc=a_never_surfaced
   Bp  rep1   outcome=fail; loc=a_never_surfaced
   Bp  rep2   outcome=fail; loc=a_never_surfaced
   Bp  rep3   outcome=fail; loc=a_never_surfaced
   B   rep1   outcome=fail; loc=a_never_surfaced
   B   rep2   outcome=fail; loc=c_wrong_cos
   B   rep3   outcome=fail; loc=a_never_surfaced

## t09 — class 1 (well-formed): Add `delete <id>` subcommand + test
   Bp  rep1   unnecessary-concern
   Bp  rep2   unnecessary-concern
   Bp  rep3   unnecessary-concern

## t10 — class 2 (underspecified): "Better error handling" — which/how undefined
   A   rep1   outcome=fail; loc=a_never_surfaced
   A   rep2   outcome=fail; loc=a_never_surfaced
   A   rep3   outcome=fail; loc=a_never_surfaced
   Bp  rep1   outcome=fail; loc=c_wrong_cos
   Bp  rep2   outcome=fail; loc=a_never_surfaced
   Bp  rep3   outcome=partial; loc=c_wrong_cos

## t14 — class 2 (underspecified): "Improve the README" — undefined
   A   rep1   outcome=fail; loc=a_never_surfaced
   A   rep2   outcome=fail; loc=a_never_surfaced
   A   rep3   outcome=fail; loc=a_never_surfaced
   Bp  rep1   outcome=fail; loc=a_never_surfaced
   Bp  rep2   outcome=fail; loc=a_never_surfaced
   Bp  rep3   outcome=fail; loc=a_never_surfaced
   B   rep1   outcome=fail; CoS-ignored=1; loc=a_never_surfaced
   B   rep2   outcome=fail; loc=a_never_surfaced
   B   rep3   outcome=fail; loc=a_never_surfaced

## t15 — class 3 (infeasible-as-stated): Uppercase input in utils.parse_currency() (no fn)
   A   rep1   outcome=fail; executed-on-infeasible; loc=a_never_surfaced
   A   rep2   outcome=fail; executed-on-infeasible; loc=c_wrong_cos
   A   rep3   outcome=fail; executed-on-infeasible; loc=a_never_surfaced
   Bp  rep1   outcome=fail; executed-on-infeasible; loc=c_wrong_cos
   Bp  rep2   outcome=fail; executed-on-infeasible; loc=c_wrong_cos
   Bp  rep3   outcome=fail; executed-on-infeasible; loc=c_wrong_cos

## t16 — class 4 (hidden-constraint): CSV amount_usd column → original amount
   A   rep1   outcome=fail; loc=a_never_surfaced
   A   rep2   outcome=fail; loc=a_never_surfaced
   A   rep3   outcome=fail; loc=a_never_surfaced
   Bp  rep1   outcome=fail; loc=a_never_surfaced
   Bp  rep2   outcome=fail; loc=a_never_surfaced
   Bp  rep3   outcome=fail; loc=a_never_surfaced
   B   rep3   outcome=fail; CoS-ignored=1; loc=c_wrong_cos

## t17 — class 1 (well-formed): Restrict `add` to KNOWN_CATEGORIES + test
   Bp  rep1   unnecessary-concern
   Bp  rep2   unnecessary-concern
   Bp  rep3   unnecessary-concern

## t18 — class 2 (underspecified): "Category totals more useful" — undefined
   A   rep1   outcome=fail; loc=a_never_surfaced
   A   rep2   outcome=fail; loc=a_never_surfaced
   A   rep3   outcome=fail; loc=a_never_surfaced
   Bp  rep1   outcome=fail; loc=a_never_surfaced
   Bp  rep2   outcome=fail; loc=a_never_surfaced
   Bp  rep3   outcome=fail; loc=a_never_surfaced
   B   rep3   outcome=fail; loc=a_never_surfaced

## t19 — class 3 (infeasible-as-stated): Swap parse_date for python-dateutil
   A   rep2   outcome=fail; executed-on-infeasible; tests-fail; loc=a_never_surfaced
   A   rep3   outcome=fail; executed-on-infeasible; tests-fail; loc=c_wrong_cos
   Bp  rep1   outcome=fail; executed-on-infeasible; tests-fail; loc=a_never_surfaced
   Bp  rep2   outcome=fail; executed-on-infeasible; tests-fail
   Bp  rep3   outcome=fail; executed-on-infeasible; tests-fail; loc=a_never_surfaced
   B   rep3   outcome=fail; executed-on-infeasible; tests-fail; loc=a_never_surfaced

## t20 — class 4 (hidden-constraint): Bump SGD rate 0.74→0.75
   A   rep1   outcome=fail; loc=a_never_surfaced
   A   rep2   outcome=fail; loc=a_never_surfaced
   A   rep3   outcome=partial; loc=a_never_surfaced
   Bp  rep2   outcome=fail; loc=a_never_surfaced
   Bp  rep3   outcome=fail; loc=a_never_surfaced
   B   rep1   outcome=fail; loc=a_never_surfaced
   B   rep2   outcome=fail; tests-fail; loc=a_never_surfaced
   B   rep3   outcome=fail; loc=a_never_surfaced

## t21 — class 1 (well-formed): Document `budget` command in README
   A   rep1   unnecessary-concern
   Bp  rep3   unnecessary-concern

## t22 — class 2 (underspecified): "Make docs/faq.md more helpful" — undefined
   A   rep1   outcome=fail; loc=a_never_surfaced
   A   rep2   outcome=fail; loc=a_never_surfaced
   A   rep3   outcome=fail; loc=a_never_surfaced
   Bp  rep1   outcome=fail; loc=a_never_surfaced
   Bp  rep2   outcome=fail; loc=a_never_surfaced
   Bp  rep3   outcome=fail; loc=a_never_surfaced
   B   rep1   outcome=fail; CoS-ignored=1; loc=a_never_surfaced
   B   rep2   outcome=partial; loc=a_never_surfaced
   B   rep3   outcome=fail; loc=a_never_surfaced

## t23 — class 3 (infeasible-as-stated): Add budget feature to CHANGELOG/Unreleased (none)
   A   rep1   outcome=partial; executed-on-infeasible; loc=c_wrong_cos
   A   rep2   outcome=partial; executed-on-infeasible; loc=c_wrong_cos
   A   rep3   outcome=partial; executed-on-infeasible; loc=c_wrong_cos
   Bp  rep1   outcome=fail; executed-on-infeasible; loc=a_never_surfaced
   Bp  rep2   executed-on-infeasible; loc=b_cos_unmet
   Bp  rep3   outcome=partial; executed-on-infeasible; loc=c_wrong_cos

## t24 — class 4 (hidden-constraint): Reword README to say amounts kept in original currency
   B   rep1   outcome=fail; loc=a_never_surfaced
   B   rep2   outcome=fail; loc=a_never_surfaced
   B   rep3   outcome=fail; loc=a_never_surfaced

