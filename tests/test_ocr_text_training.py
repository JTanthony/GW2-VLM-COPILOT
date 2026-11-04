import json,sys,unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
from unittest.mock import MagicMock,patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'));sys.path.insert(0,str(ROOT))
from waypoint.experiments.ocr_landmarks import text_training
from waypoint.experiments.ocr_landmarks.qwen import OCRAssistant,TextOnlyClient
from tools import run_text_sessions as runner

class QwenTextTrainingTests(unittest.TestCase):
    def test_map_completion_does_not_receive_achievement_totals(self):
        from waypoint.experiments.ocr_landmarks.qwen import public_table_context
        from waypoint.assistant.rules.evidence import focus_articles
        self.assertEqual(public_table_context('Explain Domain of Vabbi map completion.'),'')
        article={'title':'Domain of Vabbi','focus_text':'Subject: Domain of Vabbi | Type: Zone | Levels: 80',
            'text':'Area | Level | Points\nDzasha Uplands | 80 | Example'}
        focused=focus_articles('Domain of Vabbi map completion',[article])[0]
        self.assertNotIn('Dzasha Uplands',focused['text']);self.assertIn('not a point total',focused['text'])



















    def test_maintenance_message_is_plain_and_does_not_generate_a_guide(self):
        from waypoint.assistant.web_lookup import MAINTENANCE_NOTICE
        from waypoint.storage.resources import Resources
        with TemporaryDirectory() as folder:
            client=MagicMock();accounts=MagicMock();accounts.selected_game='Guild Wars 2'
            accounts.completion_answer.return_value=None;accounts.context.return_value=''
            assistant=OCRAssistant(client,resources=Resources(folder),accounts=accounts)
            with patch('waypoint.assistant.local.research',return_value=([],'\n\n'+MAINTENANCE_NOTICE)):
                self.assertEqual(assistant.chat('How do I craft bags?'),MAINTENANCE_NOTICE)
            client.complete.assert_not_called()

    def test_reference_prompt_does_not_turn_tier_thresholds_into_progress(self):
        from waypoint.storage.resources import Resources
        with TemporaryDirectory() as folder:
            client=MagicMock();client.complete.return_value='Silver requires 15 masks; Gold requires 25.'
            accounts=MagicMock();accounts.selected_game='Guild Wars 2';accounts.completion_answer.return_value=None;accounts.context.return_value=''
            assistant=OCRAssistant(client,resources=Resources(folder),accounts=accounts)
            assistant.chat('Does Fallen Masks Silver require 25 masks?',articles=[{'title':'Fallen Masks','text':'Silver: 15. Gold: 25.'}])
            prompt=client.complete.call_args.args[0]
            self.assertIn('Never assume a previous tier was earned',prompt)
            self.assertIn('one to three sentences and stop',prompt)

    def test_single_invented_city_name_gets_a_controlled_followup(self):
        from waypoint.testing.text_sessions import next_question
        player=MagicMock();player.complete.return_value=json.dumps({'question':'Where should I start near the city of Veridian?'})
        question,note=next_question(player,json.dumps({'original_player_question':'Help me explore Verdant Brink.'}),[],1)
        self.assertNotIn('Veridian',question);self.assertIn('unsupported',note)

    def test_failed_preflight_does_not_load_models_or_accounts(self):
        from waypoint.assistant.web_lookup import WikiMaintenanceError
        with TemporaryDirectory() as folder:
            root=Path(folder);config=self.fixture(root)
            with patch.object(runner,'ROOT',root),patch.object(runner.socket,'socket') as socket,patch.object(runner,'Engine') as engines,patch.object(runner,'test_accounts') as accounts:
                socket.return_value.__enter__.return_value.connect_ex.return_value=1
                with self.assertRaises(SystemExit):runner.main(['--account-mode','none'],copilot_profile=config,
                    source_preflight=MagicMock(side_effect=WikiMaintenanceError()))
                engines.assert_not_called();accounts.assert_not_called()
            self.assertFalse((root/'local-data').exists())

    def test_wrapper_reuses_existing_tester_with_qwen_and_no_account(self):
        config={'port':17867}
        with patch.object(text_training,'profile',return_value=config),patch.object(runner,'main',return_value=0) as run:
            self.assertEqual(text_training.main(['--sessions','10','--turns','4']),0)
        self.assertEqual(run.call_args.args[0],['--account-mode','none','--sessions','10','--turns','4'])
        self.assertIs(run.call_args.kwargs['assistant_factory'],OCRAssistant)
        self.assertIs(run.call_args.kwargs['client_factory'],TextOnlyClient)
        self.assertEqual(run.call_args.kwargs['copilot_profile'],config)
        self.assertEqual(run.call_args.kwargs['report_folder'],'text-playtests-qwen')

    def test_no_account_adapter_cannot_be_overridden_to_saved(self):
        with patch.object(runner,'main') as run:
            for argv in (['--account-mode','saved'],['--account-mode=saved']):
                with self.assertRaises(SystemExit):text_training.main(argv)
            run.assert_not_called()

    def test_stop_flag_is_isolated_and_does_not_load_any_model(self):
        with TemporaryDirectory() as folder,patch.object(text_training,'ROOT',Path(folder)),patch.object(text_training,'profile') as profile:
            self.assertEqual(text_training.main(['--stop']),0)
            self.assertTrue((Path(folder)/'local-data/text-playtests-qwen/STOP').exists())
            self.assertFalse((Path(folder)/'local-data/text-playtests/STOP').exists())
            profile.assert_not_called()

    def fixture(self,root):
        (root/'config').mkdir();(root/'fake.exe').touch();(root/'player.gguf').touch();(root/'qwen.gguf').touch()
        player={'executable':'fake.exe','model_path':str(root/'player.gguf'),'port':17866,'alias':'player'}
        (root/'config/player.local.json').write_text(json.dumps(player),'utf-8')
        # An unavailable Gemma model must not prevent the Qwen profile test.
        (root/'config/inference.local.json').write_text('{"model_path":"missing-gemma.gguf"}','utf-8')
        names=('assistant/research.py','assistant/web_lookup.py','assistant/local.py','assistant/rules/text.py','assistant/rules/evidence.py','assistant/rules/sections.py','inference/budget.py','testing/text_sessions.py','testing/test_titles.json')
        for name in names:
            target=root/'src/waypoint'/name;target.parent.mkdir(parents=True,exist_ok=True)
            target.write_bytes((ROOT/'src/waypoint'/name).read_bytes())
        return {'executable':'fake.exe','model_path':str(root/'qwen.gguf'),'port':17867,'alias':'qwen','projector_path':'not-used.gguf'}

    def test_shared_runner_uses_qwen_factory_and_its_own_report_and_stop(self):
        with TemporaryDirectory() as folder:
            root=Path(folder);config=self.fixture(root)
            parent=root/'local-data/text-playtests-qwen';parent.mkdir(parents=True);(parent/'STOP').touch()
            original=root/'local-data/text-playtests';original.mkdir();(original/'STOP').touch()
            accounts=SimpleNamespace(selected_game='Guild Wars 2',snapshot=None,disconnect=MagicMock())
            plans=[{'name':'test','game':'Guild Wars 2','starter':'Hello'}]
            def sessions(player,make_assistant,account,out,*args,**kwargs):
                assistant=make_assistant(0)
                self.assertIsInstance(assistant,OCRAssistant);self.assertIsInstance(assistant.client,TextOnlyClient)
                self.assertIsNone(account.snapshot);self.assertEqual(Path(out).parent,parent)
                self.assertEqual(kwargs['plans'],plans)
                return {'errors':0}
            with patch.object(runner,'ROOT',root),patch.object(runner.socket,'socket') as socket,patch.object(runner,'Engine') as engines,patch.object(runner,'test_accounts',return_value=accounts) as load,patch.object(runner,'title_scenarios',return_value=plans),patch.object(runner,'run_sessions',side_effect=sessions):
                socket.return_value.__enter__.return_value.connect_ex.return_value=1
                result=runner.main(['--account-mode','none','--sessions','1','--turns','1'],copilot_profile=config,
                    assistant_factory=OCRAssistant,client_factory=TextOnlyClient,report_folder='text-playtests-qwen',copilot_label='Qwen test')
            self.assertEqual(result,0);self.assertEqual(load.call_args.args[0],'none')
            self.assertNotIn('projector_path',engines.call_args_list[1].args[0])
            self.assertFalse((parent/'STOP').exists());self.assertTrue((original/'STOP').exists())
            info=json.loads(next(parent.glob('*/run-info.json')).read_text('utf-8'))
            self.assertEqual(info['copilot_model'],'Qwen test');self.assertFalse(info['capture'])
            accounts.disconnect.assert_called_once()

    def test_occupied_engine_port_blocks_before_account_access_or_engine_start(self):
        with TemporaryDirectory() as folder:
            root=Path(folder);config=self.fixture(root)
            with patch.object(runner,'ROOT',root),patch.object(runner.socket,'socket') as socket,patch.object(runner,'Engine') as engines,patch.object(runner,'test_accounts') as accounts:
                socket.return_value.__enter__.return_value.connect_ex.return_value=0
                with self.assertRaises(SystemExit):runner.main(['--account-mode','none'],copilot_profile=config)
                accounts.assert_not_called();engines.assert_not_called()
            self.assertFalse((root/'local-data').exists())

if __name__=='__main__':unittest.main()
