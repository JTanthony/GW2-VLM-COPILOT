import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from waypoint.integrations.map_achievements import load_table,category_progress

class MapAchievementTests(unittest.TestCase):
    def test_table_scope_and_unique_membership(self):
        table=load_table()
        self.assertGreaterEqual(len(table['maps']),28)
        self.assertEqual(len({row['map_id'] for row in table['maps']}),len(table['maps']))
        self.assertTrue({'Heart of Thorns','Path of Fire','End of Dragons','Secrets of the Obscure','Janthir Wilds','Visions of Eternity'}.issubset({r['expansion'] for r in table['maps']}))
        for row in table['maps']:
            ids=[a['id'] for a in row['achievements']]
            self.assertTrue(ids); self.assertEqual(len(ids),len(set(ids)))
            self.assertEqual(set(ids),{value for c in row['categories'] for value in c['achievement_ids']})
            self.assertTrue(all(type(value) is int for value in ids))

    def test_only_done_true_counts_once_and_only_in_category(self):
        table={'verified_at':'verified','maps':[{'map_name':'Test Map','category_id':12,'achievements':[{'id':1},{'id':2}]}]}
        snapshot={'fetched_at':'dated snapshot','records':[{'id':1,'done':True},{'id':1,'done':True},
                   {'id':2,'done':False,'current':5,'max':5},{'id':3,'done':True}]}
        result=category_progress('test map',snapshot,table)
        self.assertEqual((result['completed'],result['total']),(1,2))
        self.assertEqual(result['snapshot_time'],'dated snapshot')
        self.assertIsNone(category_progress('Other Map',snapshot,table))
        self.assertIsNone(category_progress('Test Map',None,table))

    def test_shared_story_and_convergence_categories_excluded(self):
        sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
        from refresh_map_achievements import select_maps
        groups=[{'id':'story','name':'Story Journal','categories':[1]},
                {'id':'expansion','name':'Visions of Eternity','categories':[2,3]}]
        categories=[{'id':1,'name':'Bloodstone Fen'}, {'id':2,'name':'Convergence: Nexus of Eternity'},
                    {'id':3,'name':'Shipwreck Strand'}]
        maps=[{'id':100,'name':'Bloodstone Fen','type':'Public'},
              {'id':101,'name':'Convergence: Nexus of Eternity','type':'Public'},
              {'id':1595,'name':'Shipwreck Strand','type':'Public'}]
        result=select_maps(groups,categories,maps)
        self.assertEqual([r['map_id'] for r in result],[1595])

    def test_inner_nayos_sections_count_each_id_once(self):
        table=load_table()
        row=next(r for r in table['maps'] if r['map_name']=='Inner Nayos')
        self.assertEqual({c['id'] for c in row['categories']},{403,409,416})
        snapshot={'fetched_at':'test','records':[{'id':row['achievements'][0]['id'],'done':True}]}
        result=category_progress('Inner Nayos',snapshot,table)
        self.assertEqual(result['completed'],1)
        self.assertEqual(len(result['category_ids']),3)

    def test_season_one_kept_separate_from_map_counts(self):
        table=load_table()
        episodes=table['episode_categories']
        self.assertEqual({r['category_id'] for r in episodes},{328,329,43,44,53,54,56,62,65})
        for episode in episodes:
            ids=[r['id'] for r in episode['achievements']]
            self.assertTrue(ids); self.assertEqual(len(ids),len(set(ids)))
            snapshot={'fetched_at':'test','records':[{'id':ids[0],'done':True}]}
            self.assertIsNone(category_progress(episode['category_name'],snapshot,table))
