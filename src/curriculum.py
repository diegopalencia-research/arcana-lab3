"""A structured, sequential 93-lesson tarot learning pathway."""
from __future__ import annotations

FOUNDATION = [
    ("Start here: how to use ARCANA LAB", "Understand the workflow and the limits of the tool.",
     ["Learn the system; do not outsource judgment.", "Use symbols as prompts, not evidence of external facts.", "End every reading with one proportionate action."],
     "Write one sentence describing what you want to learn from tarot."),
    ("The architecture of a 78-card deck", "Distinguish Major Arcana, Minor Arcana, suits and court cards.",
     ["22 Major Arcana cards: broad archetypal themes.", "40 numbered Minor Arcana cards: Ace through Ten in four suits.", "16 court cards: Page, Knight, Queen and King in each suit."],
     "Explain the difference between Major and Minor Arcana without using the words 'important' or 'less important'."),
    ("Ask a useful question", "Turn vague or predictive questions into reflective questions.",
     ["Ask what to notice, understand, consider or do.", "Separate known facts from assumptions.", "Avoid yes/no questions when a decision framework is more useful."],
     "Rewrite: 'Will everything work out?' as a question that gives you agency."),
    ("Read the spread position first", "Understand how a card's meaning changes with its assigned role.",
     ["Position = the lens; card = the symbol; context = the application.", "Do not read every card as a free-floating definition.", "Read the spread as a relationship between positions."],
     "Choose one position from a three-card spread and explain what question it asks."),
    ("Observe the image before the keyword", "Build visual literacy before consulting a memorized meaning.",
     ["Notice people, posture, objects, direction, contrast and movement.", "Describe what is visible before deciding what it means.", "Distinguish observation from interpretation."],
     "Look at one card for 30 seconds. Record three visible details without interpreting them."),
    ("Upright and reversed cards", "Use orientation as a modifier rather than a simplistic opposite.",
     ["A reversal may suggest blockage, excess, internalization or an alternate expression.", "The question and position determine which possibility is useful.", "A reversed card is not automatically negative."],
     "Give two possible readings of a reversed card that are not simply its opposite."),
]

MINOR_FOUNDATION = [
    ("The four suits and their elements", "Recognize the four suit families and their traditional elemental model.",
     ["Wands / Fire: initiative, energy, creation.", "Cups / Water: feeling, connection, receptivity.", "Swords / Air: thought, language, discernment.", "Pentacles / Earth: resources, body, work, material conditions."],
     "Name one real-life situation that could be explored through each suit."),
    ("Number patterns: Ace through Ten", "Use number as a second interpretive layer across the Minor Arcana.",
     ["Ace: seed or opening; Two: polarity; Three: development; Four: structure.", "Five: friction; Six: adjustment; Seven: test; Eight: movement or practice.", "Nine: culmination; Ten: completion, load or transition."],
     "Compare the Five of Wands and Five of Cups: what stays constant, and what changes with the suit?"),
    ("Court cards: Page, Knight, Queen, King", "Read court cards as roles, approaches or modes of expression.",
     ["Page: learning and discovery.", "Knight: pursuit and movement.", "Queen: internal mastery and cultivation.", "King: direction, responsibility and outward command."],
     "Describe how a Page and a King might approach the same challenge differently."),
    ("Combine suit, number and position", "Build a concise interpretation from several layers without overloading it.",
     ["Start with the spread position.", "Add suit and number/rank.", "Use the card's keywords and image to refine the meaning.", "Apply only correspondences that belong to a named tradition."],
     "Choose one Minor Arcana card and explain it in three layers: suit, number and position."),
]

