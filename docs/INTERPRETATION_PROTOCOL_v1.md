# ARCANA LAB — Interpretation Protocol v1.0

## Purpose

Use tarot imagery and a documented symbolic vocabulary as a structured prompt for reflective inquiry. This protocol supports learning and journaling; it is not a clinical assessment or a method for establishing facts or predicting events.

## Unit of analysis

A **reading** is one dated question, context, spread definition and ordered set of card-position observations. A reading is not treated as a verified explanation of the user's psychology or circumstances.

## Standard sequence

1. **Question:** write one open question in plain language.
2. **Context:** record a brief factual description; distinguish known facts from assumptions.
3. **Spread:** select a structure whose positions match the question.
4. **Draw:** record whether cards came from the app's random draw or a physical deck; record orientation.
5. **Observe:** describe visible objects, people, gestures, setting and spatial relationships before interpreting.
6. **Reference:** review the upright/reversed keyword cluster and, when useful, the named correspondence system.
7. **Interpret:** write a personal interpretation for each position. Treat it as a hypothesis or reflection, not a verdict.
8. **Synthesize:** identify continuity, contrast or repetition across the positions. Do not merely concatenate card definitions.
9. **Insight:** write one sentence that captures the most useful point of attention.
10. **Action:** record one small, observable action under the user's control.
11. **Follow-up:** record what happened, whether the action was completed and what was learned.

## Supported spreads

| Spread | Position sequence | Intended use |
|---|---|---|
| Single-card focus | Focus | Identify one point of attention. |
| Three-card reflection | Current state → What to understand → Conscious next step | Move from observation to insight and action. |
| Decision compass | Option A → Option B → Decision criteria → Next step | Compare trade-offs and clarify decision criteria without outsourcing the choice. |
| Five-point compass | Situation → Resources → Tension → Perspective → Action | Map the situation and identify a grounded response. |

Every spread is represented by a positional diagram in the app. Diagram geometry indicates relationships between positions; it is not a claim about causal relationships.

## Interpretation rules

- Read the spread position before the card keyword.
- Treat traditional meanings as a reference vocabulary, not a verdict.
- Treat reversals as an alternate expression (blockage, excess, internalization or reorientation), not automatically as an exact opposite.
- Separate image observation, traditional meaning, personal interpretation and action.
- Do not infer clinical diagnoses, hidden facts about other people or guaranteed outcomes.
- Do not equate repeated card frequency with an objective trait or causal explanation.
- Name the correspondence tradition. Golden Dawn / Book T is optional and not universal.

## Measurement rules

Learning outcomes may be quantified: lesson completion, quiz accuracy, review count, recall rating, study time and suggested review intervals. Reflective content may be summarized through self-selected themes and life domains. These are descriptive self-records, not psychometric measurements.

## Data quality

- Use ISO dates and preserve the wording of the original question.
- Keep card IDs stable and orientations constrained to `Upright` or `Reversed`.
- Record manual versus random draws. A physical deck draw should not contain duplicate cards.
- Preserve original interpretations when revisiting; add a follow-up record instead.
- Back up the SQLite database before schema changes or imports.
