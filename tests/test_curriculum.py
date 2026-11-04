import csv
from pathlib import Path
import unittest
from src.curriculum import build_curriculum


class CurriculumTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = Path(__file__).resolve().parents[1] / 'data' / 'cards.csv'
        with path.open(encoding='utf-8-sig', newline='') as f:
            cls.cards = list(csv.DictReader(f))

    def test_course_is_complete_and_sequential(self):
        lessons = build_curriculum(self.cards)
        self.assertEqual(len(lessons), 93)
        self.assertEqual([x['sequence'] for x in lessons], list(range(1, 94)))
        self.assertEqual(len({x['lesson_id'] for x in lessons}), 93)

    def test_card_lessons_cover_all_78_cards_once(self):
        lessons = build_curriculum(self.cards)
        card_lessons = [x for x in lessons if x['kind'] == 'card']
        self.assertEqual(len(card_lessons), 78)
        self.assertEqual(len({x['card_id'] for x in card_lessons}), 78)

    def test_curriculum_modules_are_ordered(self):
        lessons = build_curriculum(self.cards)
        module_order = list(dict.fromkeys(x['module_id'] for x in lessons))
        self.assertEqual(module_order, ['M01','M02','M03','M04','M05','M06','M07','M08'])


if __name__ == '__main__':
    unittest.main()
