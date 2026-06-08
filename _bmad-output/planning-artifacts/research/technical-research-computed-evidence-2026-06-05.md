---
stepsCompleted: [1, 2, 3, 4, 5, 6]
inputDocuments:
  - prds/prd-parley_voo-2026-06-04/prd.md
  - prds/prd-parley_voo-2026-06-04/addendum.md
workflowType: 'research'
lastStep: 6
research_type: 'technical'
research_topic: 'Computed-evidence stack for Parley Voo (FR23-FR26 + script runtime)'
research_goals: 'Survey real options, licenses, maturity, and local-first Claude Code integration fit for psycholinguistic metrics, deterministic Big Five scoring, semantic recall, and calibration scoring; recommend a script runtime for the architect to ratify.'
user_name: 'Elliot'
date: '2026-06-05'
web_research_enabled: true
source_verification: true
mode: 'headless'
---

# Research Report: Computed-Evidence Stack for Parley Voo

**Date:** 2026-06-05
**Author:** Elliot
**Research Type:** technical (headless run)
**Feeds:** imminent architecture phase

---

## Research Overview

This report evaluates the four computed-evidence requirements (FR23 psycholinguistic metrics, FR24 deterministic Big Five scoring, FR25 calibration scoring, FR26 semantic recall) plus a cross-cutting script-runtime decision, for Parley Voo: a local-first, solo-user, Claude Code-based communication coach storing data as markdown + a single SQLite file, with scripts invoked by Claude Code skills.

**Headline recommendations (one line each):**

1. **FR23 psycholinguistic metrics** — Build a custom **spaCy + curated lexicons (NRC EmoLex, hedge/tentative word lists) + psyLex** feature extractor in **Python**. Empath as an optional broad-category add-on. (Runner-up: Empath-only.)
2. **FR24 deterministic Big Five** — Use **lexicon-based scoring from transcript text and label it a weak signal** (the validated ~5%-variance ceiling). The PRD's "BFI item scoring as math" needs reframing: BFI item scoring presumes questionnaire answers, which transcripts do not provide. (Runner-up: skip deterministic scoring; let the Profiler LLM seat reason from raw linguistic features with confidence ranges.)
3. **FR26 semantic recall** — **sqlite-vec** is stable enough for this scale; pair with a **local `all-MiniLM-L6-v2` (or `bge-small`) embedding model via sentence-transformers** — no API, no data leaves the machine. (Runner-up: LanceDB if sqlite-vec proves limiting.)
4. **FR25 calibration scoring** — Plain **Brier score + hit rate per person/seat**, computed in a small script from `advice_outcomes`; **skip the reliability/resolution/uncertainty decomposition** at solo small-n. Surface "n=" alongside every number. (Runner-up: add Wilson confidence intervals on hit rate.)
5. **Cross-cutting runtime** — **Python** for the computed-evidence scripts. The entire NLP/embedding/scientific stack (spaCy, sentence-transformers, NRC ports, sqlite-vec bindings) is Python-native and deeper than Node's. (Runner-up: Deno/TypeScript, viable only if you drop spaCy-grade linguistics.)

