---
baseline_commit: 52726108c4f6fe2ae671df2816d7f68db72d12c1
---

# Story 1.2: Deliberation Engine — Parallel Topology with Peer Review & Chairman

Status: done

<!-- Created 2026-06-07 by create-story workflow — ultimate context engine analysis completed -->

## Story

As a user seeking a trustworthy verdict,
I want a council engine that runs seats independently, peer-reviews anonymously, and synthesizes without smoothing dissent,
So that majority pressure cannot suppress a correct minority read (FR5, FR6, NFR6).

## Acceptance Criteria

1. **Given** the persona file contract (`agents/<seat-id>.md`: frontmatter `seat_id`, `display_name`, `method`, `ignores`, `role`, `modes`; body = prompt), **when** `agents/chairman.md` is authored, **then** it carries `role: chairman` and the harvested output contract (Agrees / Clashes / Blind Spots / Recommendation / What You Lose / Do This First / Verify), with MIT attribution to `ngmeyer/skills` in `skills/council-engine/references/protocol.md`.
2. **Given** a roster file (`councils/<name>.md`: frontmatter `topology`, `seats`, `quick_seats`, optional `model_overrides`), **when** the engine runs `topology: parallel`, **then** stage 1 fans out each seat as a sub-agent with no visibility into any other seat's output, **and** stage 2 shuffles responses and relabels them A, B, C… (one anonymous label per participating seat) before peer review (no seat identifiable), **and** stage 3 chairman synthesis runs the devil's-advocate-vs-consensus pass, distinguishes value tensions from error catches, preserves minority positions under an explicit `Dissent:` label, and may side with a strong minority.
3. **Given** a persona file with a hardcoded model tier, **when** the engine resolves models, **then** tiers come only from roster `model_overrides` (haiku-class seats, strong-model chairman default) — persona-file tiers are ignored.

## Tasks / Subtasks

- [x] Task 1: Harvest the protocol contract → `skills/council-engine/references/protocol.md` (AC: 1)
  - [x] Fetch upstream `SKILL.md` from `ngmeyer/skills` → `skills/productivity/council-review/SKILL.md` (MIT, verified live 2026-06-07; harvest extracts already captured in Dev Notes below — use them, fetch only to confirm/expand)
  - [x] Author `protocol.md` containing the five harvest items verbatim-adapted: (a) anonymization-shuffle instruction ("Randomize the mapping — Advisor 1 should NOT always be Response A"), (b) devil's-advocate-vs-consensus pass (one strong-model attack on the *converged* answer, not 2-vs-2), (c) sycophancy guardrail lines (advisor-prompt rule + peer-review conformity check), (d) chairman output contract (full headings in Dev Notes), (e) composable-flags pattern (note only — flags land in Story 1.3)
  - [x] Open `protocol.md` with MIT attribution: source repo `ngmeyer/skills` (path `skills/productivity/council-review/`), copyright (c) 2026 Neal Meyer, MIT — adapted for Parley Voo
- [x] Task 2: Author `agents/chairman.md` per the persona file contract (AC: 1)
  - [x] Frontmatter MUST carry BOTH key sets: Claude Code keys `name: chairman` + `description: <one-liner>` (— **verified 2026-06-07: `claude plugin validate --strict` validates `agents/*.md` and FAILS on missing `description`**; extra custom keys are tolerated) AND the persona contract keys `seat_id: chairman`, `display_name: Chairman`, `method` (named: dissent-preserving synthesis per DMAD/Karpathy council protocol), `ignores` (list), `role: chairman`, `modes`
  - [x] NO model/tier key in frontmatter — model tiers live only in roster `model_overrides` (anti-pattern check, AC 3)
  - [x] Body = the synthesis prompt: consume anonymized labeled responses + peer reviews; run devil's-advocate-vs-consensus; classify each clash as **value tension** (both valid) vs **error catch** (one seat found a real flaw); preserve minority positions under an explicit `Dissent:` label with attribution `— {Display Name}, {method}`; explicitly empowered to side with a minority whose reasoning is strongest
  - [x] Output contract headings (harvested, AC-required set): Agrees / Clashes / Blind Spots / Recommendation / What You Lose / Do This First / Verify — render per UX terminal conventions (`#`→`###` max depth, confidence as `word (0.NN)`, no wide tables)