APPLICATION = [
    ("A complete three-card reading", "Move from individual card meanings to a coherent sequence.",
     ["Read each position independently first.", "Look for continuity, contrast and repetition.", "Summarize the sequence in one sentence."],
     "Use the pattern: current state → what to understand → conscious next step."),
    ("Compare options without predicting", "Use a spread to clarify trade-offs and decision criteria.",
     ["Compare options against values, resources and constraints.", "Do not treat a card as an instruction or guarantee.", "The final decision remains yours."],
     "Name one criterion that matters more than short-term comfort."),
    ("Synthesize keywords into an insight", "Create a useful interpretation without writing an essay.",
     ["Select the strongest keyword from each position.", "Identify the relationship between them.", "State the insight in one clear sentence."],
     "Write a synthesis of no more than 25 words."),
    ("Turn insight into an action", "Translate reflection into a realistic, observable next step.",
     ["Choose an action inside your control.", "Make it small enough to complete.", "Set a review date and record what actually happened."],
     "Define one action, a deadline and what observable completion looks like."),
    ("Ethics, uncertainty and follow-up", "Use tarot responsibly and evaluate the usefulness of your process.",
     ["Tarot is not a diagnostic or evidence-generating method.", "Do not use it as a substitute for professional, legal, medical or financial advice.", "Evaluate clarity, learning and actions—not predictive accuracy."],
     "Write one boundary you will keep when using tarot."),
]

SUITS = ["Wands", "Cups", "Swords", "Pentacles"]


def _lesson(lesson_id, module_id, module_title, seq, title, kind, objective, key_points, exercise, card_id=None):
    return {
        "lesson_id": lesson_id,
        "module_id": module_id,
        "module_title": module_title,
        "sequence": seq,
        "title": title,
        "kind": kind,
        "objective": objective,
        "key_points": key_points,
        "exercise": exercise,
        "card_id": card_id,
    }


def build_curriculum(cards: list[dict]) -> list[dict]:
    """Build a deterministic course ordered from foundations to full readings."""
    lessons = []
    seq = 1
    modules = [
        ("M01", "Foundations", FOUNDATION),
    ]
    for module_id, module_title, items in modules:
        for i, (title, objective, points, exercise) in enumerate(items, 1):
            lessons.append(_lesson(f"{module_id}-L{i:02}", module_id, module_title, seq, title,
                                   "foundation", objective, points, exercise))
            seq += 1

    major = sorted([c for c in cards if c.get("arcana") == "Major"], key=lambda c: int(c.get("rank", 0)))
    for i, card in enumerate(major, 1):
        lessons.append(_lesson(f"M02-L{i:02}", "M02", "Major Arcana", seq, card["card_name"],
                               "card", "Study the archetype, image, keywords and orientation of this card.",
                               ["Begin with the spread position.", "Observe the image before consulting the meaning.", "Compare upright and reversed keywords."],
                               "Describe one visible symbol and connect it to one keyword.", card["card_id"]))
        seq += 1

    for i, (title, objective, points, exercise) in enumerate(MINOR_FOUNDATION, 1):
        lessons.append(_lesson(f"M03-L{i:02}", "M03", "Minor Arcana framework", seq, title,
                               "foundation", objective, points, exercise))
        seq += 1

    for suit_index, suit in enumerate(SUITS, 4):
        module_id = f"M{suit_index:02}"
        module_title = f"{suit} suit"
        suit_cards = sorted([c for c in cards if c.get("suit") == suit], key=lambda c: int(c.get("rank", 0)))
        for i, card in enumerate(suit_cards, 1):
            lessons.append(_lesson(f"{module_id}-L{i:02}", module_id, module_title, seq, card["card_name"],
                                   "card", f"Understand how {suit.lower()} expresses this card's number or court role.",
                                   [f"Suit: {suit}.", "Read number/rank and position together.", "Use the image to make the meaning specific."],
                                   "Explain this card in one sentence using its suit and one keyword.", card["card_id"]))
            seq += 1

    for i, (title, objective, points, exercise) in enumerate(APPLICATION, 1):
        lessons.append(_lesson(f"M08-L{i:02}", "M08", "Integrated practice", seq, title,
                               "application", objective, points, exercise))
        seq += 1
    return lessons
