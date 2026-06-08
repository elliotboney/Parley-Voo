---
name: Parley Voo
status: final
created: 2026-06-05
updated: 2026-06-05
sources:
  - {planning_artifacts}/prds/prd-parley_voo-2026-06-04/prd.md
  - {planning_artifacts}/prds/prd-parley_voo-2026-06-04/addendum.md
  - {planning_artifacts}/ux-designs/ux-parley_voo-2026-06-05/.decision-log.md
---

# Parley Voo — Experience Spine

> Terminal-first product inside Claude Code. No GUI app. Three UX surface classes: in-session conversation (commands/flow), emitted markdown documents (the primary UI), and targeted HTML artifacts (select → Copy Prompt → paste back). Paired with `DESIGN.md`. Design signature: **negative space** — defined by what is ignored, withheld, and stripped.

## Foundation

Form factor: a **Claude Code session (terminal)**. Commands are the navigation; emitted markdown documents are the primary interface; targeted interactive HTML artifacts are a secondary surface used only where clicking beats typing. There is no UI system framework — no React, no shadcn, no native shell. `DESIGN.md` is the visual identity reference (terminal-markdown conventions for documents; full token set for artifacts).

State lives in the **session and the SQLite/markdown store**, never in an artifact. HTML artifacts are stateless: they collect a selection and hand a prompt back. The deliberation engine is usable standalone (FR8) and exportable in a portable format (FR9); the coach pipeline is the engine plus profiles, memory, and the feedback loop.

Defaults follow config posture: ADHD Specialist + Execution Realist ON locally, OFF in the public template (FR15); quick mode is the default outside `/evaluate` (FR4).

## Information Architecture

**Commands are the navigation. Documents and HTML artifacts are the surfaces.**

| Command / surface | Reached from | Surface produced | Primary FRs |
|---|---|---|---|
| `/evaluate <transcript>` | session | Pattern report doc + profile-update docs | FR1, FR10–12, FR22–24, FR27 |
| `/advise <goal> <person>` | session | Playbook doc | FR2, FR4, FR13–14, FR28 |
| `/council <decision>` | session | Verdict doc | FR3, FR4, FR5–6 |
| Roster override | flag on `/advise`,`/council`,`/evaluate` | Roster-picker HTML artifact → Copy Prompt | FR17, FR7 |
| persona create / edit / research | session | Persona-editor flow + persona-picker artifact | FR16, FR18 |
| `/export-profile <name> [--archetype]` | session | Export-preview doc (stripped fields shown) + portable markdown file | FR19, FR29, FR32 |
| `/import-profile <file>` | session | Import-summary doc with provenance | FR30 |
| `/export-council <name>` / `/import-council <file>` | session | Portable council/persona-set file; import-summary doc | FR9 |
| Outcome scoring | follow-up after `/advise` → `/evaluate` | Outcome-score HTML artifact → Copy Prompt | FR25, FR27 |
| Profile view | session | Profile doc (confidence + attribution + track record) | FR20–21, FR25, FR28 |
| Fork / clean-template | git clone + `scripts/verify-clean-fork` | Empty-state docs; responsible-use README | FR31, FR32, FR15 |

Citation refs (FR12) are a cross-cutting primitive present in every document, not a surface of their own. Computed-evidence features (FR23 linguistic script, FR24 BFI scoring, FR25 calibration, FR26 sqlite-vec recall) have **no direct user surface** — they surface *through* the documents that consume them (numbers in the pattern report, track records in the playbook, citations everywhere). Listed here so none is orphaned; see Open Questions for the one boundary case.

→ Composition reference: `DESIGN.md` (token names, document anatomy). Spine wins on conflict.

## Voice and Tone

Microcopy and document voice. Aesthetic posture lives in `DESIGN.md`.

**Direct strategist.** Terse, confident; uncertainty lives in confidence scores, never in prose (decision log).

| Do | Don't |
|---|---|
| "Lead with the cost to him, not the upside to you." | "You might want to perhaps consider possibly leading with..." |
| "high (0.82) — he disengages when pitched cold `[2026-05-12 1:1, T17]`" | "He seems like he could be someone who maybe shuts down sometimes." |
| "What you lose: the warm open. He'll read it as transactional." | (omitting the downside to keep the plan looking clean) |
| "Red Team: batting .71 on Chris (n=14)." | "Our advanced AI is highly confident this will work! 🎯" |
| "Dissent: Negotiation Architect would wait a week." | (smoothing the minority view out of the verdict) |
| "Interpreted from 6 transcripts — a read, not a fact." | Dossier voice: "Chris said X on Tuesday and Y on Thursday." |

