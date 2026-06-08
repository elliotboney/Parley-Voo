---
stepsCompleted: ['headless-domain-research']
inputDocuments:
  - '_bmad-output/planning-artifacts/prds/prd-parley_voo-2026-06-04/prd.md'
  - '_bmad-output/planning-artifacts/prds/prd-parley_voo-2026-06-04/addendum.md'
workflowType: 'research'
research_type: 'domain'
research_topic: 'Psychological & strategic reasoning methods grounding Parley Voo persona seats'
research_goals: 'Produce practitioner-grade per-seat briefs to feed persona-prompt authoring (FR18) and the negative-space "Ignores:" line (FR11), with falsifiability-first validity framing.'
user_name: 'Elliot'
date: '2026-06-05'
web_research_enabled: true
source_verification: true
mode: 'headless'
---

# Research Report: Persona-Seat Reasoning Methods (Practitioner Briefs)

**Date:** 2026-06-05
**Author:** Elliot
**Research Type:** domain (psychological / strategic methods)
**Run mode:** headless — no user interaction; reasonable defaults used; assumptions tagged `[ASSUMPTION]`.

---

## Research Overview

This report supplies, for each of Parley Voo's ten persona seats, a practitioner-grade brief on the named reasoning method that grounds it (FR18). Each brief follows a fixed four-part shape so it can be lifted directly into persona-prompt authoring:

- **(a) Core constructs + application** — what the method actually computes/looks for in conversation or strategy.
- **(b) Blind spots / what it ignores** — the raw material for the seat's hard-prohibition `Ignores:` line (FR11).
- **(c) Validity status + main criticisms** — Parley Voo is falsifiability-first; overclaiming is a design violation (FR21, NFR5). This section is the highest-stakes part of each brief.
- **(d) Canonical sources** — 2–3 anchors.

**Headless conventions applied.** The skill's standard industry-research steps (competitive landscape / regulatory / technical-trends) do not fit a methods brief; I followed the skill's output conventions (research-template frontmatter, `research/` location, web-verification + citation discipline) and substituted the seat-brief structure the task specifies. No `project-context.md` existed to load as persistent facts. Output path follows the task's explicit fallback path.

**A cross-cutting design note.** Almost every method below is *more valid as a descriptive/associative lens than as a predictive engine*. The recurring failure mode in the literature is the same one Parley Voo's design guards against: a sound effect-size finding ("X correlates with Y") gets marketed as forecasting ("X predicts Y with N% accuracy"). Persona prompts should be authored to state attributed, confidence-scored *interpretations*, never verdicts — which is exactly what FR21 already requires. Where a seat's method-pairing in the PRD looks weak or misattributed, it is flagged inline and collected in the closing summary.

---

## Seat 1 — Behavioral Coder (Gottman-style interaction coding + Functional Behavior Analysis)

**(a) Core constructs + application.** Two complementary observation systems. *Gottman-style coding* tags moment-to-moment interaction for corrosive patterns — the "Four Horsemen": criticism (attacking character vs. a behavior), contempt (disgust/superiority: sarcasm, eye-roll, mockery), defensiveness (deflecting responsibility), and stonewalling (withdrawal) — plus repair attempts and the balance of positive-to-negative exchanges. *Functional Behavior Analysis (FBA)* is the ABC frame: Antecedent → Behavior → Consequence, asking what *function* a behavior serves (escape, attention, access, sensory) rather than what it "means." Applied to a transcript: locate concrete behavioral units, code each against the Horsemen, and read each behavior functionally — "stonewalling here follows being interrupted twice; function = escape from escalation."

