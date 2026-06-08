---
stepsCompleted: [1, 2, 3, 4, 5, 6]
status: 'complete'
readiness: 'READY'
inputDocuments:
  - '_bmad-output/planning-artifacts/prds/prd-parley_voo-2026-06-04/prd.md'
  - '_bmad-output/planning-artifacts/prds/prd-parley_voo-2026-06-04/addendum.md'
  - '_bmad-output/planning-artifacts/architecture.md'
  - '_bmad-output/planning-artifacts/epics.md'
  - '_bmad-output/planning-artifacts/ux-designs/ux-parley_voo-2026-06-05/DESIGN.md'
  - '_bmad-output/planning-artifacts/ux-designs/ux-parley_voo-2026-06-05/EXPERIENCE.md'
---

# Implementation Readiness Assessment Report

**Date:** 2026-06-05
**Project:** parley_voo

## Document Inventory

| Type | File | Notes |
|---|---|---|
| PRD | `prds/prd-parley_voo-2026-06-04/prd.md` (+ `addendum.md`) | whole, status final |
| Architecture | `architecture.md` | whole, READY FOR IMPLEMENTATION |
| Epics & Stories | `epics.md` | whole, validated; 6 epics / 27 stories |
| UX Design | `ux-designs/ux-parley_voo-2026-06-05/DESIGN.md` + `EXPERIENCE.md` | two-file pair (visual identity + experience spine), status final |

No duplicate whole/sharded versions found. No missing document types. Process artifacts (reconcile docs, review rubrics, decision logs) and research reports excluded from assessment scope; research reports remain available for traceability reference.

## PRD Analysis

### Functional Requirements