ADHD-fit: every document front-loads the actionable; no congratulatory padding; RSD-aware framing (Execution Realist coaches in the negative — what *not* to do under pressure, FR13).

## Trust & Disclosure Patterns

Product-specific. Responsible use, falsifiability, and privacy are first-class behaviors, not footnotes.

- **Falsifiability surface (FR21).** Every profile claim carries attribution (`— Seat, method`), confidence (`word (0.NN)`), and a track record where one exists. A profile document opens with an "interpreted, not fact" line. Never rendered as a dated dossier of private anecdotes.
- **Two-layer boundary (FR19).** Subject layer (portable traits) and relationship layer (private quotes/incidents/outcomes) are split at storage time. Documents may show both to the owner; exports show subject only.
- **Export sanitization (FR29).** `/export-profile` previews show **what is stripped** before writing — relationship-layer fields rendered with the `stripped` marker from `DESIGN.md`. Named is default; `--archetype` anonymizes for public safety. Output is headed "starting hypothesis, not a verdict."
- **Import provenance (FR30).** Imported profiles are tagged `imported · source · date` and kept side by side with the user's own read — never blended. "Their Chris ≠ your Chris."
- **Mutual-benefit guardrail (FR14).** Influence tactics restricted to mutual-benefit moves; Red Team flags anything that only works if the subject doesn't notice. Surfaced in the playbook as an explicit pass/flag.
- **Responsible-use note (FR32).** README states the tool improves *your* communication, urges discretion around mutual contacts, frames profiles as interpretation, and names Archetype as the public-safe default.
- **Clean-fork guarantee (FR31).** `scripts/verify-clean-fork` confirms zero private data on a fresh clone — a verifiable acceptance check, surfaced as a pass/fail in the fork's first-run experience.

## Component Patterns

Behavioral. Visual specs live in `DESIGN.md.Components`. Two key screens are mocked: [`mockups/key-playbook-terminal.html`](mockups/key-playbook-terminal.html) (Playbook) and [`mockups/key-roster-picker.html`](mockups/key-roster-picker.html) (HTML artifact). Mocks illustrate; **the spine wins on conflict**; all other surfaces are spine-only by decision.

| Component | Surface | Behavioral rules |
|---|---|---|
| **Playbook** | `/advise` doc | Top section (above the fold, FR2): plan summary · character read · past-win receipts · fallacies to avoid. Body: frame · opening line · sequence (ordered) · objections + responses · fallback · **"what you lose"** · first concrete step. Quick mode trims to top section + opening + first step; full mode adds Red Team pass and peer-reviewed detail (FR4). Trim is **announced**: the trimmed body ends with a "Trimmed in quick mode" line naming what `--full` adds (Red Team rebuttal, peer-reviewed objections, fallback) — negative space made visible. |
| **Pattern report** | `/evaluate` doc | Per-seat findings, each claim cited (FR12) or discarded. Computed numbers from the linguistic/BFI scripts shown inline (FR23–24). Closes with profile-update summary per participant (FR27). Always full panel (FR1). |
| **Profile display** | profile doc | Subject traits with confidence + attribution + track record (FR21, FR25). Known fallacies listed. "Interpreted, not fact" header. Self-profile is a first-class subject (FR20). |
| **Council verdict** | `/council` doc | "Should we do X" answer. Dissent preserved with explicit `Dissent:` label; chairman may side with a strong minority (FR6). Off-the-shelf engine, no person (FR3). |
| **Past-win receipts** | inside playbook | Dated, queryable record of what worked with this person (FR28), pulled from `advice_outcomes`. |
| **HTML artifact** | roster/persona/outcome | Stateless. User selects on a card, clicks **Copy Prompt**, pastes back into the session. Persona cards show **"Ignores:"** as prominently as method (FR11, FR18 — negative-space picking). Mock "Ignores:" copy is derived from each method's blind spot; canonical copy comes from the authored persona prompts (FR11) — swap when written. |
| **Empty-state doc** | new person / no transcripts / fresh fork | One sentence + the one next command. No skeleton, no spinner — it's a printed document. |

