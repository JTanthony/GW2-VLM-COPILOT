import json,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import MagicMock
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from waypoint.testing.text_sessions import scenarios,validate_question,run_sessions,findings,title_scenarios,next_question
from waypoint.integrations.accounts import Accounts

class TextSessionTests(unittest.TestCase):
    def test_player_invented_quoted_topic_recovers(self):
        player=MagicMock(); player.complete.return_value=json.dumps({'question':'How do I finish "Imaginary Quest"?'})
        question,note=next_question(player,'Verdant Brink',[],1)
        self.assertNotIn('Imaginary',question); self.assertIn('unsupported',note)
    def test_duplicate_player_question_replaced_with_useful_followup(self):
        player=MagicMock(); player.complete.return_value='{"question":"What next?"}'
        question,note=next_question(player,'scenario',[{'question':'What next?'}],1)
        self.assertNotEqual(question,'What next?'); self.assertIn('repeated',note)
    def test_truncated_player_response_is_distinct_from_other_failures(self):
        player=MagicMock(); player.complete.side_effect=ValueError('Incomplete model response: length')
        question,note=next_question(player,'scenario',[],1)
        self.assertTrue(question); self.assertIn('truncated',note)
        player.complete.side_effect=ValueError('Unexpected tool call.')
        with self.assertRaises(ValueError): next_question(player,'scenario',[],1)
    def test_helper_role_recovers_without_ending_session(self):
        player=MagicMock(); player.complete.return_value='{"question":"What kind of gameplay do you enjoy?"}'
        question,note=next_question(player,'scenario',[],1)
        self.assertIn('helper role',note); self.assertIn('requirements',question)
    def test_title_rotation_keeps_account_evidence_in_its_game(self):
        accounts=Accounts(); accounts.selected_game='Guild Wars 2'; accounts.names={1:'Private Trial'}
        accounts.snapshot={'records':[{'id':1,'done':False}]}
        titles=json.loads((Path(__file__).resolve().parents[1]/'src/waypoint/testing/test_titles.json').read_text('utf-8'))
        plans=title_scenarios(accounts,titles)
        self.assertEqual(len({p['game'] for p in plans[:12]}),12)
        for plan in plans:
            validate_question(plan['starter'])
            if plan['game']!='Guild Wars 2':
                self.assertNotIn('Private Trial',json.dumps(plan)); self.assertFalse(plan['account_evidence_available'])
                self.assertNotIn('API',plan['starter'])
                self.assertNotIn('my account progress',plan['starter'])
                self.assertNotIn(plan['name'],('saved goal versus progress','account completion False','account completion True'))
            if plan['game']=="Baldur's Gate 3": self.assertNotEqual(plan['name'],'event timing and missed events')
    def test_credentials_never_enter_scenarios(self):
        accounts=Accounts(); accounts.key='synthetic-private-key'; accounts.names={1:'Trial'}
        accounts.snapshot={'fetched_at':'test','records':[{'id':1,'done':False}]}
        context=json.dumps(scenarios(accounts))
        self.assertNotIn(accounts.key,context); self.assertIn('Trial',context)
    def test_generated_credentials_and_oversized_questions_blocked(self):
        for question in ('my api key is example','x'*501,'','What is the most important thing you want to accomplish?'):
            with self.assertRaises(ValueError): validate_question(question)
    def test_scenarios_use_selected_game_without_invented_progress(self):
        accounts=Accounts(); accounts.selected_game='A different MMO'
        plans=scenarios(accounts)
        self.assertGreaterEqual(len(plans),13)
        for plan in plans:
            self.assertEqual(plan['game'],'A different MMO')
            validate_question(plan['starter'])
            self.assertNotIn('Guild Wars 2',json.dumps(plan))
        self.assertFalse(any('record' in plan for plan in plans))
    def test_research_handoff_flag_is_reviewable(self):
        self.assertTrue(findings('Help with this achievement','Search the wiki and paste the guide here.',Accounts(),1))
        self.assertFalse(findings('Help with this achievement','Which achievement and game are you working on?',Accounts(),1))
    def test_dialogue_logs_and_stop_flag(self):
        player=MagicMock(); player.complete.return_value='{"question":"What next?"}'
        assistant=MagicMock(); assistant.chat.return_value='Choose a goal.'
        with tempfile.TemporaryDirectory() as directory:
            out=Path(directory)/'run'
            summary=run_sessions(player,lambda session:assistant,Accounts(),out,sessions=1,turns=2,delay=0)
            self.assertEqual(summary['cases'],2)
            self.assertIn('Choose a goal.',player.complete.call_args.args[0])
            self.assertIn('whether it needs unlocks or a group',player.complete.call_args.args[0])
            self.assertEqual(len((out/'conversations.jsonl').read_text().splitlines()),2)
            (out.parent/'STOP').touch()
            self.assertEqual(run_sessions(player,lambda session:assistant,Accounts(),out,sessions=1,turns=2,delay=0)['cases'],0)
    def test_repeated_failures_stop_bounded_run(self):
        player=MagicMock(); player.complete.return_value='not JSON'
        with tempfile.TemporaryDirectory() as directory:
            helper=MagicMock(); helper.chat.return_value='A normal answer.'
            summary=run_sessions(player,lambda session:helper,Accounts(),directory,sessions=100,turns=6,delay=0)
        self.assertEqual(summary['errors'],3); self.assertEqual(summary['stop_reason'],'repeated errors')
