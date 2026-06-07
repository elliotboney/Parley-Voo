-- Parley Voo — versioned schema (greenfield rebuilds during V1; no migrations)
-- schema_version: 1
-- Conventions: tables plural snake_case, FKs <singular>_id, booleans is_*,
-- timestamps *_at as ISO-8601 UTC TEXT (e.g. 2026-06-05T14:30:00Z),
-- date-only fields as *_on where time is meaningless.

-- slug: lowercase-kebab; 'me' reserved for the self-profile (Story 3.5)
CREATE TABLE people (
    id INTEGER PRIMARY KEY,
    slug TEXT NOT NULL UNIQUE,
    display_name TEXT NOT NULL,
    created_at TEXT NOT NULL
);

-- participants: JSON array of person slugs
CREATE TABLE conversations (
    id INTEGER PRIMARY KEY,
    source TEXT NOT NULL,
    occurred_at TEXT NOT NULL,
    setting TEXT NOT NULL CHECK (setting IN ('1:1', 'group')),
    participants TEXT NOT NULL
);

-- char_span: source character offsets for citation back-mapping
CREATE TABLE turns (
    id INTEGER PRIMARY KEY,
    conversation_id INTEGER NOT NULL REFERENCES conversations(id),
    turn_no INTEGER NOT NULL,
    speaker TEXT NOT NULL,
    text TEXT NOT NULL,
    char_span TEXT
);

-- thin shape is deliberate; consumers land in Epic 3
CREATE TABLE patterns (
    id INTEGER PRIMARY KEY,
    person_id INTEGER NOT NULL REFERENCES people(id),
    kind TEXT,
    description TEXT,
    created_at TEXT
);

-- provisional: define-or-drop decision in Story 3.6
CREATE TABLE conflicts (
    id INTEGER PRIMARY KEY,
    person_id INTEGER REFERENCES people(id),
    description TEXT,
    created_at TEXT
);

CREATE TABLE advice_outcomes (
    id INTEGER PRIMARY KEY,
    person_id INTEGER NOT NULL REFERENCES people(id),
    seat TEXT NOT NULL,
    forecast_prob REAL NOT NULL,
    outcome TEXT, -- NULL until resolved
    predicted_at TEXT NOT NULL,
    resolved_at TEXT
);

-- per-turn AND speaker-keyed embeddings (FR26); populated in Story 3.2
-- all-MiniLM-L6-v2 = 384 dims
CREATE VIRTUAL TABLE vec_turns USING vec0(
    embedding float[384],
    +turn_id INTEGER,
    +speaker TEXT
);

-- single-row config table; Story 3.2 writes the row
CREATE TABLE meta (
    embedding_model_id TEXT,
    lexicon_version TEXT,
    schema_version INTEGER
);
