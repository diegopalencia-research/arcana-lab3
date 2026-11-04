import os
import unittest
from unittest.mock import patch

from src.ai_guide import _transcript, get_api_key, get_model


class AIGuideTests(unittest.TestCase):
    def test_api_key_reads_environment(self):
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-secret'}, clear=False):
            self.assertEqual(get_api_key(), 'test-secret')

    def test_model_is_configurable(self):
        with patch.dict(os.environ, {'ARCANA_AI_MODEL': 'test-model'}, clear=False):
            self.assertEqual(get_model(), 'test-model')

    def test_transcript_uses_recent_context(self):
        history = [{'role': 'user', 'content': f'question {i}'} for i in range(10)]
        result = _transcript(history, 'latest question')
        self.assertNotIn('question 0', result)
        self.assertIn('question 9', result)
        self.assertIn('latest question', result)


if __name__ == '__main__':
    unittest.main()
