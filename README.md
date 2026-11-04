# ARCANA LAB

**Personal Tarot Learning, Interpretation & Self-Reflection System**  
Prototype v0.3 · Python · Streamlit · SQLite · Pandas · Plotly · Optional OpenAI API

ARCANA LAB is a structured learning and reflection application built around a clear workflow:

**START → LEARN → ASK → PRACTICE → RECORD → OBSERVE**

- **Start here:** a guided entry page showing the full workflow, the next lesson and visual course progress.
- **Learn:** a sequential 93-lesson course, with keyword-orbit diagrams, connected concept maps, checkpoints and progress tracking.
- **AI Guide (optional):** Question Coach, Reading Interpreter and Study Tutor modes using the OpenAI API.
- **Practice:** four spreads with positional diagrams, suit-composition charts, card keywords, image cues, key insight and action.
- **Observe:** descriptive visualizations of study progress, reading activity, card/suit patterns, life domains and recorded actions.
- **Data:** SQLite backup and CSV exports.

Tarot is treated as a symbolic learning and self-reflection practice. The app does not diagnose psychological states, establish facts, make decisions for the user or predict future events.

## Design language

A typographic, data-led interface using IBM Plex Sans and IBM Plex Mono; dark charcoal, off-white and restrained element colors; thin rules, dot patterns and geometric diagrams. The interface avoids decorative card layouts, gradients and excessive theory. See `docs/PRODUCT_DESIGN_v0.3.md` and `docs/AI_GUIDE_SETUP_v0.3.md` for the product and AI setup specifications.

## Learning course

| Module | Lessons |
|---|---:|
| M01 — Foundations | 6 |
| M02 — Major Arcana | 22 |
| M03 — Minor Arcana framework | 4 |
| M04 — Wands | 14 |
| M05 — Cups | 14 |
| M06 — Swords | 14 |
| M07 — Pentacles | 14 |
| M08 — Integrated practice | 5 |
| **Total** | **93** |

## Reading spreads

| Spread | Positions |
|---|---:|
| Single-card focus | 1 |
| Three-card reflection | 3 |
| Decision compass | 4 |
| Five-point compass | 5 |

Every spread has a position diagram, shown before the draw and with the resulting cards. Interpretation is organized by position, keywords, image cue, personal reading, key insight and action.

## Quick start

Requirements: Python 3.10+ (3.11 recommended).

### Windows PowerShell

```powershell
cd arcana-lab
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

### macOS / Linux

```bash
cd arcana-lab
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

The local app normally opens at `http://localhost:8501`. SQLite is initialized automatically and seeded from `data/cards.csv` and `data/correspondences.csv`.

## Deploy with Streamlit Community Cloud

1. Push the contents of this folder to the root of a GitHub repository.
2. Confirm that `data/arcana_lab.db` and personal exports are not committed.
3. In [Streamlit Community Cloud](https://share.streamlit.io/), connect GitHub, select the repository and set `app.py` as the entrypoint.
4. Deploy.

Official instructions: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy

## Database and privacy

The app uses SQLite for the prototype. Hosted local storage should not be treated as durable; download backups from Data. For long-term cloud storage, add authentication and migrate to a managed PostgreSQL database before relying on hosted personal reading records. Do not upload the SQLite setup script unchanged to PostgreSQL; the dialect needs adaptation.

Keep `data/arcana_lab.db`, private reading exports, credentials and API keys out of the public repository. This remains a single-user prototype without authentication.

## Project structure

```text
arcana-lab/
├── app.py
├── requirements.txt
├── data/
│   ├── cards.csv
│   ├── correspondences.csv
│   └── deck_metadata.json
├── database/
│   ├── schema.sql
│   └── setup_arcana_lab.sql
├── docs/
│   ├── AI_GUIDE_SETUP_v0.3.md
│   ├── CARD_DATA_NOTES.md
│   ├── INTERPRETATION_PROTOCOL_v1.md
│   ├── PORTFOLIO_BRIEF.md
│   ├── PRODUCT_DESIGN_v0.2.md
│   └── PRODUCT_DESIGN_v0.3.md
├── src/
│   ├── ai_guide.py
│   ├── curriculum.py
│   ├── db.py
│   └── tarot_engine.py
└── tests/
    ├── test_ai_guide.py
```

## Correspondence policy

The dataset distinguishes suit-element correspondences from Golden Dawn / Book T card-specific attributions. Wands—Fire, Cups—Water, Swords—Air and Pentacles—Earth is one traditional model; other tarot schools may differ. Astrological correspondences are attributed to their named tradition and should not be presented as scientific facts.

## Tests

```bash
python -m unittest discover -s tests -v
```

## AI Guide setup

The AI Guide is optional. Add the following to `.streamlit/secrets.toml` locally, or to **App → Settings → Secrets** on Streamlit Community Cloud:

```toml
OPENAI_API_KEY = "your-api-key"
ARCANA_AI_MODEL = "gpt-6-astra"
```

The OpenAI Python SDK is installed through `requirements.txt`. Do not commit API keys. The AI receives the active prompt and only the selected reading or lesson context; it does not upload the complete SQLite database. Conversation history is session-only. Avoid entering sensitive personal information. ChatGPT subscriptions and API usage are billed separately. Full instructions are in `docs/AI_GUIDE_SETUP_v0.3.md`.

## Version 0.3 scope

Included: all v0.2 functionality; beginner onboarding; optional AI question coach, reading interpreter and study tutor; keyword-orbit diagrams; foundation concept maps; per-reading suit-composition chart; visual-first design specification.

Not included: user accounts, durable cloud persistence, AI-powered prediction, card-image recognition or multi-user access.