## State Patterns

| State | Surface | Treatment |
|---|---|---|
| Quick mode (default) | `/advise`, `/council` | Fewer experts, no peer review (FR4). Playbook trims to top section + opening + first step. Header notes `quick mode`. |
| Full mode | `--full` flag; always for `/evaluate` | All seats + anonymized peer review. Header notes `full mode`. |
| Advice recorded | after `/advise` | Plan written to `advice_outcomes`, status `awaiting outcome` (FR27). Session reminds: run `/evaluate` after the conversation. |
| Awaiting outcome | between `/advise` and `/evaluate` | Surfaced when re-advising the same person: "1 plan awaiting outcome." Offers outcome-score artifact. |
| Outcome scored | after `/evaluate` or outcome control | Calibration recomputed; track records update (Red Team batting average, Brier) (FR25). |
| Confidence lifecycle | profile doc | New claim → low; corroborated across transcripts → rises; contradicted → falls or flagged. Shown as `word (0.NN)`, never hidden. |
| Imported-profile provenance | profile doc | Permanently tagged `imported`; shown beside the native read; never merged (FR30). |
| Empty — new person | profile doc | "No profile yet. Run `/evaluate` on a transcript to start one." |
| Empty — no transcripts | `/evaluate` | "Nothing in `ingest/`. Drop a Zoom transcript there and re-run." |
| Empty — fresh fork | first run | Zero private data (verified by `scripts/verify-clean-fork`). Only archetype example profiles present. ADHD Specialist + Execution Realist OFF (FR15). Responsible-use note shown once. |

## Interaction Primitives