**Finding that materially changes a PRD assumption:** FR24 as written ("BFI item scoring computed as math, feeding the Personality Profiler") is **not achievable from transcripts as stated** — see [Section 4](#4-fr24-deterministic-big-five-scoring). Deterministic Big-Five-from-text is lexicon-based and validated only as a *weak* signal (LIWC categories explain ~5% of self-reported personality variance; ρ .08-.14). The honest framing the PRD's own falsifiability principle (FR21) demands: treat it as a low-confidence input, not "math," and never let it harden into a trait claim.

---

## Table of Contents

1. Introduction and Methodology
2. FR23 — Psycholinguistic Metrics (LIWC alternatives)
3. (FR23 continued in Section 2)
4. FR24 — Deterministic Big Five Scoring
5. FR26 — Semantic Recall (sqlite-vec + embeddings)
6. FR25 — Calibration Scoring (Brier track records)
7. Cross-Cutting — Script Runtime (Python vs Node/Deno)
8. Consolidated Recommendations and Architecture Notes
9. Source Documentation

---

## 1. Introduction and Methodology

**Scope.** Four computed-evidence FRs that distinguish Parley Voo from a prompt: scripted linguistic metrics, deterministic personality scoring, calibration over recorded advice outcomes, and semantic recall over transcript history. Each is evaluated on real options, license, maturity (as of June 2026), and fit for a local-first, single-SQLite-file, Claude-Code-invoked-script architecture.

**Constraints carried from the PRD/addendum:**
- **NFR4 Bounded infrastructure:** single local SQLite file, no server.
- **NFR1/NFR3 Privacy + portability:** privacy-sensitive personal transcripts; nothing should require sending data to a third-party API.
- **NFR5 Responsible use + FR21 falsifiability:** every computed claim must carry confidence; nothing hardens into "fact."
- Scripts are invoked by Claude Code skills (`scripts/ingest.*`, etc.), so the runtime must be trivially shellable from a skill.

**Method.** Web research current as of June 2026, multiple sources per claim, decisive recommendation + runner-up per area. Assumptions are tagged `[ASSUMPTION]`.

---

## 2. FR23 — Psycholinguistic Metrics (LIWC Alternatives)

**Requirement:** Compute LIWC-style metrics (pronoun ratios, hedging density, language-style matching) from transcripts to feed the Psycholinguist seat hard numbers.

**The licensing problem:** LIWC is proprietary/commercial — unusable in a public forkable template repo without per-user licensing. Open alternatives exist and several validate well against LIWC.

### Options surveyed

| Tool | What it is | License | Fit |
|---|---|---|---|
| **Empath** | Dictionary tool, 200+ categories, built from word2vec/GloVe + ConceptNet + crowdsourcing; can mint new categories from seed words | Open source (MIT) | Strong, validated against LIWC across shared categories |
| **psyLex** | Open Python reimplementation of the LIWC *method* (dictionary + Porter stemmer wildcard matching) | Open source | Closest to LIWC's own methodology; English only |
| **spaCy** | Production NLP: POS tagging, dependency parse, lemmatization | MIT | The right base for *custom* metrics (pronoun ratios, tentative-word density) |
| **NRC EmoLex** | Word-emotion association lexicon (8 emotions + sentiment) | Free for research; (C) NRC Canada — **check redistribution terms before bundling** | Good for emotion features |
| **VADER** | Rule-based sentiment, tuned for short/informal text | MIT-style | Cheap sentiment signal; Python (`vaderSentiment`) and JS ports exist |

### Decisiveness

The three FR23 metrics decompose cleanly:
- **Pronoun ratios** — direct from spaCy POS tags (`token.pos_ == "PRON"`) plus a first-person word set. Trivial, exact, deterministic.
- **Hedging density** — lexicon-based: a curated tentative/hedge word list ("maybe, perhaps, might, seems, I think, sort of") counted and normalized by token count. Matches LIWC's "tentative" category approach. (A trained CoNLL-2010 hedge classifier is more accurate but overkill here.)
- **Language-style matching (LSM)** — a *function-word* similarity metric between two speakers; computed from spaCy function-word counts (articles, prepositions, pronouns, auxiliaries, conjunctions, etc.) — no special library, just the standard LSM formula over function-word category proportions. `[ASSUMPTION]` Two-speaker transcripts give the two distributions LSM needs; ingestion metadata (FR22) tags speakers.

**Recommendation:** **Custom spaCy + curated lexicons + psyLex**, in Python.
- spaCy handles tokenization/POS/lemmas → pronoun ratios + LSM function-word counts.
- A small hand-maintained hedge/tentative lexicon → hedging density (auditable, fork-safe, no licensing).
- psyLex (or Empath) supplies broader LIWC-style category coverage when the Psycholinguist seat wants more dimensions.
- NRC EmoLex/VADER optional for emotion/sentiment — **verify NRC redistribution terms before shipping it in the public template** (research-only attribution may constrain bundling).

**Runner-up:** **Empath-only** — fastest to stand up, validated against LIWC, broad categories out of the box; weaker on the three *specific* metrics FR23 names (pronoun ratios and LSM you'd still compute yourself).

**Ecosystem note:** Node has community ports (`nrc-sentiment`, `vader-sentiment`, AFINN), but **no production-grade equivalent to spaCy's POS/dependency parsing**, which the pronoun-ratio and LSM metrics depend on. This is the first of several forces pushing the runtime to Python (Section 7).

---

## 4. FR24 — Deterministic Big Five Scoring

**Requirement (as written):** "Deterministic personality scoring: BFI item scoring computed as math, feeding the Personality Profiler." Addendum: "BFI item scoring as deterministic math."

### The core problem (PRD-material)

**BFI/IPIP item scoring is deterministic — but it scores *questionnaire responses*, not free text.** The IPIP-NEO procedure is: each item rated 1-5, reverse-key the minus-keyed items, sum/average per domain. Fully deterministic, public domain (IPIP items are explicitly public domain, copy with citation). **But this presumes a person answered 50-300 Likert items.** Parley Voo has transcripts, not questionnaire answers. There is no deterministic "BFI item score" to compute from a Zoom transcript.

What *is* possible deterministically from transcript text is **lexicon-based Big-Five estimation** — and the validated evidence says it is a **weak signal**:

- Meta-analysis (31 samples, n=85,724): LIWC categories correlate with **self-reported** Big Five at only ρ = **.08-.14**; the 52 LIWC categories explain on average **~5.1% of personality variance**.
- Against **observer-rated** personality the signal is better (ρ .18-.39, ~38% variance) — relevant because Parley Voo is the *user observing others*, not self-report.
- Social-media digital-footprint prediction (separate meta-analysis) tops out at the behavioral "correlational upper limit": r ≈ **0.29 (Agreeableness) to 0.40 (Extraversion)** — and that uses ML models + demographics, not a pure lexicon.
- A 2025 study found out-of-the-box LLMs are **not** reliably better and are non-deterministic — so swapping in an LLM does not rescue determinism *or* validity.

### Decisiveness

**Recommendation:** Implement **lexicon-based Big Five scoring from transcript text, explicitly labeled a weak, low-confidence signal**, and **reframe FR24** away from "BFI item scoring as math."
- Use an open, validated personality lexicon (e.g., the 2026 *Scientific Data* standardized personality lexicon, all five dimensions hit-rate >0.7 in validation; lexicon scoring is deterministic by construction) **or** map Empath/LIWC-style categories to Big Five via the published meta-analytic correlations.
- Emit each trait with the **correlation range as its confidence** — which is exactly what FR21 ("Profiler correlation ranges") already anticipates. The PRD's falsifiability machinery is the right home for this; the word "math" in FR24 oversells it.
- Keep the **IPIP keying logic** in the codebase only for the case where the *user self-administers* a real BFI/IPIP questionnaire about themselves or a known person — that path *is* legitimately deterministic math and public-domain. `[ASSUMPTION]` This is the most defensible "deterministic Big Five" feature; transcript-derived scores are the weak adjunct.

**Runner-up:** **Drop deterministic personality scoring entirely.** Feed the Personality Profiler seat the *raw linguistic features* (Section 2) and let it reason qualitatively with attributed confidence. This is more honest than dressing up a 5%-variance lexicon output as a "score," and it sidesteps the validity caveat the public repo's responsible-use note would otherwise have to carry.

**Validity caveats to surface honestly (FR21/NFR5 require this):**
1. Transcript Big Five is weak: ~5% variance vs self-report, better but still modest vs observer ratings.
2. It degrades on short texts and conversational (vs essay) registers.
3. It is context-blind (dictionary matching can't read sarcasm, metaphor, or situational framing).
4. Never present a trait as a number without its confidence band; never let it become a dossier claim.

---

## 5. FR26 — Semantic Recall (sqlite-vec + Embeddings)

**Requirement:** sqlite-vec search over transcript history feeding the citation rule and past-win receipts — same SQLite file, no added infra.

### sqlite-vec maturity (mid-2026)

- Created by Alex Garcia; **C, zero dependencies, MIT/Apache-2.0 dual license** — clean for a public fork.
- First "stable" v0.1.0 in 2024; now **v0.1.7+** with DELETE support, KNN distance-column constraints (pagination), and fuzz testing catching rare memory bugs.
- **Still pre-1.0.** Roadmap is v1 "within a year or so." Search is **brute-force KNN by default** (ANN indexes — rescore/ivf/DiskANN — are experimental/alpha, not enabled).
- Brute-force is **fine for this scale**: the maintainer's own framing is "thousands to hundreds of thousands of vectors, rarely millions." A solo user's transcript history is firmly in that range — likely **low thousands of chunks**. `[ASSUMPTION]`
- Runs everywhere (macOS/Linux/Windows/WASM), with Python bindings.

**Verdict:** sqlite-vec is **the correct choice** — it is the only option that keeps everything in *one SQLite file* (NFR4), is permissively licensed, and is mature enough at this scale. Its pre-1.0 status and brute-force search are non-issues for solo-scale data.

### Embedding model (the privacy-load-bearing decision)

For a privacy-sensitive local tool, **embeddings must be computed locally** — sending personal transcripts to an embedding API contradicts NFR1. Open local models in 2026 match/approach OpenAI `text-embedding-3-small` for semantic search at zero API cost:

| Model | Profile | When |
|---|---|---|
| **all-MiniLM-L6-v2** | Tiny, fast on CPU, 384-dim | Default for speed on modest hardware |
| **bge-small-en-v1.5 / bge-large-en-v1.5** | Strong English quality | When recall quality matters more than speed |
| **nomic-embed-text-v2** | Fast CPU, long context (8k), multilingual | If transcripts are long or multilingual |
| **bge-m3** | SOTA quality, multilingual, long doc | Heaviest; overkill for solo scale |

**Recommendation:** **sqlite-vec + local `all-MiniLM-L6-v2` via sentence-transformers** as the default; **bge-small-en-v1.5** as the quality upgrade. CPU-only, ~80MB model, no GPU, no API, fork-safe. Store the embedding model id in the DB so re-embedding is detectable if you switch models.

**Runner-up:** **LanceDB** — embedded, fast IVF-PQ ANN, scales to ~10M+ vectors. The cost: it's **directory-based, not a single file**, which violates the "same SQLite file, no added infra" framing of FR26/NFR4. Reach for it only if sqlite-vec brute-force latency becomes a felt problem (it won't at solo scale). **FAISS** is rejected: a bare library with no metadata/persistence layer — you'd rebuild what SQLite gives free.

---

## 6. FR25 — Calibration Scoring (Brier Track Records)

**Requirement:** Per-person prediction hit rates ("Red Team batting .71 on this person") + Brier scores measuring calibration quality of Red Team predictions and Profiler claims, computed from `advice_outcomes`.

### Math conventions (light treatment, as requested)

- **Brier score** = mean squared error of probabilistic predictions: `BS = (1/N) Σ (forecast_prob − outcome)²`, outcome ∈ {0,1}. 0 = perfect, 1 = worst. Strictly proper scoring rule.
- **Hit rate** = fraction of predictions that resolved correctly (threshold at 0.5 for the "batting average" framing).
- The textbook **three-part decomposition** (Brier = Uncertainty − Resolution + Reliability) requires **binning predictions by probability** and is **unreliable at small n** — bins end up nearly empty. The literature explicitly warns: with ~10 predictions, reliability/resolution can't be estimated robustly; extra within-bin correction terms exist precisely because binning is unstable at low n.

### Decisiveness

**Recommendation:** **Plain per-person, per-seat Brier score + hit rate, computed in a small script from `advice_outcomes`. Skip the reliability/resolution/uncertainty decomposition.**
- At solo scale, predictions per person will be in the single-to-low-double digits for a long time. Decomposition would be statistical theater.
- **Always display `n`** next to every Brier/hit-rate number ("Red Team: .71 over n=7 on Chris"). The honesty requirement (FR21/NFR5) makes hiding small-n unacceptable.
- A Brier of 0 is unrealistic even for a perfect model — don't treat low Brier as "solved."
- Keep comparisons **within the same person/context** — Brier conflates calibration, discrimination, and base-rate difficulty, so cross-person leaderboards mislead.

**Runner-up:** Add **Wilson score confidence intervals** on the hit rate to make small-n uncertainty visible as a band rather than a point — cheap, no new deps, and reinforces the falsifiability stance. Defer the full decomposition until a person accumulates enough predictions to bin (realistically a V2+ concern, if ever).

**No PRD change needed** — FR25 is implementable as stated; the only nuance is *what to omit* (decomposition) and *what to always show* (n).

---

## 7. Cross-Cutting — Script Runtime (Python vs Node/Deno)

**Decision for the architect to ratify.**

The computed-evidence stack's library gravity is overwhelmingly Python:

| Need | Python | Node/Deno |
|---|---|---|
| POS/dependency parsing (pronoun ratios, LSM) | **spaCy** (industrial, latest release Mar 2026) | No production equivalent |
| LIWC-style lexicons | psyLex, Empath | Community sentiment ports only (AFINN/VADER/NRC), no LIWC-method tool |
| Big Five lexicons | Validated lexicons + sklearn pipelines | None mature |
| Local embeddings | sentence-transformers (de facto standard) | transformers.js exists but smaller model zoo, more friction |
| sqlite-vec | First-class Python bindings | Bindings exist, less documented |
| Brier/stats | numpy/scipy trivial | doable, more hand-rolling |

**Recommendation:** **Python** for all computed-evidence scripts (`scripts/ingest.py`, feature extraction, scoring, calibration). Every load-bearing library (spaCy, sentence-transformers, the lexicons, sqlite-vec, numpy) is Python-native and more mature than any Node counterpart. Claude Code skills shell out to `python3 scripts/...` exactly as cleanly as to Node.

**Runner-up:** **Deno/TypeScript** — attractive only if you (a) drop spaCy-grade linguistics (compute pronoun ratios with a hand-rolled tokenizer + word lists) and (b) accept transformers.js for embeddings. Given Sir E's noted bun/Deno-script preference, this is the *only* reason to consider Node — but it forfeits spaCy, the validated lexicon ecosystem, and sentence-transformers, which is a steep price for the FR23/FR24 features specifically. `[ASSUMPTION — flagging the bun/Deno preference from your global setup; the libraries still point to Python.]`

**Pragmatic middle path `[ASSUMPTION]`:** If you want to keep glue/CLI in Deno/TypeScript per your house style, isolate the *heavy NLP/embedding* steps in small Python scripts and call them from the Deno layer. The data store (SQLite) is language-neutral, so a Deno orchestration + Python evidence-compute split is clean. Architect should decide whether the polyglot cost is worth honoring the house style.

---

## 8. Consolidated Recommendations and Architecture Notes

| FR | Recommendation | Runner-up | License posture | PRD impact |
|---|---|---|---|---|
| FR23 | spaCy + curated hedge lexicon + psyLex (Python) | Empath-only | All open/MIT; verify NRC terms before bundling | none |
| FR24 | Lexicon-based, labeled **weak** signal; keep IPIP keying for self-administered questionnaires | Drop scoring; feed raw features to Profiler seat | IPIP public domain; lexicons open | **Reframe FR24** — "BFI item scoring as math" not achievable from transcripts |
| FR25 | Plain per-person/seat Brier + hit rate, **always show n**, skip decomposition | Add Wilson CIs | n/a (own code) | none (omit decomposition) |
| FR26 | sqlite-vec + local all-MiniLM-L6-v2 (sentence-transformers) | LanceDB | sqlite-vec MIT/Apache-2.0; models open | none |
| Runtime | **Python** | Deno/TS (drops spaCy) or polyglot split | n/a | none |

**Privacy invariant confirmed:** the entire stack runs locally with no third-party API calls (local embeddings, local lexicons, local SQLite) — consistent with NFR1/NFR4. Vet NRC EmoLex's redistribution terms as the one bundling caveat for the public template.

**Architecture follow-ups (for the architect):**
1. Ratify Python as the evidence-compute runtime (or accept the polyglot split).
2. Reframe FR24 in the architecture doc; carry the validity caveats into the responsible-use note (FR32).
3. Store `embedding_model_id` and `lexicon_version` in the DB for reproducibility/falsifiability.
4. Decide `advice_outcomes` schema to support per-person/per-seat Brier (forecast_prob, outcome, person_id, seat, predicted_at, resolved_at).
5. Confirm transcript chunking strategy for embeddings (per-turn vs sliding window) `[ASSUMPTION: per-turn chunks keyed to speaker, to serve the citation rule FR12]`.

---

## 9. Source Documentation

**FR23 — psycholinguistic metrics:**
- Empath (PyPI / paper): https://libraries.io/pypi/empath · https://arxiv.org/pdf/1602.06979 · https://github.com/Ejhfast/empath-client
- psyLex (open LIWC reimplementation): https://github.com/seanrife/psyLex
- spaCy linguistic features / POS: https://spacy.io/usage/linguistic-features · https://spacy.io/ · https://pypi.org/project/spacy/
- Hedge detection: https://arxiv.org/pdf/2405.13319
- LIWC open-alternative discussion: https://codingtechroom.com/question/open-source-liwc-alternatives
- NRC EmoLex (Node port + terms): https://github.com/jeremylind/nrc-sentiment · https://github.com/JianLoong/sentimentanalysis

**FR24 — Big Five from text:**
- Kernel-of-truth meta-analysis (LIWC × Big Five, ~5% variance): https://research.vu.nl/en/publications/the-kernel-of-truth-in-text-based-personality-assessment-a-meta-a/ · https://repository.tilburguniversity.edu/server/api/core/bitstreams/6954e6ad-d510-43fb-bda3-54d102be8eb3/content
- Digital-footprint prediction meta-analysis (r .29-.40): https://www.sciencedirect.com/science/article/abs/pii/S0191886917307328 · https://www.cs.columbia.edu/~julia/papers/azucaretal2017.pdf
- LLMs not reliable / non-deterministic for Big Five: https://arxiv.org/pdf/2511.23101
- Standardized personality lexicon (2026, hit-rate >0.7): https://www.nature.com/articles/s41597-026-06783-6
- IPIP scoring + public domain: https://ipip.ori.org/MiniIPIPKey.htm · https://psychkit.org/ipip-neo-120/ · https://www.sciencedirect.com/science/article/abs/pii/S0191886913005138

**FR26 — sqlite-vec + embeddings:**
- sqlite-vec stable release + repo: https://alexgarcia.xyz/blog/2024/sqlite-vec-stable-release/index.html · https://github.com/asg017/sqlite-vec · https://github.com/asg017/sqlite-vec/releases
- State of vector search in SQLite: https://marcobambini.substack.com/p/the-state-of-vector-search-in-sqlite · https://sqlite.org/vec1
- LanceDB vs sqlite-vec vs FAISS: https://shaharia.com/blog/choosing-embeddable-vector-database-go-application/ · https://zilliz.com/comparison/faiss-vs-lancedb
- Local embedding models 2026: https://www.promptquorum.com/power-local-llm/best-embedding-models-local-rag-2026 · https://www.bentoml.com/blog/a-guide-to-open-source-embedding-models · https://huggingface.co/sentence-transformers

**FR25 — Brier / calibration:**
- Brier score + decomposition: https://en.wikipedia.org/wiki/Brier_score · https://www.emergentmind.com/topics/brier-score-term
- Small-sample / binning caveats: https://journals.ametsoc.org/view/journals/wefo/23/4/2007waf2006116_1.xml
- Misconceptions about Brier (2026): https://www.sciencedirect.com/science/article/pii/S2590113325000604 · https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12818272/

**Cross-cutting runtime:**
- Python NLP ecosystem 2026: https://www.clickittech.com/ai/python-nlp-libraries/
- Node sentiment ports: https://dev.to/frikishaan/sentiment-analysis-using-node-js-4kfb

---

**Research Completion Date:** 2026-06-05
**Mode:** headless (no [C] gate; reasonable defaults taken, assumptions tagged)
**Source Verification:** all claims web-verified, multiple sources where load-bearing
**Confidence:** High on FR23/FR26/FR25/runtime; the FR24 reframing is the one finding the architect must consciously ratify.
