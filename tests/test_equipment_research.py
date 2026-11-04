"""Broad gear questions must retrieve category evidence without invented item names."""
import unittest
from unittest.mock import MagicMock, patch
from waypoint.assistant.research import research
from waypoint.assistant.web_lookup import ascended_topic, lookup


class EquipmentResearchTests(unittest.TestCase):
    def test_common_rarity_typos_and_equipment_categories(self):
        for rarity in ('ascended','acended','asended','ascened'):
            for noun,title in (('gear','equipment'),('armour','armor'),('weapons','weapon'),('trinkets','trinket'),('backpacks','back item')):
                self.assertEqual(ascended_topic(f'How can I get {rarity} {noun} for my mesmer?'),'Ascended '+title)

    def test_named_item_and_recipe_requests_are_not_replaced(self):
        for question in ("Zojja's ascended armor",'Ascended armor recipe','Ascended armor stat changing','Armor named Ascended Glory'):
            self.assertIsNone(ascended_topic(question))

    @patch('waypoint.assistant.research.lookup')
    def test_reported_question_bypasses_failed_planner(self,fetch):
        client=MagicMock();client.complete.side_effect=TimeoutError()
        fetch.return_value=[{'title':'Ascended armor','text':'Acquisition facts'}]
        articles,notice=research(client,'I need acended gear for my mesmer what can I do to acquire some pieces?',[],selected_game='Guild Wars 2',allowed_sources=('Guild Wars 2',))
        fetch.assert_called_once_with('Guild Wars 2','Ascended equipment')
        client.complete.assert_not_called()
        self.assertTrue(articles);self.assertEqual(notice,'')

    @patch('waypoint.assistant.research.lookup')
    def test_equipment_route_does_not_assume_an_unknown_game(self,fetch):
        client=MagicMock();client.complete.return_value='{"game":"none","query":""}'
        research(client,'I need ascended gear',[])
        client.complete.assert_called_once();fetch.assert_not_called()

    def test_broad_gear_includes_acquisition_article_with_two_page_limit(self):
        with patch('waypoint.assistant.web_lookup.article_html',return_value=('<p>Verified acquisition facts.</p>',False)) as html:
            articles=lookup('Guild Wars 2','Ascended equipment')
        self.assertEqual([a['title'] for a in articles],['Ascended equipment','Ascended armor'])
        self.assertEqual(html.call_count,2)
        self.assertTrue(all('acquisition' in call.args[3] for call in html.call_args_list))


if __name__=='__main__':unittest.main()
