import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from waypoint.assistant.grounding import gold_reading,guard_screen_stats
from waypoint.assistant.routing import needs_screen,force_new_analysis

class GroundingTests(unittest.TestCase):
    def test_recheck_gold_requires_new_analysis(self):
        question='Check again and confirm I have 58 gold'
        self.assertTrue(needs_screen(question)); self.assertTrue(force_new_analysis(question))
    def test_desired_amount_not_used_as_evidence(self):
        answer=gold_reading({'visible_text':['Gold: 57']},'Confirm I have 58 gold',20)
        self.assertIn('57 gold',answer); self.assertNotIn('58 gold',answer)
    def test_missing_currency_does_not_invent_other_stats(self):
        answer=gold_reading({'visible_text':['Level: 80']},'Confirm I have 58 gold',20)
        self.assertIn("can't reliably read",answer); self.assertNotIn('80',answer)
    def test_unsupported_level_blocked(self):
        answer=guard_screen_stats('You are currently Level 100 with 112.2% HP',{'visible_text':['Inventory']},'Guild Wars 2')
        self.assertNotIn('Level 100',answer)
    def test_invalid_player_level_even_if_ocr_reports_it(self):
        answer=guard_screen_stats('You are currently Level 110',{'visible_text':['Level 110']},'GW2')
        self.assertIn('invalid GW2',answer)

    def test_other_game_does_not_inherit_character_level_limit(self):
        answer='You are currently Level 110'
        self.assertEqual(guard_screen_stats(answer,{'visible_text':['Level 110']},'Example Adventure'),answer)
