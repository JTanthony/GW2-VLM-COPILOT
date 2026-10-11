import json,tempfile,unittest
from unittest.mock import patch
from pathlib import Path
from waypoint.storage.vision_review import VisionReview

class ReviewTests(unittest.TestCase):
    def test_frames_are_opt_in_and_linked_to_exact_observation(self):
        import time
        png=(Path(__file__).parent/'fixtures/vision-known-text.png').read_bytes()
        with tempfile.TemporaryDirectory() as folder:
            log=VisionReview(folder); stamp=time.monotonic()
            self.assertIsNone(log.save_frame(stamp,png)); self.assertFalse(log.directory.exists())
            log.set_enabled(True)
            first=log.save_frame(stamp,png); second=log.save_frame(stamp+0.5,png)
            self.assertEqual(log.save_frame(stamp,png),first)
            log.record('question',question='What is this?',frame_stamp=stamp+0.5)
            log.record('answer',answer='Earlier analyzed frame',frame_stamp=stamp)
            records=[json.loads(line) for line in log.path.read_text('utf-8').splitlines()]
            self.assertEqual(records[-2]['frame_file'],second)
            self.assertEqual(records[-1]['frame_file'],first)
            self.assertEqual((log.directory/first).read_bytes(),png)
            self.assertEqual(len([r for r in records if r['kind']=='frame']),2)

    def test_frame_limit_disables_recording_without_writing(self):
        import time
        with tempfile.TemporaryDirectory() as folder:
            log=VisionReview(folder); log.set_enabled(True); log.frame_bytes=5_000_000_000
            with self.assertRaises(OSError): log.save_frame(time.monotonic(),b'png')
            self.assertFalse(log.enabled); self.assertFalse(log.path.with_suffix('').exists())

    def test_packaged_app_rejects_review_before_opening_window(self):
        from waypoint.ui.app import App
        with patch('sys.frozen',True,create=True),patch('waypoint.ui.app.tk.Tk') as window:
            with self.assertRaises(ValueError): App(vision_review=True)
            window.assert_not_called()

    def test_error_records_contain_only_type_and_duration(self):
        with tempfile.TemporaryDirectory() as folder:
            log=VisionReview(folder); log.set_enabled(True)
            log.record('vision_error',error_type='TimeoutError',analysis_seconds=120.0)
            record=json.loads(log.path.read_text('utf-8'))
            self.assertEqual(record['error_type'],'TimeoutError')
            self.assertEqual(record['analysis_seconds'],120.0)
            self.assertIsNone(record['observation'])

    def test_opt_in_and_disable(self):
        with tempfile.TemporaryDirectory() as folder:
            log=VisionReview(folder)
            log.record('answer',question='Hello')
            self.assertFalse(log.directory.exists())
            log.set_enabled(True)
            log.record('answer',question='What next?',answer='Try the event',observation={'visible_text':['event']},frame_age_seconds=12)
            log.set_enabled(False)
            log.record('answer',answer='not recorded')
            records=[json.loads(line) for line in log.path.read_text('utf-8').splitlines()]
            self.assertEqual(len(records),1)
            self.assertEqual(records[0]['frame_age_seconds'],12)
            self.assertEqual(records[0]['observation']['visible_text'],['event'])
    def test_sensitive_fields_and_keys_removed(self):
        with tempfile.TemporaryDirectory() as folder:
            log=VisionReview(folder); log.set_enabled(True)
            key='12345678-1234-1234-123456789012345678901234567890'
            log.record('observation',observation={'visible_text':[key,'api_key=example-secret'],
                       'png':'pixels','account_snapshot':{'id':123},'token':'private'})
            text=log.path.read_text('utf-8')
            for secret in (key,'example-secret','pixels','private','account_snapshot'):
                self.assertNotIn(secret,text)
            self.assertIn('[redacted]',text)
    def test_new_session_keeps_old_log(self):
        with tempfile.TemporaryDirectory() as folder:
            log=VisionReview(folder); log.set_enabled(True); log.record('observation')
            first=log.path; log.set_enabled(False); log.set_enabled(True)
            self.assertNotEqual(first,log.path); self.assertTrue(first.exists())
