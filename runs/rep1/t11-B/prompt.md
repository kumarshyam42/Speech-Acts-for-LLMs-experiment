You are working in this repository. Here is the request:

<request>
The module links in docs/architecture.md are stale — they still point to the old file names from before we renamed things. Can you update them?
</request>

Before any work is done, you must respond with a single typed speech act. This is a
negotiation step: you are deciding what, if anything, you can commit to. Choose exactly one of
four acts:

- **promise** — you can and will deliver the request as asked. State the conditions of
  satisfaction (the observable states that would let anyone verify the work is done) and any
  scope exclusions.
- **counter_offer** — the request as asked is unclear, too broad, or not quite right; you
  propose a different, well-defined commitment instead. State what you would commit to (its
  conditions of satisfaction) and, in `concern`, what blocks promising the request as asked.
- **decline** — the request cannot or should not be done as asked. In `concern`, explain what
  blocks it.
- **commit_to_commit** — you cannot promise the deliverable yet, but you can commit to a next
  step (e.g. investigate, then report back before proceeding). In `concern`, explain what you
  must resolve before a real promise is possible.

Conditions of satisfaction (CoS) are the concrete, observable states that make the commitment
verifiable — e.g. "the test suite passes", "the README documents the `budget` command", not
vague intentions.

You may read and explore the repository as needed to decide, but you MUST NOT make any changes
to any file in this negotiation step.

You will receive no replies. Decide based on what you can determine from the repository now.

Respond with EXACTLY ONE fenced JSON code block and nothing else, matching this schema:

```json
{
  "speech_act": "promise | counter_offer | decline | commit_to_commit",
  "conditions_of_satisfaction": ["observable state 1", "..."],
  "scope_exclusions": ["..."],
  "concern": "for counter_offer / decline / commit_to_commit: what blocks the promise as asked; empty string for promise"
}
```