- [x] Task 3: Author `skills/council-engine/SKILL.md` — parallel topology orchestration (AC: 2, 3)
  - [x] Frontmatter `name: council-engine` + `description`; body <500 lines (architecture hard rule) — split detail into `references/protocol.md` (Task 1) and `references/topologies.md`
  - [x] Roster resolution: read `councils/<name>.md` frontmatter (`topology`, `seats`, `quick_seats`, optional `model_overrides`); load each seat from `agents/<seat-id>.md`; missing seat file → stop and name the missing seat ID (mirrors the import-time validation pattern)
  - [x] Stage 1 — independent fan-out: spawn ALL seats in ONE message (parallel Task/Agent tool calls) so no seat can see another's output; each sub-agent prompt = persona body + the framed input; upstream warning applies: "Sequential lets earlier responses contaminate later ones"
  - [x] Stage 2 — anonymized peer review: shuffle responses, relabel A, B, C… (one label per participating seat, randomized mapping), then fan out peer reviewers over the anonymized set; include the harvested conformity check ("is the agreement genuine — or conformity to a shared framing?")
  - [x] Stage 3 — chairman synthesis: spawn `chairman` seat with all responses + peer reviews + devil's-advocate instruction; output per the Task 2 contract
  - [x] Model resolution rule, written as a hard instruction: tier per seat comes ONLY from roster `model_overrides` (default: haiku-class seats, strong-model chairman); any model/tier key found in a persona file is IGNORED
  - [x] `references/topologies.md`: document the parallel topology stages; stub a `## Staged` heading marked "Story 1.3" so 1.3 extends rather than restructures
- [x] Task 4: Structural tests — contracts enforceable in CI (AC: 1, 3)
  - [x] `tests/test_persona_contract.py`: parse `agents/*.md` frontmatter (stdlib-parseable YAML — see Dev Notes); assert chairman has all six persona keys + `role: chairman` + `name`/`description`; assert NO model/tier key in any persona file; assert `skills/council-engine/SKILL.md` body <500 lines; assert `protocol.md` contains the MIT attribution line
  - [x] Keep tests dependency-light: no new deps without halting for approval (PyYAML is NOT in pyproject — either parse frontmatter with a minimal splitter or add PyYAML only with user approval)
- [x] Task 5: Validation + CI green (AC: all)
  - [x] `claude plugin validate ./ --strict` exit 0 locally (the new `agents/` dir and `skills/council-engine/` are now auto-discovered and validated — description keys mandatory)
  - [x] `uv run pytest` green locally; push; both CI jobs green
- [x] Task 6: Live smoke verification (AC: 2)
  - [x] In-session: create a throwaway test roster (e.g. `tests/fixtures/test-council.md`, NOT in `councils/` — default rosters are Stories 1.4/2.3) with 2–3 minimal inline test seats; run the engine skill on a toy decision; verify by inspection: parallel single-message fan-out happened, labels were shuffled/anonymous, synthesis used the contract headings, dissent carried a `Dissent:` label
  - [x] Record the observed run shape in Dev Agent Record (this is prompt-orchestration — pytest cannot verify runtime behavior; honest manual verification + structural tests is the bar)

### Review Findings

