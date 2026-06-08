---
stepsCompleted: [1, 2, 3, 4, 5, 6, 7, 8]
lastStep: 8
status: 'complete'
completedAt: '2026-06-05'
inputDocuments:
  - '_bmad-output/planning-artifacts/prds/prd-parley_voo-2026-06-04/prd.md'
  - '_bmad-output/planning-artifacts/prds/prd-parley_voo-2026-06-04/addendum.md'
  - '_bmad-output/planning-artifacts/ux-designs/ux-parley_voo-2026-06-05/DESIGN.md'
  - '_bmad-output/planning-artifacts/ux-designs/ux-parley_voo-2026-06-05/EXPERIENCE.md'
  - 'docs/parley-spec.md'
  - '_bmad-output/planning-artifacts/research/technical-research-computed-evidence-2026-06-05.md'
  - '_bmad-output/planning-artifacts/research/domain-research-psych-methods-2026-06-05.md'
workflowType: 'architecture'
project_name: 'parley_voo'
user_name: 'Elliot'
date: '2026-06-05'
---

# Architecture Decision Document

_This document builds collaboratively through step-by-step discovery. Sections are appended as we work through each architectural decision together._

## Project Context Analysis

### Requirements Overview

**Functional Requirements:**

32 FRs in 8 clusters, mapping to distinct architectural subsystems:

| Cluster | FRs | Architectural implication |
|---|---|---|
| Modes & Commands | FR1–4 | Three command surfaces + quick/full cost tiers; mode routing logic |
| Deliberation Engine | FR5–9 | Core skill adapted from `ngmeyer/council-review`; dual topology (parallel / sequential decoder-ring handoff); standalone-usable; portable council export/import (`/export-council`, `/import-council`) |
| Expert Panels | FR10–15 | One agent file per seat; orthogonality via hard "Ignores:" prohibitions; citation rule enforced at synthesis; config posture local-vs-template (optional seats ON/OFF) |
| Persona Management | FR16–18 | Create/edit/research persona commands; per-mode default rosters; named-reasoning-method constraint |
| Profiles & Data | FR19–22 | Two-layer profile split **at storage time**; source-organized ingestion with context metadata (schema = architecture decision); user's own profile first-class |
| Computed Evidence | FR23–26 | Script layer: spaCy+lexicon metrics, lexicon-based Big Five (reframed — see below), Brier calibration, sqlite-vec + local embeddings |
| Feedback Loop | FR27–28 | `advice_outcomes` plan recording → outcome scoring → past-win receipts query path |
| Sharing & Distribution | FR29–32 | Export sanitizers (Named/Archetype), import provenance, gitignored private data, `verify-clean-fork` acceptance script, responsible-use docs |

**FR24 reframe (ratified by technical research):** "BFI item scoring as math" is not achievable from transcripts — BFI items presume questionnaire answers. Architecture treats transcript-derived Big Five as a **lexicon-based weak signal with published correlation ranges as confidence** (exactly what FR21 anticipates); IPIP deterministic keying retained only for self-administered questionnaires. Validity caveats carry into the responsible-use note (FR32).

**Non-Functional Requirements:**

- **NFR1 Privacy** — hard layer separation at storage time; no third-party API calls (local embeddings, local lexicons); export strips relationship layer
- **NFR2 Cost** — quick mode default; debate only where it earns tokens
- **NFR3 Portability** — markdown profiles; councils consumable by other LLMs
- **NFR4 Bounded infra** — single SQLite file, no server; graph DB deferred
- **NFR5 Responsible use** — interpretation-not-fact framing; mutual-benefit influence; Archetype public-safe default
- **NFR6 Anti-sycophancy** — independence-first protocol; dissent preserved

**Scale & Complexity:**

- Primary domain: **Claude Code-native agentic system** (skills + agents + commands + evidence scripts + local data store) — not web/mobile/API
- Complexity level: **medium** (novel multi-agent orchestration; trivial ops: solo user, local, no server)
- Estimated architectural components: ~10 (estimate, not commitment): engine skill, persona agents, command layer, ingestion pipeline, evidence scripts, storage layer, calibration loop, export/import sanitizers, HTML artifact generators, fork-verification

### Technical Constraints & Dependencies

