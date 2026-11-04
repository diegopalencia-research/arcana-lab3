PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS cards (
    card_id TEXT PRIMARY KEY,
    card_name TEXT NOT NULL UNIQUE,
    arcana TEXT NOT NULL CHECK (arcana IN ('Major','Minor')),
    suit TEXT NOT NULL,
    rank INTEGER NOT NULL,
    element TEXT,
    upright_keywords TEXT NOT NULL,
    reversed_keywords TEXT NOT NULL,
    technical_upright TEXT NOT NULL,
    technical_reversed TEXT NOT NULL,
    child_explanation TEXT NOT NULL,
    imagery_observation TEXT NOT NULL,
    reflection_prompt_1 TEXT NOT NULL,
    reflection_prompt_2 TEXT NOT NULL,
    astrological_correspondence TEXT,
    correspondence_system TEXT,
    source_note TEXT
);

CREATE TABLE IF NOT EXISTS correspondences (
    correspondence_id INTEGER PRIMARY KEY AUTOINCREMENT,
    layer TEXT NOT NULL,
    tarot_group TEXT NOT NULL,
    element TEXT,
    zodiac_signs TEXT,
    traditional_sign_rulers TEXT,
    scope TEXT,
    system TEXT,
    caution TEXT
);

CREATE TABLE IF NOT EXISTS readings (
    reading_id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    question TEXT NOT NULL,
    life_domain TEXT NOT NULL,
    context TEXT,
    spread_type TEXT NOT NULL,
    draw_method TEXT NOT NULL,
    initial_observation TEXT,
    overall_interpretation TEXT,
    key_insight TEXT,
    action_commitment TEXT,
    theme_tags TEXT,
    follow_up_due TEXT
);

CREATE TABLE IF NOT EXISTS reading_cards (
    reading_card_id INTEGER PRIMARY KEY AUTOINCREMENT,
    reading_id INTEGER NOT NULL REFERENCES readings(reading_id) ON DELETE CASCADE,
    position_index INTEGER NOT NULL,
    position_label TEXT NOT NULL,
    card_id TEXT NOT NULL REFERENCES cards(card_id),
    orientation TEXT NOT NULL CHECK (orientation IN ('Upright','Reversed')),
    visual_observation TEXT,
    personal_interpretation TEXT,
    UNIQUE(reading_id, position_index)
);

CREATE TABLE IF NOT EXISTS study_reviews (
    review_id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    card_id TEXT NOT NULL REFERENCES cards(card_id),
    quiz_score INTEGER NOT NULL,
    quiz_total INTEGER NOT NULL,
    recall_rating INTEGER CHECK (recall_rating BETWEEN 1 AND 5),
    minutes_spent INTEGER,
    next_review_at TEXT,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS followups (
    followup_id INTEGER PRIMARY KEY AUTOINCREMENT,
    reading_id INTEGER NOT NULL REFERENCES readings(reading_id) ON DELETE CASCADE,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    outcome_note TEXT,
    action_completed INTEGER NOT NULL DEFAULT 0 CHECK (action_completed IN (0,1)),
    alignment_rating INTEGER CHECK (alignment_rating BETWEEN 1 AND 5),
    emotion_label TEXT
);

CREATE INDEX IF NOT EXISTS idx_readings_created_at ON readings(created_at);
CREATE INDEX IF NOT EXISTS idx_readings_domain ON readings(life_domain);
CREATE INDEX IF NOT EXISTS idx_reading_cards_card_id ON reading_cards(card_id);
CREATE INDEX IF NOT EXISTS idx_study_reviews_created_at ON study_reviews(created_at);
CREATE INDEX IF NOT EXISTS idx_followups_reading_id ON followups(reading_id);

CREATE VIEW IF NOT EXISTS v_reading_detail AS
SELECT
    r.reading_id, r.created_at, r.question, r.life_domain, r.context,
    r.spread_type, r.draw_method, r.initial_observation,
    r.overall_interpretation, r.key_insight, r.action_commitment,
    r.theme_tags, rc.position_index, rc.position_label,
    c.card_name, c.arcana, c.suit, c.element, rc.orientation,
    rc.visual_observation, rc.personal_interpretation
FROM readings r
JOIN reading_cards rc ON rc.reading_id = r.reading_id
JOIN cards c ON c.card_id = rc.card_id;


CREATE TABLE IF NOT EXISTS lesson_progress (
    lesson_id TEXT PRIMARY KEY,
    completed_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
