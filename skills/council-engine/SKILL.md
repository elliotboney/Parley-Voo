---
name: council-engine
description: Run a council deliberation over a question or artifact — parallel seat fan-out, anonymized peer review, dissent-preserving chairman synthesis. Use when a skill or user supplies a roster file and asks for a council verdict.
---

# Council Engine

Orchestrates a deliberation: independent seats reason in parallel, peer-review
each other anonymously, and a chairman synthesizes without smoothing dissent.

The full protocol contract (verbatim guardrail text, output headings,
rationale) lives in `references/protocol.md`. Topology details live in
`references/topologies.md`. Read both before your first run.

## Inputs

You need two things:

1. **A roster file** — `councils/<name>.md` (or an explicit path the caller
   provides, e.g. a test fixture).
2. **The framed input** — the question, decision, or artifact under
   deliberation, exactly as the caller framed it.

## Step 1: Resolve the roster

Read the roster file's YAML frontmatter:

| Key | Meaning |
|---|---|
| `topology` | `parallel` or `staged` — how the deliberation runs |
| `seats` | ordered list of seat IDs participating in a full run |
| `quick_seats` | subset of `seats` used in quick mode (Story 1.3 — ignore for now) |
| `model_overrides` | optional map of `seat_id → tier` |

Validate the roster before loading anything:

- `seats` must be non-empty — an empty list → STOP: `Roster '<name>' has no seats.`
- `seats` must contain no duplicates — a duplicate would let one voice review
  and vote twice. STOP and name it: `Roster '<name>' lists seat '<id>' twice.`
- `topology` must be a value this engine implements (see Step 3). Unknown or
  unimplemented values fail closed — never fall back to `parallel` silently.

For each seat ID in `seats`, load the persona file `agents/<seat-id>.md`.

**If any persona file is missing, STOP immediately and name the missing seat
ID** — e.g. `Roster 'council-default' names seat 'behavioral-coder' but
agents/behavioral-coder.md does not exist.` Do not run a partial council.

Each persona file is frontmatter (`seat_id`, `display_name`, `method`,
`ignores`, `role`, `modes`) plus a body — the body IS that seat's prompt.

## Step 2: Resolve models

**HARD RULE: model tiers come ONLY from the roster's `model_overrides` map.**

- Default when a seat has no override: **haiku-class** for seats,
  **strong model** (the session's top tier) for the chairman.
- If a persona file contains any model or tier key, **IGNORE IT**. Persona
  files never choose models — that would kill per-roster overrides.

Validate `model_overrides` before spawning anything:

- Every key must be a seat ID in `seats` or `chairman`. Unknown key → STOP:
  `model_overrides names '<id>', which is not in this roster.` (A typo here
  would silently run the wrong tier.)
- Every value must be a known tier: `haiku-class` or `strong-model`.
  Unknown value → STOP and name it.

Tier mapping for sub-agent spawns: `haiku-class` → the fast/cheap model
parameter; `strong-model` → the session's top-tier model parameter.

## Step 3: Run the topology

Dispatch on the roster's `topology` value. This engine implements `parallel`
only. `staged` is declared in the contract but NOT yet implemented (Story 1.3)
— a roster with `topology: staged` (or any other value) fails closed:
STOP and say so, e.g. `Roster '<name>' declares topology 'staged', which is
not implemented yet (Story 1.3).` Never silently run it as parallel.

**Sub-agent failure rule (applies to every stage):** if any spawn returns
empty output, an error, or times out, retry that one spawn ONCE. If it fails
again, STOP and name the seat/stage — e.g. `Seat 'test-purist' returned no
response in stage 1 after one retry.` Never proceed with a partial council:
a missing voice silently biases the verdict.

### Stage 1 — independent fan-out

Spawn ALL seats as sub-agents **in ONE message** (one Task/Agent tool call
per seat, all in the same message). Never sequentially:

> "Sequential lets earlier responses contaminate later ones."

Each sub-agent prompt is exactly:

1. The persona file body (the seat's method and discipline).
2. The sycophancy guardrail, verbatim from `references/protocol.md` §3.
3. The framed input.

No seat sees any other seat's output, the roster, or the seat list. This
boundary is non-negotiable — independence is the whole point of the topology.

### Stage 2 — anonymized peer review

1. Collect all stage-1 responses.
2. **Shuffle them and relabel A, B, C…** — one anonymous label per
   participating seat. Randomize the mapping every run; seat 1 must NOT
   always be Response A (`references/protocol.md` §1).
3. Fan out peer reviewers (again, all in one message). **The reviewers ARE
   the participating seats** — each seat's persona body becomes its review
   lens. Each reviewer receives the framed input plus ALL anonymized
   responses, and is asked to assess the reasoning of each — including the
   conformity check, verbatim from `references/protocol.md` §4.

Reviewers never learn which seat wrote which response — which means each
seat unknowingly reviews its own response too. This is by design: labels
are anonymous, the chairman weighs reasoning rather than counting votes,
so self-review is acceptable noise, not a leak.

### Stage 3 — devil's advocate, then chairman synthesis

Two spawns, strictly in order (the harvested protocol requires the attack
to be a SEPARATE voice, not the chairman attacking its own draft):

**3a — devil's advocate.** Spawn ONE sub-agent on a strong model with the
framed input + all anonymized responses + all peer reviews, instructed to:
state the emerging consensus in one sentence, then make the strongest
possible case that this answer is WRONG (the three demands in
`references/protocol.md` §2). If there is no consensus, it says so and
attacks the leading position instead.

**3b — chairman.** Spawn the `chairman` seat (persona file
`agents/chairman.md`, strong model unless the roster overrides) with:

1. The framed input.
2. All anonymized responses (labels intact, **mapping withheld**).
3. All peer reviews.
4. The devil's-advocate attack from 3a — the chairman must rebut or
   concede it explicitly before finalizing the verdict.

The chairman renders the output contract (Agrees / Clashes / Blind Spots /
Recommendation / What You Lose / Do This First / Verify) per its persona
file and `references/protocol.md` §5, attributing any dissent **by response
label** (e.g. `— Response B`) — it never sees the seat mapping.

## Rendering

The chairman's output is the deliverable, with ONE mechanical substitution:
the engine (which holds the withheld label→seat mapping) replaces each
label attribution in `Dissent:` lines with `— {Display Name}, {method}`
from the persona files. This keeps the mapping away from the chairman while
still rendering named attribution. Touch nothing else — heading depth ≤
`###`, confidence as `word (0.NN)`, no wide tables.
