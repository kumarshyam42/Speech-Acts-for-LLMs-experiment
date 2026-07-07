# The Experiment, In Plain Language

*Companion to `Experiment Design.md` (v2). Same experiment, no jargon. 2026-07-04.*

## The question we're asking

Your paper claims that AI agents coordinate better when they behave like responsible
performers: before doing a task, they either promise (with clear conditions of satisfaction),
counter-offer, decline, or ask for time — instead of just silently attempting whatever they
were asked. That's a prediction, and nobody has tested it. This experiment tests it.

## The setup: one worker, three sets of instructions

We give an AI agent a batch of tasks on a small practice codebase. Every task runs three
times, with the agent operating under three different "employment contracts":

- **Group A — how agents work today.** Get the task, do your best, hand back the result.
- **Group B — your protocol.** Before touching anything, you must respond the way your
  framework says a performer should: promise with conditions of satisfaction, counter-offer,
  decline, or commit-to-commit (Flores's term for "I can't commit yet, but I'll give you a
  commitment by X"). Only a promise lets you proceed, and your final report gets checked
  against the conditions you declared.
- **Group B′ — the "control" group, and the sneaky-important one.** Before starting, jot down
  any concerns and what success would look like — but with no speech-act structure, no menu
  of four responses, no commitment step. Just "think first, then go."

Why the third group? Here's the trap it protects us from. Suppose Group B does better than
Group A. A skeptic will say: *"That proves nothing about speech acts. You made the agent pause
and think before acting — ANY pause would have helped."* And they'd have research on their
side; "make the model reflect first" is already known to improve results. So the real
comparison isn't B against A. It's **B against B′**: does your specific structure — the four
responses, the explicit conditions of satisfaction — add anything beyond a generic moment of
reflection? It's like testing a commitment-management training for salespeople: if the trained
group improves, you still have to rule out that any workshop that made them slow down would
have worked just as well.

## The tasks: mostly booby-trapped, on purpose

24 tasks, in four flavors, six of each. Not all are coding tasks — about a third are document
tasks (fix a README, update a pricing doc) living in the same practice repo, because the
framework is about delegation generally, not software. For those, what gets graded is the
agent's *response behavior* — did it propose conditions of satisfaction, offer two directions
to choose from, flag the contradiction? — never whether the prose is "good":

1. **Clean requests** — clear, doable, checkable. These exist to answer: does the protocol
   *get in the way* when nothing is wrong? (An agent that counter-offers on a perfectly clear
   request is being annoying, and we need to know if the protocol produces that.)
2. **Vague requests** — "improve readability," "make it faster." A good performer negotiates
   what that means before acting. A bad one guesses.
3. **Impossible requests** — the file doesn't exist, or the ask contradicts the rules of the
   codebase. A good performer declines or counter-offers. A bad one flails and produces garbage.
4. **Requests with a hidden catch** — doable on the surface, but doing it naively breaks
   something the agent could discover if it looked (a failing test, a requirement written
   elsewhere that contradicts the ask). Your published essay's proofreading example — catching
   the pricing contradiction, not just the typos — is exactly this flavor.

Notice that 18 of the 24 tasks are problematic by design. That's deliberate — you test a smoke
detector with smoke. But it also means we can't average everything into one score and say "the
protocol improved results by X%." Real-world requests aren't 75% broken. So we report each
flavor separately, and we treat the clean-request results as just as important as the rest.

## How a task ends

If the agent pushes back — declines, counter-offers, asks what you really meant — the task
ends right there and the pushback itself is what gets graded. We don't simulate a whole
back-and-forth conversation with a fake human (that would introduce its own problems). If the
agent asks a question mid-task, it gets one standard reply, the same in all three groups:
"proceed as you judge best, and note your concerns in your final report."

One fairness rule matters a lot here: an agent in Group A that says, in plain prose, "I can't
find that file, are you sure it exists?" gets full credit — same as a formal decline in
Group B. We're grading the behavior, not the paperwork.

## How we grade

Two layers, and the order matters.

**Things a script can count, no opinions involved.** Did the agent modify files on an
impossible task? (The computer can check that directly.) Do the tests pass at the end? How
much work did it burn before raising a problem? Did Group B's agent actually check its own
declared conditions, or declare them and then ignore them? These countable measures carry the
main conclusions, because they can't be argued with.

**Things that need judgment** — like "did the output match what the requester actually
wanted?" For these we use an AI judge from a *different company's* model family (a judge from
the same family tends to favor its sibling's work — same reason you don't let a parent judge
their own kid's science fair). The judge must quote the exact part of the transcript that
justifies every grade, and you personally spot-check a sample. One honest limitation: the
judge can always tell which group a transcript came from, because Group B's transcripts have
the structured responses right in them. We can't hide that — which is exactly why the
countable layer, where no judgment is involved, does the heavy lifting.

## The measurement that matters most

Here's the one your paper actually stakes itself on. When a task goes wrong, can you point at
*where* the coordination broke? There are only four places: the problem was never surfaced and
no real commitment was ever made · a commitment was made but not kept · a commitment was made
and kept, but it was the *wrong* commitment (the agent misread what you wanted) · the
commitment was right and the agent just made an execution mistake.

The paper's bet is that failures in Group B can be pinned to one of those four, while failures
in Groups A and B′ mostly land in a fifth bucket: "something went wrong, can't tell what."
That difference — failures you can diagnose versus failures that are just fog — is the paper's
central practical claim. It matters even if the raw success rates end up identical, because a
diagnosable failure can be fixed and a foggy one can't.

## Deciding what results mean — before we run it

We've written down, in advance, what every possible outcome means. This is the experiment
declaring its own conditions of satisfaction before executing — so we can't fool ourselves
into a flattering interpretation after seeing the data:

- **B beats B′ beats A, and B doesn't annoy on clean tasks** → the speech-act structure itself
  changes behavior. Strongest result. Green light for building it into a real protocol layer.
- **B's failures are diagnosable and the others' aren't** — even if success rates tie → the
  paper's core claim holds. Also a win.
- **B and B′ tie** → the benefit was "pausing to think," not the framework. The framework's
  value is a *vocabulary for diagnosing* coordination, not a driver of behavior. Humbler, but
  honest and still worth publishing — your paper already allows for exactly this.
- **B does worse** — agents mislabel their own responses, declare conditions then ignore them,
  counter-offer reflexively on clean requests → the "complexity ceiling" your paper names as
  failure mode #1 is real. That's a finding, not an embarrassment. It goes in the paper too.

The whole thing is a **pilot**: 24 tasks and 3 repeats is enough to see which way the wind
blows and decide whether to invest further — not enough to claim statistical proof. We say so
plainly in the writeup.

## What this experiment cannot tell us

Three things, so nobody oversells it later: it can't test trust-building over time (every
agent here is an identical blank slate, so "this agent has a good track record" is fiction);
it tests the protocol as *instructions and forms* rather than as real infrastructure (that's
the Pi phase, if this shows signal); and it can't say how often real-world requests are vague
or impossible — so it can't say whether the protocol pays for itself in everyday use, only
whether it works when it's needed.
