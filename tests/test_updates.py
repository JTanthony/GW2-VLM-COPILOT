import sys,unittest,json
from pathlib import Path
from unittest.mock import patch,MagicMock
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from waypoint.updates import newer_windows_release,check_for_update,version_key

def release(tag,**changes):
    result={'tag_name':tag,'prerelease':True,'draft':False,'assets':[{'name':'GW2-VLM-COPILOT-'+tag+'-windows-x64.zip','state':'uploaded','size':100}]}
    result.update(changes); return result

class UpdateTests(unittest.TestCase):
    def test_prerelease_version_order_not_creation_order(self):
        result=newer_windows_release([release('v0.1.9-alpha'),release('v0.1.11-alpha'),release('v0.1.10-alpha')],'0.1.9-alpha')
        self.assertEqual(result['version'],'0.1.11-alpha')
    def test_same_older_draft_and_missing_windows_assets_ignored(self):
        self.assertIsNone(newer_windows_release([release('v0.1.10-alpha'),release('v0.1.9-alpha'),release('v0.1.11-alpha',draft=True),release('v0.1.12-alpha',assets=[])],'0.1.10-alpha'))
    def test_incomplete_asset_ignored(self):
        data=release('v0.1.11-alpha'); data['assets'][0]['state']='new'
        self.assertIsNone(newer_windows_release([data],'0.1.10-alpha'))
    def test_stable_release_follows_alpha_and_untrusted_urls_not_used(self):
        data=release('v0.1.10',html_url='https://example.com',prerelease=False)
        result=newer_windows_release([data],'0.1.10-alpha')
        self.assertEqual(result['url'],'https://github.com/JTanthony93/GW2-VLM-COPILOT/releases/tag/v0.1.10')
        self.assertIsNone(version_key('v0.1.11/../../other'))
    def test_numeric_prerelease_and_stable_order(self):
        self.assertLess(version_key('1.0.0-alpha.2'),version_key('1.0.0-alpha.10'))
        self.assertLess(version_key('1.0.0-rc.1'),version_key('1.0.0'))
    def test_public_request_uses_release_list_and_no_auth(self):
        with patch('waypoint.updates.http.client.HTTPSConnection') as cls:
            conn=cls.return_value; response=conn.getresponse.return_value
            response.status=200; response.getheader.return_value='application/json'
            response.read.return_value=json.dumps([release('v0.1.11-alpha')]).encode()
            self.assertEqual(check_for_update('0.1.10-alpha')['version'],'0.1.11-alpha')
            args=conn.request.call_args
            self.assertIn('/releases?per_page=100',args.args[1]); self.assertNotIn('Authorization',args.kwargs['headers'])
            conn.close.assert_called_once()
    def test_redirect_and_oversized_response_fail_closed(self):
        for status,payload in [(302,b'[]'),(200,b'x'*1000001)]:
            with patch('waypoint.updates.http.client.HTTPSConnection') as cls:
                response=cls.return_value.getresponse.return_value
                response.status=status; response.getheader.return_value='application/json'; response.read.return_value=payload
                with self.assertRaises((RuntimeError,ValueError)): check_for_update()
                cls.return_value.close.assert_called_once()
    def test_update_event_does_not_unlock_inference(self):
        from waypoint.ui.app import App
        import queue
        app=App.__new__(App); app.events=queue.Queue(); app.events.put(('update_result',(None,False,False)))
        app.finish_update_check=MagicMock(); app.lock=MagicMock(); app.feed=None; app.last_vision_status=10**20; app.closing=False; app.root=MagicMock()
        app.update_account_indicator=MagicMock()
        app.poll(); app.finish_update_check.assert_called_once(); app.lock.assert_not_called()
