---
title: Parley Voo PRD
status: final
created: 2026-06-04
updated: 2026-06-04
---

# Parley Voo PRD

## Overview

Parley Voo (*parlez-vous?* — to talk things through, especially across a divide) is a Claude Code-based personal communication coach. Councils of expert personas — each grounded in a distinct, named reasoning discipline — evaluate past conversations and strategize upcoming ones, reasoning from living profiles the user builds of real people over time. A feedback loop scores whether advice actually worked, so the system sharpens with use.

What makes it more than a prompt: experts reason from **computed evidence with track records** — scripted linguistic metrics, deterministic personality scoring, calibration scores over recorded advice outcomes, and semantic recall over transcript history — applied to accumulated person-specific data nobody can prompt their way to.

Design signature — **negative space**: experts are defined by what they ignore, coaching by what not to do, exports by what is stripped.

## Users & Stakes

- **Primary:** a single solo user coaching their own communication and navigating specific people. The user's own profile is a first-class subject; ADHD-aware coaching (RSD, over-explaining) is a load-bearing design input, not a nice-to-have.
- **Secondary:** forkers of the public template repo, who clone the framework and start clean with zero private data.

Hobby-stakes project, but the public forkable repo elevates privacy and responsible-use requirements to must-haves.

## Goals & Signals

1. Advice quality visibly sharpens with use — per-person "what lands" knowledge and calibration scores improve over time.
2. The user can prepare for a high-stakes conversation in one `/advise` run and walk in with a playbook they will actually execute.
3. A clean fork contains zero private data (verifiable acceptance check).
4. Council verdicts resist sycophancy — dissent survives synthesis; the chairman can side with a strong minority.

**Counter-metrics:** token cost per routine run stays low (quick mode default outside `/evaluate`); profiles never harden into "facts" — every claim stays attributed, provisional, and confidence-scored.

## Core Loop

The user runs `/advise` before a real conversation ("how do I get Chris to back this proposal?") and gets a playbook. They have the conversation. They feed the Zoom transcript to `/evaluate`, which updates Chris's profile **and** scores whether the advice worked. The next `/advise` for Chris reasons from the updated profile, past-win receipts, and the Red Team's batting average.

## Functional Requirements

### Modes & Commands

- **FR1** `/evaluate` — input: a transcript; output: a pattern report plus profile updates for participants. Always runs the full parallel panel. A mid-conversation transcript is a valid input (the "halftime report") with no special handling — same command, partial transcript.
- **FR2** `/advise` — input: a goal plus a person; output: a playbook. Top section: quick plan summary, character read, past-win receipts, fallacies to avoid. Body: frame, opening line, sequence, objections + responses, fallback, "what you lose," first concrete step.
- **FR3** `/council` — input: a generic decision, no person; output: a "should we do X" verdict from the off-the-shelf engine.
- **FR4** Cost tiers: quick mode (fewer experts, no peer review) is the default for `/advise` and `/council`; a full-mode flag escalates. `/evaluate` always runs full panel.

### Deliberation Engine

