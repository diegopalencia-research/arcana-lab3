from __future__ import annotations
import random

# Four compact, reflective spreads. The positions—not a card's definition alone—
# determine the lens through which its keywords are considered.
POSITION_LABELS = {
    'Single-card focus': [
        ('Focus', 'What deserves my attention?'),
    ],
    'Three-card reflection': [
        ('Current state', 'What is happening within me or around this situation?'),
        ('What to understand', 'What pattern, tension or perspective deserves attention?'),
        ('Conscious next step', 'What is one grounded action I can take?'),
    ],
    'Decision compass': [
        ('Option A', 'What does this option ask of me or make possible?'),
        ('Option B', 'What does this option ask of me or make possible?'),
        ('Decision criteria', 'Which value, resource or constraint should guide the choice?'),
        ('Next step', 'What can I clarify or do before deciding?'),
    ],
    'Five-point compass': [
        ('Situation', 'What is the central situation or question?'),
        ('Resources', 'What strength, support or resource is available?'),
        ('Tension', 'What friction or limitation needs attention?'),
        ('Perspective', 'What alternative view might I be missing?'),
        ('Action', 'What is the most useful next step within my control?'),
    ],
}

SPREAD_DESCRIPTIONS = {
    'Single-card focus': 'One symbol. One clear point of attention.',
    'Three-card reflection': 'A sequence: observe → understand → act.',
    'Decision compass': 'Compare options through values and practical criteria; do not ask the cards to choose for you.',
    'Five-point compass': 'Map the situation, resources, friction, perspective and a grounded action.',
}


def draw_cards(cards: list[dict], count: int = 3, reversed_probability: float = 0.5,
               rng: random.Random | None = None) -> list[dict]:
    """Draw unique cards and assign orientation; randomness is illustrative, not predictive."""
    if not 1 <= count <= len(cards):
        raise ValueError('count must be between 1 and the number of available cards')
    if not 0 <= reversed_probability <= 1:
        raise ValueError('reversed_probability must be between 0 and 1')
    rng = rng or random.Random()
    selected = rng.sample(cards, count)
    return [{**card, 'orientation': 'Reversed' if rng.random() < reversed_probability else 'Upright'}
            for card in selected]


def card_meaning(card: dict, orientation: str) -> dict:
    """Return concise stored meanings for one card orientation."""
    if orientation not in {'Upright', 'Reversed'}:
        raise ValueError('orientation must be Upright or Reversed')
    suffix = 'upright' if orientation == 'Upright' else 'reversed'
    astrology = card.get('astrological_correspondence')
    system = card.get('correspondence_system')
    if not isinstance(astrology, str) or not astrology.strip():
        astrology = 'Not assigned'
    if not isinstance(system, str) or not system.strip():
        system = 'Not specified'
    return {
        'keywords': card[f'{suffix}_keywords'],
        'technical': card[f'technical_{suffix}'],
        'simple': card['child_explanation'],
        'astrology': astrology,
        'system': system,
    }


def build_reflection_prompt(question: str, position_label: str, card: dict,
                            orientation: str) -> str:
    meaning = card_meaning(card, orientation)
    return (
        f"Question: {question}\nPosition: {position_label}\n"
        f"Card: {card['card_name']} ({orientation})\n"
        f"Keywords: {meaning['keywords']}\n"
        f"Reflect on: {card['reflection_prompt_1']} {card['reflection_prompt_2']}"
    )
