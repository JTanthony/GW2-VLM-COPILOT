import sys,json,unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch,MagicMock
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from waypoint.experiments.ocr_landmarks.qwen import profile,TextOnlyClient,OCRAssistant,reasoning_observation,public_table_context

class QwenOCRTests(unittest.TestCase):
    def test_social_messages_answer_without_lookup_planning(self):
        from waypoint.storage.resources import Resources
        with TemporaryDirectory() as folder:
            client=MagicMock();client.complete.return_value='Hello Joe! What would you like to test?'
            accounts=MagicMock();accounts.selected_game='Guild Wars 2'
            accounts.completion_answer.return_value=None;accounts.context.return_value=''
            assistant=OCRAssistant(client,resources=Resources(folder),accounts=accounts,allowed_sources=('Guild Wars 2',))
            with patch('waypoint.assistant.research.lookup') as fetch:
                for question in ('Hi chat',"You can call me Joe. I'm testing your model for a GW2 game copilot"):
                    client.reset_mock()
                    answer=assistant.chat(question)
                    self.assertIn('Hello Joe',answer)
                    client.complete.assert_called_once()
                    self.assertNotIn('schema',client.complete.call_args.kwargs)
                    self.assertIn(question,client.complete.call_args.args[0])
                fetch.assert_not_called()

    def test_greeting_or_introduction_does_not_hide_game_question(self):
        from waypoint.assistant.routing import is_social_message
        for question in ('Hi chat. Where does the Wyvern Matriarch spawn?',
                         'Call me Joe. How do I unlock gliding?',
                         'Hi chat, what crafting disciplines make bags?',
                         'Lost Dwarven Chest', 'I am looking for an achievement'):
            self.assertFalse(is_social_message(question),question)
        client=MagicMock();client.complete.return_value=json.dumps({'game':'Guild Wars 2','query':'Bag'})
        from waypoint.assistant.research import research
        with patch('waypoint.assistant.research.lookup',return_value=[{'text':'Verified bag facts'}]) as fetch:
            articles,notice=research(client,'Hi chat, what crafting disciplines make inventory bags?',[],selected_game='Guild Wars 2')
        fetch.assert_called_once();self.assertTrue(articles);self.assertEqual(notice,'')

    def test_full_qwen_research_path_selects_regional_mastery_table(self):
        from waypoint.storage.resources import Resources
        with TemporaryDirectory() as folder:
            client=MagicMock();client.complete.side_effect=[json.dumps({'game':'Guild Wars 2','query':'Gliding mastery track'}),'Train the selected gliding level using its listed XP and mastery-point cost.']
            accounts=MagicMock();accounts.selected_game='Guild Wars 2';accounts.completion_answer.return_value=None;accounts.context.return_value=''
            assistant=OCRAssistant(client,resources=Resources(folder),accounts=accounts,allowed_sources=('Guild Wars 2',))
            html='<h3>Gliding</h3><table><tr><th>Mastery</th><th>XP required</th><th>Points</th><th>Description</th></tr><tr><td>Glider Basics</td><td>508,000</td><td>1</td><td>Learn gliding</td></tr></table>'
            with patch('waypoint.assistant.web_lookup.wiki_json',return_value={'parse':{'text':html}}) as wiki:
                assistant.chat('What does the Gliding mastery track require?',window_title='Guild Wars 2')
            self.assertEqual(wiki.call_args.args[2]['page'],'Heart of Thorns mastery tracks')
            prompt=client.complete.call_args.args[0]
            self.assertIn('XP required: 508,000',prompt)
            self.assertIn('Points: 1',prompt)
            self.assertIn('aggregate',prompt)

    def test_dated_api_completion_remains_a_deterministic_path(self):
        from waypoint.storage.resources import Resources
        with TemporaryDirectory() as folder:
            client=MagicMock();accounts=MagicMock();accounts.selected_game='Guild Wars 2'
            accounts.completion_answer.return_value='Not completed (done=false). Dated official snapshot.'
            assistant=OCRAssistant(client,resources=Resources(folder),accounts=accounts)
            answer=assistant.chat('Have I completed this achievement?',window_title='Guild Wars 2')
            self.assertIn('done=false',answer);client.complete.assert_not_called()

    def test_named_tables_are_available_without_visual_story_classification(self):
        maps=public_table_context('What achievements are in Verdant Brink?')
        self.assertIn('dedicated map category',maps);self.assertIn('Verdant Brink',maps)
        story=public_table_context('Explain Night of Fires achievements')
        self.assertIn('Path of Fire: Act 1',story);self.assertIn('explicitly_linked_achievements',story)
        self.assertIn('not verified current location',story)
        self.assertEqual(public_table_context('Hello'), '')

    def test_qwen_reuses_text_rules_without_vision_guidance_or_grounding(self):
        from waypoint.assistant.local import Assistant,TEXT_PLAYER_GUIDANCE,VISION_PLAYER_GUIDANCE
        from waypoint.inference.validation import PROMPT,BACKGROUND_PROMPT
        from waypoint.storage.resources import Resources
        with TemporaryDirectory() as folder:
            client=MagicMock();client.complete.return_value='One concrete next step.'
            accounts=MagicMock();accounts.selected_game='Guild Wars 2'
            accounts.completion_answer.return_value=None;accounts.context.return_value='Dated API rules.'
            assistant=OCRAssistant(client,resources=Resources(folder),accounts=accounts,allowed_sources=('Guild Wars 2',))
            articles=[{'title':'Fallen Masks','text':'Adventure requiring a score threshold.','url':'https://wiki.guildwars2.com/wiki/Fallen_Masks'}]
            with patch('waypoint.assistant.local.research',return_value=(articles,'')) as research,patch('waypoint.assistant.local.gold_reading') as currency,patch('waypoint.assistant.local.guard_screen_stats') as image_guard:
                assistant.answer(reasoning_observation({'visible_text':[]}), 'Explain Fallen Masks',window_title='Guild Wars 2')
            research.assert_called_once();currency.assert_not_called();image_guard.assert_not_called()
            prompt=client.complete.call_args.args[0]
            self.assertIn(TEXT_PLAYER_GUIDANCE,prompt)
            self.assertNotIn(VISION_PLAYER_GUIDANCE,prompt)
            self.assertNotIn(PROMPT,prompt);self.assertNotIn(BACKGROUND_PROMPT,prompt)
            self.assertIn('Fallen Masks',prompt);self.assertIn('dated',prompt)
            self.assertNotIn('image',client.complete.call_args.kwargs)
            self.assertTrue(Assistant.screen_grounding)
            self.assertIn(VISION_PLAYER_GUIDANCE,Assistant.player_guidance)

    def test_qwen_chat_research_preserves_shared_lookup_and_answer_style(self):
        from waypoint.storage.resources import Resources
        with TemporaryDirectory() as folder:
            client=MagicMock();client.complete.return_value='Tailor, Leatherworker and Armorsmith.'
            accounts=MagicMock();accounts.selected_game='Guild Wars 2';accounts.completion_answer.return_value=None;accounts.context.return_value=''
            assistant=OCRAssistant(client,resources=Resources(folder),accounts=accounts,allowed_sources=('Guild Wars 2',))
            articles=[{'title':'Bag','text':'Tailor, Leatherworker, Armorsmith.','url':'https://wiki.guildwars2.com/wiki/Bag'}]
            with patch('waypoint.assistant.local.research',return_value=(articles,'')) as research:
                answer=assistant.chat('What disciplines craft inventory bags?',window_title='Guild Wars 2')
            research.assert_called_once();self.assertNotIn('Sources:',answer)
            self.assertNotIn('vision is still analyzing',client.complete.call_args.args[0])
            self.assertIn('Tailor',client.complete.call_args.args[0])

    def test_profile_never_overwrites_gemma_or_loads_a_projector(self):
        with TemporaryDirectory() as folder:
            root=Path(folder);(root/'config').mkdir()
            path=root/'config/inference.local.json'
            saved={'model_path':'original.gguf','projector_path':'original-mmproj.gguf','executable':'runtime/llama.exe','port':17865}
            path.write_text(json.dumps(saved),encoding='utf-8')
            c=profile(root)
            self.assertNotIn('projector_path',c);self.assertEqual(c['context_length'],4096)
            self.assertEqual(c['gpu_layers'],8);self.assertFalse(c['kv_offload'])
            self.assertEqual(json.loads(path.read_text('utf-8')),saved)

    def test_no_image_can_enter_qwen_text_client(self):
        client=TextOnlyClient('http://127.0.0.1:17867/v1')
        with patch('waypoint.inference.client.Client.complete') as parent:
            with self.assertRaises(ValueError):client.complete('read',image=b'PNG')
            parent.assert_not_called()
            client.complete('text only',max_tokens=20)
            parent.assert_called_once_with('text only',max_tokens=20)
        with self.assertRaises(RuntimeError):OCRAssistant(MagicMock()).observe(b'PNG')

    def test_raw_ocr_is_partial_bounded_and_cannot_claim_location_or_completion(self):
        result=reasoning_observation({'map':'invented','visible_text':['OCR upper left: Background']+['OCR upper right: wedge symbols 07/5']*30})
        self.assertEqual(len(result['visible_text']),24)
        self.assertIn('invalid counter',result['visible_text'][0])
        self.assertIsNone(result['map']);self.assertIsNone(result['objective'])
        self.assertEqual(result['confidence'],0)

if __name__=='__main__':unittest.main()