**(b) Blind spots / ignores.** Ignores internal/dispositional explanation (personality, motives, "what kind of person they are") — FBA is deliberately function-over-trait. Ignores the *content/meaning* of language beyond its behavioral effect. Ignores attachment history and unspoken relational needs. Ignores word-level linguistic features (that is the Psycholinguist's footprint). The Behavioral Coder reports observable behavior + antecedent/consequence only.

**(c) Validity status + criticisms.** The four behaviors are robustly *associated* with relationship distress and dissolution — that part holds. The famous "predict divorce with 90%+ from a 15-minute argument" claim is **overstated** and is a textbook case of the failure mode Parley Voo bans: Heyman & Slep (2001) showed the original equations were post-hoc model *fitting* (reconstruction, not prediction) on small extreme-group samples (n≈60) with no cross-validation; under proper cross-validation and realistic base rates, positive predictive value collapsed to ~43%. Statistician Andrew Gelman's verdict: the published variance-explained work is fine; the word "predict" and the marketing around it are not. FBA is methodologically sound but is a single-case functional framework — it does not license population-level claims. **Authoring guardrail:** this seat must say "contempt is present and is the strongest distress signal here," never "this relationship will fail."

**(d) Sources.** Heyman, R. & Slep, A. (2001), *The Hazards of Predicting Divorce Without Crossvalidation*, J. Marriage & Family (PMC1622921); Gottman & Levenson (1992/2000) prospective studies (and the Gottman Institute's replication FAQ, read critically); Cooper, Heron & Heward, *Applied Behavior Analysis* (FBA/ABC canonical text).

---

## Seat 2 — Psycholinguist (LIWC-category interpretation of language features)

**(a) Core constructs + application.** LIWC (Linguistic Inquiry and Word Count, Pennebaker) counts words into psychologically meaningful categories. The load-bearing finding is that *function words* (pronouns, articles, prepositions, auxiliaries) — not content words — carry the psychological signal: pronoun ratios (I/we/you), hedging and tentativeness density, cognitive-process and emotion-word rates, and *language style matching* (LSM, convergence of function-word use between speakers as an index of rapport/engagement). In Parley Voo the metrics are *computed deterministically by a script* (FR23) and handed to the seat as hard numbers; the seat interprets, it does not eyeball. Practitioner read: "Subject's I-word rate drops and you-word rate rises during the objection — distancing/accusatory shift; LSM falls 0.2 — rapport breaking."

**(b) Blind spots / ignores.** Ignores meaning, intent, sarcasm, and context — it counts forms, not semantics. Ignores behavior sequences (Behavioral Coder's footprint) and stable personality (Profiler's). Ignores anything below sufficient word count (short turns are unreliable — low base rates). Reports only quantified language features.

**(c) Validity status + criticisms.** Mixed, and the developers themselves are candid. Effect sizes are *modest*; validation rests largely on judge-rating correlations that are strong for emotion categories but uneven elsewhere. Function-word categories have low base rates and non-normal distributions, so standard reliability metrics (Cronbach's alpha) don't apply cleanly — short or single utterances are especially weak. A 2025 forensic-context review flagged *circular justification* (LIWC cited as valid because widely used) and the core reliability-vs-validity tension: fast and reliable word-counting can sacrifice nuanced, contextual validity. Notably, LIWC's authors argue low correlation with self-reports is *expected* rather than disconfirming — critics call this hard-to-falsify framing. **Authoring guardrail:** treat LIWC numbers as weak-to-moderate signal requiring corroboration, never as a lie-detector or mind-reader; respect a minimum-token floor.

**(d) Sources.** Tausczik & Pennebaker (2010), *The Psychological Meaning of Words: LIWC and Computerized Text Analysis Methods*; *LIWC-22 Development and Psychometrics Manual* (liwc.app); the 2025 forensic/security critical review (ScienceDirect S2666799125000012).

---

## Seat 3 — Personality Profiler (Big Five / BFI, item-scores-first)

**(a) Core constructs + application.** The Five-Factor Model: Openness, Conscientiousness, Extraversion, Agreeableness, Neuroticism — traits on continua, not types. Parley Voo scores the BFI items as deterministic math (FR24) and feeds the seat *item-level evidence with confidence ranges*, not a vibe. Practitioner read: "Transcript evidence supports high Neuroticism (defensive under mild challenge, catastrophizing language) and low-ish Agreeableness; Conscientiousness indeterminate — insufficient evidence." Application to strategy: tailor framing to trait profile (e.g., high-Conscientiousness people respond to structured, risk-bounded plans).

**(b) Blind spots / ignores.** Ignores type systems entirely — the PRD bars MBTI/Enneagram as engines (FR18) and this seat must not smuggle them in. Ignores state/situation (it models stable dispositions, not "having a bad day"), relational dynamics, and moment-level behavior. Ignores language mechanics. Reports trait estimates with confidence only.

**(c) Validity status + criticisms.** The Big Five is the academic gold standard: strong test-retest reliability (~0.75–0.85 over 6+ months), self-peer convergence, heritability, and predictive validity for job performance, relationship satisfaction, health, and longevity. Its main limits: trait scores predict aggregate tendencies, not single acts; cross-cultural factor structure is mostly-but-not-perfectly invariant; and trait inference from a *transcript* (vs. a completed BFI) is itself an extrapolation that should carry wide confidence bands. The contrast that justifies the PRD's ban: MBTI shows 39–76% category flips on retest within weeks and lacks predictive validity (its own manual forbids selection use). **Authoring guardrail:** confidence ranges are mandatory (FR21); "evidence is consistent with high X" not "they are an X."

**(d) Sources.** John, Naumann & Soto (2008), *Paradigm Shift to the Integrative Big Five Trait Taxonomy* (BFI canonical); McCrae & Costa, *Personality in Adulthood* / NEO-PI-R; for the MBTI contrast, Pittenger (1993/2005) critiques and Costa & McCrae's MBTI–NEO convergence data.

---

## Seat 4 — Relational Needs Analyst (attachment theory + NVC + Transactional Analysis)

**(a) Core constructs + application.** Three lenses on unmet relational need. *Attachment* — secure / anxious / avoidant / disorganized working models; read bids for connection, protest behavior, deactivation (withdrawal) vs. hyperactivation (pursuit). *NVC (Nonviolent Communication, Rosenberg)* — Observation / Feeling / Need / Request; decode complaints into underlying universal needs ("you never listen" → need for being-heard). *TA (Transactional Analysis, Berne)* — Parent/Adult/Child ego states and crossed transactions; spot when a Parent-to-Child put-down provokes a Child reaction. Practitioner read: "Avoidant deactivation under pressure; the unmet need beneath the sarcasm is autonomy; the exchange is Critical-Parent → rebellious-Child — get it to Adult-Adult."

**(b) Blind spots / ignores.** Ignores observable behavior-as-such and antecedent/consequence (Behavioral Coder). Ignores trait personality (Profiler) and word-count metrics (Psycholinguist). Ignores tactics, leverage, and persuasion — this seat is about needs, not influence. Reports relational needs, attachment dynamics, and ego-state transactions only.

**(c) Validity status + criticisms.** Uneven across the three. *Attachment* has a real research base but two weakly-converging measurement traditions — the Adult Attachment Interview vs. self-report styles correlate only r≈.09; categories are less valid than dimensions; and critics warn against over-determinism (early childhood) and cultural bias in what counts as "secure." *NVC* is a clinically useful communication framework with thin controlled-outcome evidence — treat as heuristic, not validated mechanism. *TA* is largely a clinical/heuristic model with limited modern psychometric support. **Authoring guardrail:** this is the seat most prone to confident over-interpretation; force tentative, dimensional language ("leans avoidant on this evidence") and forbid diagnostic certainty. `[ASSUMPTION]` the PRD intends these as interpretive lenses, not validated instruments — consistent with FR18's "translation layer" allowance.

**(d) Sources.** Mikulincer & Shaver, *Attachment in Adulthood* (2nd ed.); Roisman et al. / Bartholomew & Shaver on AAI vs. self-report convergence (r≈.09); Rosenberg, *Nonviolent Communication*; Berne, *Games People Play* (TA).

---

## Seat 5 — ADHD Specialist (ADHD communication patterns, RSD, over-explaining)

**(a) Core constructs + application.** ADHD-linked conversational patterns: emotional dysregulation, time-blindness, interruption/blurting, working-memory drop-out mid-thread, over-explaining/justifying, and *Rejection Sensitive Dysphoria (RSD)* — fast-onset, intense pain from perceived rejection/criticism. Applied as the optional fifth `/evaluate` lens and (via the self decoder ring) to coach the user's own patterns — negative-space "don't" coaching: spot where over-explaining undercuts a request, or where an RSD spike will misread neutral feedback as rejection.

**(b) Blind spots / ignores.** Ignores everything not plausibly ADHD-linked — it must not pathologize ordinary conflict or relabel others' behavior as ADHD. Ignores trait personality, attachment, and tactics. Crucially, ignores *diagnosis* — it describes patterns, never diagnoses anyone. Reports ADHD-pattern hypotheses only, flagged as such.

**(c) Validity status + criticisms.** ADHD itself is a well-established DSM-5 diagnosis with strong evidence; emotional dysregulation is a recognized associated feature (a core feature in EU criteria). **RSD, however, is not in the DSM-5, has no validated measure, and rests on a handful of small qualitative studies** plus clinical observation (term coined by Dodson, 1990s). It overlaps heavily with the better-validated transdiagnostic constructs *rejection sensitivity* (Downey & Feldman) and *emotion dysregulation*, and its etiology is disputed (innate-ADHD claim vs. trauma-linked rejection-sensitivity evidence). For a falsifiability-first product this is the **single weakest-evidenced construct in the roster.** **Authoring guardrail:** frame RSD as a *useful experiential label, not a validated diagnosis*; prefer "rejection-sensitivity pattern" phrasing; this seat coaches the *user's own self-model* by design and should avoid attributing RSD to others. `[ASSUMPTION]` ADHD-aware self-coaching is load-bearing per PRD Users & Stakes — keep the seat, downgrade RSD's epistemic status in-prompt.

**(d) Sources.** Barkley, *ADHD and the Nature of Self-Control* / Barkley on emotional dysregulation in ADHD; Downey & Feldman (1996), *Rejection Sensitivity* (the validated parent construct); Bedford et al. (2024 preprint, PMC12822938) qualitative RS-in-ADHD study (illustrates how thin the RSD-specific base is).

---

## Seat 6 — Message Strategist (framing / message design — framing effects, inoculation theory)

**(a) Core constructs + application.** How *form* changes reception independent of content. *Framing effects / prospect theory (Kahneman & Tversky)* — gain vs. loss framing shifts risk preference (gain frames → risk-averse choices; loss frames → risk-seeking). *Inoculation theory (McGuire)* — pre-empt the counter-argument with a weakened dose plus refutation to build resistance ("you'll hear that this is too expensive; here's why that's the wrong frame"). Applied: choose gain vs. loss frame to the goal, pre-bunk the strongest objection, design the message order.

**(b) Blind spots / ignores.** Ignores the relationship and the person's needs/personality — it optimizes the *message*, not the bond. Ignores behavioral coding and linguistics. Ignores negotiation leverage and reciprocity tactics (adjacent seats). Reports framing/structure recommendations only.

**(c) Validity status + criticisms.** Both effects replicate well at the aggregate level. Prospect-theory choice patterns replicated in a 19-country, n≈4,098 study (94% of items). Inoculation is meta-analytically superior to supportive and no-message controls (Banas & Rains 2010) and powers modern "prebunking." But two real cautions: (1) *framing effects specifically* are more context- and affect-dependent than the headline implies (Kühberger's meta-analysis found them not robust across all settings); (2) replication of the *pattern* doesn't validate the *mechanism* — for inoculation the predicted mediating role of threat was not supported, and inoculation decays after ~2 weeks. **Authoring guardrail:** recommend framing as a probabilistic lever ("loss framing tends to push toward action here"), not a guaranteed switch; note recency/decay for inoculation.

**(d) Sources.** Tversky & Kahneman (1981), *The Framing of Decisions*; Ruggeri et al. (2020, *Nature Human Behaviour*) multinational prospect-theory replication; Banas & Rains (2010), *A Meta-Analysis of Research on Inoculation Theory*, Communication Monographs.

---

## Seat 7 — Negotiation Architect (principled negotiation — Fisher/Ury — + tactical empathy — Voss)

**(a) Core constructs + application.** *Principled negotiation (Fisher & Ury, "Getting to Yes")* — separate people from problem; focus on interests not positions; invent options for mutual gain; insist on objective criteria; know your BATNA (best alternative to a negotiated agreement). *Tactical empathy (Voss, "Never Split the Difference")* — labeling ("it sounds like…"), calibrated open questions ("how am I supposed to do that?"), mirroring, and accusation audits to lower defenses and surface the real constraint. Applied: map interests and BATNA, then use labels/calibrated questions to get the counterpart talking and to expose hidden interests before proposing options against objective criteria.

**(b) Blind spots / ignores.** Ignores stable personality and clinical/relational diagnosis. Ignores linguistic metrics and behavioral coding. Ignores covert/one-sided influence (that boundary is the Influence Tactician's, under a tighter ethics rule). Reports interests, BATNA, and tactical-empathy moves only.

**(c) Validity status + criticisms.** *Getting to Yes* is a widely-taught practitioner framework, not an experimentally-derived theory; interest-based bargaining has reasonable empirical support but is not a law, and critics (e.g., negotiation scholars) note it can underweight hard distributive/power situations. *Voss's tactical empathy* is practitioner wisdom from FBI hostage work; labeling and calibrated questions draw on real psychology (affect labeling has neuroscience support) but the packaged system lacks controlled-trial validation. **Authoring guardrail:** present both as battle-tested heuristics with mechanism-level support for some components, not as validated predictive models. This pairing is coherent and well-matched to the seat.

**(d) Sources.** Fisher, Ury & Patton, *Getting to Yes* (2nd ed.); Voss & Raz, *Never Split the Difference*; Lieberman et al. (2007) on affect labeling (mechanism support for "labeling").

---

## Seat 8 — Influence Tactician (Cialdini principles, mutual-benefit-only)

**(a) Core constructs + application.** Cialdini's principles: reciprocity, commitment/consistency, social proof, authority, liking, scarcity, unity. Applied under Parley Voo's hard ethical constraint (FR14): only mutual-benefit moves; the bar is "you'd be comfortable if the subject found out you used it." So: surface genuine social proof, make a real reciprocal concession, cite legitimate authority/evidence — never manufactured scarcity or false consensus. Practitioner read: "Reciprocity is the lever here — lead with a concrete concession that actually costs you something."

**(b) Blind spots / ignores.** Ignores the relationship's emotional/attachment layer and the person's needs. Ignores anything that only works if the target doesn't notice (Red Team will flag it; the seat must self-censor it first). Ignores linguistics and behavioral coding. Reports ethically-bounded influence levers only.

**(c) Validity status + criticisms.** Two tiers of evidence. *Social proof* (Bond 2005 meta-analysis, d≈0.89; Asch replications hold) and *authority* (Milgram syntheses, Burger 2009 replication) are strongly supported. *Scarcity* replicates but with consistently *smaller, context-dependent* effects (Barton et al. 2022, 416 effect sizes — modest). Reciprocity shows large effects in some studies. The principle most prone to overclaiming is scarcity; and the whole framework is easy to slide from influence into manipulation — which is precisely why the PRD wraps it in a mutual-benefit guardrail and a Red Team check. **Authoring guardrail:** weight recommendations by tier (lead with social-proof/authority/reciprocity; treat scarcity as weak); every move must pass the "comfortable if discovered" test in-prompt.

**(d) Sources.** Cialdini, *Influence: The Psychology of Persuasion* (and *Pre-Suasion*); Bond (2005) meta-analysis of conformity (d≈0.89); Barton et al. (2022) scarcity meta-analysis.

---

## Seat 9 — Red Team (adversarial decision critique — pre-mortem, devil's advocacy)

**(a) Core constructs + application.** Structured dissent. *Pre-mortem (Klein)* — assume the plan has already failed, then generate reasons; the forced certainty-of-failure removes "how likely is it" quibbling and recruits *prospective hindsight*. *Devil's advocacy* — assign someone to argue the opposing case. In Parley Voo the Red Team also polices the mutual-benefit guardrail (flags any tactic that only works covertly, FR14) and carries a *calibration track record* (Brier score / "batting .71 on this person," FR25) — so its dissent is itself falsifiable. Application: take the synthesized playbook, run a pre-mortem on it, surface the objection nobody raised.

**(b) Blind spots / ignores.** Ignores building the plan — it only attacks. Ignores rapport and relational warmth (other seats own that). Its job is to find the failure mode, the covert tactic, and the optimistic assumption. Reports critiques, failure modes, and ethics flags only.

**(c) Validity status + criticisms.** The strongest *process* evidence in the roster, though modest in scope. Prospective hindsight (Mitchell, Russo & Pennington 1989, "Back to the Future") increased the number of plausible reasons generated by ~30% — but that measured *reasons generated*, not real-world outcome improvement. The pre-mortem's main direct test (Veinott, Klein et al. 2010) targeted plan *confidence* (reducing overconfidence), not success rates. Independence is the active ingredient — silent individual generation before sharing — and the known failure mode is running it with senior people present (collapses candor). For Parley Voo this dovetails with the anti-sycophancy protocol (FR5/NFR6) and is well-matched. **Authoring guardrail:** frame pre-mortem as a debiasing *process* (surfaces privately-held doubts, reduces overconfidence), not a quantified risk-forecasting tool.

**(d) Sources.** Klein (2007), *Performing a Project Premortem*, HBR; Mitchell, Russo & Pennington (1989), prospective hindsight; Veinott, Klein & Wiggins (2010), *Evaluating the Effectiveness of the PreMortem Technique on Plan Confidence*.

---

## Seat 10 — Execution Realist (implementation intentions, behavior under pressure, ADHD-aware execution)

**(a) Core constructs + application.** *Implementation intentions (Gollwitzer)* — convert a goal into an "if-[situation]-then-[action]" plan that pre-loads the response and offloads it from in-the-moment willpower ("IF Chris pushes back on cost, THEN I say the one prepared line and stop"). Combined with behavior-under-pressure realism and ADHD-aware constraints (consumes the *self* decoder ring, FR13): does the user actually have the working memory / regulation to run this plan when an RSD spike or over-explaining urge hits? Negative-space "don't" coaching: strip the plan to the one move the user can actually execute under stress.

**(b) Blind spots / ignores.** Ignores *whether the plan is strategically right* (other seats own that) — it only asks "will the human execute it under pressure." Ignores the subject's personality and the relationship. Ignores message framing. Reports executability, if-then plans, and failure-under-pressure risks only.

**(c) Validity status + criticisms.** Implementation intentions are among the **best-validated** constructs here: Gollwitzer & Sheeran's (2006) meta-analysis across 94 studies found a medium-to-large effect (d≈0.65) on goal attainment over goal intentions alone, with replications across domains. Caveats: effects are weaker for difficult/aversive goals and can fade; they help *initiation* more than sustained complex performance. The ADHD-execution layer inherits the same RSD evidence weakness flagged in Seat 5 — keep the if-then planning (strong), hold the RSD framing loosely. **Authoring guardrail:** recommend one or two if-then plans (not a long list — that defeats the working-memory point), and frame ADHD-execution risk as a self-model hypothesis. Method-pairing is strong; the only soft spot is the shared RSD reliance.

**(d) Sources.** Gollwitzer (1999), *Implementation Intentions: Strong Effects of Simple Plans*, American Psychologist; Gollwitzer & Sheeran (2006), meta-analysis (d≈0.65), Advances in Experimental Social Psychology; Barkley on ADHD executive function (for the under-pressure layer).

---

## Cross-Seat Orthogonality Matrix

FR11 requires four (or more) genuinely independent footprints. The table lists pairs that *could* bleed and the boundary that keeps them orthogonal. Authoring the `Ignores:` lines from the **right-hand boundary** is what earns the synthesis its value.

| Seat pair | Where they could overlap | The boundary (write into `Ignores:`) |
|---|---|---|
| Behavioral Coder ↔ Psycholinguist | both read the transcript surface | Coder = behavior units + antecedent/consequence (ABC, Horsemen); Psycholinguist = word-count metrics only. Coder ignores word features; Psycholinguist ignores behavior sequences. |
| Behavioral Coder ↔ Relational Needs | both interpret conflict moments | Coder = function of behavior (escape/attention), trait-blind; Relational = the *unmet need* and ego-state behind it. Coder ignores meaning/needs; Relational ignores ABC/observable-only. |
| Psycholinguist ↔ Profiler | language as evidence of disposition | Psycholinguist = state-level language features now; Profiler = stable trait estimates with confidence ranges. Psycholinguist ignores personality; Profiler ignores word-count metrics. |
| Profiler ↔ Relational Needs | both make person-level claims | Profiler = Big Five traits (dispositional, situation-blind); Relational = attachment/needs (relationship-bound, dynamic). Profiler ignores relationship dynamics; Relational ignores trait taxonomy. |
| ADHD Specialist ↔ Relational Needs | both explain emotional reactivity | ADHD = ADHD-linked patterns/RSD (esp. the *self*); Relational = attachment/needs (any party). ADHD ignores non-ADHD relational dynamics; Relational ignores ADHD-pattern attribution. |
| Message Strategist ↔ Influence Tactician | both shape persuasion | Strategist = message *form* (framing, inoculation), person-agnostic; Tactician = social-influence *levers* (reciprocity, social proof) under mutual-benefit ethics. Strategist ignores influence tactics; Tactician ignores message framing. |
| Message Strategist ↔ Negotiation Architect | both design what to say | Strategist = framing/structure of the message; Architect = interests, BATNA, tactical-empathy moves. Strategist ignores negotiation leverage; Architect ignores framing theory. |
| Negotiation Architect ↔ Influence Tactician | both move the counterpart | Architect = overt, interest-based, mutual-by-construction; Tactician = named influence principles under the stricter "comfortable if discovered" bar. Architect ignores influence-principle tactics; Tactician ignores BATNA/interest mapping. |
| Influence Tactician ↔ Red Team | both judge tactics | Tactician = proposes ethically-bounded levers; Red Team = adversarially flags any covert/one-sided move and scores calibration. Tactician ignores critique role; Red Team ignores plan-building. |
| Red Team ↔ Execution Realist | both pressure-test the plan | Red Team = is the plan *strategically* sound / ethical (will it fail externally); Execution Realist = will the *human* run it under pressure (will it fail internally). Red Team ignores user-executability; Execution Realist ignores strategic correctness. |

**Tightest natural orthogonality (the `/evaluate` core four):** Behavioral Coder / Psycholinguist / Profiler / Relational Needs already cut cleanly along behavior / words / traits / needs — exactly four independent footprints, which is the design's intended payoff.

---

## Compact Summary

**Output file:** `/Users/eboney/Code/04 Mine/parley_voo/_bmad-output/planning-artifacts/research/domain-research-psych-methods-2026-06-05.md`

One line per seat (method → evidence status):

1. **Behavioral Coder** — Gottman coding + FBA. Behaviors validly *associated* with distress; "predict divorce 90%" claim is overstated (no cross-validation, PPV~43%) — keep as descriptive, ban predictive language.
2. **Psycholinguist** — LIWC. Modest effect sizes, function-word signal real but weak/uneven; needs a token floor and corroboration — moderate confidence at best.
3. **Personality Profiler** — Big Five/BFI. Strongest mainstream validity in the roster; MBTI ban is well-justified. Trait-from-transcript needs wide confidence bands.
4. **Relational Needs Analyst** — attachment + NVC + TA. Attachment has a real but messy measurement base (AAI vs. self-report r≈.09); NVC/TA are heuristics with thin outcome evidence — force tentative language.
5. **ADHD Specialist** — ADHD patterns + RSD. **Weakest construct: RSD is not in DSM-5, no validated measure, ~5 small qualitative studies.** Downgrade RSD to "useful label, not diagnosis"; lean on validated *rejection sensitivity* + emotion dysregulation.
6. **Message Strategist** — framing + inoculation. Both replicate at aggregate level; framing is context/affect-dependent and inoculation decays (~2 wk) and lacks its predicted mechanism — probabilistic lever, not switch.
7. **Negotiation Architect** — Fisher/Ury + Voss. Coherent, well-matched; practitioner frameworks (not validated theories) with mechanism support for some components (e.g., affect labeling).
8. **Influence Tactician** — Cialdini. Two-tier evidence: social proof/authority/reciprocity strong, **scarcity weak/context-dependent** — weight recommendations by tier; mutual-benefit guardrail is the right control.
9. **Red Team** — pre-mortem + devil's advocacy. Best *process* evidence, but it debiases confidence / generates reasons (~30%), it does not forecast outcomes — frame as debiasing, not prediction.
10. **Execution Realist** — implementation intentions + ADHD execution. Implementation intentions are **best-validated** (Gollwitzer & Sheeran d≈0.65); only soft spot is the shared RSD reliance from Seat 5.

**Seats where the PRD's method pairing looks weak or misattributed:**

- **Seat 5 (ADHD Specialist) — RSD.** The only genuinely under-evidenced construct. Not misattributed (RSD really is the ADHD-community concept the PRD means), but it is the highest falsifiability risk. Recommend the prompt phrase RSD as an experiential pattern and prefer the validated *rejection sensitivity* / *emotion dysregulation* constructs — and confine it to the user's self-model, not others.
- **Seat 1 (Behavioral Coder) — Gottman.** Not misattributed, but the Gottman *brand* carries the "90% prediction" baggage Parley Voo explicitly bans. The `Ignores:`/output rules must strip predictive framing or the seat will reproduce the exact overclaiming the product is designed to avoid.
- **Seat 8 (Influence Tactician) — Cialdini scarcity.** Sub-principle-level weakness only: scarcity is the soft member of an otherwise solid set; don't let the prompt treat all seven principles as equally strong.
- All other pairings (2, 3, 4-attachment-core, 6, 7, 9, 10) are coherent and appropriately matched; caveats are about *calibration of confidence in-prompt*, not about the method choice.

`[ASSUMPTION]` Briefs are written to feed persona-prompt authoring, so the validity sections are deliberately weighted toward what must NOT be claimed (FR21 falsifiability-first), per the task framing.
