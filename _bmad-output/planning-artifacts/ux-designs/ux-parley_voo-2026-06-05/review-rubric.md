# Spine Pair Review — parley_voo

## Overall verdict

A consumer can source-extract cleanly: all 32 FRs trace to a surface, the negative-space signature is committed consistently across both files, and the terminal/artifact dual-target convention is stated explicitly so the "no color tokens in terminal" choice reads as design, not omission. The pair is **strong-to-adequate** — downstream architecture and story-dev can build from it today. The load-bearing gaps are all aesthetic-confirm `[ASSUMPTION]`s (hues/fonts, already flagged in Open Questions) plus two real cross-file name drifts (`confidence-tag`/`confidence-chip`, `Trust & Disclosure Patterns` substituting for the canonical `State`-adjacent slot) and a set of defined-but-unnarrated dark-mode tokens. Nothing is broken; nothing load-bearing is silently undecided.

## 1. Flow coverage — strong

Checked: every UJ/FR-driven journey in the IA table against a Key Flow with named protagonist, numbered steps, a climax beat, and a failure path where applicable. The PRD has no formal UJ list, so flows were judged against the Core Loop + the three user-facing command clusters (`/advise`→`/evaluate` loop, `/council` roster tuning, clean-fork).

### Findings
- **low** Flow 2 (roster tuning) and Flow 3 (clean fork) have climax beats but no failure path, where the shadcn/Quill examples carry one per flow. Flow 2 has a plausible failure (Copy-Prompt paste-back malformed / artifact opened but nothing selected); Flow 3's failure (`verify-clean-fork` *fails* — private data leaked into the template) is arguably the most important negative-space moment in the product and is unstated. (EXPERIENCE.md L147–162). *Fix:* add a one-line failure to Flow 3: check fails → names the offending path, exits non-zero, blocks first run.
- **low** The three IA rows with no flow are the portability pair (`/export-profile`, `/import-profile`, `/export-council`, `/import-council`) and `persona create/edit/research`. These are behaviorally specified in Component Patterns / Trust & Disclosure, so absence of a dedicated flow is acceptable — noting only that export sanitization (FR29) is the second marquee negative-space beat and gets no narrated walk-through. (EXPERIENCE.md L130–162). *Fix:* optional — a short Flow 4 showing the stripped-field preview would showcase the signature; not required for extraction.

## 2. Token completeness — adequate

Checked: every key in DESIGN.md frontmatter (`colors`, `typography`, `rounded`, `spacing`, `components`) and every `{path.to.token}` reference in prose and component objects. All references resolve. Terminal typography tokens correctly use `note:` (host owns rendering) per spec convention — not a miss.