- **Command invocation** — slash commands are the entire control surface. Goals and people are positional args; mode is a flag (`--full`); sanitization is a flag (`--archetype`).
- **Transcript ingestion** — drop files into source-organized `ingest/` directories (`ingest/transcripts/`, `ingest/slack/`, extensible, FR22). `/evaluate` reads from there; no upload UI.
- **Copy-prompt round-trip** — open artifact in browser → select cards → **Copy Prompt** → paste into session. The only interaction loop that leaves the terminal, and it always returns to it. Artifact is stateless (`DESIGN.md`: copy-prompt-button, selectable-card).
- **Outcome scoring entry** — either a follow-up `/evaluate` (full path, updates profile + scores advice) or the lightweight outcome-score artifact (worked / partial / didn't → Copy Prompt) for a fast record without a transcript.
- **Banned:** wide tables in terminal docs, color-only meaning, dossier-style anecdote dumps, hedging prose, stateful artifacts.

## Accessibility Floor

Behavioral. Visual contrast deferred to `DESIGN.md`.

- **Never color-only meaning.** Confidence, dissent, stripped, and provenance always carry a text label/word beside any color. Terminal documents are monochrome by host convention and must be fully legible without color.
- **Screen-reader-sane markdown.** Strict heading hierarchy (`#` → `##` → `###`, no skips), real lists, no ASCII-art layout, no tables wider than they read aloud. Each document's first line states what it is.
- **HTML artifacts keyboard-operable.** Cards selectable and Copy Prompt invokable via keyboard alone; focus order matches reading order; visible focus state (`DESIGN.md` accent border).
- **Density caps** (ADHD floor): glanceable top section above the fold; one actionable line per section head; no section requires holding prior state in the reader's head.

## Inspiration & Anti-patterns

- **Lifted from BMAD brainstorming:** the interactive-HTML pattern — open in browser, select, Copy Prompt, paste back. Used only where clicking genuinely beats typing (roster/persona/outcome), never as a default surface.
- **Lifted from `ngmeyer/council-review` lineage (Karpathy LLM Council, DMAD ICLR 2025):** the three-stage independence-first deliberation protocol (FR5) — but extended to dual topology (FR7), which is the differentiator.
- **Rejected — the dossier.** A profile must never read as a dated file of private anecdotes about a named person. It is an attributed, confidence-scored, falsifiable *read*. This is the stated anti-pattern.
- **Rejected — sycophantic synthesis.** No smoothing dissent into consensus; the chairman can side with a strong minority (FR6, NFR6).
- **Rejected — confidence as vibes.** No bare adjectives ("very likely"). Confidence is always a number with a track record behind it.
- **Rejected — a GUI app.** No dashboard, no web app, no persistent UI. The terminal and its documents are the product.

## Key Flows

### Flow 1 — Elliot preps a proposal conversation with Chris (the core loop)

Protagonist: Elliot, solo user, ADHD. Goal: get Chris to back a proposal. The playbook produced here is mocked in [`mockups/key-playbook-terminal.html`](mockups/key-playbook-terminal.html) (quick mode, glanceable top section, announced trim).

1. Elliot runs `/advise "get Chris to back the new pricing proposal" Chris` (quick mode default).
2. Pipeline runs: Profile Translator builds Chris's decoder ring *and* Elliot's self decoder ring → Message Strategist ∥ Negotiation Architect ∥ Influence Tactician → Red Team → synthesis (FR13).
3. Playbook prints. Top section glanceable: plan summary, character read, **past-win receipts** ("warned-before-pitching landed last time `[2026-04-02 1:1, T9]`"), fallacies to avoid.
4. Body: frame, opening line, sequence, objections, fallback, **"what you lose"** (the warm open reads transactional), first step. Execution Realist flags Elliot's RSD risk: "Don't over-explain if he pauses — silence isn't rejection."
5. Elliot has the Zoom call.
6. He drops the transcript into `ingest/transcripts/` and runs `/evaluate chris-2026-06-05.vtt`.
7. Full panel runs; pattern report prints with cited claims and computed metrics; Chris's profile updates.
8. **Climax:** `/evaluate` scores the recorded plan — the proposal landed. Chris's confidence claims firm up, and the **Red Team batting average ticks from .71 to .73 (n=15)**. The next `/advise Chris` will reason from the sharper profile. The loop closed and the system got measurably better — visibly, in a number.

Failure: transcript missing from `ingest/` → empty-state doc: "Nothing in `ingest/`. Drop the transcript and re-run." No crash, no blocking screen.

### Flow 2 — Elliot tunes the roster before a hard verdict

The roster-picker step here is mocked in [`mockups/key-roster-picker.html`](mockups/key-roster-picker.html) (selectable cards with "Ignores:" lines, Copy Prompt round-trip).

1. Elliot runs `/council "should we drop the enterprise tier?"` with a roster-override flag.
2. A **roster-picker HTML artifact** opens in the browser. Each persona card shows its method *and* its **"Ignores:"** line — he picks experts by their blind spots (negative space).
3. He selects four seats, deselects the ADHD Specialist (not relevant to a pricing call), clicks **Copy Prompt**.
4. He pastes the prompt back into the session.
5. **Climax:** the verdict prints with **dissent preserved** — three seats say drop it, the Negotiation Architect dissents ("wait one quarter"), and the chairman sides with the strong minority. The disagreement survived synthesis instead of being smoothed into false consensus.

### Flow 3 — A forker starts clean (zero data, FR31/FR32)

Protagonist: a stranger who cloned the public template.

1. They `git clone` the template repo. `people/`, `transcripts/`, and `index.sqlite` are git-ignored — absent.
2. They run `scripts/verify-clean-fork`.
3. **Climax:** the check passes — **zero private data confirmed**. Only archetype example profiles are present; ADHD Specialist and Execution Realist are OFF by default; the responsible-use note prints once: "This improves *your* communication — not a tool to covertly profile others." The fork's negative space — everything Elliot's data *isn't* there — is the privacy guarantee made visible.
4. They run `/evaluate` on their own first transcript to begin building profiles from scratch.

## Open Questions

- **FR26 (sqlite-vec semantic recall)** has no dedicated user surface; it powers citations and past-win receipts behind the scenes. Treated as infrastructure surfaced *through* the playbook and pattern report. If a "search my history" command is wanted, it is unspecified — flag for PRD, do not invent.

### Resolved (2026-06-05)

- **FR9 command names:** `/export-council` / `/import-council` — mirrors the profile pair. FR8 (engine standalone) needs no command of its own; it is the engine reachable via `/council` without the coach pipeline.
- **Profile-browser HTML artifact:** out of scope for v1. Profile doc in terminal covers FR20–21. Logged as future.
- **Outcome scoring (FR27):** `/evaluate` of a real transcript auto-scores prior advice (primary path); the lightweight outcome-score artifact exists only for conversations with no transcript. Both are v1.
