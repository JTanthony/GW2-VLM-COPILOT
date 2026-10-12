import json,sys,unittest
from pathlib import Path
from unittest.mock import MagicMock,patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from waypoint.inference.client import Client,NoRedirect
from waypoint.inference.validation import validate_observation
from waypoint.inference.engine import Engine
class InferenceTests(unittest.TestCase):
    def test_trusted_guidance_uses_separate_system_message(self):
        c=Client('http://127.0.0.1:17865/v1'); c.opener=MagicMock()
        c.opener.open.return_value.__enter__.return_value.read.return_value=json.dumps({'choices':[{'finish_reason':'stop','message':{'content':'answer'}}]}).encode()
        with patch.object(c,'prompt_tokens',return_value=100): c.complete('Untrusted article and player question')
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
            with patch.object(c,'prompt_tokens',return_value=100),self.assertRaises(ValueError): c.complete('question')
    def test_oversized_request_never_sent(self):
        c=Client('http://127.0.0.1:17865/v1'); c.opener=MagicMock()
        with patch.object(c,'prompt_tokens',return_value=5284),self.assertRaisesRegex(ValueError,'4096-token'):
            c.complete('Player question: Where is the Wyvern?')
        c.opener.open.assert_not_called()
    def test_retry_fits_with_answer_reserve(self):
        c=Client('http://127.0.0.1:17865/v1'); c.opener=MagicMock()
        c.opener.open.return_value.__enter__.return_value.read.return_value=json.dumps({'choices':[{'finish_reason':'stop','message':{'content':'answer'}}]}).encode()
        with patch.object(c,'prompt_tokens',side_effect=[5284,3100]) as count:
            self.assertEqual(c.complete('Player question: Wyvern?',max_tokens=768),'answer')
        self.assertEqual(count.call_count,2)
        self.assertEqual(c.opener.open.call_count,1)
    def test_token_count_uses_formatted_template(self):
        c=Client('http://127.0.0.1:17865/v1'); c.opener=MagicMock()
        c.opener.open.return_value.__enter__.return_value.read.side_effect=[b'{"prompt":"formatted"}',b'{"tokens":[1,2,3]}']
        self.assertEqual(c.prompt_tokens([{'role':'user','content':'hello'}]),3)
        requests=[call.args[0] for call in c.opener.open.call_args_list]
        self.assertTrue(requests[0].full_url.endswith('/apply-template'))
        self.assertEqual(json.loads(requests[1].data)['content'],'formatted')
    def test_compaction_preserves_question_and_relevant_reference(self):
        from waypoint.inference.budget import compact
        p='Previous conversation: '+json.dumps([{'role':'assistant','text':'old'*2000}])+'\nPlayer question: Wyvern Matriarch spawn?\nDistinguish article facts from current screen evidence.\n'+json.dumps([{'title':'Wyvern','text':'Unrelated. '*1000+'Wyvern Matriarch spawns at the platform.'}])
        trimmed=compact(p,2)
        self.assertIn('Player question: Wyvern Matriarch spawn?',trimmed)
        self.assertIn('Wyvern Matriarch spawns at the platform.',trimmed)
        self.assertNotIn('oldold',trimmed)
        self.assertLess(len(trimmed),len(p))
    def test_compaction_keeps_whole_requested_table_row(self):
        from waypoint.inference.budget import compact
        row='Section: Fishing | Mastery: Fishing on a Full Tank | XP required: 1,016,000 | Points: 4 | Description: +100 while Nourished'
        article={'title':'End of Dragons mastery tracks','focus_text':row,'text':'Other unrelated tracks. '*1000}
        prompt='Player question: What are the requirements?\nDistinguish article facts from current screen evidence.\n'+json.dumps([article])
        result=compact(prompt,3)
        self.assertIn(row,result); self.assertNotIn('focus_text',result)
    def test_bad_observation_rejected(self):
        with self.assertRaises(ValueError): validate_observation('{"summary":"incomplete"}')
    def test_stop_only_owned_process(self):
        e=Engine({},'.'); e.stop()
        e.process=MagicMock(); e.process.poll.return_value=None; e.stop()
        e.process.terminate.assert_called_once(); e.process.wait.assert_called_once_with(timeout=10)
if __name__=='__main__': unittest.main()
