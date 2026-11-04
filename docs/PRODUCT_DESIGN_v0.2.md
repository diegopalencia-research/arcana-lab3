# ARCANA LAB — Product and visual specification v0.2

## Product direction

ARCANA LAB is a personal tarot learning, interpretation and self-reflection system. It is designed as a compact symbolic study instrument—not a tarot encyclopedia, fortune-telling service or decorative spiritual app.

**Core workflow:** LEARN → PRACTICE → RECORD → OBSERVE.

## 1. Visual system

- Typographic-first interface using IBM Plex Sans and IBM Plex Mono.
- Dark charcoal background, off-white text, muted metadata and restrained accent color.
- Flat layout, thin rules, aligned labels and square geometry; avoid rounded cards, gradients, shadows and ornamental panels.
- Dot field and geometric orbital marks provide a subtle nature/technology visual language.
- Data visualizations should communicate an actual measure or relationship. No decorative charts.

### Element color key

| Element | Color | Use |
|---|---|---|
| Fire | `#D49A55` | Wands |
| Water | `#78A8B8` | Cups |
| Air | `#B8C6CE` | Swords |
| Earth | `#94A47C` | Pentacles |
| Major Arcana | `#C1B39A` | Major Arcana cards |

Colors identify a category, not a value judgement or emotional score.

## 2. Learning curriculum

The Learn workspace contains a sequential 93-lesson pathway across eight modules:

1. Foundations — 6 lessons
2. Major Arcana — 22 card lessons
3. Minor Arcana framework — 4 lessons
4. Wands — 14 card lessons
5. Cups — 14 card lessons
6. Swords — 14 card lessons
7. Pentacles — 14 card lessons
8. Integrated practice — 5 lessons

Every lesson presents a learning objective, key points, a practice prompt or card-specific material, and a completion checkpoint. Card lessons also include upright/reversed keywords, imagery observation, a concise plain-language explanation, correspondence metadata and a retrieval check. Completion is tracked locally in SQLite.

## 3. Reading experience

Every spread has a positional diagram shown before card selection and again with selected cards after the draw.

| Spread | Positions | Reading logic |
|---|---:|---|
| Single-card focus | 1 | Focus |
| Three-card reflection | 3 | Current state → What to understand → Conscious next step |
| Decision compass | 4 | Option A → Option B → Decision criteria → Next step |
| Five-point compass | 5 | Situation → Resources → Tension → Perspective → Action |

The interpretation display prioritizes:

- spread position and its question;
- card name and orientation;
- concise keyword cluster;
- visible image cue;
- personal interpretation;
- one-sentence key insight;
- one action within the user's control.

Long theory and correspondence detail are secondary. The user remains the interpreter.

## 4. Personal observatory

The Observe workspace shows descriptive metrics only: reading volume, cards drawn, study progress, suit distribution, life-domain distribution, reading activity, recurring cards, self-selected themes and retrieval-check performance.

No chart is presented as a psychological diagnosis, causal relationship or prediction.

## 5. Data and privacy

- SQLite remains the local development database.
- `lesson_progress` records completed curriculum lesson IDs.
- Private reading content and exports must not be committed to GitHub.
- Streamlit Community Cloud local storage is not durable. Add authentication and a managed database before relying on hosted personal records.
- Correspondence data must retain a named tradition/system; esoteric correspondences are not scientific findings or universal tarot rules.

## 6. Implementation boundaries

Version 0.2 is still a single-user prototype. It does not include user accounts, cloud synchronization, AI-generated readings, image recognition or predictive claims. The interpretation workflow is intentionally transparent and user-led.
