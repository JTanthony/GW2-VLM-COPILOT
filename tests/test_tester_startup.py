"""Handle an engine-port race after the runner's early availability check."""
import contextlib,io,json,unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import MagicMock,patch
from tools import run_text_sessions as runner
from waypoint.inference.engine import EnginePortBusyError


class TesterStartupTests(unittest.TestCase):
    def fixture(self,root):
        (root/'config').mkdir();(root/'server.exe').touch();(root/'model.gguf').touch()
        for name,port in (('player',17866),('inference',17865)):
            (root/'config'/f'{name}.local.json').write_text(json.dumps({'executable':'server.exe','model_path':str(root/'model.gguf'),'port':port,'alias':name}),encoding='utf-8')
        for name in ('assistant/research.py','assistant/web_lookup.py','assistant/local.py','assistant/rules/text.py','assistant/rules/evidence.py','assistant/rules/sections.py','inference/budget.py','testing/text_sessions.py','testing/test_titles.json'):
            target=root/'src/waypoint'/name;target.parent.mkdir(parents=True,exist_ok=True)
            target.write_bytes((runner.ROOT/'src/waypoint'/name).read_bytes())

    def test_busy_first_or_second_engine_reports_failure_and_preserves_other_run(self):
        for busy_index,port in ((0,17866),(1,17865)):
            with self.subTest(port=port),TemporaryDirectory() as folder:
                root=Path(folder);self.fixture(root)
                accounts=MagicMock();accounts.selected_game='Guild Wars 2';accounts.snapshot=None
                engines=[MagicMock(),MagicMock()]
                engines[busy_index].__enter__.side_effect=EnginePortBusyError(port)
                output=io.StringIO()
                with patch.object(runner,'ROOT',root),patch.object(runner.socket,'socket') as socket,patch.object(runner,'Engine',side_effect=engines),patch.object(runner,'test_accounts',return_value=accounts),patch.object(runner,'title_scenarios',return_value=[]),patch.object(runner,'run_sessions') as run,contextlib.redirect_stderr(output),contextlib.redirect_stdout(io.StringIO()):
                    socket.return_value.__enter__.return_value.connect_ex.return_value=1
                    result=runner.main(['--account-mode','none','--sessions','1','--turns','1'])
                self.assertEqual(result,2);run.assert_not_called()
                self.assertIn('run one tester at a time',output.getvalue())
                self.assertNotIn('Traceback',output.getvalue())
                report=json.loads(next((root/'local-data/text-playtests').glob('*/startup-error.json')).read_text(encoding='utf-8'))
                self.assertEqual(report['port'],port);self.assertEqual(report['status'],'not_started')
                accounts.disconnect.assert_called_once()
                if busy_index:engines[0].__exit__.assert_called_once()
                else:engines[1].__enter__.assert_not_called()


if __name__=='__main__':unittest.main()
