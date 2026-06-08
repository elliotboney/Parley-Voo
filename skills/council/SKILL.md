---
name: council
description: "/council — get a dissent-preserving council verdict on any decision. Use when the user runs /council \"should we do X\" (optionally --full). Generic decisions only; no person, no profiles."
---

# /council — Generic Verdicts

Runs the deliberation engine on a decision and prints a verdict document.
Zero setup: no profiles, no transcripts, no database (FR3, FR8).

## Inputs

- **The decision** — the quoted argument, e.g. `/council "should we drop
  the enterprise tier?"`. If no decision text was given, ask for one in a
  single line; do not guess.
- **`--full` (optional)** — escalate to full mode.

## Step 1: Resolve mode — forward, never decide

Default is quick. If the user passed `--full`, the mode is full. That is
the ENTIRE mode logic this command owns: what each mode means (which
seats, peer review, devil's advocate) is defined by the council-engine
skill and the roster — never here (the engine's hard rule).

## Step 2: Run the engine

Invoke the **council-engine** skill with:

1. Roster: `councils/council-default.md`
2. Framed input: the decision text, verbatim — do not editorialize it
3. Mode: from Step 1

The engine owns everything orchestral: roster validation, model tiers,
seat fan-out, anonymized shuffle, peer review and devil's advocate (full
mode), chairman synthesis, and the dissent-attribution substitution
(`— {Display Name}, {method}`).

**Standalone guarantee (FR8) — hard rule:** this command reads NOTHING
beyond the roster, the persona files, and the engine skill. Never read
`people/`, `transcripts/`, `index.sqlite*`, or any `memory/` directory.
No person context exists in a generic verdict. A fresh clone with none of
those present must run clean.

## Step 3: Render the verdict document

Wrap the chairman's synthesis in the document shell:

```
# Verdict: <the decision, verbatim>

Council verdict — <quick mode (N seats, no peer review) | full mode
(N seats + anonymized peer review)>. Dissent preserved.

<chairman's seven sections, ### headings>
```

- One `#` title per document; the first line under it states what the
  document is and the mode — that line IS the mode header (AC: header
  notes `quick mode`/`full mode`).
- The body is the chairman's output contract, exactly seven `###`
  sections: Agrees / Clashes / Blind Spots / Recommendation / What You
  Lose / Do This First / Verify.

## Step 4: Render-check — verify before printing

Mechanically check the assembled document and fix violations before it
reaches the user (known model wobbles, observed live):

1. **Confidence format:** every confidence reads `word (0.NN)` — e.g.
   `high (0.82)`. Never a bare number, never a bare word, never `8 of 10`.
   Rewrite violations in place.
2. **Dissent attribution:** every `Dissent:` line carries
   `— {Display Name}, {method}` (the engine's substitution applied; no raw
   `— Response B` labels may survive to the user).
3. **Heading discipline:** one `#`, then `###` sections only; nothing
   deeper; no heading levels skipped.
4. **No extra sections:** exactly the seven contract headings. If the
   chairman emitted a stray section (e.g. a devil's-advocate answer),
   fold its content into Clashes and delete the heading.
5. **No wide tables:** two-column ≤ ~60-char rows or labeled lists.

Then print the document. The verdict is the deliverable — no commentary
before or after it.
