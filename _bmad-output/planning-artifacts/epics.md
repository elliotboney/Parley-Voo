---
stepsCompleted: [1, 2, 3, 4]
status: 'validated'
inputDocuments:
  - '_bmad-output/planning-artifacts/prds/prd-parley_voo-2026-06-04/prd.md'
  - '_bmad-output/planning-artifacts/prds/prd-parley_voo-2026-06-04/addendum.md'
  - '_bmad-output/planning-artifacts/architecture.md'
  - '_bmad-output/planning-artifacts/ux-designs/ux-parley_voo-2026-06-05/DESIGN.md'
  - '_bmad-output/planning-artifacts/ux-designs/ux-parley_voo-2026-06-05/EXPERIENCE.md'
  - '_bmad-output/planning-artifacts/research/technical-research-computed-evidence-2026-06-05.md'
  - '_bmad-output/planning-artifacts/research/domain-research-psych-methods-2026-06-05.md'
---

# parley_voo - Epic Breakdown

## Overview

This document provides the complete epic and story breakdown for parley_voo, decomposing the requirements from the PRD, UX Design if it exists, and Architecture requirements into implementable stories.

## Requirements Inventory

### Functional Requirements

**Modes & Commands**

FR1: `/evaluate` — input: a transcript; output: a pattern report plus profile updates for participants. Always runs the full parallel panel. A mid-conversation transcript is a valid input (the "halftime report") with no special handling.
FR2: `/advise` — input: a goal plus a person; output: a playbook. Top section: quick plan summary, character read, past-win receipts, fallacies to avoid. Body: frame, opening line, sequence, objections + responses, fallback, "what you lose," first concrete step.
FR3: `/council` — input: a generic decision, no person; output: a "should we do X" verdict from the off-the-shelf engine.
FR4: Cost tiers: quick mode (fewer experts, no peer review) is the default for `/advise` and `/council`; a `--full` flag escalates. `/evaluate` always runs full panel.

**Deliberation Engine**

