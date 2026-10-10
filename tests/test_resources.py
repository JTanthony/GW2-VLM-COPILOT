import sys,unittest,tempfile,json
from pathlib import Path
from unittest.mock import MagicMock
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from waypoint.storage.resources import Resources
from waypoint.assistant.local import Assistant

class ResourceTests(unittest.TestCase):
    def setUp(self):
        test_root=Path(__file__).resolve().parents[1]/'local-data/resource-tests'; test_root.mkdir(parents=True,exist_ok=True)
        self.temp=tempfile.TemporaryDirectory(dir=test_root)
        self.assertEqual(Path(self.temp.name).resolve().parent,test_root.resolve())
        self.addCleanup(self.temp.cleanup)
        self.store=Resources(self.temp.name)
    def test_explicit_goal_survives_restart(self):
        self.store.select('My game is Example Adventure'); self.store.remember('My goal is explore the northern region')
        other=Resources(self.temp.name); other.select('My game is Example Adventure')
        self.assertIn('explore the northern region',other.context())
    def test_credentials_not_persisted(self):
        result=self.store.remember('Remember that my API key is TEST-SECRET')
        self.assertIn('did not save',result)
        self.assertNotIn('TEST-SECRET',self.store.context())
    def test_cache_reuses_fetched_reference(self):
        fetch=MagicMock(return_value=[{'title':'Crafting','text':'Reference','url':'https://example.com/game/crafting'}])
        self.store.cached_lookup('Example Adventure','crafting',fetch)
        self.store.cached_lookup('Example Adventure','crafting',fetch)
        fetch.assert_called_once()
    def test_project_paths_stay_under_root(self):
        path=self.store.ensure('../../outside')
        self.assertEqual(path.parent,Path(self.temp.name))
    def test_save_ack_does_not_depend_on_model(self):
        client=MagicMock(); assistant=Assistant(client,resources=self.store)
        answer=assistant.chat('Remember that I prefer short answers')
        self.assertIn('Saved',answer); client.complete.assert_not_called()
    def test_unrequested_chat_not_saved(self):
        self.assertIsNone(self.store.remember('Hello there'))
        self.assertNotIn('Hello there',self.store.context())

    def test_no_game_project_created_by_default(self):
        self.assertEqual({p.name for p in Path(self.temp.name).iterdir()},{'general'})
    def test_explicit_game_overrides_old_window_and_isolates_goals(self):
        self.store.select('My game is Example Adventure')
        self.store.remember('My goal is explore the northern region')
        self.store.select('My game is Space Builder','Guild Wars 2')
        self.assertEqual(self.store.project,'space-builder')
        self.assertNotIn('northern region',self.store.context())
    def test_registered_alias_still_selects_connector_project(self):
        self.store.select('My game is GW2')
        self.assertEqual(self.store.project,'guild-wars-2')
