import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from waypoint.integrations.story_achievements import load_story_table,selected_story
from waypoint.assistant.achievement_intro import AchievementIntro

TABLE={'categories':[{'category_id':188,'category_name':'Path of Fire: Act 1',
        'achievements':[{'id':1,'name':'Night of Fires'},{'id':2,'name':'Other chapter task'}]}],
       'chapters':[{'story_id':82,'title':'Night of Fires','season':'Path of Fire','category_id':188,
                    'quests':[{'quest_id':486,'title':'Night of Fires'}],'chapter_achievement_ids':[1]}]}
SNAPSHOT={'fetched_at':'2026-10-18T16:00:00+00:00','records':[{'id':2,'done':True}]}

class StoryTests(unittest.TestCase):
    def test_catalog_covers_seasons_and_expansions_with_auditable_links(self):
        table=load_story_table()
        self.assertTrue({'Living World Season 1','Living World Season 2','Living World Season 3',
            'Living World Season 4','The Icebrood Saga','Heart of Thorns','Path of Fire','End of Dragons',
            'Secrets of the Obscure','Janthir Wilds','Visions of Eternity'}.issubset({c['season'] for c in table['chapters']}))
        categories={c['category_id']:c for c in table['categories']}
        for chapter in table['chapters']:
            self.assertIn(chapter['category_id'],categories)
            self.assertTrue(set(chapter['chapter_achievement_ids']).issubset({a['id'] for a in categories[chapter['category_id']]['achievements']}))
        self.assertTrue(table['unresolved_chapters'])

    def test_selected_title_is_not_instance_confirmation(self):
        result=selected_story({'visible_text':['Story chapter: Night of Fires']},SNAPSHOT,TABLE)
        self.assertIn('unconfirmed',result['instance_state'])
        self.assertEqual((result['completed'],result['total']),(1,2))
        self.assertEqual([a['id'] for a in result['unfinished_chapter_achievements']],[1])

    def test_watch_list_and_partial_names_do_not_match(self):
        for label in ('Night of Fires','Story chapter: Nightfall','Story chapter: Night of Fire'):
            self.assertIsNone(selected_story({'visible_text':[label]},SNAPSHOT,TABLE))

    def test_no_account_still_identifies_story_but_never_invents_progress(self):
        result=selected_story({'visible_text':['Story chapter: Night of Fires']},None,TABLE)
        self.assertEqual(result['category_id'],188); self.assertNotIn('completed',result)

    def test_story_intro_labels_category_and_stays_once_per_session(self):
        maps={'verified_at':'test','maps':[]};intro=AchievementIntro(maps,TABLE)
        observation={'visible_text':['Story chapter: Night of Fires'],'map':None}
        self.assertIsNone(intro.consider(observation,1,SNAPSHOT))
        message=intro.consider(observation,2,SNAPSHOT)
        self.assertIn('1/2',message);self.assertIn('Path of Fire: Act 1',message)
        self.assertIn('selected chapter: Night of Fires',message)
        self.assertIsNone(intro.consider(observation,3,SNAPSHOT))
