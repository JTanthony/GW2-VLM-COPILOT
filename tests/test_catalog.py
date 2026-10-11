import sys
import unittest
from unittest.mock import patch
from urllib.error import HTTPError
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from waypoint.testing.catalog import build_catalog,catalog_plans,mix_plans,fetch

class CatalogTests(unittest.TestCase):
    def test_temporary_failures_have_bounded_retries(self):
        error=HTTPError('https://api.guildwars2.com/v2/maps',503,'Unavailable',{},None)
        with patch('waypoint.testing.catalog.urlopen',side_effect=error) as request, patch('waypoint.testing.catalog.time.sleep'):
            with self.assertRaises(HTTPError): fetch('v2/maps')
            self.assertEqual(request.call_count,3)

    def test_batches_missing_ids_and_mastery_levels(self):
        calls=[]
        def get(path):
            calls.append(path)
            if path=='v1/event_names.json?lang=en': return [{'id':'event-1','name':'Defend the camp'}]
            if '?' not in path: return list(range(201)) if path.endswith('achievements') else [1]
            if path.startswith('v2/achievements'): return [{'id':int(i),'name':'Achievement '+i} for i in path.split('ids=')[1].split(',') if i!='200']
            if path.startswith('v2/maps'): return [{'id':1,'name':'Map','type':'Public'}]
            return [{'id':1,'name':'Track','levels':[{'name':'First level'}]}]
        catalog=build_catalog(get)
        self.assertEqual(catalog['coverage']['achievement']['missing_ids'],[200])
        self.assertTrue(any(r['kind']=='mastery_level' for r in catalog['records']))
        self.assertFalse(any('account' in path for path in calls))
        plans=catalog_plans(catalog,42)
        self.assertEqual(plans,catalog_plans(catalog,42))
        self.assertEqual(len(plans),204)
        self.assertEqual(mix_plans([{'name':'fixed'}],plans)[0],{'name':'fixed'})

    def test_instanced_maps_stay_out_of_completion_questions(self):
        catalog={'records':[{'kind':'map','id':1,'name':'Instance','map_type':'Instance'}]}
        self.assertEqual(catalog_plans(catalog,1),[])

    def test_events_fall_back_to_public_details(self):
        def get(path):
            if path.startswith('v1/event_names'): raise HTTPError(path,503,'Unavailable',{},None)
            if path.startswith('v1/event_details'): return {'events':{'abc':{'name':'Defend the camp'}}}
            return []
        catalog=build_catalog(get)
        self.assertEqual(catalog['coverage']['event']['returned'],1)
        self.assertTrue(catalog['records'][0]['source'].endswith('event_details.json'))
