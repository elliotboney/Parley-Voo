---
name: Parley Voo
description: Terminal-first communication coach inside Claude Code. Two render targets — emitted markdown documents (the primary UI) and restrained negative-space HTML artifacts for select-and-copy interactions. Identity is defined by what is stripped.
status: final
created: 2026-06-05
updated: 2026-06-05
colors:
  ink: '#1A1B1F'
  ink-muted: '#6B6560'
  ink-faint: '#9A938B'
  surface: '#FBFAF7'
  surface-raised: '#FFFFFF'
  hairline: '#E7E3DB'
  accent: '#2F5D50'
  accent-foreground: '#FFFFFF'
  confidence-high: '#2F5D50'
  confidence-mid: '#8A6D1F'
  confidence-low: '#9A938B'
  dissent: '#7A3B2E'
  stripped: '#B7B0A6'
  ink-dark: '#ECE9E3'
  ink-muted-dark: '#A39C93'
  surface-dark: '#16181C'
  surface-raised-dark: '#1F2227'
  hairline-dark: '#2C2F35'
  accent-dark: '#7FB3A2'
typography:
  doc-h1:
    note: 'Terminal markdown — rendered as # by the host. No font control; weight/size owned by terminal.'
  doc-h2:
    note: 'Terminal markdown — rendered as ## by the host.'
  body:
    note: 'Terminal markdown — host-rendered prose. Plain text, no inline color.'
  citation:
    note: 'Terminal markdown — inline code span for refs, e.g. `[2026-05-12 1:1, T17]`.'
  artifact-display:
    fontFamily: "'Newsreader', Georgia, serif"
    fontSize: 28px
    fontWeight: '400'
    lineHeight: '1.2'
    letterSpacing: -0.01em
  artifact-body:
    fontFamily: "'Inter', system-ui, sans-serif"
    fontSize: 15px
    fontWeight: '400'
    lineHeight: '1.6'
  artifact-mono:
    fontFamily: "'JetBrains Mono', ui-monospace, monospace"
    fontSize: 13px
    fontWeight: '400'
    lineHeight: '1.5'
  artifact-label:
    fontFamily: "'Inter', system-ui, sans-serif"
    fontSize: 11px
    fontWeight: '500'
    lineHeight: '1.4'
    letterSpacing: 0.08em
rounded:
  sm: 4px
  md: 8px
  full: 9999px
spacing:
  '1': 4px
  '2': 8px
  '3': 12px
  '4': 16px
  '5': 24px
  '6': 40px
  artifact-gutter: 24px
  artifact-section-gap: 40px
components:
  confidence-tag:
    foreground: '{colors.ink}'
    label-color: '{colors.ink-muted}'
    ramp-high: '{colors.confidence-high}'
    ramp-mid: '{colors.confidence-mid}'
    ramp-low: '{colors.confidence-low}'
  selectable-card:
    background: '{colors.surface-raised}'
    border: '{colors.hairline}'
    radius: '{rounded.md}'
    selected-border: '{colors.accent}'
  copy-prompt-button:
    background: '{colors.accent}'
    foreground: '{colors.accent-foreground}'
    radius: '{rounded.sm}'
  stripped-marker:
    foreground: '{colors.stripped}'
---

## Brand & Style

Parley Voo lives in a terminal. The primary interface is not a screen — it is the **emitted document**: a playbook, a pattern report, a profile, a council verdict, printed as markdown into the session that generated it. The visual identity is therefore mostly typographic discipline and structural restraint, not chrome.

The signature is **negative space**. Experts are defined by what they ignore; coaching by what *not* to do; exports by what is stripped. The design must make absence legible — a stripped field is shown as stripped, a "what you lose" section is as prominent as the plan, a confidence gap is visible rather than smoothed over. Empty is information.

Voice is the **direct strategist**: terse, confident, no hedging in prose. All uncertainty is pushed into explicit confidence scores and track records. The layout never apologizes, never pads, never buries the actionable line.

Two render targets, one identity:

1. **Terminal markdown** (primary) — every emitted document. Owns heading hierarchy, emphasis rules, list/table discipline, the citation ref format, the confidence-score convention, section dividers. No color control (the host terminal owns rendering); meaning must survive monochrome.
2. **HTML artifacts** (secondary) — the BMAD select → Copy Prompt → paste-back pattern, used only where clicking beats typing (roster/persona picking, advice-outcome scoring). Full token set applies here. Restrained, paper-white, one accent.

## Colors

Color exists **only in HTML artifacts**. Terminal documents are monochrome by host convention and must never depend on color for meaning (see Do's and Don'ts).