- [x] [Review][Decision] Fixture roster cannot run under the documented roster loader — The smoke fixture names `test-pragmatist`, `test-purist`, and `test-risk-officer`, then says those personas are inline and deliberately not in `agents/`; meanwhile `skills/council-engine/SKILL.md` requires every roster seat to load from `agents/<seat-id>.md` and stop if missing. The fix depends on intent: add explicit fixture-local inline seat support, move fixture seats into fixture persona files with a documented alternate path, or treat the smoke fixture as a manual record rather than an engine-runnable roster. → **DECIDED (user): manual record only.** Fixture re-annotated as a non-runnable smoke-run record; engine contract stays `agents/`-only.
- [x] [Review][Decision] Peer reviewer identity and self-review policy are underspecified — Stage 2 says to "fan out peer reviewers" over all anonymized responses, but does not define whether reviewers are the same participating seats, fresh generic reviewers, or another persona type. If reviewers are the same seats, they may review their own response and can sometimes recognize their own wording; if they are generic reviewers, the peer-review method differs from the seat disciplines. Choose the intended protocol before patching. → **DECIDED (user): reviewers ARE the participating seats; anonymous self-review is acceptable by design** (chairman weighs reasoning, not votes). Documented in SKILL.md stage 2 + topologies.md.
- [x] [Review][Patch] Chairman cannot both keep mapping withheld and produce required named `Dissent:` attribution [skills/council-engine/SKILL.md:95] → chairman attributes dissent by response label; engine (holder of the withheld mapping) substitutes `— {Display Name}, {method}` at render time. SKILL.md, chairman.md, protocol.md §5, topologies.md all updated consistently.
- [x] [Review][Patch] Devil's-advocate orchestration contradicts the harvested separate-spawn protocol [skills/council-engine/references/protocol.md:26] → stage 3 split into 3a (ONE separate strong-model devil's advocate states + attacks the consensus) and 3b (chairman receives the attack and must rebut or concede explicitly). chairman.md procedure updated to consume, not self-run, the attack.
- [x] [Review][Patch] Unsupported `staged` topology lacks an explicit fail-closed stop path [skills/council-engine/SKILL.md:58] → any topology other than `parallel` now STOPs with a named message; silent fallback forbidden.
- [x] [Review][Patch] Model override keys and tier values are not validated before spawning [skills/council-engine/SKILL.md:46] → keys must be roster seats or `chairman`; values must be `haiku-class`/`strong-model`; unknown → STOP and name it.
- [x] [Review][Patch] Empty, failed, or timed-out stage outputs have no retry/stop rule [skills/council-engine/SKILL.md:79] → one retry per failed spawn, then STOP naming the seat/stage; partial councils forbidden.
- [x] [Review][Patch] Duplicate or empty roster `seats` can distort peer review [skills/council-engine/SKILL.md:31] → roster validation added: empty seats STOP, duplicate seat STOP (named).
- [x] [Review][Patch] Tests do not enforce the chairman output-heading and `Dissent:` attribution contract [tests/test_persona_contract.py:52] → `test_chairman_output_contract_headings` (all 7 headings, in order) + `test_chairman_dissent_label_contract` added.
- [x] [Review][Patch] Frontmatter tests accept present-but-empty required values [tests/test_persona_contract.py:55] → `test_required_values_are_non_empty` added (`ignores` exempt — may be a legitimately empty list).

## Dev Notes

### Critical context — read before coding

- **This story is prompt engineering, not Python.** Deliverables are markdown: one skill, one agent, two reference docs, plus structural pytest checks. The only Python is the contract test.
- **Repo state after Story 1.1:** `.claude-plugin/plugin.json` (name `parley-voo`, 0.1.0, MIT, NO `skills` key — auto-discovery), `.github/workflows/ci.yml` (validate + socket-blocked pytest, both green), `.gitignore` (6 privacy entries + `index.sqlite*`), `pyproject.toml` (uv, Python 3.12+, sqlite-vec, pytest+pytest-socket, `addopts = "--disable-socket"`, `testpaths = ["tests"]`), `schema/index.sql`, `tests/test_schema.py`. **No `agents/`, `skills/`, or `councils/` dirs exist yet — this story creates the first two.**
- **VERIFIED GOTCHA (live test 2026-06-07):** once `agents/*.md` exists, `claude plugin validate --strict` validates each agent file and **fails on missing `description`** frontmatter. Persona files must carry `name` + `description` (Claude Code keys) ALONGSIDE the architecture's persona contract keys (`seat_id`, `display_name`, `method`, `ignores`, `role`, `modes`). Extra custom keys are tolerated — verified passing.
- **Do NOT touch `.claude/`** (BMAD workflow skills, unrelated). The plugin's skills live at repo-root `skills/`.
- **Plugin auto-load side effect:** authored `agents/` + `skills/` become live in any session with this plugin loaded. Keep the chairman `description` accurate so it isn't spawned for unrelated work.

### Harvest source — verified facts (fetched live 2026-06-07)

