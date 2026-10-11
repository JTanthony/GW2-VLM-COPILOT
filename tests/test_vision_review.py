import json,tempfile,unittest
from pathlib import Path
from waypoint.storage.vision_review import VisionReview

class ReviewTests(unittest.TestCase):
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
