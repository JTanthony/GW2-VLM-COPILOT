import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from waypoint.assistant.routing import is_greeting,needs_screen

class RoutingTests(unittest.TestCase):
    def test_greeting_does_not_require_screen(self):
        self.assertTrue(is_greeting('Hello!'))
        self.assertFalse(needs_screen('Hello!'))
    def test_screen_question_requires_evidence(self):
        self.assertFalse(is_greeting('Hello, what do you see on screen?'))
        self.assertTrue(needs_screen('Hello, what do you see on screen?'))
    def test_general_question_can_use_text_chat(self):
        self.assertFalse(needs_screen('Can you explain crafting?'))