- Upstream: `ngmeyer/skills` monorepo, path `skills/productivity/council-review/SKILL.md` (+ `tests/`). License: MIT, "Copyright (c) 2026 Neal Meyer" — attribution required in `protocol.md`.
- **Anonymization-shuffle (verbatim):** "Collect all 5 advisor responses. **Randomize the mapping** — Advisor 1 should NOT always be Response A." Rationale: "Reviewers defer to role names if visible."
- **Devil's-advocate-vs-consensus (Step 3.7):** after responses, state the emerging consensus in one sentence; spawn ONE Devil's Advocate on a strong model: "make the strongest possible case that this answer is WRONG"; demands: what does consensus overlook that flips the decision / construct the concrete failure scenario / what evidence would force abandoning this answer. Explicitly NOT a 2-vs-2 structure — one sharp attack on the converged answer.
- **Sycophancy guardrail (advisor prompts, verbatim):** "**Do not defer to any answer the framing seems to expect.** Reason from your method to wherever it actually leads; if that's against the apparent expected answer, say so plainly. Hedging toward the obvious answer is the failure this council exists to prevent."
- **Peer-review conformity check (verbatim):** "Where these responses agree, is the agreement genuine — or could it be conformity to a shared framing? Flag any consensus that looks like deference rather than independent reasoning."
- **Upstream chairman headings:** Where the Council Agrees / Where the Council Clashes (Value Tension or Error Catch) / Blind Spots Revealed / Recommendation / What You Lose / Do This First / How to verify — adapt to the AC's heading set (Agrees / Clashes / Blind Spots / Recommendation / What You Lose / Do This First / Verify).
- **Upstream parallelism warning (verbatim):** "Always parallel spawn advisors. Sequential lets earlier responses contaminate later ones."
- **Upstream flags** (`--quick`, `--adaptive`, `--confidence`, `--measure-diversity`, `--jury`): note the composable pattern in `protocol.md` but implement NOTHING — quick/full mode is Story 1.3; `--adaptive`/`--jury` are out of scope entirely.
- Upstream restructure note: the 31KB single-file upstream violates the <500-line SKILL.md rule — that is WHY protocol detail goes in `references/`.

### Contracts (binding — architecture.md "Implementation Patterns")

**Persona file** (`agents/<seat-id>.md`):

```yaml
---
name: chairman                      # Claude Code agent key (required)
description: <when-to-use one-liner> # Claude Code agent key (REQUIRED by --strict)
seat_id: chairman                   # canonical kebab-case; THE cross-file key
display_name: Chairman
method: <named reasoning discipline>
ignores: []                         # list — hard prohibitions (chairman: may be empty or name what synthesis skips)
role: chairman                      # seat|chairman
modes: [evaluate, advise, council]
---
<body = the prompt>
```

**Roster file** (`councils/<name>.md`): frontmatter `topology` (`parallel|staged`), `seats` (ordered seat IDs), `quick_seats` (subset), `model_overrides` (optional map seat_id → tier). Body = purpose prose. This file IS the FR9 export format. **No roster files ship in this story** — the contract is defined/parsed by the engine; `councils/council-default.md` is Story 1.4, the full bench is 2.3. Test fixture roster goes in `tests/fixtures/`.

**Naming:** seat IDs canonical kebab-case, used identically in filenames, roster files, DB `seat` column, memory dirs. Display names only in rendered documents.

### Architecture compliance checklist (binding)

- Engine = `skills/council-engine/SKILL.md` + `references/{protocol,topologies}.md`; orchestration is prompt-directed sub-agent fan-out; each seat = one agent definition
- SKILL.md body <500 lines; references split out
- Topology declared per-roster, never per-command
- Model tiers resolved ONLY in roster `model_overrides` (anti-pattern: tiers hardcoded in persona files — kills per-roster override)
- Seats never see each other's raw output pre-shuffle (boundary rule)
- Rendering follows UX terminal conventions: heading depth ≤ `###`, `Dissent:` label explicit, attribution `— {Display Name}, {method}`, confidence `word (0.NN)` never bare, no wide tables, meaning survives monochrome
- No SQLite anywhere in this story (scripts-only rule lands Epic 3); no `commands/` dir ever (commands are skills)
- Per-expert memory (`.parley/memory/<seat-id>/`) is NOT this story — do not scaffold it

### Scope boundaries — what this story does NOT include

