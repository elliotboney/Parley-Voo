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

You need two things, plus one optional flag:

1. **A roster file** — `councils/<name>.md` (or an explicit path the caller
   provides, e.g. a test fixture).
2. **The framed input** — the question, decision, or artifact under
   deliberation, exactly as the caller framed it.
3. **Mode escalation (optional)** — quick is the default; a caller passing
   the user's `--full` flag escalates to full (see Step 3).

## Step 1: Resolve the roster

Read the roster file's YAML frontmatter:

| Key | Meaning |
|---|---|
| `topology` | `parallel` or `staged` — how the deliberation runs |
| `seats` | ordered list of seat IDs participating in a full run |
| `quick_seats` | non-empty subset of `seats` that runs in quick mode (see Step 3) |
| `model_overrides` | optional map of `seat_id → tier` |

The shape of `seats` depends on topology: a flat list of seat IDs for
`parallel`; an ordered list of **stage groups** (a list of lists) for
`staged` (see `references/topologies.md` for both shapes).

Validate the roster before loading anything:

- `seats` must be non-empty — an empty list → STOP: `Roster '<name>' has no
  seats.` For `staged`, every stage group must also be non-empty.
- No duplicate seat IDs anywhere in the roster (across ALL stage groups for
  staged) — a duplicate would let one voice review and vote twice. STOP and
  name it: `Roster '<name>' lists seat '<id>' twice.`
- `chairman` must NOT appear in `seats` or any stage group — the chairman is
  implicit final synthesis in both topologies, appended by the engine. STOP:
  `Roster '<name>' lists 'chairman' as a seat; the chairman is implicit.`
- `quick_seats` must be PRESENT and non-empty — quick is the default mode,
  so a roster without a usable `quick_seats` would run zero seats. Missing
  key or empty list → STOP: `Roster '<name>' has no quick_seats; every
  roster must name its quick subset.` (An empty list is a vacuous subset —
  it passes a naive subset check; reject it explicitly.)
- `quick_seats` must be a subset of the flattened `seats` — an unknown ID →
  STOP: `quick_seats names '<id>', which is not a seat in this roster.`
  `chairman` in `quick_seats` gets the implicit-chairman STOP above, not the
  generic unknown-ID one.
- `topology` must be a value this engine implements (see Step 4). Unknown or
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

## Step 3: Resolve the mode

**HARD RULE: WHO runs comes only from the roster (`seats`, `quick_seats`,
`topology`); WHAT each mode means protocol-wise is defined HERE, once,
identically for every command. The engine never decides mode per command**
— command skills merely forward the user's flag.

- Default mode is **quick**. The caller may pass an escalation (the
  `--full` flag's semantics) → **full**.
- **Quick:** only the seats in `quick_seats` execute; the peer-review
  fan-out is SKIPPED; the separate devil's-advocate spawn is SKIPPED
  (debate only where it earns its token cost); the anonymization shuffle is
  KEPT (it costs zero spawns and preserves the chairman's anti-deference
  boundary); chairman synthesis always runs.
- **Full:** all seats execute, plus anonymized peer review, devil's
  advocate, and chairman.
- For `staged` rosters in quick mode: a stage group with no seats in
  `quick_seats` is skipped entirely; the handoff flows from the last
  non-skipped stage to the next; stage order is preserved.

## Step 4: Run the topology

Dispatch on the roster's `topology` value — `parallel` or `staged`. Any
other value fails closed: STOP and name it. Never silently fall back to
`parallel`.

**Sub-agent failure rule (applies to every stage):** if any spawn returns
empty output, an error, or times out, retry that one spawn ONCE. If it fails
again, STOP and name the seat/stage — e.g. `Seat 'test-purist' returned no
response in stage 1 after one retry.` Never proceed with a partial council:
a missing voice silently biases the verdict.

### Parallel — Stage 1: independent fan-out

Spawn the participating seats (full mode: ALL seats; quick mode: only
`quick_seats`) as sub-agents **in ONE message** (one Task/Agent tool call
per seat, all in the same message). Never sequentially:

> "Sequential lets earlier responses contaminate later ones."

Each sub-agent prompt is exactly:

1. The persona file body (the seat's method and discipline).
2. The sycophancy guardrail, verbatim from `references/protocol.md` §3.
3. The framed input.

No seat sees any other seat's output, the roster, or the seat list. This
boundary is non-negotiable — independence is the whole point of the topology.

### Parallel — Stage 2: anonymized peer review (FULL MODE ONLY)

In quick mode, perform ONLY item 2 below (the shuffle) and skip the
reviewer fan-out entirely. In full mode:

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

### Parallel — Stage 3: devil's advocate, then chairman synthesis

In full mode, two spawns, strictly in order (the harvested protocol
requires the attack to be a SEPARATE voice, not the chairman attacking its
own draft). In quick mode, skip 3a — chairman only.

**3a — devil's advocate (FULL MODE ONLY).** Spawn ONE sub-agent on a strong
model with the framed input + all anonymized responses + all peer reviews,
instructed to: state the emerging consensus in one sentence, then make the
strongest possible case that this answer is WRONG (the three demands in
`references/protocol.md` §2). If there is no consensus, it says so and
attacks the leading position instead.

**3b — chairman (ALWAYS).** Spawn the `chairman` seat (persona file
`agents/chairman.md`, strong model unless the roster overrides) with:

1. The framed input.
2. All anonymized responses (labels intact, **mapping withheld**).
3. All peer reviews (full mode; absent in quick mode).
4. The devil's-advocate attack from 3a (full mode; absent in quick mode) —
   when present, the chairman must rebut or concede it explicitly before
   finalizing the verdict.
5. One status line: `Mode: <quick|full> · Topology: <parallel|staged>` —
   so the synthesis can note the assurance level (header formatting is the
   calling skill's job, not the engine's).

### Staged — sequential stage groups

Full execution detail lives in `references/topologies.md` § Staged. The
contract in brief:

1. Stage groups execute sequentially, hard boundaries between stages.
2. All seats within one stage group spawn in ONE message; same-stage seats
   never see each other's output.
3. Decoder-ring handoff: every seat in an executing stage receives the
   original framed input + ALL outputs of the **immediately preceding
   EXECUTED stage** — one stage's outputs only, never a cumulative chain
   (attributed by display name — staged handoff is deliberately NOT
   anonymous). In quick mode "preceding executed stage" skips over
   stages that didn't run, and a partially-run stage hands off only the
   outputs of the seats that actually ran. The first executing stage has
   no predecessor: it receives the framed input only.
4. Quick mode: stage groups with no `quick_seats` members are skipped
   whole; within a surviving stage, only its quick seats run.
5. After the final stage: full mode runs the anonymized shuffle → peer
   review → devil's advocate → chairman tail (identical machinery to
   parallel stages 2–3); quick mode runs shuffle → chairman only.
6. Failure rule: one retry per failed spawn, then STOP naming the seat AND
   stage index. A failed stage never feeds a partial handoff forward.

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