FR1: `/evaluate` — input: a transcript; output: a pattern report plus profile updates for participants. Always runs the full parallel panel. A mid-conversation transcript is a valid input (the "halftime report") with no special handling — same command, partial transcript.
FR2: `/advise` — input: a goal plus a person; output: a playbook. Top section: quick plan summary, character read, past-win receipts, fallacies to avoid. Body: frame, opening line, sequence, objections + responses, fallback, "what you lose," first concrete step.
FR3: `/council` — input: a generic decision, no person; output: a "should we do X" verdict from the off-the-shelf engine.
FR4: Cost tiers: quick mode (fewer experts, no peer review) is the default for `/advise` and `/council`; a full-mode flag escalates. `/evaluate` always runs full panel.
FR5: Three-stage protocol: independent parallel analysis (experts never see each other's responses) → anonymized peer review (responses shuffled, labeled A–E) → chairman synthesis.
FR6: Synthesis distinguishes value tensions from error catches, preserves dissent rather than smoothing to consensus, and may side with a minority whose reasoning is strongest.
FR7: Engine supports two topologies: all-parallel (`/evaluate`) and staged/sequential with a decoder-ring handoff seat (`/advise`). This dual-topology capability is the differentiator versus parallel-only LLM-council clones.
FR8: Engine is usable standalone — councils can be created and run without touching the coach pipeline.
FR9: Councils and persona sets export/import in a portable format consumable by other LLMs, including import from a user's existing project.
FR10: `/evaluate` panel (parallel, four core seats): Behavioral Coder (Gottman/FBA), Psycholinguist (Pennebaker/LIWC), Personality Profiler (Big Five, item-scores-first), Relational Needs Analyst (attachment/NVC/TA). Optional fifth lens: ADHD Specialist.
FR11: Orthogonality enforced at runtime: each seat's "ignores" written into its prompt as a hard prohibition — four independent footprints make the synthesis worth more than the sum of its parts.
FR12: Citation rule: every expert claim must cite transcript lines or the chairman discards it.
FR13: `/advise` pipeline (sequential): Profile Translator (decoder ring, runs twice — subject and self) → Message Strategist ∥ Negotiation Architect ∥ Influence Tactician → Red Team → playbook synthesis. Execution Realist consumes the self decoder ring and stress-tests whether the user will actually run the plan under pressure (RSD, over-explaining — negative-space "don't" coaching).
FR14: Mutual-benefit guardrail: Influence Tactician is restricted to mutual-benefit moves; Red Team flags anything that only works if the subject doesn't notice. Bar: you'd be comfortable if the subject found out you used the tactic — not merely if they read the playbook.
FR15: Optional-seat defaults: ADHD Specialist and Execution Realist ON in the user's local config, OFF (opt-in) in the public template.
FR16: Users can create, edit, and research/define new personas via dedicated commands as part of setup — first-class capability, its own epic.
FR17: Default rosters are defined per mode and overridable.
FR18: Each expert must use a distinct, named reasoning method — not just a distinct job title. MBTI/Enneagram are barred as scoring engines (no psychometric validity); acceptable only as translation layers.
FR19: Every profile splits into two layers at storage time: subject layer (traits, style, what framing lands — portable) and relationship layer (real quotes, incidents, advice→outcome history — private, never exported).
FR20: The user's own profile is a first-class subject.
FR21: Profiles are falsifiable models: claims carry attribution, confidence (e.g., Profiler correlation ranges), and track records. Profile fields include known fallacies. A profile is interpretation, not fact — traits and patterns, attributed and provisional; never a dossier of private anecdotes about a named person.
FR22: Ingestion: Zoom transcripts are primary, organized by source (`ingest/transcripts/`, `ingest/slack/`, extensible); every item carries context metadata (1-on-1 vs. group, participants). Exact metadata schema is an architecture decision, not a PRD blocker.
FR23: Linguistic feature script: computes LIWC-style metrics (pronoun ratios, hedging density, language-style matching) from transcripts and feeds the Psycholinguist seat hard numbers.
FR24: Deterministic personality scoring: BFI item scoring computed as math, feeding the Personality Profiler. [Architecture-ratified reframe: lexicon-based weak signal with published correlation ranges as confidence; IPIP deterministic keying only for self-administered questionnaires.]
FR25: Calibration scoring computed from `advice_outcomes`: per-person prediction hit rates (e.g., "Red Team is batting .71 on this person") plus Brier scores measuring calibration quality of Red Team predictions and Profiler claims.
FR26: Semantic recall: sqlite-vec search over transcript history feeding the citation rule and past-win receipts (same SQLite file, no added infra).
FR27: `/advise` records the plan; a later `/evaluate` of the real conversation updates the person's profile and scores whether the advice worked.
FR28: Past-win receipts: dated, queryable record of what has worked with each person, surfaced in the `/advise` playbook.
FR29: `/export-profile <name>` emits subject-layer-only portable markdown — anecdotes generalized to traits, headed as a starting hypothesis, not a verdict. Two sanitization levels chosen per invocation: Named (default) and Archetype (anonymized, public-safe) via one flag.
FR30: `/import-profile <file>` ingests with provenance tagging and keeps the imported read distinct from the user's own — their Chris ≠ your Chris: two legitimately distinct reads kept side by side, never blended.
FR31: Public template repo ships engine, commands, schema, and archetype example profiles; `.gitignore` excludes `people/`, `transcripts/`, and `index.sqlite`. Acceptance: a scripted check (e.g., `scripts/verify-clean-fork`) run against a fresh clone confirms zero private data.
FR32: README includes a responsible-use note covering: the tool exists to improve your own communication, not to covertly profile others; discretion around mutual contacts; profiles are interpretation, not fact; Archetype is the default-safe level for anything public. Optional Claude Code plugin packaging stays in scope as Distribution polish, not a separate requirement.

Total FRs: 32

### Non-Functional Requirements

NFR1 Privacy: hard subject/relationship separation enforced at storage time; exports strip the relationship layer; `.gitignore` enforcement verified.
NFR2 Cost: quick mode default outside `/evaluate`; debate only where it earns its token cost.
NFR3 Portability: human-readable markdown profiles; git-friendly; council/profile artifacts consumable by other LLMs.
NFR4 Bounded infrastructure: single local SQLite file, no server; graph DB and Claude Project export stay deferred until a real trigger.
NFR5 Responsible use: profiles framed as interpretation, not fact; mutual-benefit-only influence; Archetype export is the public-safe path.
NFR6 Anti-sycophancy: independence-first protocol so majority pressure cannot suppress correct minority reads.

Total NFRs: 6

### Additional Requirements

- Counter-metrics (Goals & Signals): token cost per routine run stays low; profiles never harden into "facts" — every claim stays attributed, provisional, confidence-scored.
- Scope & Phasing: computed-evidence features (FR23–FR26) land inside the engine/data/feedback epics they serve. V2 deferrals: ride-along copilot, Claude Project export, graph DB. Cut: `parley confer`.
- Addendum constraints: built on `ngmeyer/council-review` lineage (harvest deliberation logic); storage = one markdown file per person + `transcripts/` + single `index.sqlite` + per-expert memory dirs; Claude Code mechanics (skills, agents, commands, templates, ingest scripts); optional plugin packaging.
- PRD Open Questions (both deferred by design): (1) ingestion metadata schema → architecture (resolved there); (2) session UX detail → bmad-ux (resolved there).

### PRD Completeness Assessment

PRD is final-status, tightly written, and numbered throughout — extraction was unambiguous. FRs are testable and clustered logically; NFRs each carry an enforcement intent. The single material caveat: FR24 as written ("BFI item scoring as math") was invalidated by technical research and reframed by architecture — the PRD text was not updated, so the reframe lives downstream (architecture §FR24 reframe, epics Story 3.4). Traceability must therefore validate against the reframed FR24, not the literal PRD text. Both PRD open questions were explicitly delegated and subsequently resolved by the receiving documents.

## Epic Coverage Validation

### Coverage Matrix

Verified against story text and acceptance criteria, not just the epics document's own FR Coverage Map. Where an FR spans authoring and runtime, all contributing stories are listed.

| FR | Requirement (short) | Epic/Story Coverage | Status |
|---|---|---|---|
| FR1 | `/evaluate` pattern report + profile updates; halftime valid | 3.6 (incl. partial-transcript AC) | ✓ Covered |
| FR2 | `/advise` playbook, top section + body | 4.1 (top section, quick) + 4.2 (full body) | ✓ Covered |
| FR3 | `/council` generic verdict | 1.4 | ✓ Covered |
| FR4 | Quick/full cost tiers | 1.3 (machinery) + 4.1 (default) + 3.6 (evaluate pinned full) | ✓ Covered |
| FR5 | Three-stage independence protocol | 1.2 | ✓ Covered |
| FR6 | Dissent-preserving synthesis | 1.2 + 1.4 (`Dissent:` rendering) | ✓ Covered |
| FR7 | Dual topology | 1.3 | ✓ Covered |
| FR8 | Engine standalone | 1.4 (zero-data standalone AC) | ✓ Covered |
| FR9 | Council export/import portable | 2.6 | ✓ Covered |
| FR10 | Evaluate panel seats + optional ADHD lens | 2.1 (authoring) + 3.6 (panel execution) | ✓ Covered |
| FR11 | Orthogonality via "ignores" prohibitions | 2.1/2.2 (authored) + 2.5 (displayed) | ✓ Covered |
| FR12 | Citation rule, chairman discards | 3.2 (verify mechanism) + 3.6 (enforcement) + 2.1 (prompt contract) | ✓ Covered |
| FR13 | Staged advise pipeline | 2.2 (seats) + 2.3 (stage groups) + 4.1/4.2 (execution) | ✓ Covered |
| FR14 | Mutual-benefit guardrail | 2.2 (in-prompt) + 4.2 (runtime pass/flag) | ✓ Covered |
| FR15 | Optional-seat defaults local/template | 2.3 (config posture) + 6.3 (fork verification) | ✓ Covered |
| FR16 | Persona create/edit/research commands | 2.4 | ✓ Covered |
| FR17 | Per-mode default rosters, overridable | 2.3 + 2.5 (override artifact) | ✓ Covered |
| FR18 | Named reasoning methods; MBTI bar | 2.1/2.2 (authored) + 2.4 (validation) | ✓ Covered |
| FR19 | Two-layer split at storage time | 3.5 | ✓ Covered |
| FR20 | Self-profile first-class | 3.5 (slug `me`) + 3.7 (rendering) | ✓ Covered |
| FR21 | Falsifiable profiles | 3.5 (storage) + 3.7 (display) | ✓ Covered |
| FR22 | Source-organized ingestion + metadata | 3.1 | ✓ Covered |
| FR23 | Linguistic feature script | 3.3 | ✓ Covered |
| FR24 | Personality scoring (reframed) | 3.4 (weak-signal lexicon + IPIP keying) | ✓ Covered (as reframed) |
| FR25 | Calibration: hit rates + Brier | 5.2 (compute) + 5.4 (display) | ✓ Covered |
| FR26 | sqlite-vec semantic recall | 3.2 | ✓ Covered |
| FR27 | Plan recorded → outcome scored | 5.1 (record) + 5.2 (score) + 5.3 (no-transcript path) | ✓ Covered |
| FR28 | Past-win receipts in playbook | 5.4 | ✓ Covered |
| FR29 | Export-profile Named/Archetype | 6.1 | ✓ Covered |
| FR30 | Import-profile provenance | 6.2 | ✓ Covered |
| FR31 | Clean public template, scripted check | 6.3 + 1.1 (gitignore foundation) | ✓ Covered |
| FR32 | Responsible-use README + plugin polish | 6.4 | ✓ Covered |

### Missing Requirements

None. No PRD FR lacks story coverage; no epic story claims an FR that does not exist in the PRD.

### Coverage Statistics

- Total PRD FRs: 32
- FRs covered in epics: 32
- Coverage percentage: **100%**

## UX Alignment Assessment

### UX Document Status

Found — `DESIGN.md` (visual identity, design tokens, two render targets) + `EXPERIENCE.md` (experience spine: IA, flows, component/state patterns). Both status `final`, dated 2026-06-05. Spine declared binding by architecture ("UX contracts: DESIGN.md + EXPERIENCE.md are binding"); spine wins on mock conflict by its own rule.

### UX ↔ PRD Alignment

- EXPERIENCE.md's Information Architecture table maps every command surface to its FRs — all 32 FRs are either surfaced or explicitly routed (computed-evidence FR23–26 declared "no direct user surface, surfaced through documents" — deliberate, not a gap).
- UX resolved both items the PRD delegated to it: session UX detail (document anatomies, flows) and FR9 command naming (`/export-council` / `/import-council`).
- One UX-flagged open question handled correctly downstream: FR26 has no "search my history" command — UX said "unspecified, do not invent," and the epics correctly contain no such story.
- No UX requirement exists that lacks a PRD anchor; every behavioral rule traces to an FR.

### UX ↔ Architecture Alignment

- Citation addressing reconciled: UX citation primitive `[date context, Tnn]` matches the architecture's speaker-turn-ID decision (UX decision log was updated when architecture changed from line numbers — verified consistent in both documents).
- HTML artifact surface (roster picker, outcome scorer; stateless, Copy Prompt round-trip) is architecturally supported: Python string templates → `.parley/artifacts/`, DESIGN.md tokens inlined.
- State model aligned: UX requires state in session + SQLite/markdown store, never in artifacts — matches architecture's boundary (skills never query SQLite; scripts own the store).
- Terminal-markdown conventions are renderer-free (host terminal owns rendering) — no architectural component needed; correctly absent.

### Alignment Issues

None blocking.

### Warnings

1. **Cosmetic:** EXPERIENCE.md Flow 1 step 6 uses a `.vtt` example filename (`chris-2026-06-05.vtt`) while the ratified ingestion input is markdown. Architecture already logged this as cosmetic ("ingestion is source-extensible, no spine change needed"). No action required before implementation; fix opportunistically.
2. **Mock dependency:** Two key-screen mockups are referenced as illustrations; persona-card "Ignores:" copy in mocks is placeholder until authored persona prompts exist (Story 2.1/2.2) — the UX itself flags the swap. Tracked, not a gap.

## Epic Quality Review

Method: dual-pass — author pass against the create-epics-and-stories checklist, plus an independent adversarial subagent review (no authorship bias). Findings merged and de-duplicated.

### Best Practices Compliance

| Check | E1 | E2 | E3 | E4 | E5 | E6 |
|---|---|---|---|---|---|---|
| User value (not technical milestone) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Epic independence (backward-only) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Story sizing (single dev session) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| No forward dependencies | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| AC quality (G/W/T, testable) | ✓ | ✓ | ⚠ (3.6) | ✓ | ✓ | ✓ |
| FR traceability | ✓ | ⚠ (map drift) | ✓ | ⚠ (map drift) | ✓ | ✓ |

Verified clean on the high-risk seams: minimal-council-in-E1 vs full-bench-in-E2 split is legitimate (1.2 authors chairman itself; 1.4 ships its own default council); Story 3.6 correctly does NOT claim outcome scoring (that is 5.2); the 5.1→5.3 artifact reference is a deferral note, not a dependency. Starter template requirement satisfied: architecture mandates the scaffold and Story 1.1 is exactly that story (init command, uv dependencies, initial config, CI). Greenfield indicators present (setup story, CI early).

### 🔴 Critical Violations

None found.

### 🟠 Major Issues

1. **FR Coverage Map drift on split FRs (FR10, FR13, FR14).** Stories 2.1/2.2 explicitly claim "FR10 authoring," "FR13 authoring," "FR14 in-prompt," but the epics document's coverage map and Epic 2's "FRs covered" line credit these FRs solely to the runtime epics (3 and 4). A reviewer reading the map cannot find where the persona-authoring half of these FRs lives. *Remediation:* annotate the map ("FR10: Epic 2 (authoring) + Epic 3 (runtime)" etc.) and add the authoring credits to Epic 2's covered list.
2. **Story 1.2 hardcodes "A–E" relabeling.** The literal comes verbatim from PRD FR5 (illustrative of a five-seat panel), but as a generic-engine AC it is wrong for any council that isn't exactly five seats — including Epic 1's own minimal council. *Remediation:* reword to "relabels them A, B, C… (one label per participating seat)."
3. **Story 3.6 carries non-AC content:** the `conflicts` table define-or-drop decision is a bare `**And**` outside Given/When/Then structure, bolted onto the heaviest story in the breakdown. *Remediation:* convert to a proper G/W/T criterion (decision stays in 3.6 per architecture's "define or drop during the /evaluate epic").
4. **Story 3.6 omits its Epic 2 preconditions.** It consumes `councils/evaluate-default.md` and the optional-seat config posture (both Story 2.3) without a Given naming them — unlike 4.1, which cites its roster explicitly. Backward-valid, but an implementer isn't told. *Remediation:* add the precondition Given.

### 🟡 Minor Concerns

1. **Story 3.4 questionnaire input plumbing unspecified** — the self-administered IPIP path has no ingestion route (3.1 ingests transcripts only). Intended: file passed directly to `personality.py` via CLI arg; should be stated.
2. **Story 1.1 schema is provisional on 3.6's `conflicts` decision** — acceptable under greenfield-rebuild policy; worth a one-line note in 1.1.
3. **Story 2.5 AC names `/advise` and `/evaluate` roster-override flags** — commands that exist only in Epics 3–4. The artifact mechanism is fully buildable and testable on `/council` (Epic 1); later commands only re-use it. Wording should scope to "any council-running command (at minimum `/council`)."
4. **Non-human story personas (3.3, 3.4)** — "As the Psycholinguist seat" frames scripts from the consuming seat's perspective. Stylistic; value is clear.
5. **LLM-behavior ACs** (e.g., "preserves minority positions") are not deterministically testable — inherent to the domain; prompts are inspectable and golden-style transcript fixtures can approximate.
6. **No UX-DR-to-story coverage table in epics.md** — UX-DRs are validated per-document-story (and were verified complete at epic creation); an explicit table would give UX the same audit trail FRs have. Optional.

## Summary and Recommendations

### Overall Readiness Status

**READY** — with 4 pre-dev text fixes recommended (none structural, all confined to `epics.md`).

Evidence: 32/32 FR coverage verified against story text (not just the map); UX fully aligned with PRD and Architecture on both axes; zero critical quality violations; epic chain is strictly backward-dependent; the architecture-mandated scaffold story is in place; the one PRD-level discrepancy (FR24) is a ratified, traceable reframe, not a gap.

### Critical Issues Requiring Immediate Action

None. No issue found blocks implementation.

### Recommended Next Steps

1. **Apply the 4 major-issue text fixes to `epics.md`** (~5 min total): annotate the coverage map for split FRs 10/13/14 and add authoring credits to Epic 2's header; reword Story 1.2's "A–E" to per-seat labeling; convert Story 3.6's `conflicts` decision to proper Given/When/Then; add Story 3.6's Epic 2 precondition Given.
2. **Optionally apply minors 1–3** while in the file (questionnaire input via CLI arg in 3.4; `conflicts`-provisional note in 1.1; scope 2.5's flag wording to `/council`-first). Minors 4–6 need no action.
3. **Proceed to `bmad-sprint-planning`** (fresh context window) to generate the sprint status plan, then begin the story cycle at Story 1.1.

### Final Note

This assessment identified 12 issues across 3 categories (4 major, 6 minor, 2 cosmetic UX warnings) — zero critical. The major issues are documentation-precision fixes inside `epics.md`, not planning failures; the artifact set is internally consistent and traceable end-to-end (PRD → Architecture → UX → Epics). Address the majors before dev-agent handoff so implementers inherit a drift-free coverage map, or proceed as-is accepting minor traceability friction.

---

**Assessor:** adversarial PM review (dual-pass: author + independent subagent) · **Date:** 2026-06-05

### Post-Assessment Addendum (2026-06-05)

All 4 major issues and minors 1–3 were applied to `epics.md` (10 surgical edits) and verified resolved by an independent subagent pass: coverage-map dual-credits for FR10/13/14, Epic 2 authoring credits, per-seat anonymization labels in 1.2, `conflicts` decision as proper G/W/T in 3.6, Epic 2 preconditions in 3.6, questionnaire input plumbing in 3.4, provisional-`conflicts` note in 1.1, and `/council`-scoped flag wording in 2.5. No regressions found. Minors 4–6 accepted as-is per assessment. **Status: READY, majors cleared.**