- **FR5** Three-stage protocol: independent parallel analysis (experts never see each other's responses) → anonymized peer review (responses shuffled, labeled A–E) → chairman synthesis.
- **FR6** Synthesis distinguishes value tensions from error catches, preserves dissent rather than smoothing to consensus, and may side with a minority whose reasoning is strongest.
- **FR7** Engine supports two topologies: all-parallel (`/evaluate`) and staged/sequential with a decoder-ring handoff seat (`/advise`). This dual-topology capability is the differentiator versus parallel-only LLM-council clones.
- **FR8** Engine is usable standalone — councils can be created and run without touching the coach pipeline.
- **FR9** Councils and persona sets export/import in a portable format consumable by other LLMs, including import from a user's existing project.

### Expert Panels

- **FR10** `/evaluate` panel (parallel, four core seats): Behavioral Coder (Gottman/FBA), Psycholinguist (Pennebaker/LIWC), Personality Profiler (Big Five, item-scores-first), Relational Needs Analyst (attachment/NVC/TA). Optional fifth lens: ADHD Specialist.
- **FR11** Orthogonality enforced at runtime: each seat's "ignores" written into its prompt as a hard prohibition — four independent footprints make the synthesis worth more than the sum of its parts.
- **FR12** Citation rule: every expert claim must cite transcript lines or the chairman discards it.
- **FR13** `/advise` pipeline (sequential): Profile Translator (decoder ring, runs twice — subject and self) → Message Strategist ∥ Negotiation Architect ∥ Influence Tactician → Red Team → playbook synthesis. Execution Realist consumes the self decoder ring and stress-tests whether the user will actually run the plan under pressure (RSD, over-explaining — negative-space "don't" coaching).
- **FR14** Mutual-benefit guardrail: Influence Tactician is restricted to mutual-benefit moves; Red Team flags anything that only works if the subject doesn't notice. Bar: you'd be comfortable if the subject found out you used the tactic — not merely if they read the playbook.
- **FR15** Optional-seat defaults: ADHD Specialist and Execution Realist ON in the user's local config, OFF (opt-in) in the public template.

### Persona Management

- **FR16** Users can create, edit, and research/define new personas via dedicated commands as part of setup — first-class capability, its own epic.
- **FR17** Default rosters are defined per mode and overridable.
- **FR18** Each expert must use a distinct, named reasoning method — not just a distinct job title. MBTI/Enneagram are barred as scoring engines (no psychometric validity); acceptable only as translation layers.

### Profiles & Data

- **FR19** Every profile splits into two layers **at storage time**: subject layer (traits, style, what framing lands — portable) and relationship layer (real quotes, incidents, advice→outcome history — private, never exported).
- **FR20** The user's own profile is a first-class subject.
- **FR21** Profiles are falsifiable models: claims carry attribution, confidence (e.g., Profiler correlation ranges), and track records. Profile fields include known fallacies. A profile is interpretation, not fact — traits and patterns, attributed and provisional; never a dossier of private anecdotes about a named person.
- **FR22** Ingestion: Zoom transcripts are primary, organized by source (`ingest/transcripts/`, `ingest/slack/`, extensible); every item carries context metadata (1-on-1 vs. group, participants). Exact metadata schema is an architecture decision, not a PRD blocker.

### Computed Evidence

- **FR23** Linguistic feature script: computes LIWC-style metrics (pronoun ratios, hedging density, language-style matching) from transcripts and feeds the Psycholinguist seat hard numbers.
- **FR24** Deterministic personality scoring: BFI item scoring computed as math, feeding the Personality Profiler.
- **FR25** Calibration scoring computed from `advice_outcomes`: per-person prediction hit rates (e.g., "Red Team is batting .71 on this person") plus Brier scores measuring calibration quality of Red Team predictions and Profiler claims.
- **FR26** Semantic recall: sqlite-vec search over transcript history feeding the citation rule and past-win receipts (same SQLite file, no added infra).

### Feedback Loop

- **FR27** `/advise` records the plan; a later `/evaluate` of the real conversation updates the person's profile and scores whether the advice worked.
- **FR28** Past-win receipts: dated, queryable record of what has worked with each person, surfaced in the `/advise` playbook.

### Sharing, Portability & Distribution

- **FR29** `/export-profile <name>` emits subject-layer-only portable markdown — anecdotes generalized to traits (e.g., "tends to disengage when pitched without warning," never "shut down when you pitched X on Tuesday"), headed as a starting hypothesis, not a verdict. Two sanitization levels chosen per invocation: Named (default) and Archetype (anonymized, public-safe) via one flag.
- **FR30** `/import-profile <file>` ingests with provenance tagging and keeps the imported read distinct from the user's own — their Chris ≠ your Chris: two legitimately distinct reads kept side by side, never blended.
- **FR31** Public template repo ships engine, commands, schema, and archetype example profiles; `.gitignore` excludes `people/`, `transcripts/`, and `index.sqlite`. Acceptance: a scripted check (e.g., `scripts/verify-clean-fork`) run against a fresh clone confirms zero private data — no profile, transcript, or database contents present.
- **FR32** README includes a responsible-use note covering: the tool exists to improve your own communication, not to covertly profile others; discretion around mutual contacts; profiles are interpretation, not fact; Archetype is the default-safe level for anything public. Optional Claude Code plugin packaging stays in scope as Distribution polish, not a separate requirement.

## Non-Functional Requirements

- **NFR1 Privacy:** hard subject/relationship separation enforced at storage time; exports strip the relationship layer; `.gitignore` enforcement verified.
- **NFR2 Cost:** quick mode default outside `/evaluate`; debate only where it earns its token cost.
- **NFR3 Portability:** human-readable markdown profiles; git-friendly; council/profile artifacts consumable by other LLMs.
- **NFR4 Bounded infrastructure:** single local SQLite file, no server; graph DB and Claude Project export stay deferred until a real trigger.
- **NFR5 Responsible use:** profiles framed as interpretation, not fact; mutual-benefit-only influence; Archetype export is the public-safe path.
- **NFR6 Anti-sycophancy:** independence-first protocol so majority pressure cannot suppress correct minority reads.

## Scope & Phasing

**V1 epics:** Repo scaffold → Deliberation engine → Expert panel → Persona management → Data model & storage → `/evaluate` → `/advise` → `/council` → Feedback loop → Profile sharing → Distribution polish. Final ordering belongs to epics planning. Computed-evidence features (FR23–FR26) land inside the engine/data/feedback epics they serve.

**Later / V2:** ride-along copilot (live in-conversation coaching, Red Team courtside pings, auto-feed transcript to `/evaluate`), Claude Project export, graph DB (only if joins get ugly). The "halftime report" needs no new machinery (see FR1) and is V1 usage, not a V2 feature.

**Cut:** `parley confer` — artifact of project-name brainstorming, never a mode.

## Glossary

- **Subject layer / relationship layer** — the portable-traits half vs. the private-history half of a profile, split at storage time.
- **Decoder ring** — Profile Translator's output: how a person decides, what framing lands, what triggers a "no."
- **Past-win receipts** — dated record of what has worked with a person, queried from `advice_outcomes`.
- **Topology** — how a council is wired: all-parallel (`/evaluate`) vs. sequential with decoder-ring handoff (`/advise`).
- **Quick / full mode** — fewer experts, no peer review vs. all seats plus anonymized peer review.
- **Negative space** — design signature: experts defined by what they ignore, coaching by what not to do, exports by what is stripped.

## Open Questions

1. Ingested-item context metadata schema — defer to architecture.
2. Session UX detail beyond the playbook top-section layout (report formatting, in-session flow) — defer to `bmad-ux`.
