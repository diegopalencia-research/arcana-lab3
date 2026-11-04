# ARCANA LAB — Product and visual specification v0.3

## Product direction

ARCANA LAB is a visual learning and reflective analysis environment for Tarot. It combines a sequenced course, an optional AI guide, diagram-led readings, a personal journal and a descriptive data observatory.

**Primary workflow:** START → LEARN → ASK → PRACTICE → RECORD → OBSERVE.

A new user must be able to open the application and understand what to do next without knowing tarot terminology.

## 1. Entry experience

The default page is **Start here**. It presents:

- a six-stage workflow diagram;
- current learning and reading metrics;
- the next recommended lesson;
- a module-level course progress chart;
- three clear entry paths: beginner, question-led, or user has already drawn cards.

The Learn module remains sequential. The AI Guide is available as an optional second pathway, not a requirement.

## 2. AI Guide

Three bounded assistant roles:

- **Question Coach:** refine vague thoughts into open questions; recommend a spread based on the kind of reflection required.
- **Reading Interpreter:** examine a selected saved reading with the actual spread positions and stored card data; identify possible patterns, contrasts and actions.
- **Study Tutor:** explain the current course lesson, give examples and test retrieval.

The AI is user-led, non-predictive and transparent about uncertainty. It must not claim that a card establishes a fact or reveals another person's hidden thoughts. Its outputs are short, structured and diagram-oriented.

AI requires an optional OpenAI API key. No key is stored in the codebase or GitHub. The local application is functional without AI.

## 3. Visualization-first interface

The visual representation is the default way to communicate information. Every content type should use the most meaningful visual form:

| Information | Preferred representation |
|---|---|
| Learning journey | Ordered pathway and module-progress chart |
| Single-card study | Keyword orbit, card metadata, image cue |
| Tarot spread | Positional geometric diagram |
| Reading composition | Suit/element distribution chart |
| Interpretation | Position matrix, keyword sequence and action map |
| Study progress | Completion and retrieval charts |
| Personal patterns | Frequency, time-series, distribution and domain charts |
| Data relationships | Geometric maps and network diagrams where useful |

Avoid charts without an analytical purpose. Keep prose short, use keyword labels, and provide enough text for accessibility and interpretation.

## 4. Visual identity

- IBM Plex Sans + IBM Plex Mono.
- Charcoal background, warm off-white, thin rules and subdued metadata.
- Restrained accents: Fire amber, Water blue, Air silver, Earth olive, Major Arcana warm stone.
- Geometric vocabulary: orbital rings, nodes, radial structures, grids, point patterns, axes and connected sequences.
- No decorative gradients, ornamental cards, excessive rounded panels, gamification or chart clutter.
- Visuals must encode structure or data, not imply supernatural causation.

## 5. Reading model

Question/context → spread choice → position → card/orientation → stored symbolism → user interpretation → optional AI hypotheses → key insight → user action → later follow-up.

The user retains interpretive agency. AI-generated suggestions are hypotheses, not authoritative meanings. Do not score predictive accuracy.

## 6. Data and privacy

SQLite remains the prototype database. The AI receives only the current prompt plus bounded context for the selected role. Reading Interpreter sends only the selected reading and related card metadata; it does not upload the entire database. Conversation history is session-only.

API keys must be stored in Streamlit secrets or environment variables. Private user records must not be committed to GitHub. Hosted SQLite is not durable; use managed PostgreSQL before relying on cloud persistence.

## 7. Technical boundaries

- Python, Streamlit, SQLite, Pandas and Plotly.
- Optional OpenAI Python SDK using the Responses API.
- Model selection via `ARCANA_AI_MODEL`; default `gpt-6-astra`.
- The application must run without an API key.
- AI use is optional and API charges are separate from ChatGPT billing.
- Tarot remains a symbolic self-reflection practice, never a clinical or predictive instrument.
