import sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch,MagicMock
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from waypoint.integrations.credentials import CredentialStore
from waypoint.integrations.accounts import Accounts

class CredentialTests(unittest.TestCase):
    def test_windows_roundtrip_is_encrypted_and_can_be_forgotten(self):
        with tempfile.TemporaryDirectory() as directory:
            store=CredentialStore(directory); token='synthetic-test-token-not-a-real-account'
            store.save('Example game',token)
            self.assertNotIn(token.encode(),store.path('Example game').read_bytes())
            self.assertEqual(CredentialStore(directory).load('Example game'),token)
            store.forget('Example game'); self.assertIsNone(store.load('Example game'))
    def test_corrupt_token_fails_without_disclosing_content(self):
        with tempfile.TemporaryDirectory() as directory:
            store=CredentialStore(directory); store.path('Example').write_bytes(b'not-a-token')
            with self.assertRaisesRegex(RuntimeError,'could not be unlocked'): store.load('Example')
    def test_reconnect_and_disconnect_preserve_saved_token(self):
        store=MagicMock(); store.load.return_value='synthetic-test-token-123456'; accounts=Accounts(store)
        with patch('waypoint.integrations.accounts.get_gw2',side_effect=[{'permissions':['account','progression']},[]]):
            accounts.connect('','GW2',remember=True)
        store.load.assert_called_once_with('Guild Wars 2'); store.save.assert_called_once_with('Guild Wars 2','synthetic-test-token-123456')
        accounts.disconnect(); self.assertIsNone(accounts.key); store.forget.assert_not_called()
        accounts.forget('GW2'); store.forget.assert_called_once_with('Guild Wars 2')
    def test_invalid_token_is_not_saved(self):
        store=MagicMock(); accounts=Accounts(store)
        with patch('waypoint.integrations.accounts.get_gw2',return_value={'permissions':[]}):
            with self.assertRaises(ValueError): accounts.connect('synthetic-test-token-123456','GW2',remember=True)
        store.save.assert_not_called()
    def test_save_failure_keeps_session_and_reports_failure(self):
        store=MagicMock(); store.save.side_effect=OSError('test'); accounts=Accounts(store)
        with patch('waypoint.integrations.accounts.get_gw2',side_effect=[{'permissions':['account','progression']},[]]):
            result=accounts.connect('synthetic-test-token-123456','GW2',remember=True)
        self.assertIn('could not be saved',result); self.assertIsNotNone(accounts.key)
