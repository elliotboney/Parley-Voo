# Parley Voo — Project Specification

> **Name:** **Parley Voo** — to talk things through, especially across a divide.
> **Tagline:** *Parlez-vous?*
> **Command:** `parley` (e.g. `parley evaluate`, `parley confer "..."`)
> **What it is:** A Claude Code project that runs your conversations and communication decisions through a panel of expert personas, builds living profiles of the people you interact with (and yourself), and gets sharper over time.
> **Status:** Design locked. Two small decisions open (see [Open Decisions](#open-decisions)). Ready to scaffold.

---

## 1. The One-Liner

A personal communication coach built as a council of expert advisors. Feed it a transcript and it tells you what patterns showed up and how to improve. Give it a goal ("how do I get Chris to back this proposal?") and the same panel — reasoning from the *actual* profile you've built on Chris — hands you a grounded strategy. Every real conversation feeds back in, so the system learns who people are and what advice actually works.

**Why it's different from asking one chatbot:** It reasons from accumulated, person-specific profiles instead of generic stereotypes, and it uses a structured multi-perspective protocol that resists the "AI just agrees with you" failure mode.

---

## 2. Core Architecture: One Engine, Three Lenses

A single deliberation engine, pointed in different directions:

| Command | Direction in time | Input | Output |
|---|---|---|---|
| `/evaluate` | **Backward** | A transcript | Pattern report + profile updates |
| `/advise` | **Forward** | A goal + a person | A grounded strategy / playbook |
| `/council` | **Neutral** | A generic decision (no person) | A "should we do X" verdict |

`/council` is essentially the off-the-shelf behavior of the engine we're building on, kept for free.

---

## 3. The Deliberation Engine

Built on the proven protocol from [`ngmeyer/council-review`](https://github.com/ngmeyer/council-review) (itself based on Karpathy's LLM Council + the DMAD ICLR 2025 research). We harvest its deliberation logic — the annoying-to-get-right part — and graft our domain experts, memory, and storage onto it.

**The protocol (per run):**

1. **Parallel, independent analysis** — each expert reasons on the input without seeing the others' responses. (No groupthink.)
2. **Anonymized peer review** — responses are shuffled/labeled A–E; experts critique each other without knowing who said what. (No deference to roles.)
3. **Chairman synthesis** — one synthesizer combines everything, distinguishing *value tensions* (both sides valid) from *error catches* (one expert found a real flaw), and **preserves dissent** rather than smoothing to consensus. The chairman may side with a minority if its reasoning is strongest.

**Non-negotiable design principle (from the research):** each expert must use a **distinct reasoning method**, not just a distinct job title. Same-model panels converge into one opinion unless their reasoning *footprints* differ. This is the single most important thing to get right in the prompts.

**Cost-tiered modes** (inherited): a full multi-call mode for high-stakes work and a quick mode (fewer experts, no peer review) for gut-checks. Multi-agent runs cost meaningfully more tokens, so quick mode should be the default for routine use.

---

## 4. The Expert Panel

One stable spine; a few experts rotate by mode. Each carries a **distinct reasoning method**.

| Expert | Reasoning lens | `/evaluate` job | `/advise` job |
|---|---|---|---|
| **Communication Analyst** | Structure & clarity | What patterns showed up (assertive/passive/aggressive, repair attempts)? | How to frame and sequence the message |
| **Personality-Fit Strategist** | Type-based adaptation | How did their type shape this exchange? | How to tailor the pitch to *this* person |
| **ADHD Specialist** | Executive-function / RSD | Where did EF load or rejection-sensitivity create friction (both sides)? | How *you* realistically execute the plan given your patterns |
| **Clinical / Social Psychologist** | Emotional subtext | Defensiveness, attachment/conflict style, what went unsaid | What's likely to trigger resistance |
| **Contrarian** *(advise-only)* | Inversion | — | How does this backfire? What if they say no? |
| **Influence / Negotiation Strategist** *(advise-only)* | Leverage & timing | — | Concrete moves: timing, sequencing, concessions |

> These are the **proposed** roster. Confirm or edit before/at scaffold time — see [Open Decisions](#open-decisions).

---

## 5. Data Model — Two-Layer Profiles

The most important structural decision. Every profile splits into two layers **at storage time**, so sharing is free later instead of a painful retrofit.

| Layer | Holds | Shareable? |
|---|---|---|
| **Subject** (about the person) | Communication style, decision-making, what framing lands, triggers, personality read | ✅ Portable |
| **Relationship** (about you + them) | Real quotes, transcript links, specific incidents, your own reactions, advice→outcome history | ❌ Private |

A shareable profile = **subject layer only**, with anecdotes generalized into traits ("tends to disengage when surprised in front of peers" — never "shut down when you pitched X on Tuesday").

**Your own profile is a first-class subject** — the system tracks your patterns, where your instincts and execution diverge, etc.

### Storage decisions (deliberately boring, deliberately scalable)

- **Profiles:** one markdown file per person (`people/<name>.md`), YAML frontmatter + body. Human-readable, git-friendly, easy to share.
- **Transcripts:** files in `transcripts/`.
- **Index/spine:** a single local **SQLite** file (`index.sqlite`) — people, conversations, tagged patterns, conflict flags, advice→outcome records. SQL-native, no server, "relationship-shaped" queries are just joins.
- **Per-expert memory:** each expert subagent gets a `memory` directory so it accumulates its own running notes across runs.
- **Deferred (don't build until there's a real trigger):**
  - *Vector search* via the `sqlite-vec` extension (stays inside the same SQLite file) — add only when "find conversations similar to this one" becomes a bottleneck at scale.
  - *Graph DB* — only if genuinely multi-hop queries get ugly as joins. Most communication work never needs this.

---

## 6. The Feedback Loop (build this in by default)

The compounding mechanism that makes it more than a toy:

```
/advise (plan approach to Chris)
        │
        ▼
  you have the real conversation
        │
        ▼
/evaluate that transcript
        │
        ├── updates Chris's profile
        └── scores whether the advice actually worked
```

Over time the system learns not just *who* Chris is, but *what advice lands* with Chris — and where your own instincts vs. execution diverge.

---

## 7. Sharing & Portability

Two distinct features:

### A. Clone-and-use the framework (easy)
The public template repo ships the engine, commands, schema, and example/archetype profiles — and a `.gitignore` that **excludes your real `people/`, `transcripts/`, and `index.sqlite`**. You can fork it public without leaking private data. Forkers start clean; you stay private.

### B. Share an individual profile (the interesting one)
- **`/export-profile <name>`** → clean, portable markdown (subject layer only, your data stripped, anecdotes → traits).
- **`/import-profile <file>`** → ingests someone else's shared profile, tagged with **provenance** (whose read this is). Their Chris ≠ your Chris; the system keeps the two reads distinct rather than blending them.

**Two sanitization levels (chosen per export):**
- **Named** — keeps the real name. For a *mutual* real person you and a colleague both deal with.
- **Archetype** — anonymizes the name into a reusable example ("the skeptical-analytical stakeholder"); safe to ship publicly.

---

## 8. Responsible Use (matters more because the repo is public)

A behavioral profile is an **interpretation**, not a fact — it's the person as *you* experienced them. Bake this in:

- Every exported profile carries a header framing it as a **starting hypothesis, not a verdict**; import treats it the same way.
- Profiles describe **traits and patterns, attributed and provisional** — not a dossier of private anecdotes about a named person.
- README should include a short "responsible use" note: this is a tool for improving *your own* communication, profiles of real people should be handled with discretion, and named-profile sharing assumes a context where that's appropriate (e.g., mutual professional contacts), with Archetype mode as the default-safe option for anything public.

---

## 9. Repository Structure

```
parley/
├── README.md                  # vision + responsible-use note + quickstart
├── CLAUDE.md                  # how Claude Code should operate in this project
├── .gitignore                 # excludes people/, transcripts/, index.sqlite
├── .claude/
│   ├── skills/
│   │   └── council-engine/
│   │       └── SKILL.md       # adapted from council-review: protocol + experts
│   ├── agents/                # one file per expert persona
│   │   ├── communication-analyst.md
│   │   ├── personality-fit-strategist.md
│   │   ├── adhd-specialist.md
│   │   ├── clinical-psych.md
│   │   ├── contrarian.md
│   │   └── influence-strategist.md
│   └── commands/
│       ├── evaluate.md
│       ├── advise.md
│       ├── council.md
│       ├── export-profile.md
│       └── import-profile.md
├── schema/
│   └── index.sql              # SQLite schema
├── templates/
│   ├── profile.subject.md     # shareable layer template
│   └── profile.relationship.md# private layer template
├── examples/
│   └── archetype-skeptical-stakeholder.md
├── scripts/
│   └── ingest.*               # drop-in transcript importer → files + SQLite upsert
├── people/                    # GITIGNORED — your real subject+relationship profiles
├── transcripts/               # GITIGNORED — raw inputs
└── index.sqlite               # GITIGNORED — the spine
```

---

## 10. Tech Decisions — Summary

| Decision | Choice | Why |
|---|---|---|
| Multi-agent pattern | Orchestrator + independent experts, reconcile on conflict | Independence first; debate only where it earns its cost |
| Engine source | Adapt `ngmeyer/council-review` | Protocol already correct (anonymization, dissent preservation) |
| Expert differentiation | Distinct **reasoning methods**, not just titles | Same-model panels converge otherwise (DMAD) |
| Profile storage | Markdown files, two layers (subject/relationship) | Portable, git-friendly, sharing comes free |
| Index/spine | SQLite (single file) | SQL-native, no server, joins cover relationship queries |
| Vector / graph DB | Deferred (`sqlite-vec` first if needed) | Premature at your scale; avoid infra creep |
| Privacy | Private data `.gitignore`'d; export strips relationship layer | Public fork without leaks |
| Disagreement handling | Preserve dissent, chairman can side with minority | A noted minority view beats a smoothed average |

---

## 11. Build Backlog (turn these into stories)

Ordered roughly by dependency. Each epic is independently shippable.

### Epic 0 — Repo scaffold
- [ ] Init repo, `README.md` (vision + responsible-use note), `CLAUDE.md`
- [ ] `.gitignore` excluding `people/`, `transcripts/`, `index.sqlite`
- [ ] Folder structure from §9

### Epic 1 — Deliberation engine
- [ ] Pull `council-review` `SKILL.md`; adapt into `.claude/skills/council-engine/`
- [ ] Implement the 3-stage protocol: parallel independent → anonymized peer review → chairman synthesis
- [ ] Verify dissent preservation + chairman-can-override-majority behavior
- [ ] Wire full vs. quick mode

### Epic 2 — Expert panel
- [ ] One agent file per expert (final roster), each with a **distinct reasoning method** in its prompt
- [ ] Give each expert a `memory` directory
- [ ] Per-mode role behavior (evaluate vs. advise framing) inside each expert

### Epic 3 — Data model & storage
- [ ] `index.sql` schema: people, conversations, patterns, conflicts, advice_outcomes
- [ ] `profile.subject.md` + `profile.relationship.md` templates
- [ ] Two-layer write logic (analysis writes to the correct layer)

### Epic 4 — `/evaluate` (analysis mode)
- [ ] Read transcript + relevant profiles → run panel → pattern report
- [ ] Write pattern tags to SQLite; update subject + relationship layers
- [ ] Output: pattern report + improvement recommendations

### Epic 5 — `/advise` (advisory mode)
- [ ] Take goal + person → load that person's subject profile + recent history
- [ ] Run panel (with advise-only experts) → strategy/playbook
- [ ] Output: grounded recommendation + "what you lose" + first concrete step

### Epic 6 — `/council` (neutral mode)
- [ ] Generic decision input, no person → native council verdict

### Epic 7 — Feedback loop
- [ ] After `/advise`, record the plan
- [ ] `/evaluate` of a later transcript links back to that plan and scores outcome
- [ ] Surface "what advice actually lands with this person" over time

### Epic 8 — Profile sharing
- [ ] `/export-profile` (subject-only, anecdotes→traits, hypothesis header)
- [ ] Named vs. Archetype sanitization levels
- [ ] `/import-profile` with provenance tagging (keep distinct from your own read)
- [ ] One archetype example in `examples/`

### Epic 9 — Distribution polish
- [ ] Quickstart in README; sample run
- [ ] Confirm a clean fork has zero private data
- [ ] Optional: package as a Claude Code plugin for one-step install

---

## 12. Open Decisions

Two things to confirm. Defaults are set so you're not blocked.

1. **Final expert roster** — the §4 panel is proposed. Add (e.g., a "long-game relationship" advisor), cut (e.g., drop the Influence Strategist if it feels manipulative), or rename. *Default if unchanged: build the §4 roster as-is.*
2. **Default export sanitization level** — Named or Archetype? Per-export override always available. *Default if unchanged: **Named** for `/export-profile`, with Archetype as a one-flag switch (safest for anything public).*

---

## 13. References

**Foundation**
- `ngmeyer/council-review` — the engine we adapt: https://github.com/ngmeyer/council-review
- `karpathy/llm-council` — original concept (web app, multi-provider): https://github.com/karpathy/llm-council
- Other Claude Code ports for alternate advisor prompts: `aiwithremy/claude-skills-llm-council`, `tenfoldmarc/llm-council-skill`

**Claude Code mechanics**
- Custom subagents (`.claude/agents/`, frontmatter, `memory`, tool scoping): https://code.claude.com/docs/en/sub-agents
- Agents overview (subagents vs. agent teams vs. worktrees): https://code.claude.com/docs/en/agents.md

**Patterns & research**
- Anthropic, "How we built our multi-agent research system" (orchestrator-worker)
- DMAD (ICLR 2025) — reasoning-method diversity in multi-agent debate
- Note from debate research: majority pressure can suppress correct minority views → favor independence, preserve dissent

---

## 14. Addendum — Session Decisions (2026-06-04)

Refinements from kickoff brainstorming. These amend the sections above.

### Persona management is a first-class feature (amends §4, §11)
- Default rosters are defined **per mode** — the ingest/evaluate roster and the advise roster may differ.
- New users must be able to **change, build, and research/define new personas** as part of setup — via dedicated commands/workflows (e.g., create-persona, edit-persona, research-a-persona). This becomes its own epic, not a footnote.

### Ingestion structure (amends §5, §9)
- Primary source today: **Zoom transcripts**.
- Ingest is organized **by source**: e.g. `ingest/transcripts/` (Zoom), `ingest/slack/` (Slack messages), extensible per source type.
- Every ingested item carries **context metadata**: 1-on-1 vs. group setting, participants, etc. Exact metadata schema TBD.

### Parked for V2
- **Claude Project export** — output personality/profile artifacts into a file structure loadable into a normal Claude Project for browsing past conversations. Deferred: the SQLite spine is what makes retrieval work; don't dilute v1.

### Council engine is standalone-usable and exportable (amends §2, §7, §11)
- The deliberation engine ships **inside** Parley Voo (no separate project) but is a **first-class standalone capability**: users can create/build councils without touching the coach pipeline (profiles, ingest, feedback loop).
- **Council export/import**: output a council or persona set in a **portable format consumable by other LLMs**; import existing personas/councils from a user's own project. Mirrors §7 profile portability — profiles and councils are both portable artifacts.
- Discovered requirement: engine supports **two topologies** — all-parallel (evaluate) and staged/sequential with a decoder-ring handoff seat (advise).

### Default rosters (locked 2026-06-04 brainstorm; full detail in brainstorm memlog)
- **`/evaluate` panel (parallel):** Behavioral Coder (Gottman/FBA), Psycholinguist (Pennebaker/LIWC), Personality Profiler (Big Five, item-scores-first method), Relational Needs Analyst (attachment+NVC+TA) + optional 5th ADHD lens. Each seat's "ignores" column written into its prompt as a hard prohibition; every claim must cite transcript lines.
- **`/advise` panel (sequential):** Profile Translator (decoder ring, runs twice — subject + self) → Message Strategist ∥ Negotiation Architect ∥ Influence Tactician → Red Team → playbook synthesis. Optional Execution Realist consumes the self decoder ring. Guardrail: mutual-benefit influence only; bar = "comfortable if the subject read the playbook."

### Still open (brainstorm paused, resumable)
- **Session UX** — playbook/report formats partially explored (summary-top + receipts + don't-list; ride-along copilot dreamed, halftime report as realist candidate); quick vs. full mode defaults undecided.
- v1 scope line — figure out as we go.