FR5: Three-stage protocol: independent parallel analysis (experts never see each other's responses) → anonymized peer review (responses shuffled, labeled A–E) → chairman synthesis.
FR6: Synthesis distinguishes value tensions from error catches, preserves dissent rather than smoothing to consensus, and may side with a minority whose reasoning is strongest.
FR7: Engine supports two topologies: all-parallel (`/evaluate`) and staged/sequential with a decoder-ring handoff seat (`/advise`).
FR8: Engine is usable standalone — councils can be created and run without touching the coach pipeline.
FR9: Councils and persona sets export/import in a portable format consumable by other LLMs, including import from a user's existing project (`/export-council`, `/import-council`).

**Expert Panels**

FR10: `/evaluate` panel (parallel, four core seats): Behavioral Coder (Gottman/FBA), Psycholinguist (Pennebaker/LIWC), Personality Profiler (Big Five), Relational Needs Analyst (attachment/NVC/TA). Optional fifth lens: ADHD Specialist.
FR11: Orthogonality enforced at runtime: each seat's "ignores" written into its prompt as a hard prohibition — four independent footprints make the synthesis worth more than the sum of its parts.
FR12: Citation rule: every expert claim must cite transcript lines (speaker-turn IDs) or the chairman discards it.
FR13: `/advise` pipeline (sequential): Profile Translator (decoder ring, runs twice — subject and self) → Message Strategist ∥ Negotiation Architect ∥ Influence Tactician → Red Team → playbook synthesis. Execution Realist consumes the self decoder ring and stress-tests whether the user will actually run the plan under pressure (RSD, over-explaining — negative-space "don't" coaching).
FR14: Mutual-benefit guardrail: Influence Tactician is restricted to mutual-benefit moves; Red Team flags anything that only works if the subject doesn't notice. Bar: you'd be comfortable if the subject found out you used the tactic.
FR15: Optional-seat defaults: ADHD Specialist and Execution Realist ON in the user's local config, OFF (opt-in) in the public template.

**Persona Management**

FR16: Users can create, edit, and research/define new personas via dedicated commands as part of setup — first-class capability, its own epic.
FR17: Default rosters are defined per mode and overridable.
FR18: Each expert must use a distinct, named reasoning method — not just a distinct job title. MBTI/Enneagram are barred as scoring engines; acceptable only as translation layers.

**Profiles & Data**

FR19: Every profile splits into two layers at storage time: subject layer (traits, style, what framing lands — portable) and relationship layer (real quotes, incidents, advice→outcome history — private, never exported).
FR20: The user's own profile is a first-class subject (reserved slug `me`).
FR21: Profiles are falsifiable models: claims carry attribution, confidence (e.g., Profiler correlation ranges), and track records. Profile fields include known fallacies. A profile is interpretation, not fact.
FR22: Ingestion: Zoom transcripts (markdown) are primary, organized by source (`ingest/transcripts/`, `ingest/slack/`, extensible); every item carries context metadata (1-on-1 vs. group, participants).

**Computed Evidence**

FR23: Linguistic feature script: computes LIWC-style metrics (pronoun ratios, hedging density, language-style matching) from transcripts and feeds the Psycholinguist seat hard numbers.
FR24 (reframed by architecture): Transcript-derived Big Five as a lexicon-based weak signal with published correlation ranges as confidence; IPIP deterministic keying retained only for self-administered questionnaires. Validity caveats carry into the responsible-use note.
FR25: Calibration scoring computed from `advice_outcomes`: per-person prediction hit rates plus Brier scores measuring calibration quality of Red Team predictions and Profiler claims.
FR26: Semantic recall: sqlite-vec search over transcript history feeding the citation rule and past-win receipts (same SQLite file, no added infra).

**Feedback Loop**

FR27: `/advise` records the plan; a later `/evaluate` of the real conversation updates the person's profile and scores whether the advice worked.
FR28: Past-win receipts: dated, queryable record of what has worked with each person, surfaced in the `/advise` playbook.

**Sharing, Portability & Distribution**

FR29: `/export-profile <name>` emits subject-layer-only portable markdown — anecdotes generalized to traits, headed as a starting hypothesis. Two sanitization levels per invocation: Named (default) and Archetype (anonymized, public-safe) via one flag.
FR30: `/import-profile <file>` ingests with provenance tagging and keeps the imported read distinct from the user's own — never blended.
FR31: Public template repo ships engine, commands, schema, and archetype example profiles; `.gitignore` excludes `people/`, `transcripts/`, and `index.sqlite`. Acceptance: a scripted check (`scripts/verify_clean_fork.py`) run against a fresh clone confirms zero private data.
FR32: README includes a responsible-use note covering: the tool exists to improve your own communication, not to covertly profile others; discretion around mutual contacts; profiles are interpretation, not fact; Archetype is the default-safe level for anything public. Optional Claude Code plugin packaging stays in scope as Distribution polish.

### NonFunctional Requirements

NFR1: Privacy — hard subject/relationship separation enforced at storage time; exports strip the relationship layer; `.gitignore` enforcement verified; no third-party API calls (local embeddings, local lexicons).
NFR2: Cost — quick mode default outside `/evaluate`; debate only where it earns its token cost; tiered models (haiku-class seats, strong-model chairman + Red Team).
NFR3: Portability — human-readable markdown profiles; git-friendly; council/profile artifacts consumable by other LLMs.
NFR4: Bounded infrastructure — single local SQLite file, no server; graph DB and Claude Project export deferred until a real trigger.
NFR5: Responsible use — profiles framed as interpretation, not fact; mutual-benefit-only influence; Archetype export is the public-safe path.
NFR6: Anti-sycophancy — independence-first protocol so majority pressure cannot suppress correct minority reads.

### Additional Requirements

**Starter template (Epic 1 Story 1):**

- Project scaffold via `claude plugin init parley-voo --with skills hooks` + `claude plugin validate ./ --strict` as CI gate; MIT prompt-contract harvest from `ngmeyer/skills` monorepo (anonymization-shuffle, devil's-advocate pass, sycophancy guardrail, chairman output contract, composable flags pattern). First implementation story per architecture.
- `schema/index.sql` versioned, greenfield rebuilds (no migrations): tables `people`, `conversations`, `turns`, `patterns`, `conflicts`, `advice_outcomes`, `vec_turns` (sqlite-vec), `meta` (embedding_model_id, lexicon_version, schema_version).
- MIT license; repo root = plugin root; `.claude-plugin/plugin.json` + `marketplace.json` (polish phase).

**Runtime & stack:**

- Python 3.12+ scripts managed with uv (`pyproject.toml`); stdlib `sqlite3` + `sqlite-vec` (v0.1.7+); spaCy + curated hedge lexicon (+ optional psyLex/Empath); sentence-transformers with local `all-MiniLM-L6-v2` embeddings; pytest + pytest-socket.
- Script I/O contract: CLI args in (argparse, never stdin), JSON to stdout (snake_case), progress to stderr; exit codes 0/1 (user-fixable, message states the fix)/2 (internal). Every numeric claim carries evidence fields `{"value": 0.71, "n": 14, "method": "brier"}` — never a bare number.
- Skills never query SQLite directly — only Python scripts touch `index.sqlite`.

**Privacy mechanisms (three verified seams):**

- Storage-write: nothing writes `people/*.md` except `scripts/profile_write.py` — default-deny layer-routing chokepoint; unknown field → exit 1, never silently routed. Property test required.
- Export: sanitizer strips relationship layer; golden-file tests (input profile → expected Named export → expected Archetype export).
- Repo: `verify_clean_fork.py` + `.gitignore` for `people/`, `transcripts/`, `ingest/`, `index.sqlite`, `.parley/`, `config.local.yaml`.
- Per-expert memory at `.parley/memory/<seat-id>/` — gitignored, never exported, excluded from council export.
- No-network invariant: evidence scripts make zero external calls; enforced in CI by socket-blocking the pytest run.

**Citations & transcripts:**

- Speaker-turn ID addressing: ingestion normalizes markdown transcripts into canonical turn files (`transcripts/<person-or-context>/<YYYY-MM-DD>-<slug>.md`); pinned turn-line grammar `^\*\*T(\d+) · ([a-z0-9-]+):\*\* `; `T17` = turn 17.
- `recall.py --verify-citations` accepts `Tnn` refs + conversation id, returns which exist; chairman calls it before accepting any claim — hallucinated citations mechanically impossible.
- sqlite-vec chunking is per-turn, speaker-keyed.

**Engine & config:**

- Council-engine is a skill (`skills/council-engine/SKILL.md` + references/); orchestration is prompt-directed sub-agent fan-out; each seat = one agent definition in `agents/<seat-id>.md`.
- Topology declared per-roster, not per-command; roster file (`councils/<name>.md`) frontmatter: `topology`, `seats`, `quick_seats`, `model_overrides`. The roster file IS the FR9 export format. Import validates referenced seat IDs at import time (exit 1 listing the missing).
- Persona file contract: frontmatter `seat_id`, `display_name`, `method`, `ignores` (list), `role` (`seat|chairman`), `modes`; body = the prompt. Model tiers resolved only in roster `model_overrides` — never hardcoded in persona files.
- Seat IDs canonical kebab-case (`behavioral-coder`, `red-team`); person slugs lowercase-kebab; the only cross-file keys.
- Commands are skills: `skills/{evaluate,advise,council,persona,export-profile,import-profile,export-council,import-council}/SKILL.md`; SKILL.md body <500 lines, references split out.
- Config posture: `config.yaml` (template defaults, optional seats OFF) vs `config.local.yaml` (gitignored, optional seats ON).

**Calibration & evidence (research-ratified detail):**

- Plain per-person, per-seat Brier + hit rate from `advice_outcomes`; skip reliability/resolution/uncertainty decomposition at solo n; always display `n`; comparisons within same person/context only.
- Hedge lexicon hand-maintained (auditable, fork-safe); NRC EmoLex license must be vetted before bundling in public template (research-only terms) — FR23 does not block on it.
- Persona-prompt authoring guardrails from domain research: no predictive Gottman language ("contempt is present," never "this relationship will fail"); LIWC numbers need token floor + corroboration; RSD framed as experiential label not diagnosis, confined to self-model; Cialdini principles weighted by evidence tier (scarcity weak); pre-mortem framed as debiasing process, not forecasting; trait claims as "evidence is consistent with high X," never "they are X." Orthogonality matrix boundaries feed each seat's `Ignores:` line.

**CI & quality gates:**

- GitHub Actions: `claude plugin validate --strict` · `pytest` (socket-blocked) · `verify-clean-fork` against fresh clone.
- Tests: pytest, `tests/test_<script>.py`, golden files in `tests/golden/`.

**Story-level minors logged by architecture:**

- Exact prompt text HTML artifacts emit on Copy Prompt — define in artifact stories.
- NRC EmoLex license vetting before public bundling.
- `conflicts` table usage is spec-carried but thin — define or drop during the `/evaluate` epic.

### UX Design Requirements

**Terminal document conventions (binding, every emitted document):**

UX-DR1: Heading hierarchy `#` → `##` → `###`, never skip a level, never deeper than `###`; `**bold**` only for the single load-bearing word or section verdict; italic reserved for "interpreted, not fact" disclaimers and quoted transcript fragments; no ALL-CAPS runs; bullets for parallel items, numbers only for ordered sequences; list nesting capped at one level; no wide tables (two-column ≤ ~60 char rows max, else labeled lists); single `---` divider between major sections only; meaning must survive monochrome.
UX-DR2: Citation ref primitive: inline code span `` `[date context, Tnn]` `` (Tnn = speaker-turn ID) on every expert claim — present in every document.
UX-DR3: Confidence display convention: `word (0.NN)` — word first, number second, always paired; never a bare adjective or bare number. Sits immediately after the claim it qualifies.
UX-DR4: Attribution line `— {Seat name}, {method}` after a claim or section.
UX-DR5: Track-record line: e.g. `Red Team: batting .71 on Chris (n=14) · Brier 0.19` — plain text, always with sample size.
UX-DR6: Density cap (ADHD rule): glanceable top section above the fold; each section front-loads its one actionable sentence; a section needing a full screen gets a one-line summary head; no section requires holding prior state in the reader's head.
UX-DR7: Voice — direct strategist: terse, confident, no hedging in prose; all uncertainty pushed into confidence scores. Banned: hedging prose, dossier-style anecdote dumps, congratulatory padding, color-only meaning, stateful artifacts.

**Document anatomies (composed of the primitives above):**

UX-DR8: Playbook (`/advise`): top section above the fold — plan summary · character read · past-win receipts · fallacies to avoid; body — frame · opening line · sequence (ordered) · objections + responses · fallback · "what you lose" · first concrete step. Quick mode trims to top section + opening + first step; trim is announced ("Trimmed in quick mode" line naming what `--full` adds). Header notes quick/full mode.
UX-DR9: Pattern report (`/evaluate`): per-seat findings, each claim cited or discarded; computed numbers from linguistic/personality scripts shown inline; closes with profile-update summary per participant.
UX-DR10: Profile doc: opens with "interpreted, not fact" line; subject traits with confidence + attribution + track record; known fallacies listed; self-profile first-class; imported profiles permanently tagged and shown beside the native read, never merged.
UX-DR11: Council verdict (`/council`): "should we do X" answer; dissent preserved with explicit `Dissent:` label; chairman may side with a strong minority.
UX-DR12: Export preview (`/export-profile`): stripped fields rendered as `~~field~~ (stripped: relationship layer)` — the user sees what leaves before writing; output headed "starting hypothesis, not a verdict."
UX-DR13: Empty-state docs: one sentence + the one next command; never apologize, never spinner. Three cases: new person ("No profile yet. Run `/evaluate`…"), no transcripts ("Nothing in `ingest/`…"), fresh fork (zero data confirmed, responsible-use note shown once).
UX-DR14: State surfacing: advice recorded → status `awaiting outcome` + session reminder to run `/evaluate`; re-advising same person surfaces "1 plan awaiting outcome" and offers the outcome-score artifact; confidence lifecycle (new → low, corroborated → rises, contradicted → falls/flagged) always shown as `word (0.NN)`.

**HTML artifacts (secondary surface, stateless, select → Copy Prompt → paste back):**

UX-DR15: Roster-picker artifact (roster override flag on `/advise`/`/council`/`/evaluate`): selectable persona cards each showing method AND an "Ignores:" line as prominently as method; accent border selection state; Copy Prompt always visible (sticky); single column max-width ~720px. Canonical "Ignores:" copy comes from authored persona prompts.
UX-DR16: Outcome-score artifact: ordinal picker (worked / partial / didn't), each option a selectable card; Copy Prompt sends the score back; no free-text required.
UX-DR17: Persona-editor flow + persona-picker artifact for persona create/edit/research.
UX-DR18: Artifact build: generated from Python string templates into `.parley/artifacts/`; DESIGN.md tokens inlined (colors: ink/surface/accent pine `#2F5D50`/confidence ramp/dissent/stripped; typography: Newsreader display, Inter body, JetBrains Mono machine text, tracked labels; spacing/radius tokens); tone-not-shadow depth; one accent used only on select + Copy Prompt; no category palette, no gradients.
UX-DR19: Provenance tag component: `imported · {source} · {date}` chip on imported-profile data, visually distinct from native data.
UX-DR20: Accessibility floor: never color-only meaning (confidence/dissent/stripped/provenance always carry text labels); WCAG AA contrast in artifacts (4.5:1 body, 3:1 large/UI); artifacts fully keyboard-operable with visible focus states, focus order = reading order; screen-reader-sane markdown (strict hierarchy, real lists, no ASCII-art layout); each document's first line states what it is.

### FR Coverage Map

FR1: Epic 3 - `/evaluate` command, pattern report + profile updates
FR2: Epic 4 - `/advise` command, playbook document
FR3: Epic 1 - `/council` command, generic verdict
FR4: Epic 1 - quick/full cost tiers in the engine
FR5: Epic 1 - three-stage independence-first protocol
FR6: Epic 1 - dissent-preserving chairman synthesis
FR7: Epic 1 - dual topology (parallel / staged)
FR8: Epic 1 - engine standalone-usable
FR9: Epic 2 - `/export-council` / `/import-council` portable format
FR10: Epic 2 (authoring, Story 2.1) + Epic 3 (runtime panel) - `/evaluate` four-seat panel + optional ADHD Specialist
FR11: Epic 2 - orthogonality via hard "Ignores:" prohibitions in persona prompts
FR12: Epic 3 - citation rule + mechanical verification
FR13: Epic 2 (authoring, Story 2.2) + Epic 4 (pipeline runtime) - staged `/advise` pipeline (decoder rings → strategists → Red Team → synthesis)
FR14: Epic 2 (in-prompt, Story 2.2) + Epic 4 (runtime surfacing) - mutual-benefit guardrail
FR15: Epic 2 - optional-seat config posture (local ON / template OFF)
FR16: Epic 2 - persona create/edit/research commands
FR17: Epic 2 - per-mode default rosters, overridable
FR18: Epic 2 - distinct named reasoning methods; MBTI/Enneagram bar
FR19: Epic 3 - two-layer profile split at storage time
FR20: Epic 3 - self-profile first-class (slug `me`)
FR21: Epic 3 - falsifiable profiles (attribution, confidence, track records, fallacies)
FR22: Epic 3 - source-organized ingestion with context metadata
FR23: Epic 3 - linguistic feature script
FR24: Epic 3 - lexicon-based Big Five weak signal + IPIP keying (reframed)
FR25: Epic 5 - calibration scoring (Brier + hit rates from `advice_outcomes`)
FR26: Epic 3 - sqlite-vec semantic recall
FR27: Epic 5 - plan recording + outcome scoring loop
FR28: Epic 5 - past-win receipts
FR29: Epic 6 - `/export-profile` Named/Archetype sanitization
FR30: Epic 6 - `/import-profile` provenance tagging
FR31: Epic 6 - clean public template + `verify-clean-fork`
FR32: Epic 6 - responsible-use README + plugin packaging polish

## Epic List

### Epic 1: Working Council — Scaffold + Engine + `/council`

Clone the repo and get a dissent-preserving verdict on any decision. Plugin scaffold (`claude plugin init` + `schema/index.sql` — the architecture's mandated first story), council-engine skill with both topologies, anonymized peer review, chairman synthesis, quick/full modes, a minimal default council.
**FRs covered:** FR3, FR4, FR5, FR6, FR7, FR8

### Epic 2: The Expert Bench — Personas, Rosters & Portability

Author, tune, export, and import the experts the system thinks with. All 12 persona files authored from the research briefs (with `Ignores:` lines and validity guardrails), persona create/edit/research commands, default rosters per mode, roster-picker + persona-picker artifacts, `/export-council` / `/import-council`, config posture (local vs template seat defaults).
**FRs covered:** FR9, FR11, FR15, FR16, FR17, FR18 · plus the authoring halves of FR10 (Story 2.1), FR13/FR14 (Story 2.2)

### Epic 3: Evidence-Grounded Evaluation — `/evaluate` + Profiles

Drop a Zoom transcript and get a cited pattern report; profiles begin accumulating. Ingestion + turn normalization, sqlite-vec embeddings + recall, linguistic features + personality scripts, the privacy chokepoint (`profile_write.py`, two-layer split), pattern report doc, profile docs, citation verification.
**FRs covered:** FR1, FR10, FR12, FR19, FR20, FR21, FR22, FR23, FR24, FR26

### Epic 4: Conversation Playbooks — `/advise`

Prep a high-stakes conversation and walk in with a playbook. Staged topology in action: decoder rings (subject + self), strategist trio, Red Team, Execution Realist, mutual-benefit guardrail, playbook doc with glanceable top section + announced quick-mode trim.
**FRs covered:** FR2, FR13, FR14

### Epic 5: The Loop Closes — Outcomes & Calibration

The system visibly sharpens with use — batting averages, Brier scores, past-win receipts. Plan recording on `/advise`, outcome scoring via `/evaluate` + outcome-score artifact, calibration script, track records in docs, awaiting-outcome state.
**FRs covered:** FR25, FR27, FR28

### Epic 6: Share It, Fork It — Sanitized Exports & Public Template

Hand a profile to a friend; a stranger forks a clean repo. `/export-profile` (Named/Archetype + stripped-field preview), `/import-profile` (provenance), golden-file sanitization tests, `verify-clean-fork`, responsible-use README, CI gates, plugin packaging polish.
**FRs covered:** FR29, FR30, FR31, FR32

## Epic 1: Working Council — Scaffold + Engine + `/council`

Clone the repo and get a dissent-preserving verdict on any decision. Plugin scaffold, council-engine skill with both topologies, anonymized peer review, chairman synthesis, quick/full modes, a minimal default council.

### Story 1.1: Plugin Scaffold & CI Gate

As a forker (or Elliot on day one),
I want the repo initialized as a valid, installable Claude Code plugin with privacy guardrails baked in,
So that every later story lands in a structure that validates cleanly and can never leak private data into git.

**Acceptance Criteria:**

**Given** a fresh clone of the repo
**When** `claude plugin validate ./ --strict` runs (locally and in CI)
**Then** validation passes with `.claude-plugin/plugin.json` carrying name `parley-voo` and an explicit `version`
**And** the scaffold came from `claude plugin init parley-voo --with skills hooks`

**Given** the repo root
**When** inspecting tracked files
**Then** `.gitignore` excludes `people/`, `transcripts/`, `ingest/`, `index.sqlite`, `.parley/`, `config.local.yaml`
**And** `LICENSE` is MIT, `pyproject.toml` is uv-managed (Python 3.12+, pytest + pytest-socket), `.python-version` present
**And** `schema/index.sql` defines the spec-locked tables (`people`, `conversations`, `turns`, `patterns`, `conflicts`, `advice_outcomes`, `vec_turns`, `meta`) with snake_case columns, `<singular>_id` FKs, ISO-8601 UTC timestamps (`conflicts` is provisional pending Story 3.6's define-or-drop decision)

**Given** a push to the repo
**When** GitHub Actions runs
**Then** the CI workflow executes `claude plugin validate --strict` and a socket-blocked `pytest` run (empty suite passes)

### Story 1.2: Deliberation Engine — Parallel Topology with Peer Review & Chairman

As a user seeking a trustworthy verdict,
I want a council engine that runs seats independently, peer-reviews anonymously, and synthesizes without smoothing dissent,
So that majority pressure cannot suppress a correct minority read (FR5, FR6, NFR6).

**Acceptance Criteria:**

**Given** the persona file contract (`agents/<seat-id>.md`: frontmatter `seat_id`, `display_name`, `method`, `ignores`, `role`, `modes`; body = prompt)
**When** `agents/chairman.md` is authored
**Then** it carries `role: chairman` and the harvested output contract (Agrees / Clashes / Blind Spots / Recommendation / What You Lose / Do This First / Verify), with MIT attribution to `ngmeyer/skills` in `skills/council-engine/references/protocol.md`

**Given** a roster file (`councils/<name>.md`: frontmatter `topology`, `seats`, `quick_seats`, optional `model_overrides`)
**When** the engine runs `topology: parallel`
**Then** stage 1 fans out each seat as a sub-agent with no visibility into any other seat's output
**And** stage 2 shuffles responses and relabels them A, B, C… (one anonymous label per participating seat) before peer review (no seat identifiable)
**And** stage 3 chairman synthesis runs the devil's-advocate-vs-consensus pass, distinguishes value tensions from error catches, preserves minority positions under an explicit `Dissent:` label, and may side with a strong minority

**Given** a persona file with a hardcoded model tier
**When** the engine resolves models
**Then** tiers come only from roster `model_overrides` (haiku-class seats, strong-model chairman default) — persona-file tiers are ignored

### Story 1.3: Dual Topology & Quick/Full Modes

As a user with different deliberation needs,
I want the engine to support staged (sequential handoff) execution and quick/full cost tiers,
So that `/advise`-style pipelines are possible and routine runs stay cheap (FR7, FR4, NFR2).

**Acceptance Criteria:**

**Given** a roster with `topology: staged` and ordered stage groups
**When** the engine runs
**Then** stages execute sequentially, each stage receiving the prior stage's output (decoder-ring handoff pattern), with seats inside a stage running parallel

**Given** any roster invoked without flags
**When** quick mode (default) runs
**Then** only `quick_seats` execute and peer review is skipped
**And** `--full` escalates to all seats plus anonymized peer review
**And** topology and mode resolution come from the roster file, never hardcoded per command

### Story 1.4: `/council` — Generic Verdicts

As a user facing a decision,
I want to run `/council "should we do X"` and get a dissent-preserving verdict document,
So that I get structured deliberation with zero coach-pipeline setup (FR3, FR8).

**Acceptance Criteria:**

**Given** a fresh install with no profiles, transcripts, or database present
**When** `/council "should we drop the enterprise tier?"` runs
**Then** the engine executes standalone with `councils/council-default.md` (quick mode) and prints a verdict document — proving FR8

**Given** the printed verdict
**When** inspecting the document
**Then** it follows terminal conventions: one `#` title, first line states what it is, heading depth ≤ `###`, no wide tables, header notes `quick mode`/`full mode`
**And** dissent appears under an explicit `Dissent:` label with attribution `— Seat, method`
**And** any confidence is rendered `word (0.NN)`, never bare

**Given** the same command with `--full`
**When** it runs
**Then** all seats plus peer review execute and the header reflects full mode

## Epic 2: The Expert Bench — Personas, Rosters & Portability

Author, tune, export, and import the experts the system thinks with. All 12 persona files authored from the research briefs, persona management commands, default rosters per mode, picker artifacts, council export/import, config posture.

### Story 2.1: Author the Evaluate Panel Personas

As a user evaluating real conversations,
I want the four core analysis seats plus the ADHD Specialist authored with named methods and hard "Ignores:" prohibitions,
So that four genuinely independent footprints make synthesis worth more than the sum of its parts (FR10 authoring, FR11, FR18).

**Acceptance Criteria:**

**Given** the persona file contract from Story 1.2
**When** `behavioral-coder`, `psycholinguist`, `personality-profiler`, `relational-needs-analyst`, and `adhd-specialist` are authored in `agents/`
**Then** each carries a distinct named reasoning method (Gottman/FBA, Pennebaker/LIWC, Big Five, attachment/NVC/TA, ADHD patterns) and an `ignores` list written as hard prohibitions taken from the research orthogonality matrix boundaries

**Given** the domain research validity guardrails
**When** inspecting each prompt body
**Then** Behavioral Coder bans predictive framing ("contempt is present," never "this relationship will fail")
**And** Psycholinguist requires a minimum-token floor and treats metrics as weak-to-moderate signal needing corroboration
**And** Personality Profiler states traits as "evidence is consistent with high X" with confidence ranges, never "they are X," and bars MBTI/Enneagram as scoring engines
**And** Relational Needs Analyst forces tentative, dimensional language ("leans avoidant on this evidence")
**And** ADHD Specialist frames RSD as an experiential label (not a diagnosis), prefers "rejection-sensitivity pattern," confines RSD attribution to the user's self-model, and never diagnoses

**Given** any claim instruction in a seat prompt
**When** the seat produces output
**Then** the prompt requires citation refs on every claim (FR12 contract) and attribution-ready output (`— Seat, method`)

### Story 2.2: Author the Advise Pipeline Personas

As a user preparing for a hard conversation,
I want the six strategy seats authored with their methods, guardrails, and handoff roles,
So that the staged pipeline has ethically-bounded, evidence-calibrated experts to run (FR13 authoring, FR14 in-prompt, FR11, FR18).

**Acceptance Criteria:**

**Given** the persona file contract
**When** `profile-translator`, `message-strategist`, `negotiation-architect`, `influence-tactician`, `red-team`, and `execution-realist` are authored
**Then** each carries its named method (decoder-ring translation; framing/inoculation; Fisher & Ury + Voss; Cialdini; pre-mortem/devil's advocacy; implementation intentions) and orthogonality-matrix `ignores` prohibitions

**Given** the mutual-benefit guardrail (FR14)
**When** inspecting the Influence Tactician prompt
**Then** it restricts moves to mutual benefit with the explicit bar "you'd be comfortable if the subject found out you used the tactic," weights principles by evidence tier (social proof/authority/reciprocity strong; scarcity weak), and self-censors covert moves
**And** the Red Team prompt flags any tactic that only works if the subject doesn't notice, frames pre-mortem as debiasing (not forecasting), and is written to carry a calibration track record

**Given** the Execution Realist's negative-space role
**When** inspecting its prompt
**Then** it consumes the *self* decoder ring, limits output to one or two if-then implementation intentions, coaches in "don't" form (RSD/over-explaining under pressure), and ignores strategic correctness (other seats' footprint)

**Given** the Profile Translator's handoff role
**When** inspecting its prompt
**Then** it produces a decoder ring (how the person decides, what framing lands, what triggers a "no") and is written to run twice — subject and self

### Story 2.3: Default Rosters & Config Posture

As a user (and as a forker with different defaults),
I want per-mode default rosters and a local-vs-template config split,
So that each command runs the right bench out of the box and my optional seats stay ON locally while the public template ships them OFF (FR17, FR15).

**Acceptance Criteria:**

**Given** the roster file contract
**When** `councils/evaluate-default.md`, `councils/advise-default.md`, and `councils/council-default.md` are authored
**Then** evaluate-default is `topology: parallel` with the four core seats (+ ADHD Specialist as optional) and is pinned full mode
**And** advise-default is `topology: staged` with stage groups: profile-translator (×2: subject, self) → message-strategist ∥ negotiation-architect ∥ influence-tactician → red-team → execution-realist → chairman synthesis
**And** each roster names its own `quick_seats` subset and tiered `model_overrides` (haiku-class seats, strong-model chairman + red-team)

**Given** `config.yaml` (template) and `config.local.yaml` (gitignored)
**When** roster resolution runs
**Then** ADHD Specialist and Execution Realist are OFF in `config.yaml`, ON in `config.local.yaml`, and local overrides win
**And** a fresh clone (no local config) resolves to template defaults without error

### Story 2.4: `/persona` — Create, Edit, Research

As a user growing my expert bench,
I want dedicated commands to create, edit, and research new personas,
So that persona management is a first-class capability, not file surgery (FR16, FR18).

**Acceptance Criteria:**

**Given** `/persona create`
**When** a new persona is defined
**Then** the flow requires a distinct named reasoning method (not just a job title), a non-empty `ignores` list, and a valid kebab-case `seat_id` not already in `agents/`
**And** the resulting file passes the persona contract (frontmatter complete, body prompt present)

**Given** a proposed persona using MBTI or Enneagram as its scoring engine
**When** validation runs
**Then** creation is refused with a message explaining the bar (translation-layer use is allowed, scoring-engine use is not)

**Given** `/persona research <topic>`
**When** it runs
**Then** it produces a method brief (core constructs, blind spots/ignores, validity status, sources) usable to author the persona prompt

**Given** `/persona edit <seat-id>`
**When** edits complete
**Then** the file still passes contract validation and any roster referencing the seat still resolves

### Story 2.5: Roster-Picker & Persona-Picker Artifacts

As a user tuning who deliberates,
I want browser artifacts where I pick seats by their blind spots and copy a prompt back,
So that clicking beats typing for roster overrides while all state stays in the session (UX-DR15, 17, 18, 20).

**Acceptance Criteria:**

**Given** a roster-override flag on any council-running command (at minimum `/council`; `/evaluate` and `/advise` reuse the same artifact when they land in Epics 3–4)
**When** the roster-picker artifact is generated into `.parley/artifacts/`
**Then** it is built from a Python string template with DESIGN.md tokens inlined (pine accent `#2F5D50`, warm surface, Newsreader/Inter/JetBrains Mono, spacing/radius tokens), single column max-width ~720px

**Given** the rendered cards
**When** the user browses seats
**Then** each card shows the seat's method AND its "Ignores:" line with equal prominence, sourced from the authored persona frontmatter
**And** selection toggles an accent border (tone, not shadow); the one accent appears only on selection and Copy Prompt

**Given** a selection
**When** Copy Prompt is clicked (always visible — sticky)
**Then** the clipboard receives a deterministic prompt naming the chosen seat IDs for paste-back into the session, and the artifact holds no state (exact Copy Prompt text defined in this story per architecture's logged minor)

**Given** keyboard-only operation
**When** navigating the artifact
**Then** cards are selectable and Copy Prompt invokable via keyboard, focus order matches reading order, focus state visible, and all text-on-surface combinations meet WCAG AA

### Story 2.6: `/export-council` & `/import-council` — Portable Benches

As a user sharing my deliberation setup (or importing someone else's),
I want councils and persona sets to export/import as portable plain-text files,
So that any LLM can consume them and other projects' councils can move in (FR9, NFR3).

**Acceptance Criteria:**

**Given** `/export-council <name>`
**When** export runs
**Then** the output bundles the roster file (which IS the portable format — no separate serialization) plus each referenced persona file, all markdown + YAML frontmatter readable by any LLM
**And** per-expert memory dirs (`.parley/memory/`) are excluded

**Given** `/import-council <file>`
**When** the bundle references seat IDs
**Then** import validates every referenced seat ID at import time and exits 1 listing the missing ones — never failing later mid-run
**And** a successful import prints an import-summary doc naming what was added

**Given** a council exported from a user's existing non-Parley project
**When** it matches the roster/persona contract
**Then** it imports and runs through the engine unchanged

## Epic 3: Evidence-Grounded Evaluation — `/evaluate` + Profiles

Drop a Zoom transcript and get a cited pattern report; profiles begin accumulating. Ingestion, embeddings + recall, evidence scripts, the privacy chokepoint, pattern report and profile documents.

### Story 3.1: Transcript Ingestion & Turn Normalization

As a user with real conversations to learn from,
I want dropped transcripts normalized into canonical, citable turn files and indexed in the database,
So that every later claim can point at `T17` and survive reformatting (FR22).

**Acceptance Criteria:**

**Given** a Zoom markdown transcript in `ingest/transcripts/` (source dirs extensible: `ingest/slack/`, …)
**When** `scripts/ingest.py` runs
**Then** a canonical file lands at `transcripts/<person-or-context>/<YYYY-MM-DD>-<slug>.md` with frontmatter `source`, `occurred_at`, `setting` (`1:1|group`), `participants` (slugs)
**And** body turns match the pinned grammar `^\*\*T(\d+) · ([a-z0-9-]+):\*\* ` — turn IDs visible and human-checkable in the file

**Given** a successful ingest
**When** inspecting `index.sqlite`
**Then** `conversations` and `turns` rows exist (turn_no, speaker, text, char_span), created from `schema/index.sql` definitions
**And** the script follows the I/O contract: argparse in, JSON summary to stdout, progress to stderr, exit 0/1/2 (1 names the user fix)

**Given** `ingest/` is empty
**When** `scripts/ingest.py` runs
**Then** it exits 1 with the fix line "Nothing in `ingest/`. Drop a Zoom transcript there and re-run." — one sentence + the one next command, ready for any skill to print verbatim (no apology, no spinner)

### Story 3.2: Semantic Recall & Mechanical Citation Verification

As a user relying on cited claims,
I want per-turn embeddings, semantic search, and a citation verifier — all local,
So that hallucinated citations are mechanically impossible and recall never sends data off-machine (FR26, FR12 mechanism, NFR1, NFR4).

**Acceptance Criteria:**

**Given** ingested turns
**When** embedding runs
**Then** per-turn, speaker-keyed vectors land in `vec_turns` (sqlite-vec) using local `all-MiniLM-L6-v2` via sentence-transformers, and `meta` records `embedding_model_id`, `lexicon_version`, `schema_version`

**Given** `scripts/recall.py "<query>"`
**When** semantic search runs
**Then** results return turn references (conversation, `Tnn`, speaker) as JSON — same single SQLite file, no added infra

**Given** `recall.py --verify-citations` with a list of `Tnn` refs + conversation id
**When** verification runs
**Then** it returns which refs exist and which don't

**Given** the no-network invariant
**When** the test suite runs under pytest-socket
**Then** embedding and recall pass with all sockets blocked

### Story 3.3: Linguistic Features Script

As the Psycholinguist seat (serving the user's read),
I want LIWC-style metrics computed deterministically from transcripts,
So that the seat interprets hard numbers instead of eyeballing prose (FR23).

**Acceptance Criteria:**

**Given** a canonical transcript
**When** `scripts/linguistic_features.py` runs
**Then** it emits pronoun ratios (spaCy POS), hedging density (hand-maintained hedge lexicon — auditable, fork-safe), and language-style matching between speakers (function-word LSM formula)
**And** every numeric claim carries evidence fields `{"value": …, "n": …, "method": …}` — never a bare number

**Given** a turn below the minimum-token floor
**When** metrics are computed
**Then** the output flags low-reliability segments rather than reporting confident numbers

**Given** the public-template bundling caveat
**When** lexicons are packaged
**Then** NRC EmoLex is excluded or license-vetted before inclusion (logged minor); the hedge lexicon ships regardless so FR23 doesn't block

### Story 3.4: Personality Signal Script (Reframed FR24)

As the Personality Profiler seat,
I want a lexicon-based Big Five signal with published correlation ranges as confidence — plus real IPIP keying for questionnaires,
So that trait evidence is honest math where math exists, and labeled weak signal where it doesn't (FR24 reframed, FR21).

**Acceptance Criteria:**

**Given** a canonical transcript
**When** `scripts/personality.py` runs
**Then** it emits per-trait lexicon scores explicitly labeled weak signal, each carrying its published correlation range as the confidence band
**And** output language supports "evidence is consistent with high X," never bare trait verdicts

**Given** a self-administered BFI/IPIP questionnaire passed directly to `personality.py` as a file argument (no ingestion pipeline involved — the one legitimately deterministic path)
**When** scoring runs
**Then** reverse-keying and domain sums compute deterministically per IPIP public-domain keying

**Given** any output consumed by the Profiler seat
**When** validity caveats apply (short text, conversational register, context-blindness)
**Then** they are present in the JSON so downstream rendering can surface them (feeds the FR32 responsible-use note)

### Story 3.5: Two-Layer Profile Storage — The Privacy Chokepoint

As a user accumulating sensitive reads on real people,
I want every profile write routed through one default-deny script that splits subject from relationship at storage time,
So that the privacy boundary is a mechanism, not a convention (FR19, FR20, FR21, NFR1).

**Acceptance Criteria:**

**Given** profile claims as JSON (from any skill)
**When** `scripts/profile_write.py` runs
**Then** claims route to the subject layer (portable traits) or relationship layer (quotes, incidents, advice→outcome history) by explicit field schema in `templates/profile.subject.md` / `templates/profile.relationship.md`
**And** an unknown field exits 1 naming the field — never silently routed to subject
**And** a property test proves no input JSON reaches the subject file without an explicit schema match

**Given** any other code path in the repo
**When** searching for writes to `people/*.md`
**Then** `profile_write.py` is the only writer (anti-pattern check)

**Given** a first write for a new person
**When** the profile is created
**Then** `people/<slug>.md` uses the lowercase-kebab slug as the FK-stable key, a `people` row exists, and the user's own profile lives at the reserved slug `people/me.md`
**And** every claim lands with attribution, confidence, and a known-fallacies field available (FR21)

### Story 3.6: `/evaluate` — Full Panel Pattern Report

As a user who just had a real conversation,
I want `/evaluate <transcript>` to run the full panel over computed evidence and print a cited pattern report with profile updates,
So that my read of each person sharpens from evidence a prompt can't fabricate (FR1, FR10, FR12).

**Acceptance Criteria:**

**Given** an ingested transcript, `councils/evaluate-default.md`, and the optional-seat config posture (both from Story 2.3)
**When** `/evaluate` runs
**Then** the full parallel panel executes (four core seats + ADHD Specialist per config posture) — quick mode is not available on this command
**And** each seat receives the canonical turns plus its computed evidence (linguistic features → Psycholinguist; personality signal → Profiler)

**Given** seat claims entering synthesis
**When** the chairman processes them
**Then** it calls `recall.py --verify-citations` and discards any claim whose `[date context, Tnn]` ref does not verify

**Given** synthesis completes
**When** the pattern report prints
**Then** it shows per-seat findings with citations, computed numbers inline, attribution lines, confidence as `word (0.NN)`, and closes with a per-participant profile-update summary
**And** profile updates flow only through `profile_write.py`

**Given** a mid-conversation (partial) transcript
**When** `/evaluate` runs on it
**Then** it processes identically — the halftime report needs no special handling

**Given** the `conflicts` table is spec-carried but has no defined consumer
**When** this story completes
**Then** the table either has a write path exercised by `/evaluate` synthesis or is removed from `schema/index.sql` (architecture's logged minor; greenfield rebuild, no migration)

### Story 3.7: Profile Documents — Falsifiable Reads on Real People

As a user checking what the system believes about someone,
I want a profile document that is visibly interpretation, not fact,
So that claims stay attributed, confidence-scored, and falsifiable (FR20, FR21 display, UX-DR10).

**Acceptance Criteria:**

**Given** a person with profile data
**When** the profile doc renders
**Then** it opens with the "interpreted, not fact" line, first line states what the document is
**And** every trait shows confidence `word (0.NN)` + attribution `— Seat, method` + track record with `n=` where one exists
**And** known fallacies are listed; the owner sees both layers, never rendered as a dossier of dated anecdotes

**Given** the user's own profile (`me`)
**When** rendered
**Then** it is a first-class subject with identical treatment

**Given** a person with no profile yet
**When** a profile is requested
**Then** the empty state prints: "No profile yet. Run `/evaluate` on a transcript to start one."

## Epic 4: Conversation Playbooks — `/advise`

Prep a high-stakes conversation and walk in with a playbook. Staged topology in production use: decoder rings, strategist trio, Red Team, Execution Realist, mutual-benefit guardrail, playbook document.

### Story 4.1: `/advise` Quick Mode — The Default Playbook

As a user about to walk into a conversation that matters,
I want `/advise "<goal>" <person>` to produce a glanceable playbook by default,
So that routine prep is cheap and the actionable line is the first thing I see (FR2, FR13 core path, FR4, NFR2).

**Acceptance Criteria:**

**Given** a person with a profile and a stated goal
**When** `/advise "get Chris to back the pricing proposal" chris` runs (no flags)
**Then** the staged pipeline executes in quick mode per `advise-default.md`: Profile Translator runs twice — subject decoder ring from `people/chris.md`, self decoder ring from `people/me.md` — then the roster's `quick_seats`, then synthesis, with no peer review

**Given** the printed playbook
**When** inspecting the top section
**Then** plan summary, character read, past-win receipts, and fallacies to avoid all sit above the fold — receipts render an honest empty state until outcomes exist ("No recorded outcomes with Chris yet")
**And** the body trims to opening line + first concrete step, header notes `quick mode`

**Given** the quick-mode trim
**When** the playbook ends
**Then** a "Trimmed in quick mode" line names exactly what `--full` adds (Red Team rebuttal, peer-reviewed objections, fallback) — negative space made visible

**Given** a person with no profile
**When** `/advise` runs
**Then** the empty state prints: "No profile yet. Run `/evaluate` on a transcript to start one."

### Story 4.2: `/advise --full` — Red Team, Execution Realist & the Complete Body

As a user preparing for a high-stakes conversation,
I want the full pipeline with adversarial review and an executability check,
So that I walk in with a playbook that survived attack and that I will actually run under pressure (FR2 full body, FR13, FR14).

**Acceptance Criteria:**

**Given** `/advise --full`
**When** the pipeline runs
**Then** all stages execute: Profile Translator ×2 → Message Strategist ∥ Negotiation Architect ∥ Influence Tactician → Red Team → Execution Realist (per config posture) → playbook synthesis, with anonymized peer review

**Given** the full playbook body
**When** it prints
**Then** it contains frame, opening line, ordered sequence, objections + responses, fallback, "what you lose" (as prominent as the plan), and first concrete step — header notes `full mode`

**Given** the mutual-benefit guardrail (FR14)
**When** the Influence Tactician proposes moves
**Then** the Red Team pass surfaces in the playbook as an explicit pass/flag on each tactic — flagging anything that only works if the subject doesn't notice

**Given** the Execution Realist seat is ON
**When** synthesis completes
**Then** the playbook carries its negative-space coaching from the *self* decoder ring — at most one or two if-then plans, "don't" framing for pressure moments (e.g., "Don't over-explain if he pauses — silence isn't rejection")

## Epic 5: The Loop Closes — Outcomes & Calibration

The system visibly sharpens with use — batting averages, Brier scores, past-win receipts. Plan recording, outcome scoring via both paths, calibration script, track records in documents.

### Story 5.1: Plan Recording & the Awaiting-Outcome State

As a user acting on advice,
I want every `/advise` plan recorded with its predictions,
So that the system can later score whether the advice actually worked (FR27 record side).

**Acceptance Criteria:**

**Given** a completed `/advise` run
**When** the playbook prints
**Then** the plan lands in `advice_outcomes` (person_id, seat, forecast_prob, predicted_at, outcome NULL) with status `awaiting outcome`, written via the script layer (skills never touch SQLite directly)
**And** the session reminds: run `/evaluate` after the conversation

**Given** Red Team predictions in the full pipeline
**When** the plan records
**Then** each prediction carries its forecast probability so Brier scoring is possible later

**Given** a re-`/advise` for the same person with plans awaiting
**When** the command starts
**Then** the session surfaces "N plan(s) awaiting outcome" (the outcome-score artifact offer is wired in Story 5.3)

### Story 5.2: Outcome Scoring via `/evaluate` + Calibration Script

As a user feeding back the real conversation,
I want `/evaluate` to auto-score prior advice and recompute calibration,
So that advice quality becomes a number that moves (FR27 score side, FR25).

**Acceptance Criteria:**

**Given** a transcript whose participants have plans `awaiting outcome`
**When** `/evaluate` runs
**Then** it scores each awaiting plan against what happened (outcome resolved, `resolved_at` set) in the same run that updates profiles — the primary scoring path

**Given** resolved outcomes
**When** `scripts/calibrate.py` runs
**Then** it emits per-person, per-seat hit rate and Brier score from `advice_outcomes`, every number carrying `{"value": …, "n": …, "method": …}`
**And** it skips the reliability/resolution/uncertainty decomposition (statistical theater at solo n)
**And** comparisons stay within the same person/context — no cross-person leaderboards

**Given** an `/evaluate` run that resolves outcomes
**When** the pattern report prints
**Then** it shows the calibration movement (e.g., "Red Team: batting .71 → .73 on Chris (n=15)")

### Story 5.3: Outcome-Score Artifact — Scoring Without a Transcript

As a user whose conversation left no transcript,
I want a lightweight browser control to record how it went,
So that the loop still closes when there's nothing to `/evaluate` (FR27 alternate path, UX-DR16).

**Acceptance Criteria:**

**Given** a plan awaiting outcome
**When** the outcome-score artifact generates into `.parley/artifacts/`
**Then** it presents an ordinal picker — worked / partial / didn't — as selectable cards, DESIGN.md tokens inlined, no free text required

**Given** a selection
**When** Copy Prompt is clicked
**Then** the clipboard receives the deterministic score prompt for paste-back; the session records the outcome through the same script path as 5.2
**And** the artifact is stateless and keyboard-operable with WCAG AA contrast

### Story 5.4: Past-Win Receipts & Track Records Everywhere

As a user being advised,
I want dated receipts of what worked and live expert track records inside the documents,
So that I can see the system getting sharper — and trust advice proportionally (FR28, FR25 display, UX-DR5).

**Acceptance Criteria:**

**Given** a person with resolved outcomes
**When** `/advise` runs for them
**Then** the playbook top section shows dated past-win receipts queried from `advice_outcomes` (e.g., "warned-before-pitching landed last time `[2026-04-02 1:1, T9]`")

**Given** any document rendering a track record
**When** it prints
**Then** the line follows the convention: `Red Team: batting .71 on Chris (n=14) · Brier 0.19` — plain text, always with `n=`, never a bare number

**Given** corroborating or contradicting outcomes
**When** profile claims are re-rendered
**Then** confidence follows the lifecycle (new → low; corroborated → rises; contradicted → falls or flagged), always shown as `word (0.NN)`

## Epic 6: Share It, Fork It — Sanitized Exports & Public Template

Hand a profile to a friend; a stranger forks a clean repo. Export sanitizers with visible stripping, provenance-tagged imports, the scripted clean-fork guarantee, responsible-use framing, distribution polish.

### Story 6.1: `/export-profile` — Named & Archetype Sanitization

As a user handing a read to someone I trust (or to the public),
I want exports that strip the relationship layer and show me exactly what leaves,
So that sharing is safe by mechanism and the negative space is visible (FR29, NFR1 seam #2).

**Acceptance Criteria:**

**Given** `/export-profile chris`
**When** the preview prints before writing
**Then** relationship-layer fields render as `~~field~~ (stripped: relationship layer)` — struck, surviving monochrome — so the user sees what leaves
**And** the written export contains subject layer only: anecdotes generalized to traits ("tends to disengage when pitched without warning," never "shut down when you pitched X on Tuesday"), headed "starting hypothesis, not a verdict"

**Given** `/export-profile chris --archetype`
**When** sanitization runs via `scripts/export_profile.py`
**Then** the output is additionally anonymized (no real name, no identifying detail) — the public-safe level

**Given** the golden-file test suite
**When** pytest runs
**Then** input profile → expected Named export → expected Archetype export triples in `tests/golden/` pass exactly — relationship-layer content provably cannot leak into either output

### Story 6.2: `/import-profile` — Their Chris ≠ Your Chris

As a user receiving someone else's read,
I want imports tagged with provenance and kept beside my own read,
So that two legitimately distinct interpretations never blend (FR30, NFR3).

**Acceptance Criteria:**

**Given** `/import-profile <file>`
**When** import runs
**Then** the imported read is stored with provenance (`imported · {source} · {date}`), distinct from the user's native profile data, and an import-summary doc prints naming what arrived

**Given** a person who already has a native profile
**When** the imported read is added
**Then** both reads render side by side — the imported one permanently tagged with the provenance chip, never merged into native claims

**Given** any later `/advise` or profile view for that person
**When** imported claims appear
**Then** they remain visibly tagged so the user always knows whose read they're consuming

### Story 6.3: `verify-clean-fork` — The Privacy Guarantee, Scripted

As a forker cloning the public template,
I want a scripted check proving zero private data and a clean first-run experience,
So that the privacy promise is a verifiable acceptance check, not a claim (FR31, NFR1 seam #3).

**Acceptance Criteria:**

**Given** a fresh clone of the template repo
**When** `scripts/verify_clean_fork.py` runs
**Then** it confirms zero private data — no profiles, no transcripts, no `index.sqlite` contents, no per-expert memory, no `config.local.yaml` — and exits 0 with a pass report; any finding exits 1 naming the offending path

**Given** CI on every push
**When** the workflow runs
**Then** `verify-clean-fork` executes against a fresh checkout alongside `claude plugin validate --strict` and the socket-blocked pytest run

**Given** the fresh fork's first run
**When** the forker starts
**Then** only archetype example profiles are present (`examples/archetype-*.md`), ADHD Specialist + Execution Realist are OFF, and the empty-state doc points to the one next command

### Story 6.4: Responsible-Use README & Distribution Polish

As the project owner publishing the template,
I want the README to set the ethical frame and the plugin to be one-click installable,
So that strangers fork a tool for improving their own communication — with eyes open (FR32, NFR5).

**Acceptance Criteria:**

**Given** the public README
**When** a stranger reads it
**Then** the responsible-use note covers all four points: the tool improves *your own* communication (not covert profiling), discretion around mutual contacts, profiles are interpretation not fact, and Archetype is the default-safe level for anything public
**And** it carries the FR24 validity caveats (transcript-derived personality is a weak signal) from the research

**Given** the fresh fork's first run
**When** the responsible-use note prints
**Then** it shows once, not on every session

**Given** distribution polish
**When** packaging completes
**Then** `.claude-plugin/marketplace.json` enables one-click install, `plugin.json` version is current, and `claude plugin validate --strict` still passes
