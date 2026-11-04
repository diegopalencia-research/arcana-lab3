# ARCANA LAB v0.3 — Release notes

## Added

- New **Start here** landing page with a six-stage process map, progress metrics, recommended next lesson, module progress chart and three beginner entry routes.
- Optional **AI Guide** with Question Coach, Reading Interpreter and Study Tutor modes.
- OpenAI Responses API integration through the OpenAI Python SDK.
- API key loading through environment variables or Streamlit secrets; no secrets in source code.
- Session-only AI conversation history; bounded selected-reading/lesson context.
- Card keyword-orbit diagram with upright/reversed lens.
- Connected concept maps for foundation lessons.
- Suit-composition chart for every saved reading.
- Updated visual-first product and AI setup documentation.

## Compatibility

- The existing SQLite schema is unchanged; no database migration is required.
- The app remains usable without an API key.
- `requirements.txt` now includes the optional OpenAI SDK dependency.

## Validation

- Python compilation passed.
- Existing automated tests: 9/9 passed.
- Streamlit browser rendering and live OpenAI API requests were not run in this environment because Streamlit and the OpenAI SDK are not installed here. They will be installed from `requirements.txt` on deployment.
