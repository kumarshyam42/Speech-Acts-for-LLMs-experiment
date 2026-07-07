# The Full Run, In Plain Language

*Companion to `The Experiment, In Plain Language.md`. That doc explains what the experiment is;
this one explains the phase we're about to enter — the actual run — and what it's for. Written
2026-07-05, at the point where everything is built and nothing has yet been measured.*

## Where we are

Everything up to now has been building and checking the measuring instrument, not measuring
anything. Four pieces got built in sequence: the practice codebase with its 24 booby-trapped
tasks; the machinery that runs an agent through a task under each of the three contracts; the
part that counts the things a script can count; and, last, the AI judge from a different model
family that grades the things needing judgment.

Each piece was tested on a deliberately tiny dry run — four tasks, run under all three contracts,
twelve episodes in total — so that any wiring fault would show up cheaply, before spending
anything at scale. That dry run is done, and it holds up: the judge cites real quotes from the
transcripts, the counting is reproducible, and an independent check confirmed every citation the
judge made actually appears where it says it does. The instrument works. What it hasn't done yet
is take a real measurement.

## What this phase actually is

The full run is the experiment finally happening. The same 24 tasks, under the same three
contracts, run start to finish three times over — three "repeats," 72 episodes each, a bit over
two hundred episodes in all. After each repeat, the counting runs, the judge runs, and the
results get assembled into tables. The one piece still to build is that final assembly step —
the part that merges the countable measures and the judge's verdicts into something you can
read. It gets built first and proven on the dry-run data (where you can check every cell by hand)
before a single real repeat starts.

Why three repeats rather than one? Because a single agent on a single task is one roll of the
dice. The same task, run three times, tells you whether a behavior is a tendency or a fluke.
Three is not enough to prove anything statistically — this is a pilot, and the writeup says so
plainly — but it's enough to see which way the wind is blowing and decide whether the idea earns
a larger investment.

## What it's staked on — the connection to your paper

Your paper makes a specific bet, and this run is the first time that bet meets data. The bet is
not "the protocol makes agents succeed more often." It's that **when a task goes wrong, the
protocol lets you point at where it broke** — the problem was never surfaced, or a commitment was
made and dropped, or the wrong commitment was made, or the right one was fumbled in execution.
Four nameable places. The claim is that failures under your protocol land in one of those four,
while failures under the other two contracts mostly land in a fifth bucket: *something went
wrong, can't tell what.*

That distinction — failures you can diagnose versus failures that are just fog — is the practical
heart of the paper, and it's what these tables are built to show. It matters even if the plain
success rates come out identical across all three contracts, because a failure you can locate is
a failure you can fix, and a foggy one isn't.

The other comparison the run is built to protect is the one a skeptic would reach for first:
Group B versus Group B′, not Group B versus Group A. If the protocol group does better, the
honest question is whether your specific structure — the four responses, the explicit conditions
of satisfaction — did the work, or whether merely making the agent pause and think first would
have done the same. B′ is the "pause and think, but no structure" group that isolates that. The
run reports the two side by side so the answer isn't left to interpretation.

## The guardrails — what protects the result from me, and from you

A few rules are baked into this phase specifically so neither of us can nudge the outcome toward
a flattering story:

- **The verdict criteria are frozen.** The tasks, the hidden grading rubrics, and the judge's
  instructions were all locked and fingerprinted before this run — so nobody can quietly reword a
  grading criterion after seeing a result they don't like. This is the experiment declaring its
  own conditions of satisfaction before it acts, which is, fittingly, the exact discipline your
  framework asks of a performer.
- **Weird results are results.** No episode gets re-run because its number looks wrong. The only
  reason to re-run anything is a genuine technical failure — a crash, an outage — and every such
  re-run gets logged with its reason. An agent that behaves strangely is data, not a bug to be
  smoothed away.
- **The judge is from a different family.** The grader is a different company's model, for the
  same reason you don't let a parent judge their own child's science fair. And every grade it
  gives has to quote the transcript, so you can spot-check it.
- **You hold the trigger.** Building the assembly step and proving it on the dry run costs
  nothing to speak of. The real run — a few hundred dollars and several hours — starts only when
  you say go. It can also run overnight and pick up exactly where it left off if it's
  interrupted, so a stall in the middle is never lost work.

## What you'll get, and the decision it forces

The output is one document of per-class tables — each flavor of task reported on its own, never
averaged into a single headline number, because 18 of the 24 tasks are broken by design and a
combined score would be a fiction. The final section lines those tables up against the four
outcomes you wrote down in advance, so reading the result is a matter of seeing which
pre-registered reading the data matches:

- **The protocol changes behavior, and doesn't get in the way on clean tasks** → the strongest
  result, and a green light to build this into real infrastructure — the Pi phase.
- **The protocol's failures are diagnosable and the others' aren't, even if success rates tie** →
  the paper's central claim holds. A win on the terms that actually matter.
- **The protocol and the "pause and think" group tie** → the value was reflection, not your
  structure; the framework earns its keep as a *vocabulary for diagnosing* coordination rather
  than a driver of behavior. Humbler, still honest, still publishable — your paper already makes
  room for this.
- **The protocol does worse** — agents mislabel their own responses, declare conditions then
  ignore them, negotiate reflexively on clean requests → the "complexity ceiling" your paper
  names as its own first failure mode is real. That's a finding, and it goes in the paper too.

Whichever way it lands, the result feeds the same next move in your roadmap: it decides how the
paper's results section gets framed, and whether the infrastructure phase is justified yet. The
run doesn't tell you what to conclude — you wrote the conclusions in advance. It tells you which
one you're in.

## What this phase still can't tell you

The same three limits from the experiment overall carry through, and it's worth keeping them in
view so the tables don't get oversold later. It can't test trust built over time — every agent
here is an identical blank slate. It tests the protocol as instructions and forms, not as real
infrastructure; that's the Pi phase, if the signal justifies it. And it can't say how often
real-world requests are actually vague or impossible, so it can't tell you whether the protocol
pays for itself in everyday use — only whether it works when it's needed.

One more, specific to how the dry run happened to go: on the two trickiest task flavors — the
impossible ones and the ones with a hidden catch — all three contracts declined to act, so the
judge never got to grade an agent that pushed ahead into a trap. The full run is the first time
you'll see what happens when an agent actually walks into one, which is exactly the situation the
whole framework is meant to handle. Expect that part of the picture to be messier than the dry
run suggested — and that messiness is the point, not a problem to fix.
