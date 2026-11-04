from pathlib import Path
import tempfile
import unittest
from src.db import init_db, table_counts, fetch_cards, create_reading, save_lesson_completion, completed_lessons

class DatabaseTests(unittest.TestCase):
    def test_seed_and_create_reading(self):
        with tempfile.TemporaryDirectory() as td:
            db = Path(td)/'test.sqlite'
            init_db(db)
            self.assertEqual(table_counts(db)['cards'],78)
            cards=fetch_cards(db)
            selected=cards[0]
            rid=create_reading({'question':'What should I understand?','life_domain':'Other',
                'spread_type':'Single-card focus','draw_method':'test'},
                [{'card_id':selected['card_id'],'orientation':'Upright','position_label':'Focus'}],db)
            self.assertEqual(table_counts(db)['readings'],1)
            self.assertGreater(rid,0)
            save_lesson_completion('M01-L01', db)
            self.assertIn('M01-L01', completed_lessons(db))
            self.assertEqual(table_counts(db)['lesson_progress'], 1)

if __name__ == '__main__':
    unittest.main()