- **Ink (`#1A1B1F`)** — primary text on artifacts. Near-black, slightly warm.
- **Ink-muted / Ink-faint** — secondary text and metadata (attributions, line refs, timestamps). The falsifiability furniture sits here: present, readable, never shouting.
- **Surface (`#FBFAF7`)** — warm off-white canvas. Paper, not app. Reduces the clinical feel; reinforces "document."
- **Accent (`#2F5D50`, muted pine)** — the single chromatic color. Used for the active selection state and the Copy Prompt action — the two things the user is there to *do*. Never decorative, never a state-badge palette. The constraint "one restrained accent, used only on select + copy" is from the negative-space signature.
- **Confidence ramp (high pine / mid ochre / low faint)** — the *only* place a second and third hue appear, and only as a redundant channel beside the always-present numeric score and word label. Color never carries confidence alone.
- **Dissent (`#7A3B2E`, faded brick)** — marks a preserved minority position in a council-verdict artifact. Reinforces "dissent survived synthesis." Redundant with an explicit `Dissent:` label.
- **Stripped (`#B7B0A6`)** — the negative-space color. Marks fields that are *removed* in an export preview (relationship-layer content, named anecdotes) — shown struck/greyed so the user sees what leaves.

Avoid: a category palette (no "Behavioral = blue, Psycholinguist = green"), gradients, saturated fills, success-green / error-red form chrome. This is a reading surface, not a dashboard.

**Contrast target:** every text-on-surface combination in artifacts meets WCAG AA (4.5:1 body, 3:1 large text / UI borders). `ink-faint` and `stripped` are metadata-only and never carry load-bearing text.

## Typography

### Terminal markdown (primary target — rules, not fonts)

The terminal owns fonts, sizes, and weights. The spec here is **structural**, enforced in every emitted document. Illustrated by [`mockups/key-playbook-terminal.html`](mockups/key-playbook-terminal.html) — the playbook's terminal markdown rendering (heading hierarchy, inline citation spans, confidence convention). Mocks illustrate; **the spine wins on conflict**; all other surfaces are spine-only by decision.

