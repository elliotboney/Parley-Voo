---
baseline_commit: eb3f6dc8873ca1035ff98f9272f0dad4b0edbc84
---

# Story 1.1: Plugin Scaffold & CI Gate

Status: done

<!-- Created 2026-06-07 by create-story workflow — ultimate context engine analysis completed -->

## Story

As a forker (or Elliot on day one),
I want the repo initialized as a valid, installable Claude Code plugin with privacy guardrails baked in,
So that every later story lands in a structure that validates cleanly and can never leak private data into git.

## Acceptance Criteria

1. **Given** a fresh clone of the repo, **when** `claude plugin validate ./ --strict` runs (locally and in CI), **then** validation passes with `.claude-plugin/plugin.json` carrying name `parley-voo` and an explicit `version`, **and** the scaffold came from `claude plugin init parley-voo --with skills hooks`.
2. **Given** the repo root, **when** inspecting tracked files, **then** `.gitignore` excludes `people/`, `transcripts/`, `ingest/`, `index.sqlite`, `.parley/`, `config.local.yaml`, **and** `LICENSE` is MIT, `pyproject.toml` is uv-managed (Python 3.12+, pytest + pytest-socket), `.python-version` present, **and** `schema/index.sql` defines the spec-locked tables (`people`, `conversations`, `turns`, `patterns`, `conflicts`, `advice_outcomes`, `vec_turns`, `meta`) with snake_case columns, `<singular>_id` FKs, ISO-8601 UTC timestamps (`conflicts` is provisional pending Story 3.6's define-or-drop decision).
3. **Given** a push to the repo, **when** GitHub Actions runs, **then** the CI workflow executes `claude plugin validate --strict` and a socket-blocked `pytest` run (empty suite passes).

## Tasks / Subtasks

- [x] Task 1: Generate and relocate the plugin scaffold (AC: 1)
  - [x] Run `claude plugin init parley-voo --with skills hooks` — **gotcha:** this scaffolds at `~/.claude/skills/parley-voo/`, NOT the cwd (verified against CLI help 2026-06-07). Move the generated contents into the repo root, then delete `~/.claude/skills/parley-voo/` so it doesn't auto-load as a stray skill
  - [x] Edit `.claude-plugin/plugin.json`: `name` = `parley-voo` (kebab-case — required for marketplace sync), explicit `version` (`0.1.0`), `description`, `author`, `license: "MIT"`
  - [x] Prune scaffold stubs that violate project constraints: delete `hooks-handlers/on-session-start.ts` (TypeScript — project is Python-only) and the example skill; remove the `hooks` key from plugin.json and the `hooks/` dir if nothing references them (architecture's directory structure has no hooks dir)
  - [x] Run `claude plugin validate ./ --strict` locally and iterate until exit 0 — **prefer omitting the `skills` key entirely** (omitted keys auto-discover standard dirs, and a stray placeholder risks colliding with Story 1.2's real council-engine skill); only add a minimal placeholder `skills/council-engine/SKILL.md` if `--strict` fails without one
- [x] Task 2: Privacy guardrails + repo hygiene files (AC: 2)
  - [x] Create `.gitignore` (none exists today) with exactly these privacy exclusions: `people/`, `transcripts/`, `ingest/`, `index.sqlite`, `.parley/`, `config.local.yaml` — plus standard Python noise (`__pycache__/`, `.venv/`, `*.pyc`)
  - [x] Create `LICENSE` — MIT (required: matches the `ngmeyer/skills` harvest source license)
  - [x] Create `pyproject.toml`: `name = "parley-voo"`, `requires-python = ">=3.12"`, deps `sqlite-vec` (>=0.1.7 per architecture; 0.1.9 current on PyPI), dev deps `pytest` + `pytest-socket` (0.7.0), and `[tool.pytest.ini_options] addopts = "--disable-socket"` so sockets are blocked on every pytest run by default. This is an application, not a library — `[project]` needs only `name`/`version`/`requires-python`/deps; no `[build-system]` (if `uv sync` complains, that's the fix)
  - [x] Create `.python-version` containing `3.12`; run `uv sync` + `uv lock` and commit `uv.lock`
- [x] Task 3: `schema/index.sql` — versioned, spec-locked schema (AC: 2)
  - [x] Author all 8 tables per the column contract in Dev Notes below; snake_case everywhere; FKs `<singular>_id`; timestamps `*_at` as ISO-8601 UTC TEXT
  - [x] `vec_turns` uses sqlite-vec vec0 virtual-table DDL with `embedding float[384]` (all-MiniLM-L6-v2 = 384 dims — do NOT use 1536)
  - [x] Mark `conflicts` with a comment: `-- provisional: define-or-drop decision in Story 3.6`
  - [x] `meta` is a single-row config table (one row, columns = `embedding_model_id`, `lexicon_version`, `schema_version`); leave it empty in this story — Story 3.2 writes the row
- [x] Task 4: Smoke test so the pytest gate is green (AC: 3)
  - [x] Write `tests/test_schema.py`: load sqlite-vec into an in-memory stdlib `sqlite3` connection, execute `schema/index.sql`, assert all 8 tables exist. If `enable_load_extension` is unavailable on the local interpreter, `pytest.skip` the vec_turns statement only — never let the suite silently pass on nothing
  - [x] **Gotcha:** a literally empty pytest suite exits code 5 ("no tests collected") and would FAIL CI — this smoke test is what makes the AC's "empty suite passes" intent actually hold
  - [x] Verify locally: `uv run pytest` passes with sockets blocked
- [x] Task 5: GitHub Actions CI workflow (AC: 1, 3)
  - [x] Create `.github/workflows/ci.yml` with two jobs on `[push, pull_request]`:
    - **validate:** checkout → install Claude CLI (`curl -fsSL https://claude.ai/install.sh | bash`, then add `$HOME/.claude/bin` to PATH) → `claude plugin validate ./ --strict` (runs offline, NO API key needed)
    - **test:** checkout → `astral-sh/setup-uv@v8` → `uv sync` → `uv run pytest` (socket blocking comes from pyproject addopts)
  - [x] Push and verify both jobs green (verify-clean-fork job is Story 6.3 — do NOT add it now)
- [x] Task 6: Final verification sweep (AC: all)
  - [x] Fresh-clone check: `git clone` to a temp dir, run `claude plugin validate ./ --strict` and `uv run pytest` there — both pass
  - [x] `git status` confirms no private-data paths trackable (touch `people/test.md` + `index.sqlite` locally, confirm git ignores them, delete)

### Review Findings

- [x] [Review][Patch] SQLite sidecar files can still cross the privacy boundary [`.gitignore`:5]
- [x] [Review][Patch] sqlite-vec availability check does not match the intended skip/fail behavior [`tests/test_schema.py`:33]
- [x] [Review][Patch] `meta` is documented as single-row but not enforced [`schema/index.sql`:69]
- [x] [Review][Patch] `participants` is documented as a JSON array but stored as unconstrained text [`schema/index.sql`:15]
- [x] [Review][Patch] `forecast_prob` accepts impossible probability values [`schema/index.sql`:55]

## Dev Notes

### Critical context — read before coding

- **Greenfield repo.** Root today contains only `README.md`, `docs/parley-spec.md`, `_bmad/`, `_bmad-output/`, `.agents/`, `.claude/`. There is **no `.gitignore`, no `pyproject.toml`, no plugin manifest** yet. Nothing existing gets modified except possibly README (optional, not required by ACs).
- **Do NOT touch `.claude/`** in the repo — it holds the BMAD workflow skills, unrelated to the plugin. The plugin lives at **repo root** (`.claude-plugin/`, `skills/`, `agents/` at top level), per architecture: "plugin root = repo root".
- **Stray prior experiment exists:** `~/.claude/skills/parley_voo_plugin/` — Elliot ran an earlier init with the non-kebab name `parley_voo_plugin`. Do not reuse, move, or copy it; it is not this story's scaffold (wrong name; would fail marketplace sync). Recommend deleting it at the end of the story (confirm with user first — it auto-loads in his sessions).
- **Plugin name is `parley-voo`** (kebab-case) everywhere — plugin.json `name`, pyproject `name`. The project display name "Parley Voo" appears only in descriptions.

### Verified CLI facts (researched + locally verified 2026-06-07)

- `claude plugin init parley-voo --with skills hooks` — valid syntax; flags: `--author`, `--author-email`, `--description`, `-f`. Scaffolds to `~/.claude/skills/<name>/` (move required). Generates: `.claude-plugin/plugin.json`, `skills/example/SKILL.md`, `hooks/hooks.json`, `hooks-handlers/on-session-start.ts`, root `SKILL.md`.
- `claude plugin validate <path> --strict` — treats warnings as errors, exit 0/1, runs fully offline (no API key). Caveat: validator schema can diverge from runtime loader — a real `claude` session loading the plugin is the truer test, but validate is the CI gate the AC requires.
- plugin.json required fields: `name`, `version`, `description`. Optional: `author{name,email}`, `license`, `homepage`, `repository`, `keywords`. `skills`/`agents`/`hooks` keys are conditional path arrays; omitted keys auto-discover standard dirs.
- Versions: sqlite-vec **0.1.9** (PyPI), pytest-socket **0.7.0**, setup-uv action **@v8** (v8.1.0 current).
- `marketplace.json` is explicitly polish-phase (Story 6.4) — do NOT create it now.

### Schema contract (spec-locked — architecture.md "Data Architecture" + "Naming Patterns")

| Table | Columns (minimum) |
|---|---|
| `people` | `id` PK, `slug` UNIQUE (lowercase-kebab; comment in SQL: `me` reserved for self-profile, Story 3.5), `display_name`, `created_at` |
| `conversations` | `id` PK, `source`, `occurred_at`, `setting` (`1:1\|group`), `participants` |
| `turns` | `id` PK, `conversation_id` FK, `turn_no`, `speaker`, `text`, `char_span` |
| `patterns` | `id` PK, `person_id` FK, + fields as needed (thin is fine; consumers land Epic 3) |
| `conflicts` | provisional — minimal shape + `-- provisional` comment (Story 3.6 decides) |
| `advice_outcomes` | `id` PK, `person_id` FK, `seat`, `forecast_prob`, `outcome` (NULL until resolved), `predicted_at`, `resolved_at` |
| `vec_turns` | `CREATE VIRTUAL TABLE vec_turns USING vec0(embedding float[384], +turn_id INTEGER, +speaker TEXT)` — per-turn AND speaker-keyed (FR26); columns must exist now, Story 3.2 populates |
| `meta` | `embedding_model_id`, `lexicon_version`, `schema_version` — single-row config table |

Rules: tables plural snake_case; FKs `<singular>_id`; booleans `is_*`; timestamps `*_at` ISO-8601 UTC TEXT (`2026-06-05T14:30:00Z`); date-only allowed as `occurred_on` where time is meaningless. Column shapes: `participants` = JSON array of person slugs; `setting` TEXT constrained to `1:1`/`group`; `char_span` = source character offsets for citation back-mapping. **No migrations** — versioned `schema/index.sql`, greenfield rebuilds during V1.

### Dependency policy (deliberate minimalism)

Architecture's full dep list (spacy, sentence-transformers, sqlite-vec, pytest, pytest-socket) lands incrementally: **this story adds only `sqlite-vec` + `pytest` + `pytest-socket`.** spaCy and sentence-transformers arrive with their consuming stories (3.2/3.3) — keeps CI fast and the scaffold lean. Python-only project: no Node, no npm, no package.json, no TypeScript (hence pruning the scaffolded `.ts` hook handler).

### Architecture compliance checklist (binding)

- Repo root = plugin root; shipped code above the gitignore line, private data below — **the gitignore line IS the privacy boundary** (FR31, NFR1 seam #3)
- `.gitignore` six privacy entries are non-negotiable: `people/`, `transcripts/`, `ingest/`, `index.sqlite`, `.parley/`, `config.local.yaml`
- MIT license is required (harvest-source compatibility), not a default choice
- No network anywhere in tests: pytest-socket `--disable-socket` via pyproject `addopts` — this is NFR1's no-network invariant enforced in CI from day one
- Script I/O contract (argparse in, JSON stdout, exit 0/1/2) applies to future `scripts/*.py` — no scripts are authored in this story, but don't scaffold anything that contradicts it
- Anti-patterns to avoid: committing `index.sqlite`; any data dir tracked; model tiers/config hardcoded anywhere; creating `commands/` (commands are skills in this plugin system)

### Scope boundaries — what this story does NOT include

- No skills content (council-engine SKILL.md body = Story 1.2; only an optional placeholder if strict validation demands one)
- No `agents/*.md` personas (Epic 2), no `councils/` rosters (2.3), no `scripts/*.py` (3.1+), no `templates/` (3.5), no `config.yaml` (2.3), no `verify_clean_fork.py` or its CI job (6.3), no `marketplace.json` (6.4), no `examples/` (6.3)
- CI = exactly two gates: plugin validate + socket-blocked pytest

### Project Structure Notes

End-state of repo root after this story (new items only):

```
.claude-plugin/plugin.json     # name parley-voo, version 0.1.0, MIT
.github/workflows/ci.yml       # validate + test jobs
.gitignore                     # 6 privacy entries + python noise
.python-version                # 3.12
LICENSE                        # MIT
pyproject.toml                 # uv-managed; sqlite-vec; pytest+pytest-socket; addopts --disable-socket
uv.lock
schema/index.sql               # 8 spec-locked tables, conflicts provisional
skills/council-engine/SKILL.md # minimal placeholder ONLY if strict validate requires it
tests/test_schema.py           # schema smoke test (keeps pytest gate meaningful)
```

No conflicts detected with existing tree — `_bmad*/`, `.agents/`, `.claude/`, `docs/` are untouched neighbors.

### Testing standards

- pytest, files `tests/test_<thing>.py`; golden files (later stories) in `tests/golden/`
- Sockets blocked globally via addopts — any test needing network is a bug by definition
- This story's bar: `uv run pytest` green locally and in CI, ≥1 real assertion (schema smoke test)

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Story 1.1] — story + ACs (verbatim)
- [Source: _bmad-output/planning-artifacts/epics.md#Additional Requirements → Starter template / Runtime & stack / Privacy mechanisms / CI & quality gates]
- [Source: _bmad-output/planning-artifacts/architecture.md#Starter Template Evaluation] — init command, scaffold rationale, harvest plan
- [Source: _bmad-output/planning-artifacts/architecture.md#Core Architectural Decisions → Data Architecture] — schema, Python 3.12+/uv, sqlite-vec ≥0.1.7
- [Source: _bmad-output/planning-artifacts/architecture.md#Implementation Patterns & Consistency Rules] — naming, I/O contract, anti-patterns
- [Source: _bmad-output/planning-artifacts/architecture.md#Project Structure & Boundaries] — directory layout, gitignore-as-boundary
- [Source: PRD FR31/FR32, NFR1/NFR4] — privacy gitignore, MIT/distribution, no-network, bounded infra
- CLI facts verified live against `claude plugin init --help` / `claude plugin validate --help` on 2026-06-07; versions via PyPI/docs research same date

## Dev Agent Record

### Agent Model Used

Claude Opus 4.8 (claude-opus-4-8[1m]) via Claude Code

### Debug Log References

- `astral-sh/setup-uv@v8` failed in CI ("unable to find version v8") — the repo publishes only full tags (`v8.2.0`), no bare `v8` major alias. Fixed by pinning `@v8.2.0` (run 27095456741 → 27095478799 green).
- Naive `split(";")` statement parsing in the smoke test broke on a `;` inside a schema header comment — replaced with `re.sub` strip of the vec_turns statement + `executescript`.
- pytest initially collected `_bmad/scripts/tests/` — constrained with `testpaths = ["tests"]` in pyproject so the CI gate only runs plugin tests.

### Completion Notes List

- Scaffold: ran `claude plugin init parley-voo --with skills hooks`; moved only `.claude-plugin/plugin.json` to repo root (the other generated files — TS hook handler, hooks.json, example skill, root SKILL.md — were all prune targets, so they were never copied); deleted `~/.claude/skills/parley-voo/`. The stray prior experiment `~/.claude/skills/parley_voo_plugin/` mentioned in Dev Notes no longer exists — nothing to clean up.
- plugin.json: name `parley-voo`, version `0.1.0`, MIT license, no `skills` key (auto-discovery). `claude plugin validate ./ --strict` exits 0 without any placeholder skill — `skills/council-engine/SKILL.md` NOT created (per story preference).
- All 6 privacy gitignore entries verified via `git check-ignore` against live test files (created + confirmed ignored + deleted).
- pyproject: app-style `[project]` (no `[build-system]`), deps `sqlite-vec>=0.1.7` (resolved 0.1.9), dev group pytest + pytest-socket (resolved 0.8.0 — story cited 0.7.0 as current; unpinned, newer is fine), `addopts = "--disable-socket"`. `uv sync`/`uv lock` clean on CPython 3.12.11.
- Schema: all 8 tables authored per the column contract; `vec_turns` vec0 with `embedding float[384]` + `+turn_id`/`+speaker` aux columns; `conflicts` carries the provisional comment; `meta` left empty.
- Tests: 2 tests (regular tables via stdlib sqlite3; vec_turns with real sqlite-vec extension loaded — passes locally and in CI, skip path only triggers where `enable_load_extension` is unavailable). Both green with sockets blocked.
- CI: both jobs green on `6110ea3` (run 27095478799 + follow-up). validate job runs Claude CLI offline, no API key. Also bumped `actions/checkout` v4→v5 after GitHub's annotation that Node 20 actions get force-migrated 2026-06-16 (9 days out) — one-line change to a file authored in this story.
- Fresh-clone check: cloned to temp dir; `claude plugin validate ./ --strict` exit 0 and `2 passed` there.
- Code pushed in 3 commits: `a22e01c` (story files), `f7d1d17` (setup-uv pin), `6110ea3` (checkout v5).
- ✅ Resolved review finding [Patch]: SQLite sidecar files — `.gitignore` now uses `index.sqlite*`; all 4 sidecar variants verified via `git check-ignore`.
- ✅ Resolved review finding [Patch]: `_vec_available()` now actually attempts `sqlite_vec.load()` (with conn cleanup) instead of returning True on import alone.
- ✅ Resolved review finding [Patch]: `meta` single-row enforced via `id INTEGER PRIMARY KEY DEFAULT 1 CHECK (id = 1)`.
- ✅ Resolved review finding [Patch]: `participants` constrained with `CHECK (json_valid(...) AND json_type(...) = 'array')` — json_valid guard needed because bare `json_type()` raises OperationalError on malformed JSON instead of failing the CHECK.
- ✅ Resolved review finding [Patch]: `forecast_prob` bounded with `CHECK (forecast_prob BETWEEN 0.0 AND 1.0)`.
- Review fixes: 3 new red-green constraint tests (suite now 5 passed); pushed as `5272610`, CI green.

### File List

- `.claude-plugin/plugin.json` (new)
- `.github/workflows/ci.yml` (new)
- `.gitignore` (new)
- `.python-version` (new)
- `LICENSE` (new)
- `pyproject.toml` (new)
- `uv.lock` (new)
- `schema/index.sql` (new)
- `tests/test_schema.py` (new)

## Change Log

- 2026-06-07: Story 1.1 implemented — plugin scaffold (validate --strict green), privacy gitignore (6 entries verified), MIT license, uv-managed pyproject (Python 3.12+, sqlite-vec, socket-blocked pytest), 8-table spec-locked schema, schema smoke tests, 2-job CI (validate + test) green on GitHub Actions. Status → review.
- 2026-06-07: Addressed code review findings — 5 items resolved (sqlite sidecar gitignore, vec availability check, meta single-row, participants JSON-array, forecast_prob bounds). Commit `5272610`, CI green. Status → review.
