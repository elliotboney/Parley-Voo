# Reconciliation — Brainstorm Sources vs. PRD + Addendum

Date: 2026-06-04
Inputs: brainstorm-intent.md (SOURCE A), .memlog.md (SOURCE B)
Compared against: prd.md + addendum.md
Scope: silent drops only. Known intentional deltas excluded per instructions (ride-along/copilot deferral, halftime folded into FR1, quick-vs-full defaults, optional-seat defaults, rejected ideas Verbatim Witness / MBTI-engine / council-engine split).

---

## Method

Walked every DECISION, kept idea, guardrail, roster detail, and qualitative-intent line in both sources. For each, located its home in the PRD (FRs/NFRs/narrative) or addendum. Below are items present in a source but absent — or materially weakened — in both PRD and addendum, ordered by severity.

---

## Gaps found

### HIGH — Qualitative / intent drops the FR structure silently lost

**G1. "Comfortable if the subject *found out you used it*" — the manipulation bar was softened.**
- SOURCE A §2 + SOURCE B line 29: the mutual-benefit bar is "you'd be **comfortable if the subject found out you used it**" — i.e., comfortable knowing a *tactic* was deployed on them.
- PRD FR14 restates the bar as "comfortable if the subject **read the playbook**."
- These are not the same test. "Read the playbook" is a transparency-of-document test; "found out you used it" is a transparency-of-*intent/tactic* test, which is the stronger, manipulation-specific ethic the brainstorm actually chose. The harder ethical line was rounded off.
- Severity rationale: this is the project's named responsible-use guardrail; the wording carries the ethic.

**G2. Negative-space philosophy is stated but its third pillar ("exports defined by what's stripped") is never operationalized as intent.**
- SOURCE A §6 + SOURCE B line 44: negative space = (a) experts defined by what they ignore, (b) coaching defined by what not to do, (c) **exports defined by what is stripped**.
- PRD restates all three in the Overview narrative (good) — but the *export* pillar is only present mechanically (FR19/FR29 strip the relationship layer). The brainstorm framed stripping as a *signature design value*, not just a privacy mechanism. The PRD treats it purely as privacy (NFR1/NFR5). The philosophical framing — that what you withhold is the product's identity — survives for experts and coaching but is demoted to plumbing for exports.
- Severity rationale: this is the stated *signature* of the system; losing one-third of it as intent dilutes the through-line.

**G3. "Four independent footprints is what makes synthesis worth more than the parts" — the *why* behind orthogonality is dropped.**
- SOURCE A §1 + SOURCE B line 16: the rationale for the orthogonality table is that four *independent footprints* make the synthesis exceed the sum. FR11 enforces orthogonality as a runtime prohibition but drops the *reason* — independence-as-value-creation. The PRD's anti-sycophancy framing (NFR6) covers independence-against-pressure, but not independence-as-richer-synthesis. Different rationale, silently merged away.

### MEDIUM — Roster / pipeline specifics lost or blurred

**G4. Profile Translator's lineage as the *carryover of the Relational Needs Analyst facing forward* is dropped.**
- SOURCE A §2 + SOURCE B line 22: the Profile Translator is explicitly "carryover of the Relational Needs Analyst facing forward." FR13 names the Profile Translator but severs this lineage. This is a load-bearing design link (the most-actionable `/evaluate` seat becomes the first `/advise` seat) — it tells implementers these are the same lens in two orientations, not two unrelated seats.

**G5. Negotiation Architect's "four levers + BATNA" and the reframe of "win them over" → "find overlap where their yes is in their interest" is dropped.**
- SOURCE A §2 + SOURCE B line 24: Negotiation Architect = Fisher & Ury, "positions vs interests, **four levers + BATNA**," and the explicit reframe "win Chris over" → "find overlap where his yes is in his interest." PRD FR13 lists the seat by name + framework only (addendum line 21 lists "Fisher & Ury" as a grounding framework). The substantive method (BATNA, the reframe that defines the seat's job) is absent. Same shallowing applies to Influence Tactician's concrete moves (mirroring, labeling, calibrated questions) — present in SOURCE A §2 / SOURCE B line 25, reduced to "Voss/Cialdini" name-drop in the addendum.

**G6. Influence Tactician "needs a leash" framing → the leash exists (FR14) but the seat's flagged-as-dangerous character is lost.**
- SOURCE A §2 + SOURCE B line 25: the Tactician is repeatedly flagged as the seat that "needs a leash." FR14 supplies the leash mechanism but the PRD never marks this seat as the one requiring active policing — it reads as one neutral seat among equals. The intent (this seat is the manipulation risk; the Red Team's policing job exists *because of it*) is implicit at best.

### MEDIUM — Feedback-loop / data intent

**G7. Red Team courtside "that's the one we called, run play 2" — deferred with ride-along, but the *play-numbered playbook* idea is orphaned.**
- SOURCE B lines 28, 37: the playbook synthesis output is structured enough to have *numbered plays* ("run play 2 from the playbook"). The ride-along is correctly deferred (known delta), but the implication that the V1 playbook should have addressable/numbered objection-responses is a near-term structural detail that didn't have to defer with it. PRD FR2 lists "objections + responses" as flat, not addressable. Low-cost V1 affordance that fell out with the V2 feature.

### LOW — Minor specifics

**G8. RSD named explicitly as the trigger condition for the don't-list, not just over-explaining.**
- SOURCE A §5 + SOURCE B lines 38–39: the don't-list / negative-space coaching fires specifically "mid-conversation, **RSD spiking**." PRD FR13/Users section names RSD and over-explaining as design inputs generally, but does not tie the don't-list's *activation* to the RSD-spike moment. Minor, but it's the concrete behavioral trigger the user cares about.

**G9. "What's worked before" as *literally a SQL query over `advice_outcomes`* is preserved (FR26/FR28) — NOT a gap.** Logged here to show it was checked.

**G10. Two-topology "only surfaced by designing the consumer first."**
- SOURCE B line 46: the insight that the dual-topology differentiator was *only discoverable by designing the consumer (coach) before the engine* is a process/strategy note. FR7 captures the differentiator but not this design-sequence lesson. Arguably belongs in addendum rationale, not PRD. Flagged as lowest-severity / optional.

---

## Confirmed-present (checked, not gaps)

- Orthogonality table contents, all four core seats + ADHD optional: FR10. ✓
- Citation rule: FR12. ✓
- Sequential `/advise` pipeline shape: FR13. ✓
- Profile Translator runs twice (subject + self): FR13. ✓
- Execution Realist consumes ring #2 / "best plan you won't execute is worthless": FR13. ✓
- Red Team batting average / per-person calibration: FR25. ✓
- "His fallacies" as profile field: FR21. ✓
- Profile-as-falsifiable-model: FR21. ✓
- One-project / standalone capability / portable export: FR8, FR9. ✓
- Playbook top section contents: FR2. ✓
- Negative-space (experts + coaching pillars): Overview narrative. ✓

---

## Recommendation summary

Fix-worthy now: **G1** (restore the stronger manipulation bar wording in FR14), **G4** (restore Translator↔Needs-Analyst lineage in FR13), **G5** (restore BATNA + the "find overlap" reframe and the Tactician's concrete moves — either FR13 or addendum). G2/G3 are intent-preservation edits to the Overview/NFR rationale. G6–G10 are optional polish.