- NO staged topology, NO quick/full modes, NO `--full` flag (Story 1.3 — but stub the `## Staged` heading in `topologies.md`)
- NO `/council` command skill, NO `councils/council-default.md` (Story 1.4)
- NO real seat personas — behavioral-coder etc. are Epic 2 (test seats are throwaway fixtures only)
- NO citation verification (`recall.py --verify-citations` is Story 3.2; chairman citation-discard wiring is 3.6)
- NO export/import, NO config.yaml posture (2.3/2.6)
- CI stays exactly two jobs — verify-clean-fork is 6.3

### Previous story intelligence (Story 1.1, status done)

- `claude plugin validate --strict` exit 0 with NO `skills` key in plugin.json (auto-discovery) — adding `skills/council-engine/SKILL.md` keeps that posture; do not add a `skills` array
- CI: validate job installs Claude CLI via `curl -fsSL https://claude.ai/install.sh | bash` + PATH add, runs offline, no API key; test job = `setup-uv@v8.2.0` (bare `@v8` tag does NOT exist — do not "fix" the pin) + `actions/checkout@v5` (Node 24)
- pytest collection constrained by `testpaths = ["tests"]` (BMAD's own tests under `_bmad/` would otherwise collect); sockets blocked globally via addopts — any test needing network is a bug
- Schema review hardening already landed: meta single-row CHECK, participants JSON-array CHECK, forecast_prob bounds — don't re-touch `schema/index.sql` this story
- Code review (Codex) pattern from 1.1: findings land as `### Review Findings` checkboxes under Tasks — leave the section absent until a review writes it
- 3-commit cadence worked well: implementation commit, then targeted fix commits; CI watched to green via `gh run watch`

### Sub-agent mechanics (Claude Code runtime facts)

- Plugin `agents/*.md` are auto-registered as spawnable agent types in sessions where the plugin is loaded; the engine skill may fan out either via registered agent types or generic Task-tool sub-agents carrying the persona body as prompt — dev agent's choice, but independence is non-negotiable: all stage-1 spawns in a single message, no shared context between seats
- Task-tool spawns accept a model override parameter (haiku/sonnet/opus class) — this is the mechanism for roster `model_overrides`; map "haiku-class" → fast/cheap tier, "strong-model" → the session's top tier
- SKILL.md frontmatter `name` + `description` both present (description required under --strict for skills as for agents)

### Testing standards

- pytest, `tests/test_<thing>.py`, sockets blocked globally; this story adds `tests/test_persona_contract.py`
- Frontmatter parsing in tests WITHOUT new deps: split on `---` fences and parse the simple `key: value` / `key: [a, b]` lines directly (the contract keys are all flat) — or HALT for approval if PyYAML genuinely needed
- The runtime behavior (fan-out independence, shuffle, synthesis shape) is verified by a live in-session smoke run recorded in the Dev Agent Record — never claim pytest covers it

### Project Structure Notes

New items only (everything else untouched):

```
agents/chairman.md                          # persona contract + name/description
skills/council-engine/SKILL.md              # orchestration, <500 lines
skills/council-engine/references/protocol.md    # harvested contract + MIT attribution
skills/council-engine/references/topologies.md  # parallel detail + staged stub (1.3)
tests/test_persona_contract.py              # structural contract checks
tests/fixtures/test-council.md              # throwaway smoke-run roster (NOT councils/)
```

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Story 1.2] — story + ACs (verbatim)
- [Source: _bmad-output/planning-artifacts/epics.md#Additional Requirements → Engine & config] — skill/persona/roster contracts, seat-ID rules
- [Source: _bmad-output/planning-artifacts/architecture.md#Engine & Orchestration] — invocation model, topology-per-roster, model tiers
- [Source: _bmad-output/planning-artifacts/architecture.md#Starter Template Evaluation] — harvest list, SKILL.md discipline, upstream restructure note
- [Source: _bmad-output/planning-artifacts/architecture.md#Implementation Patterns & Consistency Rules] — persona/roster contracts, anti-patterns
- [Source: _bmad-output/planning-artifacts/prds/prd-parley_voo-2026-06-04/prd.md#FR5/FR6/NFR6] — protocol + anti-sycophancy requirements
- [Source: docs/parley-spec.md#3 The Deliberation Engine] — protocol rationale, DMAD distinct-reasoning-method principle
- [Source: _bmad-output/planning-artifacts/epics.md#UX Design Requirements UX-DR1/3/4/11] — rendering conventions the chairman output must follow
- Harvest content + license verified live from `github.com/ngmeyer/skills` 2026-06-07; `validate --strict` agent-description requirement verified locally same date

## Dev Agent Record

### Agent Model Used

claude-opus-4-8[1m] (Claude Code); seats/reviewers on haiku-class, chairman on strong model per roster `model_overrides`

### Debug Log References

- RED: `uv run pytest tests/test_persona_contract.py` → 4 failed / 2 vacuous-pass before authoring (files absent)
- GREEN: `uv run pytest` → 11 passed (5 schema + 6 contract); `claude plugin validate ./ --strict` → ✔ Validation passed
- CI run on `fc81578` watched to green via `gh run watch --exit-status` (both jobs)

### Completion Notes List

- Upstream `ngmeyer/skills` SKILL.md re-fetched live; all five harvest extracts confirmed verbatim against Dev Notes. License/copyright not in the SKILL.md body itself — MIT + "Neal Meyer" attribution per Dev Notes verification of the repo LICENSE (2026-06-07).
- Frontmatter parsing in tests uses a minimal `---` splitter + flat `key: value` / `key: [a, b]` parser — no PyYAML, no new deps.
- **Live smoke run shape (toy decision: exact pins vs ranges for a small OSS Python lib; roster `tests/fixtures/test-council.md`, 3 seats):**
  - Stage 1: 3 seats spawned in ONE message (3 parallel Agent calls, haiku-class, 7–9s each), each prompt = persona body + verbatim sycophancy guardrail + framed input; no seat saw another's output.
  - Stage 2: responses shuffled to a non-identity mapping (risk-officer→A, pragmatist→B, purist→C; mapping withheld); 3 peer reviewers spawned in ONE message with all anonymized responses + verbatim conformity check. All three reviewers explicitly answered the conformity question (verdict: genuine independent convergence, orthogonal methods).
  - Stage 3: chairman on strong model with framed input + anonymized responses + reviews + display-name/method list (attribution only). Output rendered the contract headings (Agrees/Clashes/Blind Spots/Recommendation/What You Lose/Do This First/Verify), classified clashes as value tension vs error catch, confidence as `high (0.85)`, two `Dissent:` entries with `— {Display Name}, {method}` attribution, and sided against one seat's reasoning while preserving its position.
  - Adversarial robustness observed: reviewer 3 hallucinated a "pins vs ranges" disagreement that didn't exist; the chairman identified the claim as false against the source responses and discounted that review (smoke prompt included a generic verify-reviewer-claims nudge, not the answer).
  - Honest deviations noted: (1) the smoke run drove sub-agents with a compressed paraphrase of chairman.md/SKILL.md rather than file-verbatim prompts; (2) the chairman rendered dissents as a separate `### Dissent` section between What You Lose and Do This First instead of inside Recommendation — the AC's substance (explicit `Dissent:` label + attribution, minority preserved, dissent unsmoothed) is verified; exact placement adherence should be re-observed when `/council` (Story 1.4) drives prompts from the files verbatim.

### File List

- `agents/chairman.md` (new)
- `skills/council-engine/SKILL.md` (new)
- `skills/council-engine/references/protocol.md` (new)
- `skills/council-engine/references/topologies.md` (new)
- `tests/test_persona_contract.py` (new)
- `tests/fixtures/test-council.md` (new)
- `_bmad-output/implementation-artifacts/1-2-deliberation-engine-parallel-topology-peer-review-chairman.md` (modified — story tracking)
- `_bmad-output/implementation-artifacts/sprint-status.yaml` (modified — status tracking)

## Change Log

- 2026-06-07: Story 1.2 implemented — council-engine skill (parallel topology, 3 stages), chairman persona, harvested protocol reference with MIT attribution, topologies reference with staged stub, structural contract tests (6), live 3-seat smoke run verified. Commit `fc81578` on `main`, CI green.
- 2026-06-07: Addressed code review findings (Codex) — 10 items resolved (2 decisions resolved by user, 8 patches): separate devil's-advocate spawn (3a/3b), label-based dissent attribution with engine-side substitution, fail-closed topology/roster/model-override validation, spawn retry/stop rule, reviewer-identity policy documented, fixture re-annotated as manual record, 3 new contract tests (14 total).
