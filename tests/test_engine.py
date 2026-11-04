import csv
import random
from pathlib import Path
import unittest

from src.tarot_engine import draw_cards, card_meaning, POSITION_LABELS

ROOT = Path(__file__).resolve().parents[1]
with (ROOT/'data'/'cards.csv').open(newline='',encoding='utf-8-sig') as f:
    CARDS = list(csv.DictReader(f))

class TarotEngineTests(unittest.TestCase):
    def test_deck_has_78_unique_cards(self):
        self.assertEqual(len(CARDS), 78)
        self.assertEqual(len({c['card_id'] for c in CARDS}), 78)

    def test_draw_has_no_duplicates(self):
        drawn = draw_cards(CARDS, 3, rng=random.Random(10))
        self.assertEqual(len(drawn), 3)
        self.assertEqual(len({c['card_id'] for c in drawn}), 3)

    def test_all_supported_spreads_have_defined_positions(self):
        self.assertEqual([len(v) for v in POSITION_LABELS.values()], [1, 3, 4, 5])
        self.assertEqual(len(POSITION_LABELS), 4)

    def test_orientation_meaning(self):
        five = next(c for c in CARDS if c['card_name']=='Five of Pentacles')
        self.assertIn('Recovery', card_meaning(five,'Reversed')['keywords'])

    def test_five_pentacles_golden_dawn_decan(self):
        five = next(c for c in CARDS if c['card_name']=='Five of Pentacles')
        self.assertEqual(five['astrological_correspondence'], 'Mercury in Taurus — decan 1 of 3')

if __name__ == '__main__':
    unittest.main()
