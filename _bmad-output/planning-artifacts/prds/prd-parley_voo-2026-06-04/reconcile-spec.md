# Reconciliation: parley-spec.md → PRD + Addendum

**Source:** `docs/parley-spec.md`
**Compared against:** `prd.md` + `addendum.md`
**Date:** 2026-06-04

Known intentional deltas excluded from this report: §4 proposed roster (superseded by addendum locked rosters), `parley confer` cut, sqlite-vec un-parked into V1, tech detail living in addendum.

---

## Gaps found (severity-ordered)

### HIGH — Qualitative intent silently dropped

**G1. "Their Chris ≠ your Chris" framing collapsed.**
Spec §7B frames import as: *"Their Chris ≠ your Chris; the system keeps the two reads distinct rather than blending them."* FR30 preserves the mechanical rule ("provenance tagging, keeps the imported read distinct, no blending") but loses the **conceptual stance** — that a profile is one person's *read*, and two reads of the same human are legitimately different artifacts, not a conflict to resolve. This is the philosophical spine of the whole import feature. The FR reduces it to a dedup constraint.

**G2. "Interpretation, not a fact" framing weakened.**
Spec §8 is emphatic and repeated: a behavioral profile is *"the person as you experienced them,"* a *"starting hypothesis, not a verdict,"* *"traits and patterns, attributed and provisional — not a dossier of private anecdotes about a named person."* The PRD keeps "starting hypothesis, not a verdict" (FR29) and "attributed, provisional, confidence-scored" (counter-metrics, FR21, NFR5) — but drops the explicit anti-dossier framing ("never a dossier of private anecdotes about a named person") as a stated design value. FR21 says "not dossiers" in passing; the *moral weight* the spec puts on it is gone.

**G3. README responsible-use note lost its specific content.**
Spec §8 prescribes what the README note must actually *say*: (a) this is a tool for improving **your own** communication, (b) profiles of real people handled with discretion, (c) named-profile sharing assumes a context where that's appropriate (mutual professional contacts), (d) Archetype as the default-safe public option. FR32 flattens all of this to "README includes a short responsible-use note." The required *substance* of the note is dropped — a downstream writer has no spec for its content.

### MEDIUM — Concrete requirements absent

**G4. Per-export sanitization choice ("chosen per export").**
Spec §7 says the two sanitization levels are *"chosen per export."* FR29 names Named (default) + Archetype (one flag) but doesn't state that the level is a **per-invocation choice** vs. a global config setting. Spec §12 Open Decision #2 reinforces "per-export override always available." Minor but load-bearing for the export command's UX.

**G5. Anecdote-generalization example/rule dropped.**
Spec §5 and §7A give the concrete transformation rule with an example: *"anecdotes generalized into traits ('tends to disengage when surprised in front of peers' — never 'shut down when you pitched X on Tuesday')."* FR29 says "anecdotes generalized to traits" but loses the worked example that defines what "generalized" actually means — the acceptance criterion a developer would test against.

**G6. Per-expert `memory` directories.**
Spec §5 ("Per-expert memory: each expert subagent gets a `memory` directory so it accumulates its own running notes across runs") and §11 Epic 2 ("Give each expert a `memory` directory"). This appears in `addendum.md` ("per-expert memory dirs") but is **absent from the PRD body** as a functional requirement. Since it's a per-expert accumulation mechanism (part of "sharpens over time"), it arguably belongs as an FR, not just a tech note. Borderline — covered in addendum, so flagged as low-medium.

**G7. Clone-and-use framework as a distinct first feature.**
Spec §7 explicitly splits sharing into **two distinct features**: (A) clone-and-use the whole framework, (B) share an individual profile. FR31 covers the public-template/gitignore mechanics, but the spec's framing of "fork it public without leaking" as feature A *paired against* feature B is flattened. The "forkers start clean; you stay private" intent survives (FR31 + Users), so this is mostly preserved — flagged for the lost pairing only.

### LOW — Minor framing / detail

**G8. `/council` "kept for free" rationale.**
Spec §2: *"`/council` is essentially the off-the-shelf behavior of the engine we're building on, kept for free."* PRD FR3 says "off-the-shelf engine" but drops the "kept for free / zero added cost" rationale that justifies why `/council` exists at all as a mode.

**G9. Quick-mode "default for routine use" reasoning.**
Spec §3: *"Multi-agent runs cost meaningfully more tokens, so quick mode should be the default for routine use."* The PRD has the rule (FR4, NFR2) but the *gut-check vs. high-stakes* usage framing ("a quick mode for gut-checks") is partly lost — FR4 keeps the mechanics, not the "gut-checks" intent.

**G10. "Same-model panels converge into one opinion" — the why.**
Spec §3 calls reasoning-method diversity *"the single most important thing to get right in the prompts."* FR18 keeps the rule and the MBTI/Enneagram bar, but drops the spec's stated **priority ranking** — that this is THE most important prompt-engineering risk. The emphasis that would guide a builder's attention is gone.

**G11. Self-profile "instincts vs. execution diverge" nuance.**
Spec §5/§6: the system tracks *"where your instincts and execution diverge."* FR20 keeps "own profile is first-class subject"; the Execution Realist (FR13) covers execution-under-pressure. But the specific *"instincts vs. execution divergence"* as a tracked profile dimension is only implicit. Mostly covered by FR13 — low severity.

---

## Confirmed preserved (no action)

- Two-layer profile model, storage-time split — FR19, NFR1. ✅
- SQLite spine, no server, deferred graph DB — FR/NFR4, addendum. ✅
- 3-stage protocol, dissent preservation, chairman-minority override — FR5, FR6. ✅
- Dual topology — FR7. ✅
- Locked rosters + "ignores" prohibition + citation rule — FR10–13. ✅
- Mutual-benefit guardrail, "comfortable if subject read the playbook" — FR14. ✅
- Persona management as first-class epic — FR16. ✅
- Feedback loop / advice scoring — FR27, FR28. ✅
- Zoom-primary, source-organized ingest, context metadata — FR22. ✅
- Council standalone + portable export/import — FR8, FR9. ✅

---

## Recommended actions

1. **Restore G1–G3 as explicit PRD content** (responsible-use section is under-specified for a public repo where the spec calls it a must-have). Highest leverage.
2. **G4–G5** — fold the "per-export" choice and the anecdote→trait worked example into FR29 as acceptance criteria.
3. **G6** — promote per-expert memory dirs to an FR if "sharpens over time" is a tracked goal.
4. **G8–G11** — optional; rationale/emphasis losses, recoverable downstream.