- **Heading hierarchy** — `#` document title (one per document), `##` major sections, `###` sub-sections. Never skip a level. Never go below `###` in a terminal document; deeper nesting does not render distinctly and breaks glanceability.
- **Emphasis** — `**bold**` for the single load-bearing word or the section's verdict; never for whole sentences. Italic reserved for the "interpreted, not fact" disclaimers and quoted transcript fragments. No ALL-CAPS runs (screen-reader hostile, shouty).
- **Citations** — inline code span, compact, always visible: `` `[2026-05-12 1:1, T17]` ``. Date · context · turn (speaker-turn ID in the canonical transcript — survives reformatting; architecture decision 2026-06-05). Code-span styling makes them scannable and skippable in one pass without breaking prose flow.
- **Confidence display** — fixed convention: `word (0.NN)` — e.g. `high (0.82)`, `low (0.31)`. Word first for the skim, number for the audit. Always paired; never a bare adjective, never a bare number.
- **Lists** — bullets for parallel items, numbers only for ordered sequences (the playbook's `sequence` and `first step`). Cap nesting at one level.

### HTML artifacts (secondary target — full type system)

- **artifact-display** (Newsreader serif, 28px) — the one editorial moment: the subject's name on a profile artifact, the decision question on a council artifact. A punctuation mark, not the default voice.
- **artifact-body** (Inter, 15px) — all artifact prose.
- **artifact-mono** (JetBrains Mono, 13px) — transcript line refs, scores, the prompt text shown in/near the Copy Prompt button. Signals "this is machine-bound text."
- **artifact-label** (Inter, 11px, tracked 0.08em) — section labels, confidence labels, the `STRIPPED` / `DISSENT` tags.

## Layout & Spacing

### Terminal documents

- **Glanceable top section first.** The playbook's plan summary / character read / past-win receipts / fallacies-to-avoid live above the fold and must read without scrolling past the first screen. The first line is the most actionable line.
- **No wide tables.** Terminal wrapping destroys multi-column tables. Use short two-column tables only (≤ ~60 char rows) or fall back to labeled lists. Anatomy sections are vertical stacks, never grids.
- **Section dividers** — a single `---` horizontal rule between major sections of long documents (playbook, pattern report). Sparingly; whitespace does most of the separating.
- **Density cap (ADHD rule).** Each section front-loads its one actionable sentence, then optional detail. A section that needs a full screen gets a one-line summary at its head.

### HTML artifacts

- Single column, `max-width ~720px`. Generous `{spacing.artifact-section-gap}` (40px) between sections; `{spacing.artifact-gutter}` (24px) inside. The artifact is a focused picker, not a dashboard — never multi-pane. Illustrated by [`mockups/key-roster-picker.html`](mockups/key-roster-picker.html) — the roster-picker artifact's single-column layout, card spacing, and sticky Copy Prompt.
- The Copy Prompt action is **always visible** (sticky footer or top-right), because it is the only exit back into the session.

## Elevation & Depth

Effectively none. Terminal documents have no z-axis. HTML artifacts use **tone, not shadow**: selectable cards sit on `{colors.surface-raised}` against `{colors.surface}`, separated by a `{colors.hairline}` 1px border. The only depth cue is the selected state — a `{colors.accent}` border, not a shadow or a fill. Hierarchy comes from type and space.

## Shapes

- Terminal: N/A (text).
- HTML artifacts: `{rounded.sm}` (4px) for buttons and inputs, `{rounded.md}` (8px) for selectable cards. `{rounded.full}` only on the confidence tag (artifact rendering) and provenance tag. Crisp, document-like; no consumer-app pill buttons.

## Components

These are **primitives**. The document types named in `EXPERIENCE.md.Component Patterns` (playbook, pattern report, profile, verdict) are *composed* of them — there is no separate visual spec per document type.

### Terminal-document components (primary)

These primitives compose the playbook shown in [`mockups/key-playbook-terminal.html`](mockups/key-playbook-terminal.html).

- **Confidence tag** — `word (0.NN)` inline. Sits immediately after the claim it qualifies, never in a separate legend. This is the load-bearing falsifiability primitive.
- **Citation ref** — `` `[date context, Tnn]` `` inline code span (Tnn = speaker-turn ID). Every expert claim carries one or the chairman discards it (FR12).
- **Attribution line** — `— {Seat name}, {method}` after a claim or section, so the reader knows *which expert and which discipline* produced it (falsifiability: interpreted, not fact).
- **Stripped marker** — in `/export-profile` previews, removed fields render as `~~field~~ (stripped: relationship layer)` so the user sees the negative space leave. Strikethrough survives monochrome.
- **Track-record line** — e.g. `Red Team: batting .71 on Chris (n=14) · Brier 0.19`. Plain text, always with sample size.
- **Section divider** — `---` between major sections only.

### HTML-artifact components (secondary)

These primitives compose the roster picker shown in [`mockups/key-roster-picker.html`](mockups/key-roster-picker.html).

- **Selectable card** — `{components.selectable-card}`. A persona, roster seat, or profile. Click toggles selection (`{colors.accent}` border). Negative-space detail: each persona card shows an **"Ignores:"** line as prominently as its method — you pick experts by their blind spots. Mock "Ignores:" copy is derived from each method's blind spot; canonical copy comes from the authored persona prompts (FR11) — swap when written.
- **Copy Prompt button** — `{components.copy-prompt-button}`. The round-trip exit. Emits the constructed prompt to the clipboard; artifact holds no state of its own (the session does).
- **Confidence tag (artifact rendering)** — the same primitive as the terminal confidence tag, rendered as a `{rounded.full}` chip: word + number + redundant ramp color (`{components.confidence-tag}`). Never color-only. One primitive, two render targets.
- **Provenance tag** — on imported-profile artifacts: `imported · {source} · {date}` chip, visually distinct from native data so "their Chris ≠ your Chris" is unmistakable (FR30).
- **Outcome-score control** — for advice-outcome scoring: a small ordinal picker (worked / partial / didn't), each option a selectable card; Copy Prompt sends the score back. No free-text required to record an outcome.

## Do's and Don'ts

| Do | Don't |
|---|---|
| Put the most actionable line first; keep the glanceable top section above the fold | Bury the opening line, plan summary, or first step below a screen of preamble |
| State every trait with a confidence `word (0.NN)` and a source attribution | State a trait without a confidence and a source (no un-attributed "facts") |
| Make absence visible — render stripped fields as struck, give "what you lose" its own section | Silently omit what was removed, or smooth a confidence gap into prose |
| Push all uncertainty into confidence scores; keep prose terse and confident | Hedge in prose ("might possibly perhaps") — hedging lives in the number |
| Carry redundant text/label beside any color in artifacts | Encode confidence, dissent, or category by color alone (terminal is monochrome) |
| Preserve dissent with an explicit `Dissent:` label in verdicts | Synthesize minority positions away into false consensus |
| One accent, used only on select + Copy Prompt | Use accent decoratively, or add a per-expert category palette |
| Cap heading depth at `###`, cap list nesting at one level | Use wide multi-column tables or deep nesting that breaks terminal wrapping |
| Frame exports as "starting hypothesis" and tag imports with provenance | Render a profile as a dossier of named, dated anecdotes about a person |

## Open Questions

None outstanding for the visual identity.

### Resolved (2026-06-05)

- **Palette (accent, surface, confidence ramp, dissent, stripped hues):** approved by Elliot from the roster-picker key-screen mock, 2026-06-05 — pine `#2F5D50` accent on warm paper `#FBFAF7`, one-accent rule.
- **Font stacks (Newsreader / Inter / JetBrains Mono):** approved by Elliot from the roster-picker key-screen mock, 2026-06-05 — one serif display moment, sans body, mono for machine text.
- Profile-browser HTML artifact: out of scope for v1 (decision log). The provenance tag component applies to imported-profile data wherever it renders.
