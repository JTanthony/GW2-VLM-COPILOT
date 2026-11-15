import sys,json,time,unittest
from pathlib import Path
from datetime import datetime,timezone,timedelta
from unittest.mock import MagicMock
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from waypoint.experiments.ocr_landmarks.nearby import NearbyGate,RULES,matches,unfinished,verify

NOW=datetime(2026,10,24,23,tzinfo=timezone.utc)
def snapshot(done=False):return {'fetched_at':NOW.isoformat(),'records':[{'id':3870,'done':done,'current':0,'max':1}]}
def observation():return {'visible_text':['OCR upper right: Facing the Truth','OCR upper left: Wedge Symbol! Hollow,','OCR upper right: wedge symbols: 0/5']}

class NearbyTests(unittest.TestCase):
    def test_ui_map_intro_reads_ocr_and_respects_hints_switch(self):
        from waypoint.ui.app import App
        from waypoint.assistant.achievement_intro import AchievementIntro
        app=App.__new__(App)
        app.ocr_tips=MagicMock();app.ocr_tips.get.return_value=True
        app.ocr_reader=MagicMock();app.feed=MagicMock()
        app.busy=False;app.closing=False
        app.achievement_intro=AchievementIntro({'verified_at':'test','maps':[{'map_name':'Test Map',
            'category_id':1,'achievements':[{'id':10}]}]})
        app.accounts=MagicMock()
        app.accounts.selected_game='Guild Wars 2'
        app.accounts.snapshot={'fetched_at':NOW.isoformat(),'records':[{'id':10,'done':True}]}
        app.append=MagicMock();app.mark_response=MagicMock();app.record_review=MagicMock()
        app.assistant=MagicMock();app.assistant.history=[]
        obs={'visible_text':['OCR upper left: Test Map','OCR upper left: Completion']}
        app.feed.ocr_context.return_value=(1,obs)
        app.announce_achievement_count()
        app.feed.ocr_context.return_value=(2,obs)
        app.announce_achievement_count()
        app.append.assert_called_once()
        self.assertIn('1/1',app.append.call_args.args[1])
        app.feed.observation_context.assert_not_called()
        app.ocr_tips.get.return_value=False
        app.feed.ocr_context.reset_mock()
        app.announce_achievement_count()
        app.feed.ocr_context.assert_not_called()

    def test_new_landmarks_require_local_text_and_unfinished_account_record(self):
        cases={
            'lohrashi-dive':['Lohrashi the Mournful','Defeat Lohrashi the','Time limit:'],
            'forgotten-teleporter':['Forgotten Teleporter'],
        }
        for rule,lines in cases.items():
            obs={'visible_text':['OCR upper right: '+line for line in lines]}
            self.assertTrue(matches(rule,obs))
            snap={'fetched_at':NOW.isoformat(),'records':[{'id':RULES[rule]['id'],'done':False}]}
            gate=NearbyGate()
            self.assertIsNone(gate.consider(obs,100,snap,NOW,102))
            self.assertEqual(gate.consider(obs,107,snap,NOW,109),rule)
            self.assertIsNotNone(gate.deliver(rule,True,obs,107,snap,NOW,110))
            for record in ([],[{'id':RULES[rule]['id'],'done':True}]):
                blocked=NearbyGate()
                blocked_snapshot={'fetched_at':NOW.isoformat(),'records':record}
                self.assertIsNone(blocked.consider(obs,100,blocked_snapshot,NOW,102))
                self.assertIsNone(blocked.consider(obs,107,blocked_snapshot,NOW,109))
            self.assertFalse(matches(rule,{'visible_text':['OCR upper right: [uncertain] '+line for line in lines]}))
        self.assertFalse(matches('lohrashi-dive',{'visible_text':['OCR upper right: Lohrashi the Mournful']}))
        self.assertFalse(matches('forgotten-teleporter',{'visible_text':[
            'OCR upper right: Kaidenna and a small band of Followers of',
            'OCR upper right: Ascension seek a Forgotten teleporter to access']}))

    def delivery_app(self):
        from waypoint.ui.app import App
        app=App.__new__(App);app.closing=False;app.busy=False
        app.ocr_tips=MagicMock();app.ocr_tips.get.return_value=True;app.ocr_reader=MagicMock()
        feed=MagicMock();feed.stop_event.is_set.return_value=False;feed.reader_generation=2
        feed.ocr_context.return_value=(time.monotonic()-1,observation());app.feed=feed
        gate=NearbyGate();gate.pending='wedge-puzzle';app.nearby_gate=gate
        snap={'fetched_at':datetime.now(timezone.utc).isoformat(),'records':[{'id':3870,'done':False}]}
        app.nearby_account=MagicMock(return_value=(snap,4))
        app.append=MagicMock();app.mark_response=MagicMock();app.record_review=MagicMock()
        app.assistant=MagicMock();app.assistant.history=[]
        result=dict(gate=gate,feed=feed,rule='wedge-puzzle',approved=True,error=None,account_generation=4,reader_generation=2)
        return app,result

    def test_ui_posts_once_and_marks_unread_without_unlocking_player_work(self):
        app,result=self.delivery_app();app.finish_nearby_tip(result);app.finish_nearby_tip(result)
        app.append.assert_called_once();app.mark_response.assert_called_once()
        self.assertEqual(len(app.assistant.history),1)
        self.assertEqual(sum(call.args[0]=='ocr_achievement_tip' for call in app.record_review.call_args_list),1)

    def test_jimoh_requires_npc_and_escort_not_watch_list(self):
        obs={'visible_text':['OCR lower right: Jimoh','OCR upper right: defectors alive and reach']}
        for rule in ('jimoh-flowers','jimoh-defectors'):
            self.assertTrue(matches(rule,obs))
            for lines in (['Jimoh'],['Flowers for Jimoh','Defector Protector'],
                          ['[uncertain] Jimoh','Elonian Defectors Alive: 2'],
                          ['Jimoh','Elonian Defectors Alive: 12']):
                self.assertFalse(matches(rule,{'visible_text':['OCR upper right: '+l for l in lines]}))
        self.assertIn('If you have already',RULES['jimoh-flowers']['tip'])
        self.assertIn('all ten',RULES['jimoh-defectors']['tip'])
        self.assertIn('cannot confirm',RULES['jimoh-defectors']['tip'])

    def test_augury_needs_local_cue_and_opening_not_browsed_title(self):
        for lines in (['Augury Rock is open.'],['Flameseeker Prophecies','Augury Rock is open.'],
                      ['Flameseeker Prophecies of Glint','Scroll 3, Verse 5 (Encrypted)'],
                      ['Forgotten Light'],['Branded Chest','Augury Rock is open.']):
            self.assertFalse(matches('augury-verses',{'visible_text':['OCR upper right: '+l for l in lines]}))
        self.assertTrue(matches('augury-verses',{'visible_text':['OCR upper right: Augury Rock open.',
            'OCR upper left: Flame Seeker: Verse 2']}))
        self.assertFalse(matches('augury-verses',{'visible_text':['OCR upper right: Augury Rock open.',
            'OCR upper right: Augury Rock is closed.','OCR upper left: Forgotten Light']}))

    def test_augury_short_memory_bridges_fragmented_passes(self):
        gate=NearbyGate();snap={'fetched_at':NOW.isoformat(),'records':[{'id':3604,'done':False}]}
        first={'visible_text':['OCR upper right: Augury Rock open.','OCR upper left: Flame Seeker: Verse 1']}
        second={'visible_text':['OCR upper left: Forgotten Light']}
        self.assertIsNone(gate.consider(first,100,snap,NOW,102))
        self.assertEqual(gate.consider(second,107,snap,NOW,109),'augury-verses')
        self.assertTrue(matches('augury-verses',gate.pending_evidence))
        self.assertIn('Flameseeker',gate.deliver('augury-verses',True,second,107,snap,NOW,115))
        self.assertEqual(set(gate.augury),{'open','local'})

    def test_augury_cache_expires_and_explicit_closure_clears_it(self):
        snap={'fetched_at':NOW.isoformat(),'records':[{'id':3604,'done':False}]}
        for second,stamp in [({'visible_text':['OCR upper left: Forgotten Light']},125),
            ({'visible_text':['OCR upper right: Augury Rock is closed.','OCR upper left: Forgotten Light']},107),
            ({'visible_text':['OCR upper left: unrelated scenery']},107)]:
            gate=NearbyGate()
            gate.consider({'visible_text':['OCR upper right: Augury Rock open.','OCR upper left: Forgotten Light']},100,snap,NOW,102)
            self.assertIsNone(gate.consider(second,stamp,snap,NOW,stamp+2))
        gate=NearbyGate();first={'visible_text':['OCR upper right: Augury Rock open.','OCR upper left: Forgotten Light']}
        gate.consider(first,100,snap,NOW,102);gate.consider({'visible_text':['OCR upper left: Forgotten Light']},107,snap,NOW,109)
        self.assertIsNone(gate.deliver('augury-verses',True,{'visible_text':['OCR upper left: Forgotten Light']},107,snap,NOW,123))

    def test_new_rules_suppress_completed_missing_stale_and_disconnected(self):
        observations={
            'jimoh-flowers':{'visible_text':['OCR lower right: Jimoh','OCR lower right: Elonian Defectors Alive: 2']},
            'jimoh-defectors':{'visible_text':['OCR lower right: Jimoh','OCR lower right: Elonian Defectors Alive: 2']},
            'augury-verses':{'visible_text':['OCR upper right: Augury Rock open.','OCR upper left: Forgotten Light']}}
        for rule,obs in observations.items():
            for snap in (None,{'fetched_at':NOW.isoformat(),'records':[]},
                {'fetched_at':NOW.isoformat(),'records':[{'id':RULES[rule]['id'],'done':True}]},
                {'fetched_at':(NOW-timedelta(days=2)).isoformat(),'records':[{'id':RULES[rule]['id'],'done':False}]}):
                gate=NearbyGate()
                self.assertIsNone(gate.consider(obs,100,snap,NOW,102))
                self.assertIsNone(gate.consider(obs,107,snap,NOW,109))
                self.assertNotIn('records',gate.audit)
                self.assertTrue(all(set(r)=={'rule','matched','account_status','attempted'} for r in gate.audit['rules']))

    def test_jimoh_prioritizes_one_hint_for_same_encounter(self):
        snap={'fetched_at':NOW.isoformat(),'records':[{'id':3706,'done':False},{'id':3611,'done':False}]}
        obs={'visible_text':['OCR lower right: Jimoh','OCR lower right: Elonian Defectors Alive: 2']}
        gate=NearbyGate();gate.consider(obs,100,snap,NOW,102)
        self.assertEqual(gate.consider(obs,107,snap,NOW,109),'jimoh-flowers')
        gate.deliver('jimoh-flowers',True,obs,107,snap,NOW,115)
        self.assertIsNone(gate.consider(obs,114,snap,NOW,116))

    def test_recording_gap_does_not_count_as_consecutive_confirmation(self):
        gate=NearbyGate();obs=observation()
        gate.consider(obs,100,snapshot(),NOW,102)
        self.assertIsNone(gate.consider(obs,150,snapshot(),NOW,152))
        self.assertEqual(gate.consider(obs,157,snapshot(),NOW,159),'wedge-puzzle')

    def test_new_verifier_excludes_unrelated_text_and_rejects_missing_evidence(self):
        snap={'fetched_at':NOW.isoformat(),'records':[{'id':3706,'done':False}]}
        client=MagicMock();client.complete.return_value=json.dumps({'notify':True,'rule':'jimoh-flowers'})
        obs={'visible_text':['OCR lower right: Jimoh','OCR lower right: Elonian Defectors Alive: 2','OCR upper left: unrelated personal text']}
        self.assertTrue(verify(client,'jimoh-flowers',obs,snap,NOW))
        self.assertNotIn('personal text',client.complete.call_args.args[0])
        client.reset_mock();self.assertFalse(verify(client,'jimoh-flowers',{'visible_text':[]},snap,NOW));client.complete.assert_not_called()

    def test_ui_discards_after_account_or_capture_change(self):
        for change in ['account','capture','busy','disabled']:
            app,result=self.delivery_app()
            if change=='account':result['account_generation']=3
            elif change=='capture':result['reader_generation']=1
            elif change=='busy':app.busy=True
            else:app.ocr_tips.get.return_value=False
            app.finish_nearby_tip(result);app.append.assert_not_called()

    def test_watch_list_or_selected_chapter_is_not_nearby(self):
        self.assertFalse(matches('wedge-puzzle',{'visible_text':['OCR upper right: Perfect Match','OCR upper right: Facing the Truth']}))
        self.assertFalse(matches('wedge-puzzle',{'visible_text':['OCR upper left: Wedge Symbol Hollow']}))
        bad=observation();bad['visible_text'][-1]='OCR upper right: wedge symbols: 07/5'
        self.assertFalse(matches('wedge-puzzle',bad))
        self.assertFalse(matches('dwarven-chest',{'visible_text':['OCR upper left: [uncertain] Lost Dwarven Chest']}))

    def test_api_completion_missing_and_stale_all_suppress(self):
        self.assertFalse(unfinished(snapshot(True),3870,NOW))
        self.assertFalse(unfinished(None,3870,NOW))
        self.assertFalse(unfinished({'fetched_at':NOW.isoformat(),'records':[]},3870,NOW))
        self.assertFalse(unfinished(snapshot(),3870,NOW+timedelta(days=2)))
        duplicate=snapshot();duplicate['records'].append({'id':3870,'done':True})
        self.assertFalse(unfinished(duplicate,3870,NOW))

    def test_two_distinct_fresh_passes_and_qwen_approval_are_required(self):
        gate=NearbyGate();obs=observation()
        self.assertIsNone(gate.consider(obs,100,snapshot(),NOW,101))
        self.assertIsNone(gate.consider(obs,100,snapshot(),NOW,102))
        self.assertEqual(gate.consider(obs,107,snapshot(),NOW,108),'wedge-puzzle')
        self.assertIsNone(gate.deliver('wedge-puzzle',False,obs,107,snapshot(),NOW,109))
        self.assertFalse(gate.sent)
        self.assertIsNone(gate.consider(obs,114,snapshot(),NOW,115))  # No repeated model polling.

    def test_once_per_session_and_completed_recheck(self):
        gate=NearbyGate();obs=observation()
        gate.consider(obs,100,snapshot(),NOW,101);gate.consider(obs,107,snapshot(),NOW,108)
        self.assertIsNone(gate.deliver('wedge-puzzle',True,obs,107,snapshot(True),NOW,109))
        gate=NearbyGate();gate.consider(obs,100,snapshot(),NOW,101);gate.consider(obs,107,snapshot(),NOW,108)
        message=gate.deliver('wedge-puzzle',True,obs,107,snapshot(),NOW,109)
        self.assertIn('Perfect Match',message);self.assertIn('still eligible',message)
        self.assertIsNone(gate.consider(obs,114,snapshot(),NOW,115))
        self.assertIsNone(gate.deliver('wedge-puzzle',True,obs,107,snapshot(),NOW,110))

    def test_stale_or_departed_subject_cannot_deliver_late(self):
        for clock,obs in [(130,observation()),(109,{'visible_text':[]})]:
            gate=NearbyGate();gate.consider(observation(),100,snapshot(),NOW,101);gate.consider(observation(),107,snapshot(),NOW,108)
            self.assertIsNone(gate.deliver('wedge-puzzle',True,obs,107,snapshot(),NOW,clock))

    def test_verifier_cannot_invent_an_achievement_or_receive_credentials(self):
        client=MagicMock();client.complete.return_value=json.dumps({'notify':True,'rule':'invented','reason':'yes'})
        self.assertFalse(verify(client,'wedge-puzzle',observation(),snapshot(),NOW))
        client.complete.return_value=json.dumps({'notify':True,'rule':'wedge-puzzle','reason':'active puzzle'})
        self.assertTrue(verify(client,'wedge-puzzle',observation(),snapshot(),NOW))
        prompt=client.complete.call_args.args[0]
        self.assertIn('without mistake',prompt);self.assertNotIn('fetched_at',prompt)
        self.assertNotIn('image',client.complete.call_args.kwargs)
        obs=observation();obs['visible_text'].append('OCR lower left: unrelated private chatter')
        verify(client,'wedge-puzzle',obs,snapshot(),NOW)
        self.assertNotIn('private chatter',client.complete.call_args.args[0])

if __name__=='__main__':unittest.main()
