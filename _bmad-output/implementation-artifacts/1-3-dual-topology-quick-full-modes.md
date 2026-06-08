---
baseline_commit: d03781f146c79b24d30bb5036dbaf1d1aaf62cd7
---

# Story 1.3: Dual Topology & Quick/Full Modes

Status: done

<!-- Created 2026-06-07 by create-story workflow — ultimate context engine analysis completed -->

## Story

As a user with different deliberation needs,
I want the engine to support staged (sequential handoff) execution and quick/full cost tiers,
So that `/advise`-style pipelines are possible and routine runs stay cheap (FR7, FR4, NFR2).

## Acceptance Criteria

1. **Given** a roster with `topology: staged` and ordered stage groups, **when** the engine runs, **then** stages execute sequentially, each stage receiving the prior stage's output (decoder-ring handoff pattern), with seats inside a stage running parallel.
2. **Given** any roster invoked without flags, **when** quick mode (default) runs, **then** only `quick_seats` execute and peer review is skipped, **and** `--full` escalates to all seats plus anonymized peer review, **and** topology and mode resolution come from the roster file, never hardcoded per command.

## Tasks / Subtasks

- [x] Task 1: Replace the `## Staged` stub in `references/topologies.md` with the full staged spec (AC: 1)
  - [x] Stage groups: roster `seats` becomes an ordered list of stage groups (list of lists) when `topology: staged`; flat list stays the parallel shape — document both shapes side by side
  - [x] Sequential execution with hard stage boundaries: stage N+1 does not start until stage N fully completes
  - [x] Decoder-ring handoff: every seat in stage N+1 receives the original framed input + ALL outputs of stage N (prior stage ONLY, per AC verbatim "the prior stage's output" — not a cumulative chain; a stage that needs earlier context must carry it forward in its own output, which is exactly the decoder-ring discipline). Handoff is attributed by display name — staged handoff is deliberately NOT anonymous; the decoder ring only works if downstream seats can use it. Document the contrast with parallel's isolation invariant explicitly so no dev "fixes" it
  - [x] Intra-stage parallelism: all seats within one stage group spawn in ONE message (same single-message rule as parallel stage 1); seats in the same stage never see each other's output
  - [x] Full-mode tail for staged: after the last stage group completes, anonymized shuffle over ALL seat outputs (whole run) → peer-review fan-out → devil's advocate → chairman — same 1.2 machinery, repositioned after the pipeline
  - [x] Failure rule extends per-stage: one retry per failed spawn, then STOP naming seat + stage index; a failed stage never lets the pipeline continue with a partial handoff
