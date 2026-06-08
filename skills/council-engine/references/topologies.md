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

> Story 1.3 — not yet implemented. This heading is a stub so 1.3 extends
> this document rather than restructuring it.
