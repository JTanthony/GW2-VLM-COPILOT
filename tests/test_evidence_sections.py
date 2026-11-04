"""Regressions for confusing wiki rewards, objective rows and map metadata."""
import unittest
from unittest.mock import MagicMock,patch
from waypoint.assistant.rules.evidence import focus_articles
from waypoint.assistant.web_lookup import context,WikiText,verified_list
from waypoint.inference.budget import compact
from waypoint.assistant.research import research


class EvidenceSectionTests(unittest.TestCase):
    def event(self):
        return {'title':'Example escort','text':'Article details:\nLocation Example Valley (Example Map) Event type Group event Level 76\nObjectives\nTroops alive: x/10\nRewards\n | Reward tier | Experience | Karma | Coin\n | Gold | 15,068 | 360 | 84 [copper coin]\n | Silver | 12,808 | 306 | 71 [copper coin]\nThese are the expected rewards for a level 76 player.\nNotes\nThe following escort continues only if camp is not under attack.'}

    def test_event_reward_units_survive_compaction_and_do_not_mutate_source(self):
        source=self.event();articles=focus_articles('What rewards does Example escort give?',[source])
        text=articles[0]['text']
        self.assertIn('earned XP=15,068; karma=360; currency=84 copper',text)
        self.assertIn('Medal is NOT currency',text);self.assertIn('difficulty label',text)
        self.assertNotIn('focus_text',source)
        for level in (1,2):
            reduced=compact('Player question: What rewards?\nEnd player question.\n'+context(articles),level)
            self.assertIn('currency=84 copper',reduced);self.assertIn('earned XP=15,068',reduced)

    def test_unsolicited_rewards_are_excluded_but_trigger_note_is_retained(self):
        result=focus_articles('How do I start Example escort?',[self.event()])[0]['text']
        self.assertNotIn('15,068',result);self.assertNotIn('84 [copper',result)
        self.assertIn('following escort',result)
        self.assertIn('does not itself prove solo participation is forbidden',result)

    def test_achievement_keeps_counter_and_own_collection_names(self):
        source={'title':'Example Collection','item_names':['Example Collection'],
                'text':'Article details:\n | Example Collection | Category | 3\n | Unlock all 16 skins. Reward: Bag | Unlocked 1 Skin | 1\n | Unlocked 8 Skins | 1\n | Unlocked 16 Skins | 1\nCollection items\n | | Collectible | Type |\n'+''.join(f' | {i} | Skin {i} | Skin |\n' for i in range(1,17))+'Notes\nYou only have to unlock the skins.\nTrivia\nUnrelated.'}
        focused=focus_articles('How do I complete Example Collection?',[source])[0]
        self.assertIn('Unlocked 16 Skins',focused['focus_text'])
        for i in range(1,17):self.assertIn('Skin '+str(i),focused['focus_text'])
        self.assertNotIn('Bag',focused['focus_text'])
        answer=verified_list('List the 16 required skins',[focused])
        self.assertIn('16 retrieved names',answer)
        for i in range(1,17):self.assertIn('- Skin '+str(i),answer)
        self.assertNotIn('- Example Collection',answer)

    def test_map_type_does_not_erase_story_description_or_access(self):
        article={'title':'Story staging area','focus_text':'Subject: Story staging area | Type: Zone | Region: Example',
                 'text':'Article details:\nThis article is about the story instance. It is a staging area for the final mission.\nGetting there\nComplete the previous chapter or return via the named NPC.\nMap completion\n1 piece of rare gear\nLocations\n | Subarea | 80 | 10'}
        focused=focus_articles('How do I access Story staging area?',[article])[0]['text']
        self.assertIn('story instance',focused);self.assertIn('named NPC',focused)
        self.assertNotIn('1 piece of rare gear',focused);self.assertNotIn('Subarea',focused)

    def test_objective_icon_labels_are_preserved(self):
        parser=WikiText();parser.feed('<p>4 <img alt="Waypoint">2 <img alt="Renown Heart">30 <img alt="Point of Interest">4 <img alt="Vista"></p>')
        text=''.join(parser.parts)
        self.assertIn('4 [waypoint]',text);self.assertIn('30 [point of interest]',text)
        focused=focus_articles('Map completion', [{'title':'Example','focus_text':'Type: Zone','text':'Article details:\n'+text}])[0]['text']
        self.assertIn('waypoint: 4',focused);self.assertIn('point of interest: 30',focused)

    def test_map_gear_drop_is_labeled_reward_rather_than_discarded(self):
        source={'title':'Example','focus_text':'Type: Zone','text':'Article details:\nExample zone.\nMap completion\n1 piece of gear of Rare or higher rarity from the Elonian drop tables.\nLocations\nArea'}
        result=focus_articles('Do I need rare gear for map completion?',[source])[0]['text']
        self.assertIn('Map completion reward, NOT a requirement: 1 piece of gear',result)

    def test_mastery_order_and_distinct_costs_remain_explicit(self):
        article={'title':'Example tracks','text':'Other track', 'focus_text':'\n'.join(f'Section: Test | Mastery: Level {i} | XP required: {i}00 | Points: {i} | Description: Learn ability {i}.' for i in range(1,5))}
        result=focus_articles('Test mastery',[article])[0]['focus_text']
        self.assertIn('later levels require earlier levels',result)
        for i in range(1,5):self.assertIn(f'Points: {i} (cost)',result)

    @patch('waypoint.assistant.research.lookup')
    def test_xp_followup_supplements_ability_without_replacing_it(self,fetch):
        client=MagicMock();client.complete.return_value='{"game":"Guild Wars 2","query":"Example ability"}'
        ability={'title':'Example ability','text':'Ability evidence','focus_text':'Track: Test | Experience: 100'}
        fetch.side_effect=[[ability],[{'title':'Mastery','text':'Generic training evidence'}]]
        articles,notice=research(client,'How can I earn XP for Example ability?',[],selected_game='Guild Wars 2')
        self.assertEqual([a['title'] for a in articles],['Example ability','Mastery'])
        self.assertEqual(fetch.call_count,2);self.assertEqual(notice,'')

    @patch('waypoint.assistant.research.lookup')
    def test_optional_mastery_source_failure_preserves_verified_ability(self,fetch):
        client=MagicMock();client.complete.return_value='{"game":"Guild Wars 2","query":"Example ability"}'
        fetch.side_effect=[[{'title':'Example ability','text':'Ability evidence','focus_text':'Track: Test | Experience: 100'}],TimeoutError()]
        articles,notice=research(client,'How can I earn XP for Example ability?',[])
        self.assertEqual(len(articles),1);self.assertEqual(articles[0]['title'],'Example ability')
        self.assertEqual(notice,'')


if __name__=='__main__':unittest.main()
