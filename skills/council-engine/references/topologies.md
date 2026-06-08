# Topologies

Topology is declared per-roster (`topology:` in the roster file's
frontmatter), never per-command. The engine dispatches on that value.

## Parallel

Three stages. Stage boundaries are hard — no stage starts until the
previous one fully completes, and no information crosses a boundary except
as specified.

### Stage 1 — independent fan-out

- All seats spawn in ONE message (one sub-agent call per seat).
- Each seat receives: its own persona body + the sycophancy guardrail
  (`protocol.md` §3) + the framed input. Nothing else.
- Isolation invariants:
  - No seat sees another seat's output.
  - No seat knows the roster, the seat count, or that other seats exist.
  - Sequential spawning is a protocol violation, not a style choice —
    earlier responses contaminate later ones.

### Stage 2 — anonymized peer review

- Shuffle the stage-1 responses; relabel A, B, C… (one label per
  participating seat). The seat→label mapping is randomized per run and
  never disclosed to reviewers or the chairman.
- Fan out reviewers in one message. The reviewers are the participating
  seats themselves — each persona body is its review lens. Each reviewer
  gets the framed input + ALL anonymized responses + the conformity check
  (`protocol.md` §4).
- Anonymity means each seat unknowingly reviews its own response too —
  acceptable by design: the chairman weighs reasoning, not votes.
- Reviewers judge reasoning quality per response and flag
  consensus-by-conformity.

### Stage 3 — devil's advocate, then chairman synthesis

- Spawn 3a: ONE devil's advocate on a strong model — states the emerging
  consensus in one sentence, then attacks it (`protocol.md` §2). A separate
  voice, never the chairman attacking its own draft.
- Spawn 3b: the `chairman` persona on a strong model (roster can override).
  Input: framed input + anonymized responses + all peer reviews + the
  devil's-advocate attack. Mapping withheld — dissent is attributed by
  response label; the engine substitutes `— {Display Name}, {method}`
  when rendering.
- The chairman must rebut or concede the attack explicitly, then renders
  the output contract (`protocol.md` §5).
- Dissent preservation is the success criterion: a minority position must
  appear under an explicit `Dissent:` label, and the chairman may side
  with the minority outright.
- Any spawn in any stage that returns empty/errors gets ONE retry, then
  the run stops naming the seat/stage — no partial councils.

## Staged

Sequential pipeline with a decoder-ring handoff (FR7, FR13). Used for
`/advise`-style work where downstream seats must build ON an upstream
seat's read, not reason independently of it.

### Roster shape

When `topology: staged`, the roster's `seats` is an ordered list of
**stage groups** (a list of lists). When `topology: parallel`, it stays a
flat list. Both shapes are part of the portable roster contract (FR9):

```yaml
---
topology: staged
seats:
  - [profile-translator]
  - [message-strategist, negotiation-architect, influence-tactician]
  - [red-team]
quick_seats: [profile-translator, message-strategist]
model_overrides:
  chairman: strong-model
---
```

The chairman is implicit in both topologies — never listed in `seats` or
any stage group; the engine always appends chairman synthesis. A roster
that lists `chairman` as a seat fails closed.

> Forward pointer (Story 2.3): a seat that must run twice in one stage
> (Profile Translator ×2 — subject and self, FR13) collides with the
> duplicate-seat STOP. 2.3 owns resolving that (two persona files or a
> stage-level repeat param). Until then, duplicates anywhere STOP.

### Execution

- Stage groups execute **sequentially** with hard boundaries: stage N+1
  does not start until every seat in stage N has returned.
- **Intra-stage parallelism:** all seats within one stage group spawn in
  ONE message — same single-message rule as parallel stage 1. Seats in
  the same stage never see each other's output.
- **Decoder-ring handoff:** every seat in stage N+1 receives the original
  framed input + ALL outputs of stage N — the prior stage ONLY, not a
  cumulative chain. A stage that needs earlier context must carry it
  forward in its own output; that forward-carry IS the decoder-ring
  discipline.
- **Handoff is attributed, not anonymous.** Stage outputs pass downstream
  WITH display names — the decoder ring only works if downstream seats
  know what they are building on. This is a deliberate contrast with the
  parallel topology's isolation invariant, not an inconsistency to fix:
  parallel protects independent first reads; staged builds a pipeline on
  purpose. Anonymization applies only at the post-pipeline review and
  synthesis step below.
- **Failure rule per stage:** one retry per failed spawn, then STOP naming
  the seat AND the stage index (e.g. `Seat 'red-team' returned no response
  in stage 3 after one retry.`). A failed stage never lets the pipeline
  continue with a partial handoff.

### Full-mode tail

After the last stage group completes (full mode only):

1. Anonymized shuffle over ALL seat outputs from the whole run — one
   label per seat response, randomized mapping, withheld downstream.
2. Peer-review fan-out (reviewers are the participating seats, one
   message, conformity check included) — same machinery as parallel
   stage 2.
3. Devil's advocate, then chairman synthesis — same as parallel stage
   3a/3b, including label-based dissent attribution with engine-side
   substitution.

In quick mode the pipeline runs trimmed (see SKILL.md mode rules) and
this tail reduces to shuffle + chairman only.

## Modes

Mode is an engine input (default `quick`; callers forward the user's
`--full` flag). What each mode MEANS comes from the roster — never from
the command:

- **Quick (default):** only `quick_seats` execute; peer-review fan-out
  and the separate devil's-advocate spawn are SKIPPED (NFR2 — debate only
  where it earns its token cost); the anonymization shuffle is KEPT (zero
  spawn cost, preserves the chairman's anti-deference boundary); chairman
  synthesis always runs and notes the reduced assurance.
- **Full (`--full`):** all seats + anonymized peer review + devil's
  advocate + chairman.
- **Staged quick:** a stage group whose intersection with `quick_seats`
  is empty is skipped entirely; the handoff flows from the last
  non-skipped stage to the next; stage order is preserved.