- **Engine lineage:** adapt `ngmeyer/council-review` SKILL.md (Karpathy LLM Council + DMAD ICLR 2025); harvest protocol, graft experts/memory/storage
- **Script runtime — OPEN DECISION:** Python (research-recommended: spaCy, sentence-transformers, sqlite-vec bindings all Python-native) vs Deno/bun house style vs polyglot split. Single-runtime bias (two toolchains = two ways a forker's install fails). Resolve at tech-stack step.
- **Ingestion input format:** Zoom transcripts arrive as **markdown files** (user-confirmed) — normalization is near-free; architecture must define the line/turn-addressing convention that serves FR12 citations. (Cosmetic note: EXPERIENCE.md Flow 1 uses a `.vtt` example filename; ingestion is source-extensible, no spine change needed.)
- **Storage (spec-locked):** `people/<name>.md` (YAML frontmatter, two layers), `transcripts/`, single `index.sqlite` (people, conversations, patterns, conflicts, advice_outcomes), per-expert memory dirs (user-confirmed feature; privacy surface — see concern #1)
- **Embeddings:** local `all-MiniLM-L6-v2` via sentence-transformers; `embedding_model_id` + `lexicon_version` stored in DB for reproducibility
- **License caveat:** NRC EmoLex is research-only — vet before bundling in public template
- **UX contracts:** DESIGN.md + EXPERIENCE.md are binding (terminal markdown conventions, two stateless HTML artifacts, spine wins on conflict)

### Cross-Cutting Concerns Identified

1. **Privacy boundary** — subject/relationship split touches storage schema, write logic, export, import, gitignore, fork verification. Verification must exist at **three seams**: storage-write (claims land in the correct layer), export (relationship-layer content cannot leak into output), and **derived state** (per-expert memory dirs accumulate unsanitized quotes — gitignored, never exported). `verify-clean-fork` alone checks only the repo seam.
2. **Citation rule (FR12)** — requires line/turn-addressable transcript storage; touches ingestion, sqlite-vec chunking (per-turn, speaker-keyed), every seat prompt, chairman synthesis
3. **Confidence & calibration display** — `word (0.NN)` convention + track records with n; touches evidence scripts, profile schema, all document rendering
4. **Quick/full mode** — touches engine topology, roster resolution, token budgets, playbook rendering
5. **Local-vs-template config posture** — optional seats, defaults, gitignore; touches persona config, commands, distribution
6. **Orthogonality enforcement** — "Ignores:" hard prohibitions authored from research orthogonality matrix; touches persona files and synthesis weighting

## Starter Template Evaluation

### Primary Technology Domain

Claude Code-native agentic system (plugin: skills + agents + hooks + scripts + local SQLite/markdown store). No web/mobile/API starter applies.

### Starter Options Considered

| Option | Verdict | Facts |
|---|---|---|
| `ngmeyer/council-review` (standalone) | Harvest-only | **Archived 2026-05-31**, MIT; superseded by monorepo |
| `ngmeyer/skills` monorepo → `skills/productivity/council-review/` | **Harvest prompt contract** | MIT, active (pushed 2026-06-04); V2.1 protocol; also ships `/adversarial-review` |
| `aiwithremy/claude-skills-llm-council` (441★) | Skip | **No license** (unforkable); simpler clone, stale |
| `tenfoldmarc/llm-council-skill` (208★) | Skip | **No license**; single-commit clone |
| `claude plugin init` CLI scaffold | **Adopt** | Official; generates `.claude-plugin/plugin.json` + skills/agents/hooks layout; CI-validatable via `claude plugin validate --strict` |

### Selected Starter: `claude plugin init` scaffold + MIT prompt-contract harvest from `ngmeyer/skills`

**Rationale for Selection:**

No starter exists for this domain; the official plugin scaffold is the only structure that bundles skills + agents + hooks and is one-click installable/forkable (FR31/FR32 distribution). The deliberation "engine" upstream is pure prompt engineering — we lift the hard-won prompt craft verbatim (legally, MIT) and budget persistence, dual topology, and council export/import as original work. The spec's "harvest the engine" framing is hereby corrected: **there is no engine to harvest, only a protocol contract.**

**Initialization Command:**

```bash
claude plugin init parley-voo --with skills hooks
claude plugin validate ./ --strict   # CI gate
```

**Architectural Decisions Provided by Starter:**

- **Structure:** plugin root = repo root; `.claude-plugin/plugin.json` (+ `marketplace.json` for one-click install); `skills/<name>/SKILL.md` per command surface; `agents/*.md` per persona seat; `bin/` auto-PATHed scripts
- **Commands are skills:** `/advise`, `/evaluate`, `/council` etc. are each `skills/<name>/SKILL.md` — no legacy `commands/` tier (docs: use skills for new work). UX spine's slash-command IA is unaffected; only the implementation unit changes
- **SKILL.md discipline:** body <500 lines, references split out (upstream's 31KB single file violates this — restructure on harvest); `context: fork` + `agent:` for sub-agent execution
- **Versioning:** explicit `version` in plugin.json (else every commit = new version)
- **Data location — flagged for Step 4:** docs recommend `${CLAUDE_PLUGIN_DATA}` for persistent state, but the spec requires *project-local* gitignored `people/`/`transcripts/`/`index.sqlite`. Template-repo-with-plugin-manifest can keep data project-local; resolve in core decisions
- **Harvest list (verbatim-lift candidates, MIT):** anonymization-shuffle instruction, Step 3.7 devil's-advocate-vs-consensus pass, sycophancy guardrail line, chairman output contract (Agrees / Clashes / Blind Spots / Recommendation / What You Lose / Do This First / Verify), composable flags pattern (`--quick`, `--confidence`)

**Note:** Project initialization using these commands should be the first implementation story.

## Core Architectural Decisions

### Decision Priority Analysis

**Critical (block implementation):** runtime, data home, turn addressing, ingestion metadata schema, engine invocation model
**Important (shape architecture):** model tiers, portable formats, config posture, CI gates
**Deferred (post-V1, with trigger):** graph DB (joins get ugly), Claude Project export, marketplace listing (distribution polish), ANN indexes in sqlite-vec (solo scale never needs them)

### Data Architecture

- **Store:** single `index.sqlite` + markdown files (spec-locked). **Python 3.12+** scripts, deps managed with **uv** (`pyproject.toml`); SQLite access via stdlib `sqlite3` + `sqlite-vec` extension (v0.1.7+, verified current)
- **Schema (resolves PRD Open Q1):** `people`, `conversations` (id, source, occurred_at, setting `1:1|group`, participants), `turns` (conversation_id, turn_no, speaker, text, char_span), `patterns`, `conflicts`, `advice_outcomes` (person_id, seat, forecast_prob, outcome, predicted_at, resolved_at), `vec_turns` (sqlite-vec, per-turn embeddings, speaker-keyed), `meta` (embedding_model_id, lexicon_version, schema_version)
- **Citation addressing (Elliot-decided):** **speaker-turn IDs** — ingestion normalizes markdown transcripts into canonical turn-structured files; `T17` = turn 17. Survives reformatting; UX spines updated to `[date context, Tnn]`
- **Two-layer enforcement:** profile writes go through one Python writer (`scripts/profile_write.py`) that routes claims to subject vs relationship layer by field schema — the privacy seam is a *chokepoint, not a convention*
- **Embeddings:** local `all-MiniLM-L6-v2` via sentence-transformers; model id stored in `meta`
- **Migrations:** none — versioned `schema/index.sql`, greenfield rebuilds during V1

### Engine & Orchestration

- **Invocation model:** council-engine is a skill whose orchestration is prompt-directed sub-agent fan-out (harvested upstream pattern); each seat = one agent definition in `agents/`
- **Dual topology:** two orchestration modes in the engine skill — `parallel` (evaluate: fan-out → anonymized shuffle → peer review → chairman) and `staged` (advise: Profile Translator ×2 → strategist trio parallel → Red Team → Execution Realist → synthesis). Topology declared per-roster, not per-command
- **Model tiers (Elliot-decided):** tiered defaults — haiku-class seats, strong-model chairman + Red Team — **overridable per roster** in the roster config
- **Quick/full:** quick = trimmed roster + no peer review (roster config names its own quick subset); `--full` flag escalates; `/evaluate` pinned full
- **Roster/persona format (FR9 portable):** persona = markdown + YAML frontmatter (name, method, ignores, tier, memory dir); council = markdown roster file listing seats + topology + tiers. Plain-text portable to any LLM by construction

### Security & Privacy

No auth, no server, no network. In their place:

- **No-network invariant:** evidence scripts make zero external calls (local lexicons, local embeddings) — enforceable in CI by socket-blocking the pytest run
- **Three privacy seams, each verified:** storage-write (layer-routing chokepoint + unit tests), export (sanitizer strips relationship layer + golden-file tests), repo (`verify-clean-fork` + `.gitignore` for `people/`, `transcripts/`, `index.sqlite`, `agents/**/memory/`)
- **Per-expert memory (Elliot-kept):** `agents/<seat>/memory/` — gitignored, never exported, excluded from council export

### Document & Artifact Rendering

- Documents are markdown emitted per DESIGN.md terminal conventions (binding contract)
- HTML artifacts (roster picker, outcome scorer) generated from Python string templates into `.parley/artifacts/` — stateless, DESIGN.md tokens inlined

### Infrastructure & Deployment

- **Distribution (Elliot-decided):** public template repo, clone = private instance, data project-local; `.claude-plugin/plugin.json` in-repo so the engine is plugin-loadable; marketplace = polish phase
- **CI (GitHub Actions):** `claude plugin validate --strict` · `verify-clean-fork` against fresh clone · `pytest` (evidence scripts, sanitizers, schema) · no-network guard
- **License:** MIT (matches harvest source; required for public fork)

### Decision Impact Analysis

**Implementation sequence:** scaffold (plugin init + schema) → ingestion/turn normalization → engine skill + 2 topologies → personas → evidence scripts → commands → feedback loop → sharing → distribution polish

**Cross-component dependencies:** turn IDs underpin citations, vec chunking, and receipts → ingestion lands early; layer-routing chokepoint must exist before any `/evaluate` writes profiles; roster config format blocks persona management and quick-mode resolution

## Implementation Patterns & Consistency Rules

### Critical Conflict Points Identified

9 areas where implementing agents could diverge: SQL naming, person slugs, seat IDs, script I/O, frontmatter keys, date formats, document conventions, file placement, test layout.

### Naming Patterns

**Database (SQLite):**

- Tables: **plural snake_case** — `people`, `conversations`, `turns`, `patterns`, `conflicts`, `advice_outcomes` (spec-locked names)
- Columns: snake_case; FKs `<singular>_id` (`person_id`, `conversation_id`); booleans `is_*`; timestamps `*_at`
- All dates/times: **ISO 8601 strings, UTC** (`2026-06-05T14:30:00Z`); date-only allowed where time is meaningless (`occurred_on`)

**Identifiers:**

- Person slug: **lowercase-kebab from display name** — `chris`, `dana-w` → `people/chris.md`; slug is the FK-stable key, display name lives in frontmatter
- Seat IDs: **canonical kebab-case** — `behavioral-coder`, `red-team`, `execution-realist` — used identically in `agents/<seat-id>.md` filenames, DB `seat` column, roster files, and memory dirs. Display names ("Red Team") only in rendered documents
- Skills: `skills/<kebab>/SKILL.md` matching the slash command — `skills/advise/`, `skills/export-profile/`

**Python:**

- Files/functions snake_case; scripts live flat in `scripts/` — `ingest.py`, `linguistic_features.py`, `personality.py`, `calibrate.py`, `recall.py`, `profile_write.py`, `export_profile.py`, `verify_clean_fork.py`

### Format Patterns

**Script I/O contract (the skill↔script seam — most important pattern in this doc):**

- Input: CLI args (argparse), never stdin
- Output: **JSON to stdout** (snake_case keys), human-readable progress to stderr
- Exit codes: `0` success · `1` user-fixable (bad input, missing file — message states the fix) · `2` internal error
- Every numeric claim a script emits carries its evidence fields: `{"value": 0.71, "n": 14, "method": "brier"}` — never a bare number (FR21/FR25)

**File frontmatter:** YAML, snake_case keys, across persona/council/profile/transcript files

**Persona file contract** (`agents/<seat-id>.md`): frontmatter `seat_id`, `display_name`, `method` (named reasoning discipline), `ignores` (list — hard prohibitions), `role` (`seat|chairman`), `modes` (evaluate/advise behaviors); body = the prompt. Model tiers are resolved **only** in roster `model_overrides` — never hardcoded in persona files. `Ignores:` rendered as prominently as method in any UI (FR11)

**Council/roster file contract** (`councils/<name>.md`): frontmatter `topology` (`parallel|staged`), `seats` (ordered seat IDs; stage groups for staged), `quick_seats` (subset), `model_overrides` (optional). Body = purpose prose. This file IS the FR9 export format — no separate serialization. Import (`/import-council`, `/import-profile`) validates referenced seat IDs at import time — exit 1 listing the missing, never failing later mid-run

**Canonical transcript format** (`transcripts/<person-or-context>/<YYYY-MM-DD>-<slug>.md`): frontmatter `source`, `occurred_at`, `setting` (`1:1|group`), `participants` (slugs); body = numbered speaker turns. Turn-line grammar is pinned: lines matching `^\*\*T(\d+) · ([a-z0-9-]+):\*\* ` (turn number · interpunct · person slug · colon · space) start a turn; content continues until the next match. Turn IDs visible in the file itself, so citations are human-checkable

### Document & Display Patterns (binding via DESIGN.md)

- Citations `[date context, Tnn]` · confidence `word (0.NN)` · attribution `— Display Name, method` · track records always with `n=`
- Empty states: one sentence + the one next command — never apologize, never spinner

### Process Patterns

- **Layer routing — default-deny:** nothing writes `people/*.md` except `profile_write.py`; skills pass claims as JSON, the script routes subject vs relationship by explicit field schema. **Unknown field → exit 1 with the field named — never silently routed to subject.** Property test required: no input JSON reaches the subject file without an explicit schema match
- **Errors in session:** script exit 1 → skill prints the fix line verbatim; exit 2 → skill says what failed and where the stderr log is
- **No-network guard:** `pytest-socket` blocks all sockets in the test run; evidence scripts must pass with sockets disabled
- **Tests:** pytest, `tests/test_<script>.py`, golden files in `tests/golden/` (export sanitization has golden pairs: input profile → expected Named export → expected Archetype export)

### Enforcement Guidelines

All implementing agents MUST: (1) use seat IDs/person slugs as the only cross-file keys, (2) honor the script I/O contract, (3) route profile writes through the chokepoint, (4) match DESIGN.md display conventions verbatim. Enforcement: CI (pytest + golden files + verify-clean-fork + pytest-socket) and these patterns land in `project-context.md` at handoff so every future dev session inherits them.

### Anti-Patterns

- A second script that writes profile markdown directly (bypasses privacy chokepoint)
- Bare numbers without `n`/confidence anywhere in output
- Seat display names as keys (breaks when renamed)
- Model tiers hardcoded in persona files (kills per-roster override)
- Wide tables or color-dependent meaning in terminal docs (UX contract violation)

## Project Structure & Boundaries

### Complete Project Directory Structure

```
parley-voo/                          # plugin root = repo root (public template)
├── README.md                        # vision + quickstart + responsible-use note (FR32)
├── LICENSE                          # MIT
├── CLAUDE.md                        # how Claude Code operates in this project
├── pyproject.toml                   # uv-managed; spacy, sentence-transformers, sqlite-vec, pytest, pytest-socket
├── .python-version
├── .gitignore                       # people/ transcripts/ ingest/ index.sqlite .parley/ config.local.yaml
├── .github/workflows/ci.yml         # plugin validate · pytest (socket-blocked) · verify-clean-fork
├── .claude-plugin/
│   ├── plugin.json                  # name, version, skills[] paths
│   └── marketplace.json             # one-click install (polish phase)
├── skills/
│   ├── council-engine/              # the deliberation engine (FR5–8)
│   │   ├── SKILL.md                 # orchestration: roster resolution, mode, fan-out
│   │   └── references/
│   │       ├── protocol.md          # harvested contract: shuffle, devil's-advocate, chairman output
│   │       └── topologies.md        # parallel vs staged execution detail
│   ├── evaluate/SKILL.md            # FR1: ingest→panel→report→profile updates→outcome scoring
│   ├── advise/SKILL.md              # FR2: staged pipeline→playbook→plan recording
│   ├── council/SKILL.md             # FR3: generic verdict
│   ├── persona/SKILL.md             # FR16: /persona create|edit|research
│   ├── export-profile/SKILL.md      # FR29 (+ Named/Archetype sanitization)
│   ├── import-profile/SKILL.md      # FR30 (provenance tagging)
│   ├── export-council/SKILL.md      # FR9
│   └── import-council/SKILL.md      # FR9 (seat-ID validation at import)
├── agents/                          # one file per seat (shipped code, no private data)
│   ├── behavioral-coder.md          # ┐
│   ├── psycholinguist.md            # │ evaluate panel (FR10)
│   ├── personality-profiler.md      # │
│   ├── relational-needs-analyst.md  # ┘
│   ├── adhd-specialist.md           # optional seat (FR15)
│   ├── profile-translator.md        # ┐
│   ├── message-strategist.md        # │
│   ├── negotiation-architect.md     # │ advise pipeline (FR13)
│   ├── influence-tactician.md       # │ (FR14 guardrail in-prompt)
│   ├── red-team.md                  # │
│   ├── execution-realist.md         # ┘ optional seat (FR15)
│   └── chairman.md                  # role: chairman (synthesis contract)
├── councils/                        # roster files = FR9 portable format
│   ├── evaluate-default.md          # topology: parallel
│   ├── advise-default.md            # topology: staged
│   └── council-default.md           # topology: parallel (generic)
├── schema/index.sql                 # versioned; people, conversations, turns, patterns,
│                                    #   conflicts, advice_outcomes, vec_turns, meta
├── scripts/
│   ├── ingest.py                    # markdown → canonical turns → DB + embeddings (FR22, FR26)
│   ├── linguistic_features.py       # FR23
│   ├── personality.py               # FR24 (reframed)
│   ├── calibrate.py                 # FR25
│   ├── recall.py                    # FR26 semantic search
│   ├── profile_write.py             # THE privacy chokepoint (FR19, default-deny)
│   ├── export_profile.py            # FR29 sanitizers
│   └── verify_clean_fork.py         # FR31
├── templates/
│   ├── profile.subject.md
│   ├── profile.relationship.md
│   └── artifacts/                   # roster-picker.html, outcome-score.html (DESIGN.md tokens)
├── examples/
│   └── archetype-skeptical-stakeholder.md
├── config.yaml                      # template defaults (optional seats OFF — FR15)
├── tests/
│   ├── test_ingest.py … test_export_profile.py
│   └── golden/                      # export sanitization input→Named→Archetype triples
│
│  # ——— everything below is GITIGNORED (private instance data) ———
├── config.local.yaml                # local overrides (ADHD Specialist + Execution Realist ON)
├── ingest/                          # raw drop zones by source (FR22)
│   ├── transcripts/                 #   Zoom markdown exports
│   └── slack/
├── transcripts/                     # canonical normalized turn files (citation targets)
├── people/                          # <slug>.md two-layer profiles
├── .parley/
│   ├── artifacts/                   # generated HTML (roster picker, outcome scorer)
│   └── memory/<seat-id>/            # per-expert memory (moved out of agents/ — data, not code)
└── index.sqlite
```

### Architectural Boundaries

| Boundary | Rule |
|---|---|
| **skill ↔ script** | JSON-over-CLI contract only (argparse in, JSON stdout, exit codes) |
| **skill ↔ seats** | sub-agent fan-out per topology; seats never see each other's raw output pre-shuffle |
| **script ↔ SQLite** | only Python scripts touch `index.sqlite`; skills never query directly |
| **anything ↔ people/** | writes only via `profile_write.py` (default-deny chokepoint) |
| **code ↔ data** | shipped code above the gitignore line; private data below; the line IS the privacy boundary (FR31) |
| **rendering** | documents/artifacts follow DESIGN.md + EXPERIENCE.md verbatim |

### Requirements → Structure Mapping

| FR cluster | Lives in |
|---|---|
| FR1–4 commands | `skills/{evaluate,advise,council}/` |
| FR5–9 engine | `skills/council-engine/` + `councils/` |
| FR10–15 panels | `agents/*.md` + `config.yaml`/`config.local.yaml` |
| FR16–18 persona mgmt | `skills/persona/` + `agents/` |
| FR19–22 profiles/data | `templates/`, `people/`, `scripts/{ingest,profile_write}.py`, `schema/` |
| FR23–26 evidence | `scripts/{linguistic_features,personality,calibrate,recall}.py` |
| FR27–28 feedback | `advice_outcomes` tables + `scripts/calibrate.py` + advise/evaluate skills |
| FR29–32 sharing | `skills/{export,import}-*` + `scripts/{export_profile,verify_clean_fork}.py` + README + CI |

### Data Flow

`ingest/` (raw) → `ingest.py` → `transcripts/` (canonical Tnn files) + `turns`/`vec_turns` (DB) → `/evaluate` fans out seats (reading canonical + computed metrics) → chairman synthesizes (citations checked) → `profile_write.py` routes claims → `people/<slug>.md` → `/advise` reads profiles + `recall.py` receipts + `calibrate.py` track records → playbook + plan recorded → next `/evaluate` closes the loop.

## Architecture Validation Results

### Coherence Validation ✅

**Decision compatibility:** Python 3.12 + uv + spaCy + sentence-transformers + sqlite-vec (0.1.7+) verified mutually compatible (research, 2026-06-05). Turn-ID citations reconciled into DESIGN.md/EXPERIENCE.md (UX decision log updated). Plugin manifest coexists with template-repo distribution. Tiered models live only in roster `model_overrides` — no conflict with persona `role` field.

**Pattern consistency:** seat IDs/person slugs are the universal keys across DB, filenames, rosters, memory dirs. Script I/O contract matches skill orchestration model. Default-deny chokepoint aligns with NFR1.

**Structure alignment:** gitignore line cleanly separates shipped code from private data; `.parley/memory/` relocation keeps `agents/` pure code.

### Requirements Coverage Validation ✅

Every FR cluster maps to concrete paths (see Requirements → Structure Mapping). NFR enforcement: NFR1 → three verified seams; NFR2 → quick mode + tiered models; NFR3 → markdown-everything + councils-as-files; NFR4 → single SQLite + deferred list; NFR5 → reframed FR24 caveats + guardrail prompts + Archetype default-safe; NFR6 → harvested anonymization-shuffle + devil's-advocate protocol.

### Validation Issues Addressed

1. **Citation verification was aspirational** (FR12 said "or the chairman discards it" with no mechanism) → **resolved:** `recall.py --verify-citations` accepts a list of `Tnn` refs + conversation id, returns which exist; the chairman step calls it before accepting any claim. Hallucinated citations become mechanically impossible, not just discouraged.
2. **Self-profile had no slug convention** (FR20) → **resolved:** reserved slug **`me`** — `people/me.md`; Profile Translator's self decoder ring reads it; rename-proof.

### Gap Analysis Results

**Critical:** none.
**Important:** none open (2 found, both resolved above).
**Minor (logged, story-level):** (a) exact prompt text the HTML artifacts emit on Copy Prompt — define in artifact stories; (b) NRC EmoLex license vetting before public bundling — hedge lexicon is hand-maintained so FR23 doesn't block on it; (c) `conflicts` table usage is spec-carried but thin — define or drop during the `/evaluate` epic.

### Architecture Completeness Checklist

**Requirements Analysis**

- [x] Project context thoroughly analyzed
- [x] Scale and complexity assessed
- [x] Technical constraints identified
- [x] Cross-cutting concerns mapped

**Architectural Decisions**

- [x] Critical decisions documented with versions
- [x] Technology stack fully specified
- [x] Integration patterns defined
- [x] Performance (token cost) considerations addressed

**Implementation Patterns**

- [x] Naming conventions established
- [x] Structure patterns defined
- [x] Communication patterns specified
- [x] Process patterns documented

**Project Structure**

- [x] Complete directory structure defined
- [x] Component boundaries established
- [x] Integration points mapped
- [x] Requirements to structure mapping complete

### Architecture Readiness Assessment

**Overall Status:** READY FOR IMPLEMENTATION
**Confidence Level:** high — every load-bearing decision is either user-ratified, research-verified, or spec-locked; the three minors are story-level

**Key Strengths:**

- Privacy enforced by mechanism (chokepoint, socket-block, golden files), not convention
- Citations mechanically verifiable (`recall.py --verify-citations`)
- The one genuinely novel subsystem (dual-topology engine) harvests a proven protocol contract (MIT)

**Areas for Future Enhancement:** marketplace packaging, Wilson CIs on hit rates, ANN indexes if scale ever demands

### Implementation Handoff

**AI Agent Guidelines:**

- Follow all architectural decisions exactly as documented
- Implementation patterns are binding; DESIGN.md + EXPERIENCE.md govern all rendering
- Respect project structure and boundaries
- Refer to this document for all architectural questions

**First Implementation Priority:** `claude plugin init parley-voo --with skills hooks` + `schema/index.sql` (the scaffold story)
