import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from waypoint.assistant.achievement_intro import AchievementIntro

TABLE={'verified_at':'test','maps':[{'map_name':'Test Map','category_id':1,'achievements':[{'id':1},{'id':2}]}],
       'episode_categories':[{'category_name':'Sky Pirates','achievements':[{'id':3}]}]}
SNAPSHOT={'fetched_at':'2026-10-17T15:00:00+00:00','records':[{'id':1,'done':True},
          {'id':2,'done':False,'current':10,'max':10},{'id':3,'done':True}]}

class IntroTests(unittest.TestCase):
    def test_two_distinct_observations_then_one_message_only(self):
        intro=AchievementIntro(TABLE); obs={'map':'Test Map','summary':'Player exploring.'}
        self.assertIsNone(intro.consider(obs,1,SNAPSHOT))
        self.assertIsNone(intro.consider(obs,1,SNAPSHOT))
        message=intro.consider(obs,2,SNAPSHOT)
        self.assertIn('1/2',message); self.assertNotIn('Based on your account snapshot',message)
        self.assertIsNone(intro.consider(obs,3,SNAPSHOT))

    def test_options_and_unstable_map_do_not_notify(self):
        intro=AchievementIntro(TABLE)
        for stamp in (1,2):
            self.assertIsNone(intro.consider({'map':'Test Map','summary':'Options menu.'},stamp,SNAPSHOT))
        self.assertIsNone(intro.consider({'map':'Test Map','summary':'Player exploring.'},3,SNAPSHOT))
        self.assertIsNone(intro.consider({'map':None,'summary':'Unknown location.'},4,SNAPSHOT))
        self.assertIsNone(intro.consider({'map':'Test Map','summary':'Player exploring.'},5,SNAPSHOT))

    def test_readable_displayed_map_announces_without_assuming_player_location(self):
        intro=AchievementIntro(TABLE)
        message=intro.consider({'map':None,'summary':'Viewing the world map.',
                               'visible_text':['Map displayed: Test Map']},1,SNAPSHOT)
        self.assertIn('For the displayed map:',message)
        self.assertIn('1/2',message)
        self.assertIsNone(intro.consider({'map':'Test Map'},2,SNAPSHOT))

    def test_missing_account_or_unsupported_map_is_not_zero_progress(self):
        intro=AchievementIntro(TABLE)
        for stamp in (1,2):
            self.assertIsNone(intro.consider({'map':'Test Map'},stamp,None))
        self.assertFalse(intro.sent)

    def test_season_one_requires_explicit_header_and_labels_episode(self):
        intro=AchievementIntro(TABLE)
        self.assertIsNone(intro.consider({'map':None,'visible_text':['Sky Pirates']},1,SNAPSHOT))
        obs={'map':None,'visible_text':['Story episode: Sky Pirates']}
        self.assertIsNone(intro.consider(obs,2,SNAPSHOT))
        message=intro.consider(obs,3,SNAPSHOT)
        self.assertIn('1/1',message); self.assertIn('episode category',message)
