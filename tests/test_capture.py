import sys,unittest
from pathlib import Path
from unittest.mock import patch,MagicMock
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from waypoint.capture import windows
from waypoint.assistant.local import Assistant
class CaptureTests(unittest.TestCase):
    def test_focus_loss_keeps_approved_capture(self):
        target=windows.Window(10,42,'Test')
        with patch.object(windows,'process_id',return_value=42),patch.object(windows,'u') as u:
            u.IsWindow.return_value=True; u.IsWindowVisible.return_value=True; u.IsIconic.return_value=False; u.GetForegroundWindow.return_value=11
            windows.validate_target(target)
            u.GetForegroundWindow.assert_not_called()
    def test_reused_handle_blocks_capture(self):
        with patch.object(windows,'process_id',return_value=43),patch.object(windows,'u') as u:
            u.IsWindow.return_value=True
            with self.assertRaisesRegex(RuntimeError,'closed'): windows.validate_target(windows.Window(10,42,'Test'))
    def test_context_bounded_and_supplied_on_followup(self):
        client=MagicMock(); client.complete.return_value='A short answer'; a=Assistant(client)
        a.chat('I play Example Game',articles=[]); a.chat('Can you help with that game?',articles=[])
        self.assertIn('I play Example Game',client.complete.call_args.args[0])
        for i in range(8): a.chat(str(i),articles=[])
        self.assertEqual(len(a.history),12)
    def test_approved_capture_state_supplied_to_text_chat(self):
        client=MagicMock(); client.complete.return_value='Still analyzing.'
        Assistant(client).chat('Help me learn the game flow',articles=[],vision_state={'approved':True,'frames_captured':40,'analyzing':True})
        prompt=client.complete.call_args.args[0]
        self.assertIn('never ask the user to select it again',prompt)
        self.assertIn('"frames_captured": 40',prompt)
if __name__=='__main__': unittest.main()

class CaptureMinimizeTests(unittest.TestCase):
    def test_minimized_target_pauses(self):
        with patch.object(windows,'process_id',return_value=42),patch.object(windows,'u') as u:
            u.IsWindow.return_value=True; u.IsWindowVisible.return_value=True; u.IsIconic.return_value=True
            with self.assertRaisesRegex(RuntimeError,'restore'):
                windows.validate_target(windows.Window(10,42,'Game'))
