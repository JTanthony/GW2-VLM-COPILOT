import sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from waypoint.paths import app_root,data_root
class PackagePathsTests(unittest.TestCase):
    def test_packaged_assets_and_private_state_are_separate(self):
        with tempfile.TemporaryDirectory() as folder:
            with patch.object(sys,'frozen',True,create=True),patch.object(sys,'executable',str(Path(folder)/'download/App.exe')),patch.dict('os.environ',{'LOCALAPPDATA':str(Path(folder)/'private')}):
                self.assertEqual(app_root(),Path(folder)/'download')
                self.assertEqual(data_root(),Path(folder)/'private/GW2 VLM COPILOT')
                self.assertNotEqual(app_root(),data_root())
