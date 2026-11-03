"""Shared text evidence and research regression tests; no OCR or model downloads."""
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

class SharedTextRulesTests(unittest.TestCase):
    def test_all_about_and_achievement_named_all_are_not_list_requests(self):
        from waypoint.assistant.rules.text import is_list_request,answer_budget
        from waypoint.assistant.web_lookup import verified_list
        articles=[{'title':'Buried Insight','item_names':['New Horizons'],'text':'facts'}]
        for question in ('What is Buried Insight all about?','Explain All Bets Are Off'):
            self.assertFalse(is_list_request(question));self.assertIsNone(verified_list(question,articles))
            self.assertEqual(answer_budget(question,articles),768)
        self.assertTrue(is_list_request('List all achievements'))

    def test_focused_achievement_retains_own_row_and_notes(self):
        from waypoint.assistant.rules.evidence import focus_articles
        article={'title':'Buried Insight','item_names':['Cleaning House','New Horizons'],
            'text':' | Cleaning House | category | 10\nDestroy cannons\n | New Horizons | category | 5\n | Follow Kalla and Poskk. Prerequisite: Buried Insight. | Hidden lab | 5\nFind the hidden lab.'}
        focused=focus_articles('How do I complete New Horizons?',[article])[0]
        self.assertIn('Requested achievement: New Horizons',focused['focus_text'])
        self.assertIn('Listed prerequisite: Buried Insight',focused['focus_text'])
        self.assertNotIn('Destroy cannons',focused['focus_text'])
        self.assertNotIn('focus_text',article)

    def test_structured_achievement_separates_prerequisite_from_own_objective(self):
        from waypoint.assistant.rules.evidence import focus_articles
        article={'title':'Buried Insight','item_names':['New Horizons'],'text':'\n | New Horizons | Category | 5\n | Follow clues from Kalla and Poskk. Story Instance: Buried Insight Prerequisite: Buried Insight Reward: Bag | Hidden lab | 5'}
        result=focus_articles('Help me complete New Horizons',[article])[0]
        self.assertIn('Listed prerequisite: Buried Insight',result['focus_text'])
        self.assertIn('Own objective: Follow clues from Kalla and Poskk.',result['focus_text'])
        self.assertNotIn('Reward: Bag',result['focus_text'])

    def test_mastery_keeps_trained_effect_and_notes_through_normal_compaction(self):
        from waypoint.assistant.rules.evidence import focus_articles
        from waypoint.inference.budget import compact
        from waypoint.assistant.web_lookup import context
        for title,effect,note in [
            ('Feline Reflexes','Jump in midair while riding the warclaw.','Downward velocity increases jump height.'),
            ('Rejuvenating Revival','Heal downed allies with Barrel Roll.','Revive Percentage: 25%'),
            ('Adept Handiworker Crafting','Purchase legendary components from Deft Lahar.','Levels Handiworker crafting to 399.')]:
            article={'title':title,'focus_text':f'Subject: {title} | Region: Example | Track: Example | Experience: 500,000',
                'text':f'Before completion: Learn example.\nAfter completion: {effect}\nNotes\n{note}\nExample mastery track\nOther ability'}
            result=focus_articles('What does '+title+' do?',[article])
            self.assertIn(effect,result[0]['text']);self.assertIn(note,result[0]['text'])
            for level in (1,2):
                self.assertIn(effect,compact('Player question: '+title+'\nEnd player question.\n'+context(result),level))
            self.assertNotIn('Other ability',result[0]['text'])

    def test_track_retains_every_retrieved_level_and_cost_before_descriptions(self):
        from waypoint.assistant.rules.evidence import focus_articles
        from waypoint.inference.budget import compact
        from waypoint.assistant.web_lookup import context
        rows=[f'Section: Example | Mastery: Level {i} | XP required: {i}00 | Points: {i} | Description: Learn ability {i}.' for i in range(1,7)]
        article={'title':'Regional tracks','text':'Unrelated track navigation','focus_text':'\n'.join(rows)}
        result=focus_articles('Explain Example mastery track',[article])
        reduced=compact('Player question: Example\nEnd player question.\n'+context(result),1)
        for i in range(1,7):
            self.assertIn(f'Mastery: Level {i}',reduced)
            self.assertIn(f'Points: {i} (cost)',reduced)
        self.assertIn('not cumulative',reduced);self.assertNotIn('Unrelated track navigation',reduced)

    def test_story_focus_retains_branch_notes_without_importing_next_achievement(self):
        from waypoint.assistant.rules.evidence import focus_articles
        article={'title':'Chapter','item_names':['Dug In','Other task'],'requested_subject':'Dug In',
            'text':' | Dug In | Category | 5\n | Build defenses. Story Instance: Chapter Prerequisite: Chapter Reward: Bag | Built defenses | 5\nChoose Explorer Metella and salvage supplies for the Point-Defense Turret.\nMutually exclusive with Search and Rescue.\n | Other task | Category | 5\nOther task walkthrough: unrelated mechanics.'}
        result=focus_articles('What should I do next?',[article])[0]
        self.assertIn('Explorer Metella',result['text']);self.assertIn('Point-Defense Turret',result['text'])
        self.assertIn('Mutually exclusive',result['text']);self.assertNotIn('unrelated mechanics',result['text'])
        self.assertIn('Perform inside story instance: Chapter',result['text'])

    def test_branch_comparison_keeps_established_goal_but_explicit_switch_wins(self):
        from waypoint.assistant.rules.evidence import focus_articles
        article={'title':'Chapter','item_names':['Dug In','Search and Rescue'],
            'text':' | Dug In | Category | 5\n | Defend the camp. | Done | 5\nMetella branch.\n | Search and Rescue | Category | 5\n | Rescue prisoners. | Done | 5\nLaranthir branch.'}
        history=[{'role':'user','text':'How do I complete Dug In? Which branch do I choose, and what completes it?'}]
        result=focus_articles('Should I choose Search and Rescue, or the camp-defense branch?',[article],history)[0]
        self.assertIn('Requested achievement: Dug In',result['text'])
        later=history+[{'role':'user','text':'Should I choose Search and Rescue, or the camp-defense branch?'}]
        self.assertIn('Requested achievement: Dug In',focus_articles('What comes next?',[article],later)[0]['text'])
        result=focus_articles('Switch my goal to Search and Rescue. Which branch?',[article],history)[0]
        self.assertIn('Requested achievement: Search and Rescue',result['text'])

    def test_name_only_collection_fragment_is_not_a_verified_achievement_guide(self):
        from waypoint.assistant.rules.evidence import focus_articles
        article={'title':'Category','item_names':['Aetherblade Assassin'],
            'text':'Objectives\n |\nAetherblade Assassin\n | ...\nUnrelated class description'}
        result=focus_articles('Explain Aetherblade Assassin',[article])[0]
        self.assertIn('name confirmed only',result['text']);self.assertNotIn('Unrelated class',result['text'])

    def test_explicit_requested_name_beats_parent_name_later_in_question(self):
        from waypoint.assistant.rules.evidence import focus_articles
        article={'title':'Parent','item_names':['Parent','Target'],
            'text':' | Parent | Category | 0\n | Finish parent. | Done | 0\n | Target | Category | 5\n | Find the secret. Prerequisite: Parent | Found | 5'}
        self.assertIn('Requested achievement: Target',focus_articles('Explain Target after Parent',[article])[0]['text'])

    def test_adventure_current_timer_and_labeled_silver_survive_compaction(self):
        from waypoint.assistant.rules.evidence import focus_articles
        from waypoint.inference.budget import compact
        from waypoint.assistant.web_lookup import context
        article={'title':'Fallen Masks','text':'Type Adventure Time limit 3:45\n | Reward tier | Masks soothed | Experience | Reward\n | Gold | 25 | 80,010 | Gold\n | Silver | 15 | 40,005 | Silver\n | Bronze | 10 | 26,670 | Gear\nHistorical increase: 45 seconds.'}
        articles=focus_articles('Fallen Masks Silver',[article])
        prompt='Player question: Fallen Masks Silver\nEnd player question.\n'+context(articles)
        for level in (1,2,3):
            reduced=compact(prompt,level)
            self.assertIn('Current time limit: 3:45',reduced)
            self.assertIn('Reward tier: Silver | Masks soothed: 15',reduced)

    def test_compaction_ranks_question_not_app_instructions(self):
        from waypoint.inference.budget import compact
        from waypoint.assistant.web_lookup import context
        prompt='Player question: Silver\nEnd player question.\n'+'Gold '*500+context([{'text':'Gold details.\nSilver: 15.'}])
        self.assertIn('Silver: 15',compact(prompt,3))


    def test_focus_removes_neighbor_details_and_disambiguates_time_reward_units(self):
        from waypoint.assistant.rules.evidence import focus_articles
        article={'title':'Fallen Masks','text':'Type Adventure Time limit 3:45\nGetting there\nTalk to the adventure NPC.\nMechanics\nBounce and glide.\nRewards\n | Reward tier | Masks soothed | Experience | Reward\n | Silver | 15 | 40,005 | Silver\nRelated achievements\nAstralaria I'}
        focused=focus_articles('Fallen Masks Silver',[article])[0]
        self.assertIn('3 minutes 45 seconds',focused['text'])
        self.assertIn('Reward XP (earned, not required)',focused['text'])
        self.assertNotIn('Astralaria',focused['text'])

    def test_safe_api_error_code_retained_without_remote_error_text(self):
        from waypoint.assistant.research import research
        from waypoint.assistant.web_lookup import WikiAPIError
        client=MagicMock();client.complete.return_value='{"game":"Guild Wars 2","query":"Example"}'
        with patch('waypoint.assistant.research.lookup',side_effect=WikiAPIError('missingtitle')):
            articles,notice=research(client,'Research Example',[])
        self.assertFalse(articles);self.assertIn('wiki API error missingtitle',notice)
        self.assertEqual(WikiAPIError('private text with spaces').code,'unknown')

    def test_maintenance_is_recognized_but_other_html_is_never_evidence(self):
        from waypoint.assistant.web_lookup import wiki_json,WikiMaintenanceError,maintenance_response
        maintenance=b'<html><title>The Guild Wars Wikis are undergoing maintenance.</title></html>'
        self.assertFalse(maintenance_response('unapproved.example',maintenance))
        for body,expected in ((maintenance,WikiMaintenanceError),(b'<title>Unrelated HTML</title>',ValueError)):
            with patch('waypoint.assistant.web_lookup.PinnedHTTPS') as connection:
                response=connection.return_value.getresponse.return_value
                response.status=200;response.getheader.return_value='text/html';response.read.return_value=body
                with self.assertRaises(expected):wiki_json('wiki.guildwars2.com','/api.php',{'action':'query'})
                response.read.assert_called_once_with(8192)
                connection.return_value.close.assert_called_once()

    def test_preflight_requires_valid_site_metadata(self):
        from waypoint.assistant.web_lookup import check_wiki_available
        with patch('waypoint.assistant.web_lookup.wiki_json',return_value={'query':{'general':{'sitename':'Guild Wars 2 Wiki'}}}):
            self.assertTrue(check_wiki_available())
        with patch('waypoint.assistant.web_lookup.wiki_json',return_value={}):
            with self.assertRaises(ValueError):check_wiki_available()

    def test_three_lookup_failures_stop_the_batch_including_maintenance(self):
        from waypoint.testing.text_sessions import run_sessions
        from waypoint.assistant.web_lookup import MAINTENANCE_NOTICE
        for notice in (MAINTENANCE_NOTICE,'Online lookup failed during wiki retrieval (ValueError).'):
            with TemporaryDirectory() as folder:
                player=MagicMock();player.complete.return_value='{"question":"What next?"}'
                assistant=MagicMock();assistant.chat.return_value=notice
                accounts=SimpleNamespace(snapshot=None,names={},selected_game='Guild Wars 2')
                result=run_sessions(player,lambda n:assistant,accounts,Path(folder)/'run',sessions=10,turns=5,delay=0,
                    plans=[{'name':'test','game':'Guild Wars 2','starter':'Help with gliding'}])
                self.assertEqual(result['cases'],3);self.assertEqual(result['stop_reason'],'source unavailable')

    def test_planner_failure_is_not_mislabeled_as_a_wiki_outage(self):
        from waypoint.testing.text_sessions import source_failed,lookup_failed
        answer='Online lookup failed during local lookup planning (ValueError).'
        self.assertTrue(lookup_failed(answer));self.assertFalse(source_failed(answer))


if __name__ == "__main__": unittest.main()
