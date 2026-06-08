# PRD Quality Review — Parley Voo

## Overall verdict

This is a genuinely strong PRD for its stakes: it has a real thesis (the moat is the data loop, experts reason from computed evidence a prompt can't fabricate), the negative-space design signature actually drives decisions rather than decorating them, and most FRs carry testable consequences. The most material risks are concentrated in **done-ness**: a handful of FRs lean on adjectives or undefined thresholds ("low" token cost, "what lands," "strongest reasoning," the Brier-score → "batting .71" leap) that downstream story creation will have to invent. Calibrated to a public-forkable hobby project, privacy and responsible-use rigor is appropriately full and largely holds; the one soft spot is that the zero-private-data acceptance check is asserted three times but never operationalized into a verifiable command.

## Decision-readiness — strong

Decisions are stated as decisions, not hedged. The cost-tier call (FR4, NFR2) commits to quick-mode default and names the exception (`/evaluate` always full) rather than balancing both. The graph-DB rejection (addendum §4, NFR4) names what was given up and the re-trigger condition ("only if joins get ugly"). FR7 makes an explicit competitive bet — "dual-topology capability is the differentiator versus parallel-only LLM-council clones" — and stakes the PRD on it instead of softening to neutral.

Trade-offs are surfaced honestly. The MBTI/Enneagram bar (FR18, "barred as scoring engines — no psychometric validity; acceptable only as translation layers") is a real opinion with a stated reason, not a both-sides shrug. The mutual-benefit guardrail (FR14) names the line and the test ("comfortable if the subject read the playbook") rather than gesturing at "ethical influence."

The two Open Questions are genuinely open and correctly routed (metadata schema → architecture; session UX → bmad-ux), not rhetorical. No `[NOTE FOR PM]` callouts appear, which at this stake level is acceptable — but see Scope honesty for the one tension that arguably warranted one.

## Substance over theater — strong

Very little furniture. The Users & Stakes section is two bullets and earns both: the secondary persona (forkers) is the *reason* FR15/FR29/FR31 exist (opt-in defaults, archetype export, gitignore), so it drives decisions rather than padding. ADHD-aware coaching is named as "load-bearing design input, not a nice-to-have" and is actually wired into FR13 (Execution Realist, RSD/over-explaining) and FR15 defaults — not theater.

The differentiation claim (FR7) is the rare earned one: it cites a specific lineage (Karpathy LLM Council + DMAD ICLR 2025, addendum) and names what the clones lack. The negative-space signature (Overview line 16) is restated operationally in FR11 ("ignores written into prompt as hard prohibition") and FR29 (export stripping) — a design thesis that recurs as concrete rules, not a slogan.

NFRs mostly avoid boilerplate: NFR1, NFR2, NFR4 carry product-specific mechanisms (storage-time separation, token-earning debate, single SQLite file). NFR6 (anti-sycophancy) is tied to the actual independence-first protocol in FR5. Only NFR3/NFR5 drift toward adjective territory — see Done-ness.

## Strategic coherence — strong

The thesis is explicit and load-bearing: "the moat is the data loop (scored advice outcomes + accumulated profiles); tech adopted only where it feeds that loop with evidence a prompt can't fabricate" (addendum, rationale anchor). Feature selection visibly follows from it — the computed-evidence block (FR23–FR26) exists *because* of the thesis, and the addendum shows the explicit adopt/park decision (graph DB rejected because it earns no new expert capability at solo scale). This is the opposite of a backlog with headings.

Goals & Signals are thesis-validating, not activity-counting: "advice quality visibly sharpens with use," "resist sycophancy — dissent survives synthesis." Counter-metrics are named and pointed (token cost stays low; profiles never harden into facts) — and they're real counterweights to the stated goals, not decoration. MVP scope kind reads as problem-solving/capability with phasing logic that matches (engine → panel → data → modes → loop → sharing).

One coherence note, not a finding: Goal 1's signal ("'what lands' knowledge and calibration scores improve over time") presumes enough advice→outcome cycles to move a Brier score, which for a solo user is a slow signal. That's inherent to the project, not a PRD defect — but it makes Goal 1 hard to observe in V1, which is worth the user knowing.

## Done-ness clarity — thin

This is the weakest dimension and where downstream story creation will feel friction. Several FRs carry adjectives or thresholds that aren't operationalized:

The privacy acceptance check — the strongest done-ness claim in the PRD — is asserted three times (Goal 3, FR31, NFR1) as "a clean fork has zero private data (verifiable acceptance check)" but is never turned into the actual verification. What command or test proves it? "`git ls-files` returns nothing under `people/`, `transcripts/`, `index.sqlite`" would make it testable; right now "verifiable" is asserted, not specified. For the PRD's highest-stakes guarantee, that gap is high-severity.

Other soft spots: "token cost per routine run stays **low**" (Goals, NFR2) — low relative to what? FR6/the engine leans on "**strongest** reasoning" and "may side with a minority whose reasoning is strongest" — strongest by what test the chairman applies? "what **lands**" (Goal 1, FR2 character read) is the core profile signal and never gets even a loose definition of how it's recorded or scored. FR25 makes a leap from "Brier scores ... computed from `advice_outcomes`" to the surfaced artifact "Red Team is batting .71" without stating the mapping (Brier is a 0–1 error score, not a batting average) — an engineer will have to invent the translation.

Strong counter-examples exist and should be the template for fixing the above: FR5 (three named stages, "A–E" labels), FR19 (split "at storage time," two named layers), FR29 (two named sanitization levels via one flag), FR12 (cite-or-discard) are all crisply done-defined.

### Findings
- **high** "Verifiable acceptance check" is asserted, never operationalized (§ Goal 3 / FR31 / NFR1) — the zero-private-data guarantee is the PRD's highest-stakes claim and "verifiable" appears three times with no command or test behind it. *Fix:* state the check, e.g. "Acceptance: `git ls-files` lists nothing under `people/`, `transcripts/`, or matching `index.sqlite`; CI or a pre-publish script asserts this."
- **medium** Brier-score → "batting .71" mapping unspecified (§ FR25) — a Brier score is a 0–1 calibration error, not a win rate; the surfaced artifact needs a defined derivation. *Fix:* state how the displayed figure is computed from `advice_outcomes` (hit rate vs. Brier vs. calibration), or label it "directional, not a literal Brier value."
- **medium** "Low" token cost has no referent (§ Goals counter-metric / NFR2) — "stays low" is the counter-metric guarding the cost thesis but is unmeasurable as written. *Fix:* give a loose bound or comparison (e.g. "quick mode ≤ ~1/3 the tokens of a full panel run").
- **low** "What lands" never loosely defined (§ Goal 1 / FR2 / FR19) — the central per-person signal carries the PRD's learning claim but has no stated recording mechanism. *Fix:* one line on where "what framing lands" is stored and how a win is recorded (likely already implied by FR28 past-win receipts — cross-link it).
- **low** "Strongest reasoning" is an adjective at the synthesis decision point (§ FR6) — the chairman's minority-siding rule turns on an undefined test. *Fix:* name the basis (e.g. "survives peer-review challenges + citation density"), or mark it an intentional judgment seat.

## Scope honesty — strong

Omissions are explicit and well-placed. The Scope & Phasing section does real work: V1 epics enumerated, Later/V2 named (ride-along copilot, Claude Project export, graph DB), and a Cut line that explains *why* (`parley confer` was a naming artifact, never a mode). The "halftime report needs no new machinery, it's V1 usage not a V2 feature" note pre-empts exactly the silent-scope-creep a reader might assume.

The four `[ASSUMPTION]` tags (FR1, FR22, §Scope, FR32) are on genuine inferences and correctly scoped to defer-to-architecture / defer-to-epics decisions — content is sound on all four (per calibration, not flagging their existence). Open-items density is low and appropriate for the stakes: 2 Open Questions + 4 assumptions + 0 NOTE-FOR-PM, on a hobby PRD that's explicitly not a green-light-to-build gate. No blocker.

One tension arguably deserved a callout rather than silence: FR15 sets ADHD Specialist and Execution Realist ON locally / OFF in the public template — a reasonable default, but it means the forkable artifact ships *without* the seats the Overview calls "load-bearing." That's a deliberate privacy-vs-capability trade and reads as decided, so it's not a defect — but a one-line `[NOTE FOR PM]` acknowledging "forkers get a less capable default; intentional" would close the loop. Low severity.

### Findings
- **low** Load-bearing seats default OFF in the public artifact without an explicit trade callout (§ FR15 vs. Overview/Users) — defensible and reads as decided, but the capability cost to forkers is left implicit. *Fix:* one `[NOTE FOR PM]` or inline note naming the trade.

## Downstream usability — adequate

This PRD is chain-top — it explicitly feeds bmad-ux (Open Q2) and epics planning (Scope), so traceability matters here. It mostly holds. FR IDs are contiguous and unique (FR1–FR32, no gaps or dupes). NFR1–NFR6 likewise. Cross-references resolve: FR1↔Scope (halftime report), FR13↔FR15 (Execution Realist default), FR25↔FR28 (calibration/receipts), addendum→FR23–26. Sections are largely self-contained and reference by term, not "see above."

The gap is the **absent Glossary**. Several domain nouns carry precise, load-bearing meaning and are used across many FRs — "subject layer" / "relationship layer," "decoder ring," "past-win receipts," "negative space," "halftime report," "quick mode / full mode," "topology" — but none is defined in one canonical place. Most are inferable from first use, so this isn't broken; but downstream extraction (a UX or story agent pulling FR19 alone) would benefit from a 6–8 term glossary, and it's the standard mechanism for preventing the drift noted below. For the stakes, medium not high.

There are no UJs to assess (single Core Loop paragraph, intentional per calibration) — correct for this shape; see Shape fit.

### Findings
- **medium** No Glossary despite load-bearing recurring domain nouns (§ whole PRD) — "subject/relationship layer," "decoder ring," "past-win receipts," "negative space," "halftime report," "topology" each carry precise meaning across multiple FRs with no canonical definition. *Fix:* add a 6–8 term glossary; it doubles as the anti-drift anchor for the terms in Mechanical notes.

## Shape fit — strong

The PRD is correctly shaped for a solo/hobby CLI capability spec. It does *not* force consumer-product UJ density — the single Core Loop paragraph is the right call for a single-operator tool and matches the rubric's guidance (internal/single-operator → capability-spec shape, UJs may be overhead). Success signals are appropriately operational ("clean fork has zero private data," "dissent survives synthesis") rather than user-funnel metrics that wouldn't apply.

CLI/Claude Code form factor is respected throughout — requirements are framed as commands (`/advise`, `/evaluate`, `/council`, `/export-profile`), file layout (`ingest/`, `people/`, `.gitignore`), and SKILL/agent mechanics (addendum), with no phantom GUI affordances. The forkable-repo dual nature is handled as a first-class shape concern (FR15, FR29, FR31, NFR5), which is exactly where a public hobby tool needs the rigor. Nothing is over-formalized and nothing consumer-grade is under-formalized. Appropriately rigor-light without dropping the substance bar.

## Mechanical notes

- **Glossary:** absent — see Downstream usability finding. Without it, watch these for drift (already minor): "quick mode" (FR4) vs. "quick mode default" (NFR2) vs. "routine run" (Goals counter-metric) appear to mean the same thing but aren't unified; "subject layer"/"subject-layer-only" (FR19/FR29) consistent; "relationship layer" consistent.
- **ID continuity:** FR1–FR32 and NFR1–NFR6 contiguous, unique, no gaps. Clean.
- **Assumptions roundtrip:** 4 inline `[ASSUMPTION]` tags (FR1, FR22, §Scope&Phasing, FR32). No dedicated Assumptions Index section — for a 2–3 page hobby PRD that's acceptable, but if an index is added at finalize, these four roundtrip cleanly.
- **Cross-refs:** all resolve. FR1→Scope, FR7 self-contained claim, FR13→FR15, FR25→FR28, addendum→FR23–26 all check out. No "see above" dangles.
- **Required sections:** Overview, Users & Stakes, Goals & Signals, Core Loop, FRs, NFRs, Scope & Phasing, Open Questions all present. Glossary and Assumptions Index are the only standard sections absent; only the Glossary is worth adding for this PRD.
