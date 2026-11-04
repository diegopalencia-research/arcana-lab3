from __future__ import annotations
import csv
import os
import sqlite3
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DB = ROOT / 'data' / 'arcana_lab.db'
SCHEMA_PATH = ROOT / 'database' / 'schema.sql'
CARDS_PATH = ROOT / 'data' / 'cards.csv'
CORRESPONDENCES_PATH = ROOT / 'data' / 'correspondences.csv'


def get_db_path() -> Path:
    custom = os.getenv('ARCANA_DB_PATH')
    return Path(custom).expanduser() if custom else DEFAULT_DB


def connect(db_path: str | Path | None = None) -> sqlite3.Connection:
    path = Path(db_path) if db_path else get_db_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON')
    return conn


def init_db(db_path: str | Path | None = None) -> None:
    with connect(db_path) as conn:
        conn.executescript(SCHEMA_PATH.read_text(encoding='utf-8'))
        if conn.execute('SELECT COUNT(*) FROM cards').fetchone()[0] == 0:
            with CARDS_PATH.open(newline='', encoding='utf-8-sig') as f:
                rows = list(csv.DictReader(f))
            cols = list(rows[0].keys())
            sql = f"INSERT INTO cards ({','.join(cols)}) VALUES ({','.join('?' for _ in cols)})"
            conn.executemany(sql, [[r[c] for c in cols] for r in rows])
        if conn.execute('SELECT COUNT(*) FROM correspondences').fetchone()[0] == 0:
            with CORRESPONDENCES_PATH.open(newline='', encoding='utf-8-sig') as f:
                rows = list(csv.DictReader(f))
            cols = list(rows[0].keys())
            sql = f"INSERT INTO correspondences ({','.join(cols)}) VALUES ({','.join('?' for _ in cols)})"
            conn.executemany(sql, [[r[c] for c in cols] for r in rows])


def fetch_cards(db_path: str | Path | None = None) -> list[dict[str, Any]]:
    with connect(db_path) as conn:
        rows = conn.execute('SELECT * FROM cards ORDER BY CASE arcana WHEN \'Major\' THEN 0 ELSE 1 END, suit, rank').fetchall()
        return [dict(r) for r in rows]


def fetch_card(card_id: str, db_path: str | Path | None = None) -> dict[str, Any] | None:
    with connect(db_path) as conn:
        row = conn.execute('SELECT * FROM cards WHERE card_id = ?', (card_id,)).fetchone()
        return dict(row) if row else None


def create_reading(reading: dict, drawn_cards: list[dict], db_path: str | Path | None = None) -> int:
    with connect(db_path) as conn:
        cur = conn.execute('''INSERT INTO readings
            (question, life_domain, context, spread_type, draw_method, theme_tags)
            VALUES (?, ?, ?, ?, ?, ?)''',
            (reading['question'], reading['life_domain'], reading.get('context',''),
             reading['spread_type'], reading['draw_method'], reading.get('theme_tags','')))
        reading_id = int(cur.lastrowid)
        conn.executemany('''INSERT INTO reading_cards
            (reading_id, position_index, position_label, card_id, orientation)
            VALUES (?, ?, ?, ?, ?)''',
            [(reading_id, i, item['position_label'], item['card_id'], item['orientation'])
             for i, item in enumerate(drawn_cards, start=1)])
        return reading_id


def update_reading(reading_id: int, values: dict, card_updates: list[dict], db_path: str | Path | None = None) -> None:
    with connect(db_path) as conn:
        conn.execute('''UPDATE readings SET initial_observation=?, overall_interpretation=?,
            key_insight=?, action_commitment=?, follow_up_due=? WHERE reading_id=?''',
            (values.get('initial_observation',''), values.get('overall_interpretation',''),
             values.get('key_insight',''), values.get('action_commitment',''),
             values.get('follow_up_due') or None, reading_id))
        for item in card_updates:
            conn.execute('''UPDATE reading_cards SET visual_observation=?, personal_interpretation=?
                WHERE reading_id=? AND position_index=?''',
                (item.get('visual_observation',''), item.get('personal_interpretation',''),
                 reading_id, item['position_index']))


def save_review(values: dict, db_path: str | Path | None = None) -> None:
    with connect(db_path) as conn:
        conn.execute('''INSERT INTO study_reviews
            (card_id, quiz_score, quiz_total, recall_rating, minutes_spent, next_review_at, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)''',
            (values['card_id'], values['quiz_score'], values['quiz_total'], values['recall_rating'],
             values.get('minutes_spent'), values.get('next_review_at'), values.get('notes','')))


def save_followup(values: dict, db_path: str | Path | None = None) -> None:
    with connect(db_path) as conn:
        conn.execute('''INSERT INTO followups
            (reading_id, outcome_note, action_completed, alignment_rating, emotion_label)
            VALUES (?, ?, ?, ?, ?)''',
            (values['reading_id'], values.get('outcome_note',''), int(values.get('action_completed',False)),
             values.get('alignment_rating'), values.get('emotion_label','')))


def dataframe_query(sql: str, params: tuple = (), db_path: str | Path | None = None):
    import pandas as pd
    with connect(db_path) as conn:
        return pd.read_sql_query(sql, conn, params=params)


def save_lesson_completion(lesson_id: str, db_path: str | Path | None = None) -> None:
    with connect(db_path) as conn:
        conn.execute('INSERT OR IGNORE INTO lesson_progress (lesson_id) VALUES (?)', (lesson_id,))


def remove_lesson_completion(lesson_id: str, db_path: str | Path | None = None) -> None:
    with connect(db_path) as conn:
        conn.execute('DELETE FROM lesson_progress WHERE lesson_id = ?', (lesson_id,))


def completed_lessons(db_path: str | Path | None = None) -> set[str]:
    with connect(db_path) as conn:
        return {row[0] for row in conn.execute('SELECT lesson_id FROM lesson_progress').fetchall()}


def table_counts(db_path: str | Path | None = None) -> dict[str, int]:
    names = ['cards','correspondences','readings','reading_cards','study_reviews','followups','lesson_progress']
    with connect(db_path) as conn:
        return {name: int(conn.execute(f'SELECT COUNT(*) FROM {name}').fetchone()[0]) for name in names}
