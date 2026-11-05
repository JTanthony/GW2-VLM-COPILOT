"""A transient wiki failure may recover; sustained failures remain bounded."""
import io,json,unittest
from contextlib import redirect_stdout
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
from unittest.mock import MagicMock,patch
from waypoint.testing.text_sessions import run_sessions,SourceRecoveryBudget
from waypoint.assistant.local import Assistant
from waypoint.storage.resources import Resources

FAILURE='Online lookup failed during wiki retrieval (TimeoutError).'


class SourceRecoveryTests(unittest.TestCase):
    def test_reference_signal_clears_for_account_only_reply(self):
        with TemporaryDirectory() as folder:
            accounts=MagicMock();accounts.selected_game='Guild Wars 2'
            accounts.completion_answer.return_value=None;accounts.context.return_value=''
            client=MagicMock();client.complete.return_value='A reference-based answer.'
            assistant=Assistant(client,resources=Resources(folder),accounts=accounts)
            assistant.chat('Explain the named task',articles=[{'title':'Example','text':'Public facts'}])
            self.assertIs(assistant.last_research_has_evidence,True)
            accounts.completion_answer.return_value='Dated snapshot only.'
            assistant.chat('Show account progress')
            self.assertIs(assistant.last_research_has_evidence,False)

    def test_allowance_rearms_after_five_evidence_answers_and_five_minutes(self):
        budget=SourceRecoveryBudget();budget.record(True,False,0);budget.used=2
        for now in (20,40,60,80):self.assertFalse(budget.record(False,True,now))
        self.assertFalse(budget.record(False,True,100));self.assertEqual(budget.used,2)
        self.assertTrue(budget.record(False,True,301));self.assertEqual(budget.used,0)
        self.assertEqual(budget.rearms,1)

    def test_greetings_or_no_match_replies_do_not_rearm_allowance(self):
        budget=SourceRecoveryBudget();budget.record(True,False,0);budget.used=2
        for now in range(400,1000):self.assertFalse(budget.record(False,False,now))
        self.assertEqual(budget.used,2)

    def test_new_failure_resets_the_successful_period(self):
        budget=SourceRecoveryBudget();budget.record(True,False,0);budget.used=2
        for now in (10,20,30,40):budget.record(False,True,now)
        budget.record(True,False,500)
        self.assertFalse(budget.record(False,True,900));self.assertEqual(budget.successes,1)

    def run_batch(self,folder,checker,always_failed=False,sessions=2):
        first=MagicMock();first.chat.return_value=FAILURE
        second=MagicMock();second.chat.return_value='A verified answer.'
        factory=lambda session:first if always_failed or session==0 else second
        player=MagicMock();player.complete.return_value='{"question":"What is the next step?"}'
        accounts=SimpleNamespace(snapshot=None,names={},selected_game='Guild Wars 2')
        with redirect_stdout(io.StringIO()):
            result=run_sessions(player,factory,accounts,Path(folder)/'run',sessions=sessions,turns=5,delay=0,
                plans=[{'name':'test','game':'Guild Wars 2','starter':'Research the named task'}],
                source_check=checker,source_recovery_delays=(0,0))
        return result,first,second

    def test_healthy_probe_skips_failed_scene_and_resumes_next_scene(self):
        with TemporaryDirectory() as folder:
            checker=MagicMock(return_value=True)
            result,first,second=self.run_batch(folder,checker)
            self.assertEqual(result['stop_reason'],'session limit');self.assertEqual(result['cases'],8)
            self.assertEqual(first.chat.call_count,3);self.assertEqual(second.chat.call_count,5)
            checker.assert_called_once()
            self.assertEqual(result['source_recovery_checks'][0]['status'],'available')

    def test_first_probe_timeout_then_second_probe_recovers(self):
        with TemporaryDirectory() as folder:
            checker=MagicMock(side_effect=[TimeoutError(),True])
            result,_,_=self.run_batch(folder,checker)
            self.assertEqual(result['cases'],8);self.assertEqual(checker.call_count,2)
            self.assertEqual([x['status'] for x in result['source_recovery_checks']],['unavailable','available'])
            records=json.loads((Path(folder)/'run/source-recovery.json').read_text(encoding='utf-8'))
            self.assertEqual(records[0]['error_type'],'TimeoutError')

    def test_repeated_page_failures_stop_even_if_siteinfo_passes(self):
        with TemporaryDirectory() as folder:
            checker=MagicMock(return_value=True)
            result,first,_=self.run_batch(folder,checker,always_failed=True,sessions=10)
            self.assertEqual(result['stop_reason'],'source unavailable')
            self.assertEqual(result['cases'],9);self.assertEqual(first.chat.call_count,9)
            self.assertEqual(checker.call_count,2)

    def test_unconfirmed_probe_is_not_treated_as_recovery(self):
        with TemporaryDirectory() as folder:
            result,_,second=self.run_batch(folder,MagicMock(return_value=False))
            self.assertEqual(result['cases'],3);second.chat.assert_not_called()
            self.assertEqual(result['stop_reason'],'source unavailable')

    def test_stop_during_cooldown_does_not_make_network_request(self):
        with TemporaryDirectory() as folder:
            def stop_wait(seconds,stop,deadline):stop.touch();return False
            checker=MagicMock()
            with patch('waypoint.testing.text_sessions.wait_for_source',side_effect=stop_wait):
                result,_,second=self.run_batch(folder,checker)
            checker.assert_not_called();second.chat.assert_not_called()
            self.assertEqual(result['stop_reason'],'stop file');self.assertEqual(result['cases'],3)


if __name__=='__main__':unittest.main()
