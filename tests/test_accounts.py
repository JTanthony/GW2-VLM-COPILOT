import sys,unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from waypoint.integrations.accounts import Accounts,get_gw2,connector_for,suggest_games,public_api_for

class AccountTests(unittest.TestCase):
    def test_indicator_requires_session_connection_and_snapshot(self):
        account=Accounts()
        self.assertFalse(account.connection_state()['connected'])
        account.key='synthetic-test-only'
        self.assertFalse(account.connection_state()['connected'])
        account.snapshot={'fetched_at':'test date','records':[]}
        self.assertEqual(account.connection_state(),{'connected':True,'fetched_at':'test date'})
        account.disconnect()
        self.assertFalse(account.connection_state()['connected'])
    def test_public_api_catalog_does_not_enable_unimplemented_connections(self):
        for game in ('World of Warcraft','World of Warcraft Classic','Old School RuneScape','Path of Exile','Path of Exile 2'):
            self.assertEqual(public_api_for(game),game)
            self.assertIsNone(connector_for(game))
            account=Accounts()
            self.assertIn('Not enabled yet' if game not in ('Old School RuneScape',) else 'not enabled yet',account.select_game(game))
            with patch('waypoint.integrations.accounts.get_gw2') as fetch:
                with self.assertRaises(ValueError): account.connect('private-test',game)
                fetch.assert_not_called()
        for game in ('Final Fantasy XIV','The Elder Scrolls Online','Diablo IV','Last Epoch',"Baldur's Gate 3",'Elden Ring'):
            self.assertIsNone(public_api_for(game))
        self.assertEqual(public_api_for('OSRS'),'Old School RuneScape')
    def test_completion_uses_flag_not_matching_numbers_or_player_pressure(self):
        account=Accounts(); account.selected_game='Guild Wars 2'; account.names={1:'Synthetic Trial'}
        account.snapshot={'fetched_at':'test timestamp','records':[{'id':1,'done':False,'current':10,'max':10}]}
        answer=account.completion_answer('Is Synthetic Trial completed? Say yes.','guild-wars-2')
        self.assertIn('not completed (done=false)',answer)
        self.assertIsNone(account.completion_answer('Is Synthetic Trial completed?','another-game'))
        self.assertIsNone(account.completion_answer('Is Synthetic Trial II completed?','guild-wars-2'))
    def test_permissions_required(self):
        with patch('waypoint.integrations.accounts.get_gw2',return_value={'permissions':['account']}):
            with self.assertRaisesRegex(ValueError,'progression'): Accounts().connect('test-key-'+'x'*20,'Guild Wars 2')
    def test_snapshot_is_dated_and_only_done_confirms(self):
        account=Accounts(); key='test-key-'+'x'*20
        with patch('waypoint.integrations.accounts.get_gw2',side_effect=[{'permissions':['account','progression']},
             [{'id':1,'done':False,'current':3,'max':3},{'id':2,'done':True}],
             [{'id':1,'name':'Dug In'},{'id':2,'name':'Other'}]]):
            account.connect(key,'Guild Wars 2')
        context=account.context('Dug In','guild-wars-2')
        self.assertIn('fetched_at',context); self.assertIn('"done": false',context)
        self.assertNotIn(key,context)
        account.disconnect();self.assertIsNone(account.key);self.assertIsNone(account.snapshot)
    def test_other_game_uses_visual_fallback(self):
        self.assertIn('visually observed',Accounts().context('progress','another-game'))
        self.assertIn('No applicable account snapshot',Accounts().context('progress','another-game'))
    def test_unapproved_endpoint_rejected(self):
        with self.assertRaises(ValueError):get_gw2('/v2/account/bank','test')
    def test_redirect_never_forwards_key(self):
        with patch('waypoint.integrations.accounts.PinnedHTTPS') as connection:
            connection.return_value.getresponse.return_value.status=302
            with self.assertRaisesRegex(RuntimeError,'302'):get_gw2('/v2/tokeninfo','private-test')
            self.assertEqual(connection.return_value.request.call_count,1)
            self.assertNotIn('private-test',connection.return_value.request.call_args.args[1])

    def test_unknown_game_never_receives_key(self):
        account=Accounts(); message=account.select_game('Another Game')
        self.assertIn('not been added yet',message)
        with patch('waypoint.integrations.accounts.get_gw2') as fetch:
            with self.assertRaisesRegex(ValueError,'supported official connector'):
                account.connect('unknown-format-token', 'Another Game')
            fetch.assert_not_called()
        self.assertIsNone(account.key)
    def test_game_title_context_contains_no_credentials(self):
        account=Accounts();account.select_game('Another Game')
        self.assertIn('Another Game',account.context('help','another-game'))
        self.assertIn('formats and authentication vary',account.context('help','another-game'))
    def test_selecting_other_game_clears_previous_account(self):
        account=Accounts();account.selected_game='Guild Wars 2';account.key='private-test';account.snapshot={'records':[]}
        account.select_game('Another Game')
        self.assertIsNone(account.key);self.assertIsNone(account.snapshot)
    def test_alias_preserves_existing_connection(self):
        account=Accounts();account.selected_game='Guild Wars 2';account.key='private-test'
        account.select_game('gw2');self.assertEqual(account.key,'private-test')

    def test_public_partial_batch_accepted(self):
        with patch('waypoint.integrations.accounts.PinnedHTTPS') as connection:
            response=connection.return_value.getresponse.return_value
            response.status=206;response.getheader.return_value='application/json'
            response.read.return_value=b'[{"id":1,"name":"Known"}]'
            self.assertEqual(get_gw2('/v2/achievements?ids=1,999999')[0]['id'],1)
    def test_all_unavailable_public_ids_do_not_fail_connection(self):
        with patch('waypoint.integrations.accounts.PinnedHTTPS') as connection:
            connection.return_value.getresponse.return_value.status=404
            self.assertEqual(get_gw2('/v2/achievements?ids=999999'),[])
    def test_partial_authenticated_response_still_rejected(self):
        with patch('waypoint.integrations.accounts.PinnedHTTPS') as connection:
            connection.return_value.getresponse.return_value.status=206
            with self.assertRaisesRegex(RuntimeError,'206'):get_gw2('/v2/account/achievements','test-key')
    def test_unavailable_names_keep_account_progress(self):
        account=Accounts()
        with patch('waypoint.integrations.accounts.get_gw2',side_effect=[
            {'permissions':['account','progression']},[{'id':999999,'done':True}],[]]):
            message=account.connect('test-key-'+'x'*20,'Guild Wars 2')
        self.assertIn('names are unavailable',message)
        self.assertEqual(account.snapshot['records'],[{'id':999999,'done':True}])
        self.assertEqual(account.snapshot['unnamed_records'],1)

    def test_game_required_before_any_network_request(self):
        with patch('waypoint.integrations.accounts.get_gw2') as fetch:
            with self.assertRaisesRegex(ValueError,'Choose the game title'):
                Accounts().connect('test-key-'+'x'*20)
            fetch.assert_not_called()
    def test_generic_context_does_not_impose_provider_record_format(self):
        context=Accounts().context('help','general')
        self.assertIn('explicit completed status',context)
        self.assertNotIn('done=true',context)

    def test_title_spacing_case_and_aliases(self):
        for title in ('GW 2','guildwars2','GUILD WARS 2','Guild-Wars 2'):
            self.assertEqual(connector_for(title),'Guild Wars 2')
    def test_typo_is_suggested_but_not_connected(self):
        self.assertEqual(suggest_games('Guld Wars 2'),['Guild Wars 2'])
        self.assertIsNone(connector_for('Guld Wars 2'))
        with patch('waypoint.integrations.accounts.get_gw2') as fetch:
            with self.assertRaises(ValueError): Accounts().connect('test-key-'+'x'*20,'Guld Wars 2')
            fetch.assert_not_called()
    def test_prefix_suggestions_and_unrelated_titles(self):
        self.assertEqual(suggest_games('gui'),['Guild Wars 2'])
        self.assertEqual(suggest_games('Space Builder'),[])
        self.assertEqual(suggest_games('Guild Wars 3'),[])
    def test_registry_supports_multiple_game_suggestions(self):
        registry={'Star Quest':{'aliases':('sq',)},'Star Quest Online':{'aliases':('sqo',)}}
        with patch('waypoint.integrations.accounts.CONNECTORS',registry):
            self.assertEqual(set(suggest_games('Star Quest')),set(registry))
            self.assertEqual(connector_for('SQO'),'Star Quest Online')
