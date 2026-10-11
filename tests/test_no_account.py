import runpy,tempfile,unittest,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from unittest.mock import patch
from waypoint.integrations.accounts import Accounts
from waypoint.integrations.credentials import CredentialStore
from waypoint.testing.text_sessions import title_scenarios

class NoAccountTests(unittest.TestCase):
    def test_no_connection_or_credential_read(self):
        runner=runpy.run_path(str(Path(__file__).resolve().parents[1]/'tools/run_text_sessions.py'))
        with tempfile.TemporaryDirectory() as folder, patch.object(Accounts,'connect',side_effect=AssertionError('API connection')), patch.object(CredentialStore,'load',side_effect=AssertionError('Credential read')):
            accounts=runner['test_accounts']('none','Guild Wars 2',Path(folder))
            self.assertFalse(accounts.snapshot)
            self.assertFalse(accounts.names)
            plans=title_scenarios(accounts,[{'game':'Guild Wars 2','focus':'wiki'}])
            self.assertTrue(plans)
            self.assertTrue(all(not p['account_evidence_available'] for p in plans))
            self.assertNotIn('GW2 dated account versus wiki',[p['name'] for p in plans])
            self.assertTrue(all('my account progress' not in p['starter'] for p in plans))
