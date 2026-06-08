---
baseline_commit: 21d115efcea67aea4a869b7a80ce9db386fd3af4
---

# Story 1.4: `/council` — Generic Verdicts

Status: done

<!-- Created 2026-06-07 by create-story workflow — ultimate context engine analysis completed -->

## Story

As a user facing a decision,
I want to run `/council "should we do X"` and get a dissent-preserving verdict document,
So that I get structured deliberation with zero coach-pipeline setup (FR3, FR8).

## Acceptance Criteria

1. **Given** a fresh install with no profiles, transcripts, or database present, **when** `/council "should we drop the enterprise tier?"` runs, **then** the engine executes standalone with `councils/council-default.md` (quick mode) and prints a verdict document — proving FR8.
2. **Given** the printed verdict, **when** inspecting the document, **then** it follows terminal conventions: one `#` title, first line states what it is, heading depth ≤ `###`, no wide tables, header notes `quick mode`/`full mode`, **and** dissent appears under an explicit `Dissent:` label with attribution `— Seat, method`, **and** any confidence is rendered `word (0.NN)`, never bare.
3. **Given** the same command with `--full`, **when** it runs, **then** all seats plus peer review execute and the header reflects full mode.

## Tasks / Subtasks

- [x] Task 1: Author the three generic council personas in `agents/` (AC: 1)
  - [x] `agents/pragmatist.md` — method: cost-benefit triage; ignores: theoretical purity, sunk costs. `agents/risk-officer.md` — method: failure-mode enumeration; ignores: upside arguments, average-case outcomes. `agents/first-principles.md` — method: first-principles decomposition; ignores: convention/popularity of a practice, short-term convenience. (Seat IDs/methods validated live in the 1.2/1.3 smoke runs — promote that proven orthogonal trio, generic-decision flavored, NOT person-reading: the evaluate panel is Story 2.1's.)
  - [x] Each file carries the FULL dual key set (Claude Code `name` + `description`, persona `seat_id`/`display_name`/`method`/`ignores`/`role: seat`/`modes`) — `tests/test_persona_contract.py` auto-covers every `agents/*.md` uniformly (non-empty values, seat_id == filename stem, NO model/tier keys)
  - [x] Each `description` scoped tight ("council seat — spawn only inside a council-engine deliberation") — these become LIVE plugin agents on install; include the verbatim sycophancy guardrail in each body per `references/protocol.md` §3
- [x] Task 2: Author `councils/council-default.md` — the minimal default council (AC: 1, 3)
  - [x] Frontmatter per the binding roster contract: `topology: parallel`, `seats: [pragmatist, risk-officer, first-principles]`, `quick_seats: [pragmatist, risk-officer]` (strict subset — makes AC 3's "all seats" observably different), `model_overrides:` map with `chairman: strong-model`; body = purpose prose (this file IS the FR9 export format)
  - [x] MUST satisfy the engine's 1.3-hardened validation: `quick_seats` present + non-empty + subset; NO `chairman` in `seats` (implicit); no duplicates — re-read SKILL.md Step 1 before authoring
- [x] Task 3: Author `skills/council/SKILL.md` — the `/council` command (AC: 1, 2, 3)
  - [x] Frontmatter `name: council` + `description` (--strict requires both); body <500 lines; skill dir matches the slash command (`skills/council/`)
  - [x] Input contract: the decision text (quoted argument); optional `--full` flag → forward to the engine as mode escalation (default quick). The command NEVER defines mode semantics or topology — it forwards the flag and names the roster (`councils/council-default.md`), full stop (1.3 HARD RULE)
  - [x] Invoke the council-engine skill (roster + framed input + mode); the engine owns orchestration, validation, and the dissent-attribution substitution
  - [x] **Standalone guarantee (FR8), written as a hard instruction:** `/council` must not read `people/`, `transcripts/`, `index.sqlite*`, or any `memory/` dir — no profile context, no person. A fresh clone with none of those present runs clean
  - [x] Verdict document rendering contract: one `#` title (`# Verdict: <decision>`); FIRST line under the title states what the document is + the mode (e.g. `Council verdict — quick mode (2 seats, no peer review). Dissent preserved.`); chairman's 7 contract sections follow as `###`; heading depth ≤ `###`; no wide tables
  - [x] **Render-check pass (the 1.2/1.3 smoke wobbles, now owned here):** before printing, mechanically verify and fix: every confidence is `word (0.NN)` (never bare, never "8 of 10"), every `Dissent:` attribution is `— {Display Name}, {method}` (engine substitution applied), no heading deeper than `###`, no extra sections beyond the chairman contract (fold a stray devil's-advocate-answer section into Clashes)
- [x] Task 4: Structural tests (AC: 1, 2)
  - [x] Extend `tests/test_persona_contract.py`: council-default roster checks via targeted flat reads (file exists; `topology: parallel`; `seats`/`quick_seats` lines parse as flat lists with quick ⊊ seats, non-empty; `chairman` not in seats) — do NOT use the frontmatter splitter on `model_overrides` (nested map, flat parser would misread indented keys)
  - [x] `skills/council/SKILL.md` checks: exists, `name`/`description` present, <500 lines, contains the standalone-guarantee markers (`people/`, `index.sqlite`) and the mode-forwarding rule (`--full`)
  - [x] Existing uniform persona tests must pass over the 3 new agents with zero test changes (that's the point of the uniform contract) — run and confirm, don't weaken
- [x] Task 5: Validation + CI green (AC: all)
  - [x] `claude plugin validate ./ --strict` exit 0 (now validates 4 agents + 2 skills); `uv run pytest` green; push; both CI jobs green
- [x] Task 6: Live smoke verification — the FR8 proof (AC: 1, 2, 3)
  - [x] Quick run (default): in-session, execute the `/council` skill flow on a toy decision using the SHIPPED roster + personas (file-verbatim prompts — the 1.3 lesson); verify: only `quick_seats` spawned (2 seats), no reviewer/DA spawns, verdict printed with `# Verdict:` title, first-line mode note, `Dissent:` with `— {Display Name}, {method}`, confidence `word (0.NN)`
  - [x] `--full` run: all 3 seats + 3 peer reviews + DA + chairman; header reflects full mode
  - [x] Standalone check: confirm `people/`, `transcripts/`, `index.sqlite` do not exist in the repo and nothing in the run referenced them (FR8 proof is their ABSENCE + a clean run)
  - [x] Record both run shapes + any rendering fixes the render-check pass had to apply in Dev Agent Record

### Review Findings

- [x] [Review][Patch] MED: command input handling has unguarded paths — empty/whitespace quoted decision runs the engine on nothing; `--full` inside the quoted decision text could silently escalate; unknown flags (`--quick`, `-f`) fall through into the decision text; multi-line decision capture unspecified [skills/council/SKILL.md — Inputs + Step 1]
- [x] [Review][Patch] MED: mode-header seat count `N` unbound — nothing says N = the engine's ACTUAL participating seat count (chairman excluded); a model could fill it from roster length, mislabeling quick runs as "3 seats" [skills/council/SKILL.md — Step 3]
- [x] [Review][Patch] MED: quick-mode Blind Spots has no defined source — chairman.md defines the section as "what no response addressed until peer review surfaced it," but quick mode has no peer review; the exactly-seven render-check then pressures fabrication. Chairman needs a quick-mode definition + permission to say "none"; render-check must allow present-but-empty [agents/chairman.md — output contract; skills/council/SKILL.md — Step 4 rule 4]
- [x] [Review][Patch] LOW: render-check overreach risks — rule 1 could rewrite a deliberately unquantified claim into a fabricated number (must apply only to confidence claims actually made); rule 2 has no stated zero-dissent path (absence of dissent is valid, not a violation) [skills/council/SKILL.md — Step 4 rules 1–2]
- [x] [Review][Patch] LOW: roster prose omits that chairman synthesis still runs in quick mode — "runs the Pragmatist and Risk Officer with no peer review" reads as the complete quick run [councils/council-default.md — body]
- [x] [Review][Patch] LOW: test hardening — seat IDs unvalidated against kebab-case (comma-in-element would silently mis-parse the flat list); FR8 marker `index.sqlite` passes vacuously if the prohibition is gutted but the word survives (assert `index.sqlite*` + "Never read"); `model_overrides` keys never validated ⊆ seats ∪ {chairman} [tests/test_persona_contract.py]
- [x] [Review][Patch] LOW: Dev Agent Record "18 passed" conflates suite scope — reads as if all 18 live in the persona file; actual split is 13 persona-contract + 5 schema [story file — Debug Log]

## Dev Notes

### Critical context — read before coding

- **Final story of Epic 1 — this is the payoff.** Everything 1.1–1.3 built becomes user-touchable: `/council "question"` → verdict. Deliverables: 3 persona files, 1 roster file, 1 command skill, tests, smoke proof. Still prompt engineering + structural pytest; no Python scripts, no SQLite.
- **Repo state after 1.3 (commit `21d115e`, review findings resolved):** engine at `skills/council-engine/` (SKILL.md 223 lines: roster validation incl. mandatory non-empty `quick_seats`, mode resolution, parallel + staged dispatch); `agents/chairman.md` (quick-tolerant, pinned status-line, label-attribution); `references/{protocol,topologies}.md`; 16 tests green. **No `councils/` dir exists yet — this story creates it.**
- **PLANNING CONFLICT, RESOLVED HERE:** epics.md Story 2.3 lists `council-default.md` among the rosters it authors, but 1.4's AC 1 cannot pass without it, and 1.2/1.3 scope notes both deferred rosters TO 1.4. **Decision: 1.4 authors `councils/council-default.md` + its generic personas. Story 2.3's scope shrinks to evaluate-default + advise-default + config posture** (it may layer config-posture handling onto council-default but does not create it). Note this in the completion summary so 2.3's create-story run inherits the correction.
- **The generic seats are NOT the Epic 2 panels.** Story 2.1 owns the evaluate panel (behavioral-coder, psycholinguist, personality-profiler, relational-needs-analyst, adhd-specialist); 2.2 owns the advise pipeline (profile-translator, message-strategist, negotiation-architect, influence-tactician, red-team, execution-realist). The generic council reads DECISIONS, not people — its seats must be person-agnostic. The 1.2/1.3 smoke trio (cost-benefit / failure-mode / first-principles) is validated material: two live runs produced genuine orthogonal reasoning and real dissent. Promote that trio to shipped personas (cleaned up, contract-complete).
- **Plugin auto-load is now REAL:** unlike the test fixtures, these personas + the `/council` skill go live in every session with the plugin. Descriptions must prevent accidental spawning for unrelated work (the chairman's description is the model to copy).

### Verdict document contract (assembled from binding sources)

```
# Verdict: should we drop the enterprise tier?

Council verdict — quick mode (2 seats, no peer review). Dissent preserved.

### Agrees
...
### Clashes        (value tension vs error catch)
### Blind Spots
### Recommendation (verdict; Dissent: entries with — {Display Name}, {method})
### What You Lose
### Do This First
### Verify
```

- One `#` title per document; first line under it states what the document is + mode [Source: epics.md#Story 1.4 AC; DESIGN.md terminal conventions]
- UX-DR11: "should we do X" answer; dissent preserved with explicit `Dissent:` label; chairman may side with a strong minority [Source: epics.md#UX-DR11]
- Reference dissent copy: `Dissent: Negotiation Architect would wait a week.` — and the EXPERIENCE.md Flow 2 climax has the chairman siding WITH the minority [Source: EXPERIENCE.md]
- Confidence `word (0.NN)` always; attribution `— {Seat name}, {method}`; bold only the load-bearing word; no color-dependent meaning [Source: DESIGN.md UX-DR1/3/4]
- The "Trimmed in quick mode" announced-trim line is PLAYBOOK UX (UX-DR8, Story 4.1) — the verdict's quick-mode marker is the first-line mode note, don't import the playbook trim machinery

### Engine contract this command consumes (do not re-implement)

- Engine inputs: roster path + framed input + optional mode escalation; quick is default [Source: skills/council-engine/SKILL.md#Inputs — current file]
- Engine owns: roster validation (incl. mandatory non-empty `quick_seats` — the roster you author must pass it), model tiers (haiku seats / strong chairman via `model_overrides`), fan-out, shuffle, review/DA (full only), chairman spawn with pinned status line `Mode: <quick|full> · Topology: <parallel|staged>`, and the label→`— {Display Name}, {method}` dissent substitution at render time
- The command owns: framing the input, forwarding `--full`, the document shell (title + first line), and the render-check pass
- FR8 mechanically: no `people/`, no `transcripts/`, no `index.sqlite*`, no memory dirs — the engine never touches them and neither may the command [Source: prd.md#FR8; architecture.md#Security & Privacy]

### Scope boundaries — what this story does NOT include

- NO evaluate/advise personas or rosters (2.1/2.2/2.3); NO config.yaml posture, NO optional-seat ON/OFF (2.3)
- NO `/evaluate`, NO `/advise` commands (3.6/4.1); NO citation machinery — generic verdicts cite nothing (`[date context, Tnn]` citations need transcripts, Epic 3)
- NO roster picker / persona picker artifacts (2.5); NO export/import (2.6)
- NO staged topology exercise — council-default is `topology: parallel`; staged shipped in 1.3 and gets its production run in 4.x
- CI stays exactly two jobs

### Previous story intelligence (1.3, status done — review-hardened)

- The 1.3 code review (parallel clean-context layers) found 9 patchable findings; the classes to pre-empt here: validation holes (quick_seats vacuous subset — now mandatory, your roster must comply), self-contradicting rules, stale cross-references, vacuous test markers. Write the roster/tests against the CURRENT SKILL.md text, not memory of it.
- Smoke honesty bar (1.2/1.3 precedent): drive sub-agents with file-verbatim prompts; record deviations explicitly. Two known model wobbles this story must catch in its render-check: extra DA-answer section (1.2 + 1.3 full runs), `high (8 of 10)` confidence format (1.3 quick run).
- Sub-agents inherit the user's global CLAUDE.md (a 1.3 smoke seat addressed the user by name mid-document) — the command skill's seat prompts should re-state "your final text is the raw document/response, not a message to a human."
- Commit cadence: implementation commit → review/fix commits → `gh run watch --exit-status`. Pins: setup-uv `@v8.2.0`, checkout `@v5` — don't touch.
- Flat frontmatter parser in tests handles `key: value` + flat `[a, b]` lists ONLY — roster `model_overrides` is nested; use targeted line checks for it or skip it in tests (Task 4 boundary).

### Testing standards

- pytest, extend `tests/test_persona_contract.py`; zero new deps; sockets blocked
- The 3 new personas get covered by the EXISTING uniform tests automatically — that's the contract working; add only roster + command-skill checks
- Runtime behavior (spawn counts, document shape) is live-smoke territory, recorded in Dev Agent Record — pytest verifies structure only

### Project Structure Notes

New items only:

```
agents/pragmatist.md                 # generic seat (promoted from smoke trio)
agents/risk-officer.md               # generic seat
agents/first-principles.md           # generic seat
councils/council-default.md          # NEW DIR — minimal default council (FR9 format)
skills/council/SKILL.md              # the /council command
tests/test_persona_contract.py       # MODIFY: roster + command-skill checks
```

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Story 1.4] — story + ACs (verbatim); UX-DR1/3/4/11
- [Source: _bmad-output/planning-artifacts/epics.md#Story 2.1/2.2/2.3] — ownership boundaries + the council-default conflict resolved above
- [Source: _bmad-output/planning-artifacts/prds/prd-parley_voo-2026-06-04/prd.md#FR3/FR4/FR8] — command contract, quick default, standalone guarantee
- [Source: _bmad-output/planning-artifacts/architecture.md#Engine & Orchestration / Project Structure] — `skills/council/SKILL.md` placement, council-default `topology: parallel (generic)`, roster contract
- [Source: _bmad-output/planning-artifacts/ux-designs/ux-parley_voo-2026-06-05/DESIGN.md + EXPERIENCE.md] — verdict anatomy, terminal conventions, dissent copy, empty-state/fresh-fork posture
- [Source: _bmad-output/implementation-artifacts/1-3-dual-topology-quick-full-modes.md#Review Findings + Dev Agent Record] — hardened engine validation, smoke wobbles the render-check must own
- [Source: skills/council-engine/SKILL.md + agents/chairman.md — current files at `21d115e`] — the live engine contract this command consumes

## Dev Agent Record

### Agent Model Used

claude-opus-4-8[1m] (Claude Code); smoke seats/reviewers on haiku-class, DA + chairman on strong model per roster `model_overrides`

### Debug Log References

- RED: 2 new structural tests failed pre-authoring (11 existing passed)
- GREEN: `uv run pytest` → 18 passed (full suite: 13 in test_persona_contract.py + 5 in test_schema.py); `claude plugin validate ./ --strict` → ✔ (4 agents + 2 skills); council SKILL.md 83 lines
- CI green on `5ada55a` via `gh run watch --exit-status`
- FR8 state verified before smoke: no `people/`, no `transcripts/`, no `index.sqlite*` in the repo

### Completion Notes List

- The uniform persona contract paid off: all 3 new agents passed the existing `tests/test_persona_contract.py` checks with ZERO test changes — only roster + command-skill tests were added.
- **Smoke A — quick (default), decision = the AC's own "should we drop the enterprise tier?":** exactly 2 spawns in stage 1 (`quick_seats`: pragmatist + risk-officer, ONE message, file-verbatim persona bodies), zero reviewer spawns, zero DA spawn, shuffle applied (mapping withheld), chairman on strong model with `Mode: quick · Topology: parallel`. Output: exactly the 7 contract headings, confidences `high (0.86)` / `moderate (0.68)`, genuine dissent preserved (seats reached OPPOSITE verdicts: drop vs keep+reprice), chairman self-judged conformity and printed the reduced-assurance note. Render-check applied ONE fix: `Dissent: … — Response B.` → `— Pragmatist, cost-benefit triage` (engine label substitution).
- **Smoke B — `--full`, same decision (AC 3):** 3 seats ONE message → shuffle → 3 peer reviewers ONE message (all three independently flagged the same collective blind spot: support-load attribution never measured) → separate DA spawn (attack: "the council is voting on a number none of them has seen"; named a third option — surgical whale offboarding — no seat produced) → chairman. Output: exactly 7 headings with the DA answer folded INTO Clashes per the updated instruction (the 1.2/1.3 extra-section wobble did NOT recur), confidences `high (0.88)` / `low (0.40)` / `moderate (0.75)`, `Dissent:` block preserved B's exit position intact with conditions under which it wins. Render-check applied ONE fix: label→`— Pragmatist, cost-benefit triage`.
- Verdict-document shell verified on both runs: `# Verdict: <decision>` title + first-line mode note (`Council verdict — quick mode (2 seats, no peer review). Dissent preserved.` / full-mode variant). No wide tables, heading depth ≤ `###`, meaning survives monochrome.
- Quality observation for the record: the full-mode machinery demonstrably earned its cost — peer review surfaced the shared unverified assumption, and the DA dissolved a false binary the seats had accepted. Epic 1's core promise (FR5/FR6 anti-sycophancy protocol) is observable in shipped artifacts.
- PLANNING NOTE for Story 2.3's create-story run: `councils/council-default.md` now EXISTS (authored here per the conflict resolution in Dev Notes) — 2.3's scope is evaluate-default + advise-default + config posture only.

### File List

- `agents/pragmatist.md` (new)
- `agents/risk-officer.md` (new)
- `agents/first-principles.md` (new)
- `councils/council-default.md` (new — new dir)
- `skills/council/SKILL.md` (new)
- `tests/test_persona_contract.py` (modified — roster + command-skill tests, 18 total)
- `_bmad-output/implementation-artifacts/1-4-council-generic-verdicts.md` (modified — story tracking)
- `_bmad-output/implementation-artifacts/sprint-status.yaml` (modified — status tracking)

## Change Log

- 2026-06-07: Story 1.4 implemented — `/council` command skill (mode forwarding, FR8 standalone hard rule, verdict shell + render-check), `councils/council-default.md` (parallel, strict-subset quick_seats), 3 generic personas (pragmatist / risk-officer / first-principles), 2 structural tests (18 total). Live smoke: quick run (2 seats, 0 review/DA spawns) + `--full` run (3 seats + 3 reviews + DA + chairman) both verified against all 3 ACs; FR8 proven on a repo with no people/, transcripts/, or index.sqlite. Commit `5ada55a` on `main`, CI green. Epic 1 functionally complete.
- 2026-06-07: Code review (parallel clean-context layers) — 7 patch findings resolved, 0 decisions, 0 deferred: command input hardening (empty decision, --full-in-quotes, unknown flags STOP, multi-line verbatim), mode-header N bound to participating seats, quick-mode Blind Spots source defined in chairman.md + render-check present-but-empty allowance, render-check overreach guards (no fabricated confidences/dissents), roster prose notes chairman always runs, tests hardened (kebab-case seat IDs, FR8 prohibition marker, model_overrides key validation — 19 total), Debug Log suite-scope clarified. Auditor verdict: no material AC violations, zero scope leakage.
