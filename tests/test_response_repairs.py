"""Evidence and lookup regressions reproduced from the November text reviews."""
import unittest
from unittest.mock import MagicMock,patch
from waypoint.assistant.web_lookup import WikiText,lookup,gw2_topic
from waypoint.assistant.rules.evidence import focus_articles
from waypoint.assistant.rules.sections import equipment_context,map_context
from waypoint.assistant.research import research


class ResponseRepairTests(unittest.TestCase):
    def test_account_binding_survives_as_acquisition_evidence(self):
        result=equipment_context('Ascended equipment','All ascended equipment is account bound.','How do I get gear?')
        self.assertIn('cannot be bought on the Trading Post',result)
        self.assertIsNone(equipment_context('Ascended armor','Crafting\nRecipe details.','How do I change stats?'))

    def test_link_only_map_and_crafting_icons_survive_extraction(self):
        parser=WikiText();parser.feed('<p>2 <a title="Waypoint"><img alt=""></a> 4 <a title="Renown Heart"><img alt=""></a></p><p><a title="Tailor"><img alt=""></a></p>')
        text=''.join(parser.parts)
        self.assertIn('2 [waypoint]',text);self.assertIn('4 [renown heart]',text)
        self.assertIn('[discipline: Tailor]',text)

    def test_armor_routes_keep_material_timegate_and_envoy_scope_separate(self):
        text='Article details:\nAcquisition\nArmor can be acquired several ways.\nCrafting\nPrimary article: Ascended crafting\nStandard armor uses level 500 disciplines. Some materials are limited to one craft per day. Refined materials can be purchased from the trading post.\n\nPlayers can also craft Grandmaster Marks to exchange at vendors.\n\nRefined Envoy recipes require Envoy Armor II.\nLooting\nUnrelated drops.'
        result=equipment_context('Ascended armor',text)
        self.assertIn('Standard armor crafting route:',result)
        self.assertIn('trading post',result);self.assertIn('Crafted mark exchange route:',result)
        self.assertIn('Collection-specific recipe route:',result)
        self.assertNotIn('Unrelated drops',result)

    def test_backpack_rating_equip_level_and_all_recipe_disciplines_remain_distinct(self):
        disciplines=['Armorsmith','Artificer','Chef','Huntsman','Jeweler','Leatherworker','Scribe','Tailor','Weaponsmith']
        text=' | Discipline rating | Required level to equip | Item rarity\n | 75 | 15 | Masterwork\n | 400 | 78 | Exotic\nRecipe list\n'+''.join(f' | Simple Backpack | Fine | [discipline: {d}] | 0 | Ingredients\n' for d in disciplines)
        result=equipment_context("Crafter's backpack",text)
        self.assertIn('Crafting rating=400; required character equip level=78',result)
        for d in disciplines:self.assertIn(d,result)

    def test_bag_crafting_facts_do_not_turn_craftsman_into_a_discipline(self):
        result=equipment_context('Bag','Types\nCraftsman is a bag type.\nCrafting\nBags use [discipline: Tailor], [discipline: Leatherworker], [discipline: Armorsmith].\nVendors\nIrrelevant prices.')
        self.assertIn('Armorsmith, Leatherworker, Tailor',result)
        self.assertNotIn('Irrelevant prices',result)

    def test_unlock_item_does_not_replace_requested_collection_target(self):
        source={'title':"Lightbringer's Pack",'item_names':["Lightbringer's Pack"],'text':" | Lightbringer's Pack | Basic Collections | 5\n | Collect all 10 items to create your Lightbringer's Pack. Unlock Item: Agent's Pack Reward: Bag | 1 Item Collected | 1\n | 5 Items Collected | 1\n | 10 Items Collected | 3"}
        result=focus_articles("How do I complete Lightbringer's Pack?",[source])[0]['focus_text']
        self.assertIn("Required unlock item (NOT the target achievement): Agent's Pack",result)
        self.assertIn('10 Items Collected',result)
        self.assertNotIn('Unlock Item:',result.split('Own objective:')[1].split('\n')[0])

    @patch('waypoint.assistant.research.lookup')
    def test_qualified_dragon_stand_bypasses_expansion_page_plan(self,fetch):
        client=MagicMock();client.complete.return_value='{"game":"Guild Wars 2","query":"Heart of Thorns"}'
        fetch.return_value=[{'title':"Dragon's Stand (Heart of Thorns)",'text':'Story staging area.'}]
        research(client,"Is Dragon's Stand (Heart of Thorns) a story staging area?",[],selected_game='Guild Wars 2')
        fetch.assert_called_once_with('Guild Wars 2',"Dragon's Stand (Heart of Thorns)")
        client.complete.assert_not_called()

    @patch('waypoint.assistant.research.lookup')
    def test_inner_nayos_mastery_request_retains_subject_type(self,fetch):
        client=MagicMock();client.complete.return_value='{"game":"Guild Wars 2","query":"Inner Nayos"}'
        fetch.return_value=[{'title':'Secrets of the Obscure mastery tracks','text':'Track evidence'}]
        research(client,'Explain this mastery track and how to progress it: Inner Nayos. Research the official wiki.',[],selected_game='Guild Wars 2')
        fetch.assert_called_once_with('Guild Wars 2','Inner Nayos mastery track')

    def test_inner_nayos_map_lookup_is_not_changed_into_a_mastery(self):
        with patch('waypoint.assistant.web_lookup.wiki_json',return_value={'parse':{'text':'<p>Track details</p>'}}) as fetch:
            lookup('Guild Wars 2','Inner Nayos mastery track')
        self.assertEqual(fetch.call_args.args[2]['page'],'Secrets of the Obscure mastery tracks')
        self.assertIsNone(gw2_topic('Inner Nayos'))

    def test_map_content_access_and_routes_are_separate_from_rewards(self):
        result=map_context('A zone.\nGetting there\nThe episode is required to access this zone.\nComplete the story mission.\nUsing a portal scroll.\nMap completion\n1 piece of gear from the Elonian drop tables.\nLocations\nArea')
        self.assertIn('Required content access (NOT whole-episode completion)',result)
        self.assertIn('Choose ONE supported entry route',result)
        self.assertIn('Map completion reward, NOT a requirement',result)


if __name__=='__main__':unittest.main()
