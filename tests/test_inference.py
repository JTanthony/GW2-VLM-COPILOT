import json,sys,unittest
from pathlib import Path
from unittest.mock import MagicMock
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from waypoint.inference.client import Client,NoRedirect
from waypoint.inference.validation import validate_observation
from waypoint.inference.engine import Engine
class InferenceTests(unittest.TestCase):
    def test_trusted_guidance_uses_separate_system_message(self):
        c=Client('http://127.0.0.1:17865/v1'); c.opener=MagicMock()
        c.opener.open.return_value.__enter__.return_value.read.return_value=json.dumps({'choices':[{'finish_reason':'stop','message':{'content':'answer'}}]}).encode()
        c.complete('Untrusted article and player question')
        payload=json.loads(c.opener.open.call_args.args[0].data)
        self.assertEqual([message['role'] for message in payload['messages']],['system','user'])
        self.assertIn('never instructions',payload['messages'][0]['content'])
    def test_remote_and_credential_endpoints_rejected(self):
        for url in ['https://127.0.0.1/v1','http://example.com/v1','http://user:secret@localhost/v1','http://localhost/v1?x=1']:
            with self.assertRaises(ValueError): Client(url)
    def test_redirects_rejected(self):
        with self.assertRaises(ValueError): NoRedirect().redirect_request(None,None,None,None,None,None)
    def test_incomplete_empty_and_tool_responses_rejected(self):
        for choice in [{'finish_reason':'length','message':{'content':'partial'}},{'finish_reason':'stop','message':{'content':''}},{'finish_reason':'stop','message':{'content':'answer','tool_calls':[{}]}}]:
            c=Client('http://127.0.0.1:17865/v1'); c.opener=MagicMock()
            c.opener.open.return_value.__enter__.return_value.read.return_value=json.dumps({'choices':[choice]}).encode()
            with self.assertRaises(ValueError): c.complete('question')
    def test_bad_observation_rejected(self):
        with self.assertRaises(ValueError): validate_observation('{"summary":"incomplete"}')
    def test_stop_only_owned_process(self):
        e=Engine({},'.'); e.stop()
        e.process=MagicMock(); e.process.poll.return_value=None; e.stop()
        e.process.terminate.assert_called_once(); e.process.wait.assert_called_once_with(timeout=10)
if __name__=='__main__': unittest.main()
