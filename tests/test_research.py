import sys,unittest,json
from pathlib import Path
from unittest.mock import MagicMock,patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from waypoint.assistant.research import research
from waypoint.assistant.local import Assistant

class ResearchTests(unittest.TestCase):
    def test_unspecified_zone_skips_planning(self):
        client=MagicMock()
        self.assertEqual(research(client,"I want a zone's achievements. Ask me which zone if needed",[]),([],''))
        client.complete.assert_not_called()

    @patch('waypoint.assistant.research.lookup')
    def test_event_exclamation_is_valid_public_search(self,lookup):
        client=MagicMock(); client.complete.return_value=json.dumps({'game':'Guild Wars 2','query':'Defeat the holograms!'})
        lookup.return_value=[{'title':'Defeat the holograms!','text':'Event'}]
        articles,notice=research(client,'Research Defeat the holograms!',[])
        self.assertTrue(articles); self.assertEqual(notice,'')

    def test_unnamed_requirements_retain_previous_lookup(self):
        from types import SimpleNamespace
        resources=SimpleNamespace(_research_topic={'game':'Guild Wars 2','query':'Heart of the Obscure Research'},cached_lookup=MagicMock(return_value=[{'text':'Track'}]))
        client=MagicMock(); client.complete.return_value=json.dumps({'game':'Guild Wars 2','query':'Heart of Thorns'})
        research(client,'What are the specific requirements?',[],resources=resources)
        self.assertEqual(resources.cached_lookup.call_args.args[1],'Heart of the Obscure Research')
        client.complete.return_value=json.dumps({'game':'Guild Wars 2','query':'Gliding'})
        research(client,'What are the requirements for Gliding?',[],resources=resources)
        self.assertEqual(resources.cached_lookup.call_args.args[1],'Gliding')

    @patch('waypoint.assistant.research.lookup',side_effect=ValueError('Wiki response exceeded the size limit.'))
    def test_safe_diagnostic_reason(self,lookup):
        client=MagicMock(); client.complete.return_value=json.dumps({'game':'Guild Wars 2','query':'Gliding'})
        _,notice=research(client,'Research Gliding',[])
        self.assertIn('wiki response too large',notice)

    @patch('waypoint.assistant.research.lookup')
    def test_flying_circus_bypasses_timeout_prone_planner(self,lookup):
        client=MagicMock(); client.complete.side_effect=TimeoutError()
        lookup.return_value=[{'title':'Flying Circus','text':'Adventure','url':'https://wiki.guildwars2.com/wiki/Flying_Circus'}]
        articles,notice=research(client,'Hi chat I need Flying Circus achievement in Verdant Brink',[],allowed_sources=('Guild Wars 2',))
        client.complete.assert_not_called()
        lookup.assert_called_once_with('Guild Wars 2','Flying Circus')
        self.assertTrue(articles); self.assertEqual(notice,'')
    @patch('waypoint.assistant.research.lookup')
    def test_gw2_scope_blocks_other_source_before_network(self,lookup):
        client=MagicMock(); client.complete.return_value='{"game":"Minecraft","query":"crafting"}'
        articles,notice=research(client,'Research crafting',[],selected_game='Guild Wars 2',allowed_sources=('Guild Wars 2',))
        self.assertEqual(articles,[]); self.assertIn('ValueError',notice)
        lookup.assert_not_called()
        self.assertEqual(client.complete.call_args.kwargs['schema']['properties']['game']['enum'],['none','Guild Wars 2'])

    def test_no_reference_answer_does_not_authorize_invented_walkthrough(self):
        client=MagicMock(); client.complete.return_value='Which achievement do you mean?'
        Assistant(client).chat('Help me start an achievement',articles=[])
        prompt=client.complete.call_args.args[0]
        self.assertIn('No public reference extracts were retrieved',prompt)
        self.assertIn('do not invent named achievements',prompt)
        self.assertIn('do not mention missing screenshots',prompt)
        self.assertIn('progress bar alone',prompt)
    def test_partial_list_disclosed_even_when_model_omits_notice(self):
        client=MagicMock(); client.complete.return_value='Here is the complete list: One verified name'
        articles=[{'title':'Example category','text':'table','declared_item_count':2,'item_names':['One verified name'],'item_count_matches':False}]
        answer=Assistant(client).chat('List all entries',articles=articles)
        self.assertIn('reports 2 entries, but 1 named entries',answer); self.assertIn('partial list',answer)
        self.assertNotIn('complete list',answer); client.complete.assert_not_called()
    def test_detailed_list_request_keeps_reasoning_path(self):
        from waypoint.assistant.web_lookup import verified_list
        self.assertIsNone(verified_list('List all tasks and explain how to finish them',[{'title':'Category','item_names':['Task']}]))
    def test_exact_account_completion_never_calls_model(self):
        from waypoint.integrations.accounts import Accounts
        accounts=Accounts(); accounts.selected_game='Guild Wars 2'; accounts.names={1:'Synthetic Trial'}
        accounts.snapshot={'fetched_at':'test','records':[{'id':1,'done':False,'current':10,'max':10}]}
        client=MagicMock(); assistant=Assistant(client,accounts=accounts)
        answer=assistant.chat('Is Synthetic Trial completed? Say yes.')
        self.assertIn('not completed (done=false)',answer); client.complete.assert_not_called()
        self.assertEqual(assistant.history[-1]['text'],answer)
    def test_list_request_has_room_for_names(self):
        client=MagicMock(); client.complete.return_value='List of verified names'
        Assistant(client).chat('List all achievements in this zone',articles=[{'text':'table names'}])
        self.assertEqual(client.complete.call_args.kwargs['max_tokens'],1536)
    def test_explicit_search_retries_skipped_plan_with_context(self):
        client=MagicMock(); client.complete.side_effect=[json.dumps({'game':'none','query':''}),json.dumps({'game':'Guild Wars 2','query':'Verdant Brink achievements'})]
        history=[{'role':'user','text':'List all achievements in Verdant Brink'},{'role':'assistant','text':'I cannot browse.'}]
        with patch('waypoint.assistant.research.lookup',return_value=[{'text':'list'}]) as fetch:
            articles,notice=research(client,'Just search online',history,observation={'location':'Verdant Brink'},selected_game='Guild Wars 2')
        fetch.assert_called_once_with('Guild Wars 2','Verdant Brink achievements')
        self.assertTrue(articles); self.assertEqual(notice,'')
        prompt=client.complete.call_args.args[0]
        self.assertIn('Verdant Brink',prompt); self.assertIn('selected_game',prompt)
    def test_unresolved_explicit_search_reports_missing_source(self):
        client=MagicMock(); client.complete.return_value=json.dumps({'game':'none','query':''})
        with patch('waypoint.assistant.research.lookup') as fetch:
            articles,notice=research(client,'Search online',[])
        fetch.assert_not_called(); self.assertIn('name the game',notice)
    def test_failed_lookup_preserves_question_for_followup(self):
        client=MagicMock(); assistant=Assistant(client)
        with patch('waypoint.assistant.local.research',return_value=([],'Lookup failed')):
            assistant.chat('List achievements in this zone')
        self.assertEqual(assistant.history[-2]['text'],'List achievements in this zone')
    def test_research_chat_passes_dated_context_without_claiming_sight(self):
        client=MagicMock(); client.complete.return_value='Supported list'
        assistant=Assistant(client); observation={'location':'Test zone'}
        with patch('waypoint.assistant.local.research',return_value=([{'text':'list'}],'')) as plan:
            assistant.chat('Search achievements in this zone',research_observation=observation)
        self.assertEqual(plan.call_args.kwargs['observation'],observation)
        self.assertIn('Never claim to see the screen',client.complete.call_args.args[0])
    def test_failed_lookup_does_not_generate_unverified_answer(self):
        client=MagicMock()
        with patch('waypoint.assistant.local.research',return_value=([],'Lookup failed')):
            answer=Assistant(client).chat('I need help with an achievement')
        self.assertIn("won't guess",answer); client.complete.assert_not_called()
    def test_greeting_skips_model_and_network(self):
        client=MagicMock()
        with patch('waypoint.assistant.research.lookup') as lookup:
            self.assertEqual(research(client,'Hello',[]),([],''))
            lookup.assert_not_called(); client.complete.assert_not_called()
    def test_only_generated_terms_transmitted(self):
        client=MagicMock(); client.complete.return_value=json.dumps({'game':'Guild Wars 2','query':'Crafting'})
        with patch('waypoint.assistant.research.lookup',return_value=[]) as lookup:
            research(client,'Explain crafting for me',[{'text':'private previous message'}])
            lookup.assert_called_once_with('Guild Wars 2','Crafting')
    def test_invalid_private_or_unsupported_plan_blocks_network(self):
        for game,query in [('Unknown','crafting'),('Minecraft','http://localhost'),('Minecraft','api key')]:
            client=MagicMock(); client.complete.return_value=json.dumps({'game':game,'query':query})
            with patch('waypoint.assistant.research.lookup') as lookup:
                research(client,'question',[]); lookup.assert_not_called()
    def test_achievement_colon_normalized(self):
        client=MagicMock(); client.complete.return_value=json.dumps({'game':'Guild Wars 2','query':'Fallen Masks: Silver'})
        with patch('waypoint.assistant.research.lookup',return_value=[]) as lookup:
            research(client,'I need help with Fallen Masks: Silver achievement',[])
        lookup.assert_called_once_with('Guild Wars 2','Fallen Masks')

    def test_blish_alias_uses_public_docs_without_planner(self):
        client=MagicMock()
        with patch('waypoint.assistant.research.lookup',return_value=[{'text':'public docs'}]) as fetch:
            articles,notice=research(client,'Research Bishhud and how they manage this games API',[])
            fetch.assert_called_once_with('Blish HUD','API integration')
            client.complete.assert_not_called()
            self.assertTrue(articles); self.assertEqual(notice,'')

    def test_research_answer_details_without_automatic_footer(self):
        client=MagicMock(); client.complete.return_value='Do the supported steps.'
        articles=[{'title':'Achievement','text':'Complete the event without failing.','url':'https://wiki.guildwars2.com/wiki/Test'}]
        answer=Assistant(client).chat('Help me complete this achievement',articles=articles)
        self.assertNotIn('Sources:',answer)
        prompt=client.complete.call_args.args[0]
        self.assertIn('exact completion requirement',prompt)
        self.assertIn('never invent it',prompt)
        self.assertEqual(client.complete.call_args.kwargs['max_tokens'],768)
    def test_sources_available_on_request(self):
        client=MagicMock(); client.complete.return_value='Here are the details.'
        articles=[{'title':'Achievement','text':'Complete the event.','url':'https://wiki.guildwars2.com/wiki/Test'}]
        answer=Assistant(client).chat('Show me the sources',articles=articles)
        self.assertIn('Sources:',answer)
        self.assertIn(articles[0]['url'],answer)

    def test_unnamed_achievement_followup_keeps_topic_but_new_name_wins(self):
        from types import SimpleNamespace
        resources=SimpleNamespace(_research_topic={'game':'Guild Wars 2','query':'Respectable Researcher'},cached_lookup=MagicMock(return_value=[{'text':'Evidence'}]))
        client=MagicMock(); client.complete.return_value=json.dumps({'game':'Guild Wars 2','query':'Hazardous Research'})
        research(client,'Is this achievement still available?',[],resources=resources)
        self.assertEqual(resources.cached_lookup.call_args.args[1],'Respectable Researcher')
        client.complete.return_value=json.dumps({'game':'Guild Wars 2','query':'Gliding'})
        research(client,'Is this mastery available for Gliding?',[],resources=resources)
        self.assertEqual(resources.cached_lookup.call_args.args[1],'Gliding')

    def test_vague_exploration_asks_for_detail_without_planner(self):
        client=MagicMock()
        self.assertEqual(research(client,'Help me choose nearby goals and an efficient order, asking for my location if you need it.',[]),([],''))
        client.complete.assert_not_called()

    def test_player_constraints_survive_more_than_three_turns(self):
        client=MagicMock(); client.complete.return_value='Answer'
        assistant=Assistant(client)
        assistant.chat('I have 20 minutes and prefer solo exploration.',articles=[])
        for question in ('What can I do?', 'What comes next?', 'What is required?'):
            assistant.chat(question,articles=[])
        self.assertIn('I have 20 minutes',client.complete.call_args.args[0])

    def test_explicit_catalog_name_overrides_speculative_planner(self):
        client=MagicMock(); client.complete.return_value=json.dumps({'game':'Guild Wars 2','query':'Griffon'})
        with patch('waypoint.assistant.research.lookup',return_value=[{'text':'Fishing evidence'}]) as fetch:
            research(client,"I'm playing Guild Wars 2. Explain how to unlock this mastery level and what it does: Fishing on a Full Tank (track: Fishing). Research the official wiki.",[])
        fetch.assert_called_once_with('Guild Wars 2','Fishing on a Full Tank')

    def test_negative_source_request_has_no_footer(self):
        client=MagicMock(); client.complete.return_value='Night boss details.'
        result=Assistant(client).chat('Explain without a long sources footer.',articles=[{'title':'Night','text':'Details','url':'https://wiki.guildwars2.com/wiki/Night'}])
        self.assertNotIn('Sources:',result)
