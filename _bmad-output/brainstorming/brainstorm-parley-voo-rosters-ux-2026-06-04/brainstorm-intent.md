# Parley Voo — Brainstorm Intent (Rosters + UX)

Date: 2026-06-04
Purpose: Token-lean input for the downstream PRD workflow. Chosen and critical discoveries only.

Product context: Claude Code based communication coach. Councils of expert personas evaluate conversation transcripts (`/evaluate`) and advise on upcoming conversations (`/advise`), backed by stored person profiles.

---

## 1. `/evaluate` Panel Roster (DECISION)

Parallel panel. Each seat reads one layer and explicitly ignores the others. Four independent footprints make the synthesis worth more than the parts.

| Seat | Grounding discipline | Reasoning lens (looks at) | Ignores |
|---|---|---|---|
| Behavioral Coder | Gottman coding + functional behavior analysis | Observable interaction moves and sequences: bids, turning toward/away/against, repair attempts, escalation | Intent / inner state |
| Psycholinguist | Pennebaker / LIWC | Style not content: pronoun ratios, hedging, language-style matching; status/power, deception markers, who accommodates whom | Content / overt actions |
| Personality Profiler | Big Five / OCEAN only | Traits, scored via BFI-style inventory items first, then computed; carries explicit confidence (r=.22–.44) so the profile stays a hypothesis | Moment-to-moment behavior and drivers |
| Relational Needs Analyst | Attachment + NVC + Transactional Analysis | Unmet need / perceived threat driving surface behavior (most actionable seat for `/advise`) | Surface actions, style, traits |
| ADHD Specialist (optional 5th lens) | — | ADHD-specific read | — |

Roster decisions:
- **ADHD Specialist** is an OPTIONAL fifth lens, not a core seat (footprint overlaps the Needs Analyst).
- **No MBTI/Enneagram** as a primary scoring engine (no psychometric validity); acceptable only as translation layers.

Runtime rules (DECISION):
- **Orthogonality enforced at runtime:** each seat's "Ignores" is written into its prompt as a hard prohibition.
- **Citation rule:** every expert claim must cite transcript line numbers, or the chairman discards it.

---

## 2. `/advise` Panel (DECISION)

Sequential topology (not all-parallel). The Profile Translator must run first so the others receive a decoder ring instead of giving generic advice.

Pipeline:

```
Profile Translator (runs twice: subject ring + self ring)
  -> Message Strategist || Negotiation Architect || Influence Tactician
  -> Red Team
  -> playbook synthesis
Execution Realist  (consumes the self decoder ring, ring #2)
```

Seats:
- **Profile Translator** — carryover of the Relational Needs Analyst facing forward. Reads the stored profile; outputs a decoder ring: values, fears, how they decide, what framing lands, what triggers a "no." Runs twice: once for the subject, once for the user (self).
- **Message Strategist** — Crucial Conversations + Heath brothers. Craft of the message only: wording, structure, sequence, channel, timing. Produces an actual draft + delivery plan.
- **Negotiation Architect** — Fisher & Ury. Positions vs interests, four levers + BATNA; reframes "win them over" into "find overlap where their yes is in their interest."
- **Influence Tactician** — Voss tactical empathy + Cialdini 7 principles. Real-time moves: mirroring, labeling, calibrated questions. Needs a leash (see guardrail).
- **Red Team** — steelmans the no, pre-mortem, fallback plan; also polices the Tactician on the persuasion-vs-manipulation line.
- **Execution Realist** — consumes the self decoder ring (ring #2). Will the USER actually run this under pressure (RSD, over-explaining)? The best plan you won't execute is worthless.

Output — **playbook synthesis:** frame, opening line, sequence, objections + responses, fallback.

**Mutual-benefit guardrail (DECISION):** the Influence Tactician's standing instruction is mutual-benefit only. The Red Team flags anything that only works if the subject doesn't notice. Bar: you'd be comfortable if the subject found out you used it.

---

## 3. Engine Decisions (DECISION)

- **ONE project.** A considered split (decouple the council engine into a standalone project, Parley Voo as consumer) was raised and then revised/superseded. Council creation stays inside Parley Voo.
- **Council creation is a standalone-usable capability:** create councils independently of the coach pipeline.
- **Portable export:** export councils/personas in a portable format other LLMs can consume; also import/export existing councils from a user's project.
- **Two-topology engine requirement:** the engine must support both parallel (`/evaluate`) and sequential decoder-ring (`/advise`) topologies. This is the differentiator vs parallel-only LLM-council clones.

---

## 4. Feedback-Loop Extensions (DECISION)

- **Red Team batting average:** score whether each pre-mortem predicted the actual failure mode; keep a per-person calibration record.
- **"What's worked before" receipts:** a SQL query over `advice_outcomes` rendering past wins as dated receipts.
- **"His fallacies"** as a profile field.
- **Profile-as-falsifiable-model:** combining fallacies + Profiler confidence intervals + Red Team batting average, the profile is a falsifiable scored model (every claim carries confidence + a track record), not a static dossier.

---

## 5. Session UX Findings (PARTIAL — OPEN)

Direction is seeded but not locked. Treat as open for the PRD to resolve.

- **Playbook top section:** quick plan summary + character read (traits found) + past-win receipts (ways the user has convinced them before) + fallacies to avoid.
- **Don't-list / negative-space coaching:** inverted coaching keyed to the user's own profile, e.g. "do not over-explain: one sentence, then stop talking" (the Execution Realist's live job).
- **Ride-along copilot** = dream target (live real-time coaching during the conversation; surfaces contradicting history; Red Team courtside; tells the user what NOT to do mid-conversation when RSD spikes).
- **Halftime report** = the realistic near-term seed: `/evaluate` run mid-conversation. Needs zero new machinery.
- **OPEN:** quick-vs-full mode defaults are UNDECIDED.

---

## 6. Design Philosophy — "Negative Space" (DECISION)

The system's signature is what it leaves out:
- Experts are defined by what they **ignore**.
- Coaching is defined by what **not to do**.
- Exports are defined by what is **stripped**.
