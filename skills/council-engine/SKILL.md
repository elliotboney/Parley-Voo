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

Tier mapping for sub-agent spawns: `haiku-class` → the fast/cheap model
parameter; `strong-model` → the session's top-tier model parameter.

## Step 3: Run the topology

Dispatch on the roster's `topology` value. This story implements `parallel`;
`staged` lands in Story 1.3 (see `references/topologies.md`).

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
3. Fan out peer reviewers (again, all in one message): each reviewer
   receives the framed input plus ALL anonymized responses, and is asked to
   assess the reasoning of each — including the conformity check, verbatim
   from `references/protocol.md` §4.

Reviewers never learn which seat wrote which response.

### Stage 3 — chairman synthesis

Spawn the `chairman` seat (persona file `agents/chairman.md`, strong model
unless the roster overrides) with:

1. The framed input.
2. All anonymized responses (labels intact, mapping withheld).
3. All peer reviews.
4. The seat roster's display names + methods (for `Dissent:` attribution
   only — given AFTER weighing instructions, per the chairman's own prompt).

The chairman runs the devil's-advocate-vs-consensus pass and renders the
output contract (Agrees / Clashes / Blind Spots / Recommendation / What You
Lose / Do This First / Verify) — both defined in its persona file and
`references/protocol.md` §2 and §5.

## Rendering

The chairman's output is the deliverable. Pass it through untouched —
heading depth ≤ `###`, confidence as `word (0.NN)`, `Dissent:` labels with
`— {Display Name}, {method}` attribution, no wide tables.