### Findings
- **medium** All seven artifact hues plus accent/surface/ink are tagged `[ASSUMPTION]` with no human-confirmed values, and no contrast targets are stated for the load-bearing artifact combinations (ink-on-surface, accent-foreground-on-accent, confidence-ramp hues against surface). Accessibility Floor defers contrast to DESIGN.md, but DESIGN.md never states a ratio or AA/AAA target. For a reading surface this is the one place a number is owed. (DESIGN.md L105–111; EXPERIENCE.md L114). *Fix:* state "artifact text targets WCAG AA (4.5:1 body, 3:1 large)" in DESIGN.md Colors or a contrast line, even while hues stay `[ASSUMPTION]` — the *target* can commit before the *hue* does.
- **low** Six dark-mode tokens are defined (`ink-dark`, `ink-muted-dark`, `surface-dark`, `surface-raised-dark`, `hairline-dark`, `accent-dark`) but never referenced in any prose section or component, and no light/dark switching rule is stated. Either artifacts support dark mode (then say where/how) or they don't (then the tokens are speculative and should be cut per the simplicity discipline). (DESIGN.md L20–25). *Fix:* add one line under Colors or Elevation stating the dark-mode posture for artifacts, or remove the unused `-dark` tokens.
- **low** `confidence-mid` (#8A6D1F), `confidence-low`, `dissent`, `confidence-high` are defined as top-level colors but the `confidence-tag` component object references only `{colors.ink}` and `{colors.ink-muted}` — the ramp hues are narrated in prose but not wired into the component token object. Resolvable (prose carries it), but a consumer extracting components mechanically won't see the ramp on the chip. (DESIGN.md L72–74, L109). *Fix:* add `ramp-high/mid/low` keys to the `confidence-tag` (or `confidence-chip`) component object.

## 3. Component coverage — adequate

Checked: every component name used anywhere, verified against DESIGN.md.Components (visual) and EXPERIENCE.md.Component Patterns (behavioral). Both spines carry real rules, not one-word stubs.

### Findings
- **medium** Name drift between files breaks clean cross-ref. DESIGN.md frontmatter calls it `confidence-tag`; DESIGN.md prose Components (terminal) calls it **Confidence tag**, then artifact prose calls it **Confidence chip**; EXPERIENCE.md uses `word (0.NN)` inline and "confidence" but names no component. A consumer can't tell if tag and chip are one component (two render targets) or two. (DESIGN.md L72, L161, L172). *Fix:* pick one name per render target explicitly — e.g. `confidence-tag` (terminal text) and `confidence-chip` (artifact), and state they are the same primitive in two targets.
- **low** EXPERIENCE.md lists **Playbook, Pattern report, Profile display, Council verdict, Past-win receipts, HTML artifact, Empty-state doc** as components; DESIGN.md Components lists **Confidence tag, Citation ref, Attribution line, Stripped marker, Track-record line, Section divider** (terminal) + **Selectable card, Copy Prompt button, Confidence chip, Provenance tag, Outcome-score control** (artifact). These are two orthogonal granularities — EXPERIENCE names *document types*, DESIGN names *primitives inside them*. That's defensible (a playbook is composed of citation refs + confidence tags + attribution lines), but it means several EXPERIENCE "components" have no DESIGN visual row and vice-versa. (EXPERIENCE.md L79–87; DESIGN.md L159–174). *Fix:* one line in either file noting the two-tier relationship (documents are composed of primitives) so the mismatch reads as intentional, not as missing rows.
- **low** `Track-record line` and `Attribution line` (DESIGN primitives) have no explicit behavioral row in EXPERIENCE Component Patterns — they appear inside Trust & Disclosure prose instead. Resolvable, but a mechanical extractor of Component Patterns misses them. (EXPERIENCE.md L63–73). *Fix:* acceptable as-is given Trust & Disclosure covers behavior; optionally add rows.

## 4. State coverage — strong

Checked: every IA surface walked for empty / cold-load / focus / error / mode states. Coverage is notably thorough for a terminal product — quick/full mode, advice-recorded, awaiting-outcome, outcome-scored, confidence lifecycle, imported provenance, and three distinct empty states (new person / no transcripts / fresh fork) are all specified.

### Findings
- **low** No explicit error/failure state for the Copy-Prompt round-trip (artifact opens but selection is empty, or paste-back is malformed). Interaction Primitives describes the happy path only. (EXPERIENCE.md L108, L89–102). *Fix:* add a State row: "Empty selection → Copy Prompt disabled / no-op" and note malformed paste-back is handled in-session.
- **low** "Focus" state for HTML artifacts is covered in Accessibility Floor (visible focus = accent border) but not in the State Patterns table; minor, since the floor carries it. (EXPERIENCE.md L118). No fix required.

## 5. Visual reference coverage — pending (expected)

`mockups/` and `wireframes/` do not exist yet; `imports/` exists and is empty. Per the brief, mocks are pending at this stage — not a failure. Both spines correctly point composition reference at `DESIGN.md` rather than non-existent mock files (EXPERIENCE.md L44 says "→ Composition reference: `DESIGN.md`"), unlike the Quill/Drift examples which reference `mockups/*.html`. This is the right call given mocks don't exist.

### Findings
- **low** When mocks are produced, the two marquee negative-space moments (export stripped-field preview, persona-card "Ignores:" line) and the confidence ramp are the highest-value artifacts to mock first — they are the visual claims a reader most needs to see honored. *Fix:* note this as guidance for the mock pass; no action now.

## 6. Bloat & overspecification — strong

EXPERIENCE.md prose is behavioral and terse, no editorial voice, no pixel specs (correctly defers all visual values to DESIGN.md). DESIGN.md carries editorial voice appropriately (Brand & Style, Colors narration) — within its license. No source restatement beyond necessary FR anchoring. Tables used where tables fit. No decorative narrative untied to a decision.

### Findings
- **low** EXPERIENCE.md Flow climaxes carry light narrative flourish ("She picks up her coffee" is absent here — good — but "the loop closed and the system got measurably better — visibly, in a number" L143 and "the fork's negative space ... made visible" L161 edge toward editorializing in the experience spine). Defensible as climax-beat color, but the brief says EXPERIENCE prose should not carry editorial voice. (EXPERIENCE.md L143, L161). *Fix:* trim the closing editorial sentence on each climax to the observable system fact; minor.

## 7. Inheritance discipline — strong

`sources` frontmatter resolves to the three real files (prd.md, addendum.md, .decision-log.md — all present). All 32 FRs are cited by number and trace to actual PRD requirements. FR-name usage is by-number (PRD has no prose UJ names to copy verbatim), which is the correct inheritance form for this PRD. EXPERIENCE token references (`word (0.NN)`, `stripped` marker, accent border) resolve to DESIGN tokens/conventions by name.

### Findings
- **low** EXPERIENCE.md L86 cites "(FR11, FR18 — negative-space picking)" for the persona-card "Ignores:" line; FR11 is the *runtime orthogonality* prohibition and FR18 is *distinct named method*. The "Ignores:" UI surfacing is a reasonable derivation but is not literally in FR11/FR18 — it's an inference. Sound, but flag it as derived not stated. (EXPERIENCE.md L86, L150). No fix needed; correctly traceable.

## 8. Shape fit — strong

DESIGN.md sections are in canonical order: Brand & Style → Colors → Typography → Layout & Spacing → Elevation & Depth → Shapes → Components → Do's and Don'ts, then an earned `Open Questions`. EXPERIENCE.md carries all required defaults: Foundation, IA, Voice and Tone, Component Patterns, State Patterns, Interaction Primitives, Accessibility Floor, Key Flows — plus Inspiration & Anti-patterns and an invented `Trust & Disclosure Patterns`.

### Findings
- **low** Invented section `Trust & Disclosure Patterns` (EXPERIENCE.md L63) earns its place — falsifiability, two-layer boundary, sanitization, provenance, and responsible-use are genuinely first-class product behaviors and don't fit cleanly in any default section. Good call. Noting only that it absorbs behavioral spec for `Attribution line` / `Track-record line` that a reader might look for in Component Patterns (see 3). No fix.

## Mechanical notes

- **Name inconsistency (medium):** `confidence-tag` (frontmatter) vs "Confidence tag" (terminal prose) vs "Confidence chip" (artifact prose). Resolve to an explicit one-primitive-two-targets statement.
- **Unused tokens (low):** six `*-dark` color tokens defined, zero references, no dark-mode rule stated. Decide in or out.
- **Component-object gap (low):** confidence ramp hues (`confidence-high/mid/low`, `dissent`) narrated in prose but not wired into the `confidence-tag` component token object.
- **Cross-ref integrity:** all `{path.to.token}` references resolve; all three `sources` files exist; all 32 FRs + NFR6 cited and traceable. No broken references.
- **Frontmatter completeness:** both files carry `name`/`status`/`created`/`updated`; EXPERIENCE carries `sources`. DESIGN.md lacks a `sources` key (the spec doesn't require one for DESIGN.md; EXPERIENCE carries the inheritance) — acceptable.
- **Visual refs:** `mockups/`, `wireframes/` missing (pending); `imports/` empty (pending). Expected at this stage.
