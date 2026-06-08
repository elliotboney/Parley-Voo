# Parley Voo PRD — Addendum

Technical depth and rationale that belongs downstream (architecture / solution design), not in the PRD body.

## Beyond-a-prompt tech (discovery decision, 2026-06-04)

User goal: capabilities a person couldn't replicate with a single prompt. Options considered, ranked by adoption:

1. **Computed linguistic features** — ADOPTED. Script computes LIWC-style metrics (pronoun ratios, hedging density, language-style matching) from transcripts and feeds the Psycholinguist seat hard numbers instead of LLM judgment. Same pattern for Personality Profiler: BFI item scoring as deterministic math.
2. **Calibration scoring** — ADOPTED. Brier scores on Red Team predictions and Profiler claims, computed from `advice_outcomes` (SQL + small script). Makes "falsifiable profile" a number (e.g. "Red Team batting .71 on this person").
3. **sqlite-vec semantic recall** — ADOPTED, un-parked from V2 into V1. Semantic search over transcript history (same SQLite file, no new infra) feeding the citation rule and past-win receipts.
4. **Graph DB** — REJECTED for V1 (stays parked, per original spec). At solo scale, relationship edges fit in a SQLite edges table or markdown links; no new expert capability earned.

Rationale anchor: the moat is the data loop (scored advice outcomes + accumulated profiles). Tech adopted only where it feeds that loop with evidence a prompt can't fabricate.

## Tech stack notes carried from spec (for architecture)

- Built on/adapts `ngmeyer/council-review` SKILL.md (Karpathy LLM Council + DMAD ICLR 2025 lineage). Harvest deliberation logic; graft domain experts, memory, storage.
- Storage: one markdown file per person (`people/<name>.md`, YAML frontmatter), `transcripts/`, single local `index.sqlite` (people, conversations, patterns, conflicts, advice_outcomes), per-expert memory dirs.
- Claude Code mechanics: `.claude/skills/council-engine/SKILL.md`, `.claude/agents/` (one file per persona, tool scoping), `.claude/commands/`; templates `profile.subject.md` / `profile.relationship.md`; `scripts/ingest.*`. Optional plugin packaging.
- Expert grounding frameworks: Gottman/FBA, Pennebaker/LIWC, Big Five (item-scores-first), attachment/NVC/TA, Crucial Conversations/Heath, Fisher & Ury, Voss/Cialdini.
- Deferred: graph DB (trigger: joins get ugly), Claude Project export (V2).