- [x] Task 2: SKILL.md — staged dispatch + mode resolution (AC: 1, 2)
  - [x] REMOVE the fail-closed STOP for `topology: staged` (added in 1.2) — `staged` now dispatches; everything else still fails closed
  - [x] Add "Step: Resolve mode" before topology dispatch: default = quick; caller may pass an escalation flag (the `--full` semantics) → full. The engine NEVER decides mode per command — `quick_seats` membership and topology come only from the roster; the caller only passes the user's flag through (AC 2 hard rule, mirror the model-tier hard-rule formatting)
  - [x] Quick mode semantics (both topologies): only `quick_seats` execute; peer-review fan-out SKIPPED; separate devil's-advocate spawn SKIPPED (NFR2 — debate only where it earns its token cost); anonymization shuffle KEPT (zero spawn cost, preserves the anti-deference boundary for the chairman); chairman synthesis always runs
  - [x] Staged quick mode: a stage group whose intersection with `quick_seats` is empty is skipped entirely; handoff flows from the last non-skipped stage to the next; stage order preserved
  - [x] Roster validation extensions (fail-closed, same voice as 1.2's checks): staged `seats` must be a non-empty list of non-empty groups; duplicate seat IDs across the whole roster STOP (named); `quick_seats` must be a subset of flattened `seats` — unknown ID STOPs (named); `chairman` listed as a seat in ANY roster STOPs (chairman is implicit final synthesis in both topologies, spawned by the engine)
  - [x] Surface resolved mode + topology to the chairman prompt (one line, e.g. `Mode: quick · Topology: staged`) so synthesis can note it — full header formatting is Story 1.4's job, don't build it
  - [x] Body stays <500 lines — push staged detail into `references/topologies.md`, don't inline it
- [x] Task 3: chairman.md — tolerate quick-mode inputs (AC: 2)
  - [x] Inputs 3 (peer reviews) and 4 (devil's-advocate attack) marked **full mode only**; in quick mode they are absent — the chairman notes the reduced assurance in one line and NEVER fabricates reviews or an attack that didn't happen
  - [x] Procedure step 2 (answer the attack) conditioned on the attack existing; quick mode skips to weighing
  - [x] Output contract headings unchanged — `tests/test_persona_contract.py::test_chairman_output_contract_headings` must stay green (all 7 headings, in order)
- [x] Task 4: Structural tests — staged + mode contracts enforceable in CI (AC: 1, 2)
  - [x] Extend `tests/test_persona_contract.py` (same file, same flat-parser approach, zero new deps): assert `topologies.md` `## Staged` section no longer contains the "not yet implemented" stub text AND mentions the handoff (e.g. "prior stage" / "stage group"); assert SKILL.md contains the mode-resolution rule (e.g. both "quick" and "`--full`" / escalation language) and dispatches `staged`
  - [x] Do NOT try to parse roster files in tests — staged `seats` is a nested list and the 1.2 flat parser deliberately can't read it; roster parsing is engine-prompt territory, not pytest territory
- [x] Task 5: Validation + CI green (AC: all)
  - [x] `claude plugin validate ./ --strict` exit 0 locally; `uv run pytest` green locally (all 14 existing tests + new ones); push; both CI jobs green
- [x] Task 6: Live smoke verification — staged + quick (AC: 1, 2)
  - [x] Staged full run: throwaway 2-stage fixture (e.g. `tests/fixtures/test-staged-council.md`, manual-record convention from 1.2 — personas documented inline, NOT in `agents/`), toy decision; verify by inspection: stage 2 prompts contained stage 1 output with display-name attribution, intra-stage spawns went out in one message, post-pipeline shuffle/review/DA/chairman ran
  - [x] Quick run (either topology): verify only `quick_seats` spawned, ZERO reviewer spawns, ZERO devil's-advocate spawn, shuffle still applied, chairman noted quick mode / reduced assurance
  - [x] Record both observed run shapes in Dev Agent Record (prompt-orchestration bar from 1.2: honest manual verification + structural tests; pytest cannot verify runtime behavior)

### Review Findings

- [x] [Review][Patch] HIGH: `quick_seats` never required to exist or be non-empty — quick is the DEFAULT mode, so a roster missing `quick_seats` (or with `[]`, a vacuous subset) passes validation and runs zero seats; also `chairman` in `quick_seats` produces a confusing "not a seat" error instead of the implicit-chairman error [skills/council-engine/SKILL.md — Step 1 validation]
- [x] [Review][Patch] HIGH: handoff-under-skip undefined — "prior stage ONLY" conflicts with quick mode's "handoff flows from the last non-skipped stage"; partial stages promise "ALL outputs of stage N" when only the quick subset ran; a first surviving stage whose predecessors were all skipped has no defined input [skills/council-engine/SKILL.md — Staged items 3–4; references/topologies.md — Execution + Modes]
- [x] [Review][Patch] MED: Step 3 HARD RULE overstates — "mode SEMANTICS come only from the roster" is false on its face: only seat membership (`quick_seats`) and topology are roster-defined; what quick/full MEANS (skip review/DA, keep shuffle) is engine-defined in the very next bullets [skills/council-engine/SKILL.md — Step 3]
- [x] [Review][Patch] MED: staged full-mode tail claims anonymity the pipeline already spent — later-stage seats saw earlier stages' ATTRIBUTED outputs, so reviewer anonymity is partial; document honestly what the shuffle still buys (same-stage/later-stage blinding + the chairman boundary) [skills/council-engine/references/topologies.md — Full-mode tail]
- [x] [Review][Patch] MED: staged devil's-advocate consensus detection misreads the pipeline — later stages were INSTRUCTED to build on earlier ones, so "emerging consensus" detection tuned for independent parallel responses will see manufactured convergence; DA prompt must attack the pipeline's final position instead [skills/council-engine/references/topologies.md — Full-mode tail item 3]
- [x] [Review][Patch] MED: chairman procedure step 4 uses peer reviews unconditioned — step 2 was quick-mode-guarded but step 4 ("use the peer reviews to judge") was not; in quick mode this invites the exact fabrication the intro forbids; must self-judge conformity when no reviews exist [agents/chairman.md — Procedure step 4]
- [x] [Review][Patch] MED: stale roster-table row contradicts the new mode spec — `quick_seats | … (Story 1.3 — ignore for now)` still ships while Step 3 makes it load-bearing [skills/council-engine/SKILL.md — Step 1 roster table]
- [x] [Review][Patch] MED: test hardening — `## Staged` slice is unbounded (markers can match `## Modes` text below it), missing-heading case raises IndexError instead of a named assertion, `"quick"` marker is dead coverage (substring of already-asserted `"quick_seats"`), and AC1's sequential/intra-stage-parallel clauses have no marker at all [tests/test_persona_contract.py — test_staged_topology_is_specified, test_skill_md_mode_resolution_rules]
- [x] [Review][Patch] LOW: chairman status-line contract loose + degenerate single-seat run undocumented — SKILL.md pins `Mode: <quick|full> · Topology: <parallel|staged>` but chairman.md input 5 doesn't, inviting drift; and a single-`quick_seats` run reduces shuffle/dissent machinery to one label with no stated behavior [agents/chairman.md — input 5; skills/council-engine/SKILL.md / references/topologies.md — Modes]

## Dev Notes

### Critical context — read before coding

- **This story is, again, prompt engineering, not Python.** Deliverables: edits to 3 existing markdown files (`SKILL.md`, `topologies.md`, `chairman.md`), new structural tests in the existing test file, one new smoke fixture. No new dirs, no scripts, no SQLite.
- **Repo state after Story 1.2 (commit `86255a0`, all review findings resolved):** `skills/council-engine/SKILL.md` (152 lines — plenty of headroom under 500), `references/protocol.md` (harvested contract + MIT attribution), `references/topologies.md` (parallel spec + `## Staged` stub reading "Story 1.3 — not yet implemented…"), `agents/chairman.md`, `tests/test_persona_contract.py` (9 tests there; 14 total with schema), `tests/fixtures/test-council.md` (manual record). The stub was placed so THIS story extends `topologies.md` rather than restructuring it — extend under the existing heading.
- **1.2 review-hardened invariants you MUST NOT regress** (each was a Codex review finding, already fixed — do not reintroduce):
  - Fail-closed everywhere: unknown topology, empty/duplicate seats, bad `model_overrides` keys/tiers, failed spawns (one retry → STOP named). Extend these to staged shapes; never weaken them.
  - Devil's advocate is a SEPARATE spawn (stage 3a), never the chairman attacking its own draft.
  - Chairman never sees the seat↔label mapping; dissent attributed by response label (`— Response B`); the ENGINE substitutes `— {Display Name}, {method}` at render time.
  - Stage-2 reviewers ARE the participating seats; anonymous self-review is acceptable by design (user decision, documented in SKILL.md).
  - Model tiers ONLY from roster `model_overrides`; defaults haiku-class seats / strong-model chairman.
- **VERIFIED GOTCHA (1.2):** `claude plugin validate --strict` validates `agents/*.md` and `skills/*/SKILL.md` frontmatter — `name` + `description` required. You're only editing existing files that already pass; don't remove those keys.
- **Do NOT touch `.claude/`** (BMAD tooling, now gitignored). Plugin skills live at repo-root `skills/`.

### Design decisions (made here so the dev agent doesn't have to)

1. **Staged roster shape — `seats` as ordered stage groups (list of lists):**

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

   Source: architecture.md Implementation Patterns — "`seats` (ordered seat IDs; **stage groups for staged**)". Flat list remains the `parallel` shape. The roster file IS the FR9 export format — this nesting is part of the portable contract, document it in `topologies.md`.
2. **Chairman is implicit in BOTH topologies** — never listed in `seats`/stage groups; the engine always appends chairman synthesis (1.2 already works this way for parallel). A roster listing `chairman` as a seat → STOP. Keeps the synthesis contract uniform and `model_overrides.chairman` as the only chairman knob.
3. **Handoff = framed input + prior stage only, attributed.** Every stage receives the original framed input plus the immediately prior stage's outputs — NOT a cumulative all-stages chain (AC verbatim: "each stage receiving the prior stage's output"). If Red Team needs the decoder ring two stages back, the strategist stage's outputs must carry it forward — that forward-carry IS the decoder-ring pattern. Handoff is attributed, not anonymous. Staged stages pass output WITH display names downstream — the decoder-ring pattern requires downstream seats to know what they're building on (FR13: Profile Translator output feeds the strategists). Anonymization applies ONLY at the post-pipeline review/synthesis step. This is the deliberate, documented contrast with parallel's isolation invariant — call it out in `topologies.md` so a future dev doesn't "fix" the inconsistency.
4. **Quick mode skips review AND the separate DA spawn, keeps the shuffle.** AC text pins "peer review is skipped"; the DA spawn is killed by the same cost rationale (NFR2: "debate only where it earns its token cost" — quick is the gut-check tier, per spec §3 "fewer experts, no peer review"). The shuffle costs zero spawns and preserves the chairman anti-deference boundary, so it stays.
5. **Mode is an engine INPUT, semantics are roster-defined.** The engine accepts `mode: quick (default) | full` from its caller; what quick MEANS (which seats) lives in `quick_seats`. Command skills (1.4's `/council`, 4.x's `/advise`) just forward the user's `--full` flag; `/evaluate` pinning full is Story 3.6's command-level concern — NOT this story's.

### Scope boundaries — what this story does NOT include

- NO `/council` command skill, NO `councils/*.md` rosters, NO header formatting of verdict documents (Story 1.4)
- NO real personas — profile-translator etc. are Epic 2 (smoke seats are throwaway fixture records only)
- NO seat-runs-twice support (Profile Translator ×2 is FR13 / Stories 2.2+2.3+4.2). **Known forward collision:** the duplicate-seat STOP will conflict with PT×2 when advise-default.md is authored — 2.3 owns resolving that (likely two persona files or a stage-level repeat param). Leave the STOP in place; note it in `topologies.md` `## Staged` as a forward pointer so 2.3 finds it.
- NO config.yaml posture, NO optional-seat ON/OFF resolution (Story 2.3)
- NO quick-mode trim copy ("Trimmed in quick mode" line is `/advise` playbook UX, Story 4.1)
- CI stays exactly two jobs

### Previous story intelligence (Story 1.2, status done)

- RED→GREEN worked cleanly: write/extend structural tests first, watch them fail, then author markdown. Repeat it.
- Codex review pattern: findings land as `### Review Findings` checkboxes under Tasks — leave absent until a review writes it. 1.2's review produced 10 findings, heavily fail-closed-validation and protocol-fidelity shaped — this story PRE-EMPTS those classes by building validation rules in from the start (Task 2) and quoting protocol contracts exactly.
- Smoke-run honesty bar: record deviations explicitly. 1.2's smoke noted the chairman rendered a separate `### Dissent` section when driven by paraphrased prompts — when smoking 1.3, drive sub-agents with the FILE text (persona body + SKILL.md instructions), not paraphrases, to get a cleaner adherence read.
- Commit cadence that worked: implementation commit → targeted fix commits → `gh run watch --exit-status` to green. setup-uv pinned `@v8.2.0` (bare `@v8` does NOT exist), checkout `@v5` — don't "fix" pins.
- pytest: `testpaths = ["tests"]`, sockets blocked globally (`addopts = "--disable-socket"`); fixture `.md` files in `tests/fixtures/` are not collected — safe.
- Frontmatter parsing in tests: 1.2's minimal `---` splitter handles flat `key: value` / `key: [a, b]` ONLY. Staged rosters use nested lists — tests must not attempt to parse them (Task 4 boundary).

### Sub-agent mechanics (verified in 1.2's live run)

- Parallel intra-stage fan-out = multiple Agent/Task tool calls in ONE message; sequential messages = contamination (upstream warning, verified honored).
- Model param maps: `haiku-class` → haiku; `strong-model` → session top tier. Roster `model_overrides` only.
- Observed timings (1.2 smoke): haiku seats 7–9s each in parallel; strong-model chairman ~40s. A 3-stage staged run is therefore roughly 3× a parallel run's wall-clock — fine for smoke, worth noting in the run record.

### Architecture compliance checklist (binding)

- Engine stays `skills/council-engine/SKILL.md` + `references/{protocol,topologies}.md`; orchestration is prompt-directed sub-agent fan-out [Source: architecture.md#Engine & Orchestration]
- "Dual topology: `parallel` (evaluate: fan-out → anonymized shuffle → peer review → chairman) and `staged` (advise: Profile Translator ×2 → strategist trio parallel → Red Team → Execution Realist → synthesis). Topology declared per-roster, not per-command" [Source: architecture.md#Engine & Orchestration — verbatim]
- "Quick/full: quick = trimmed roster + no peer review (roster config names its own quick subset); `--full` flag escalates" [Source: architecture.md#Engine & Orchestration — verbatim]
- SKILL.md body <500 lines; references split out
- Rendering: heading depth ≤ `###`, `Dissent:` explicit, attribution `— {Display Name}, {method}`, confidence `word (0.NN)`, no wide tables, meaning survives monochrome [Source: DESIGN.md conventions]
- Anti-patterns: model tiers in persona files; topology per-command; wide tables; bare numbers

### Testing standards

- pytest, extend `tests/test_persona_contract.py`; no new deps (PyYAML still NOT approved); golden files not needed this story
- Runtime behavior (handoff content, spawn counts, skip logic) verified ONLY by the live smoke run recorded in Dev Agent Record — never claim pytest covers it

### Project Structure Notes

Changed/new items only:

```
skills/council-engine/SKILL.md                  # MODIFY: staged dispatch, mode resolution, validation extensions
skills/council-engine/references/topologies.md  # MODIFY: ## Staged stub → full spec
agents/chairman.md                              # MODIFY: quick-mode input tolerance
tests/test_persona_contract.py                  # MODIFY: staged + mode structural tests
tests/fixtures/test-staged-council.md           # NEW: staged smoke fixture (manual-record convention)
```

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Story 1.3] — story + ACs (verbatim)
- [Source: _bmad-output/planning-artifacts/epics.md#Story 1.4 / Epic 4 Stories 4.1–4.2] — downstream consumers; what NOT to build now
- [Source: _bmad-output/planning-artifacts/architecture.md#Engine & Orchestration] — dual topology, quick/full, model tiers (verbatim quotes above)
- [Source: _bmad-output/planning-artifacts/architecture.md#Implementation Patterns & Consistency Rules] — roster contract incl. "stage groups for staged", anti-patterns
- [Source: _bmad-output/planning-artifacts/prds/prd-parley_voo-2026-06-04/prd.md#FR4/FR7/FR13/NFR2] — cost tiers, dual topology differentiator, advise pipeline sequence
- [Source: docs/parley-spec.md#3 The Deliberation Engine] — quick-mode rationale ("fewer experts, no peer review… default for routine use"), distinct-reasoning-method principle
- [Source: _bmad-output/planning-artifacts/ux-designs/ux-parley_voo-2026-06-05/DESIGN.md] — terminal conventions; mode noted in headers (formatting owned by 1.4)
- [Source: _bmad-output/implementation-artifacts/1-2-deliberation-engine-parallel-topology-peer-review-chairman.md#Review Findings + Dev Agent Record] — hardened invariants, smoke methodology, honest-verification bar

## Dev Agent Record

### Agent Model Used

claude-opus-4-8[1m] (Claude Code); smoke seats/reviewers on haiku-class, DA + chairman on strong model per roster `model_overrides`

### Debug Log References

- RED: 2 new structural tests failed against the 1.2 stub/fail-closed text (9 existing passed)
- GREEN: `uv run pytest` → 16 passed; `claude plugin validate ./ --strict` → ✔; SKILL.md at 210 lines (<500)
- CI green on `6832f6f` via `gh run watch --exit-status`

### Completion Notes List

- **Smoke A — staged FULL** (fixture `tests/fixtures/test-staged-council.md`, 2 stage groups: [framer] → [strategist, skeptic]; toy decision: Sponsors vs Pro tier):
  - Stage 1 → stage 2 handoff verified: both stage-2 prompts carried the framed input + Framer's output attributed by display name; both seats demonstrably built ON the frame (strategist named which frame constraint it bet soft; skeptic attacked the frame's weakest assumption)
  - Intra-stage parallelism verified: stage-2 seats spawned in ONE message; reviewer fan-out in ONE message
  - Full tail verified: shuffle to non-identity mapping (withheld), 3 peer reviews each answering the conformity check explicitly, SEPARATE devil's-advocate spawn (found a genuine arithmetic flaw: sub-1% sponsor-conversion norms make the $300/mo gate unreachable at 300 users), chairman conceded/rebutted the attack point by point, sided with a corrected position, preserved two `Dissent:` entries attributed by response label, confidence `medium (0.62)`
  - **Deviation (recorded honestly):** chairman added an extra `### Answering the Devil's-Advocate Attack` section between Blind Spots and Recommendation — same deviation class as 1.2's separate Dissent section. Substance correct; heading-set adherence drifts when the procedure says "answer before the verdict." Candidate hardening for 1.4: fold the DA answer into Clashes explicitly.
- **Smoke B — staged QUICK** (same fixture, `quick_seats: [test-framer, test-strategist]`; fresh toy decision: README vs docs/):
  - Trim verified: stage 2 ran ONLY the strategist (skeptic skipped — not in quick_seats); total spawns = 2 seats + chairman; ZERO reviewer spawns, ZERO devil's-advocate spawn
  - Shuffle kept at zero cost (2 responses relabeled, mapping withheld)
  - Chairman explicitly stated no reviews exist in quick mode, judged conformity itself, did NOT fabricate reviews/attack, closed with the reduced-assurance note; exactly the 7 contract headings; `Dissent: — Response B` preserved
  - **Deviation (recorded honestly):** confidence rendered `high (8 of 10)` instead of `word (0.NN)` — convention violation in one spot (Smoke A rendered `medium (0.62)` correctly). Rendering-convention enforcement belongs to 1.4's verdict-document formatting; noted as a known wobble.
- Observed artifact: sub-agents inherit the user's global CLAUDE.md (one stage-2 seat addressed the user by name mid-analysis). Harmless here; worth remembering when prompts demand raw-document output.
- Smoke prompts carried the FILE-derived instructions (chairman contract verbatim incl. the new "do not add sections"/quick-mode lines) — adherence improved vs 1.2's paraphrase-driven smoke (Smoke B rendered exactly 7 headings).

### File List

- `skills/council-engine/SKILL.md` (modified — mode resolution step, staged dispatch, validation extensions, mode-aware stages)
- `skills/council-engine/references/topologies.md` (modified — `## Staged` full spec, `## Modes` section)
- `agents/chairman.md` (modified — quick-mode input tolerance, status line input)
- `tests/test_persona_contract.py` (modified — 2 new structural tests, 16 total)
- `tests/fixtures/test-staged-council.md` (new — staged smoke fixture, manual-record convention)
- `_bmad-output/implementation-artifacts/1-3-dual-topology-quick-full-modes.md` (modified — story tracking)
- `_bmad-output/implementation-artifacts/sprint-status.yaml` (modified — status tracking)

## Change Log

- 2026-06-07: Story 1.3 implemented — staged topology (stage groups, decoder-ring handoff, intra-stage parallelism, full-mode tail), quick/full mode resolution (roster-defined semantics, quick skips review+DA, keeps shuffle), chairman quick-mode tolerance, roster validation extensions, 2 new structural tests (16 total), live staged-full + staged-quick smoke runs verified. Commit `6832f6f` on `main`, CI green.
- 2026-06-07: Code review (parallel clean-context layers: Blind Hunter, Edge Case Hunter, Acceptance Auditor) — 9 patch findings resolved, 0 decisions, 0 deferred: quick_seats presence/non-empty validation, handoff-under-skip reconciliation (immediately preceding EXECUTED stage), HARD RULE reworded (who-from-roster vs what-from-engine), staged-tail partial-anonymity honesty, staged DA pipeline caveat, chairman step-4 quick-mode guard + pinned status-line format + single-voice note, stale table row fixed, tests hardened (bounded section slice, no IndexError, no vacuous markers, AC1 sequential/intra-stage markers).
