import sys,time,threading,unittest
from pathlib import Path
from unittest.mock import patch,MagicMock
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from waypoint.capture.feed import Feed

class FeedTests(unittest.TestCase):
    def test_default_capture_samples_every_five_seconds(self):
        feed=Feed(None,None,threading.Lock(),threading.Event())
        self.assertEqual(feed.interval,5)

    def test_capture_accepts_between_samples_but_rejects_stale_frames(self):
        from waypoint.capture.graphics import WindowCapture
        capture=WindowCapture.__new__(WindowCapture)
        capture.target=None;capture.interval=5;capture.lock=threading.Lock()
        capture.closed=False;capture.error=None;capture.frame=(96,b'png')
        with patch('waypoint.capture.graphics.validate_target'),patch('waypoint.capture.graphics.time.monotonic',return_value=100):
            self.assertEqual(capture.snapshot(),(96,b'png'))
            capture.frame=(92,b'old')
            with self.assertRaisesRegex(RuntimeError,'new game frames'):capture.snapshot()

    def test_latest_frame_bounded_and_capture_stops(self):
        feed=Feed(None,MagicMock(),threading.Lock(),threading.Event(),fps=20)
        with patch('waypoint.capture.feed.WindowCapture') as backend:
            backend.return_value.snapshot.side_effect=lambda:(time.monotonic(),b'png')
            feed.start(); time.sleep(.16); feed.stop(); feed.wait()
        self.assertGreaterEqual(feed.count,2)
        backend.return_value.stop.assert_called_once()
        backend.return_value.wait.assert_called_once()
        self.assertEqual(feed.snapshot()[1],b'png')
        count=feed.count; time.sleep(.06); self.assertEqual(feed.count,count)
    def test_stale_frame_refused(self):
        feed=Feed(None,None,threading.Lock(),threading.Event())
        feed.frame=(time.monotonic()-11,b'old')
        with self.assertRaisesRegex(RuntimeError,'recent'): feed.snapshot()
    def test_observation_cache_refuses_stale_evidence(self):
        feed=Feed(None,None,threading.Lock(),threading.Event())
        feed.observation=(time.monotonic(),{'summary':'recent'})
        self.assertEqual(feed.recent_observation(),{'summary':'recent'})
        feed.observation=(time.monotonic()-11,{'summary':'old'})
        self.assertIsNone(feed.recent_observation())
    def test_slow_observation_available_as_dated_context(self):
        feed=Feed(None,None,threading.Lock(),threading.Event())
        feed.observation=(time.monotonic()-35,{'summary':'last screen'})
        self.assertIsNone(feed.recent_observation())
        observation,age=feed.observation_context()
        self.assertEqual(observation,{'summary':'last screen'})
        self.assertGreaterEqual(age,35)
        feed.observation=(time.monotonic()-91,{'summary':'too old'})
        self.assertEqual(feed.observation_context(),(None,None))
    def test_pending_question_prevents_background_inference(self):
        pending=threading.Event(); pending.set(); assistant=MagicMock()
        feed=Feed(None,assistant,threading.Lock(),pending,fps=20)
        with patch('waypoint.capture.feed.WindowCapture') as backend:
            backend.return_value.snapshot.side_effect=lambda:(time.monotonic(),b'png')
            feed.start(); time.sleep(.16); feed.stop(); feed.wait()
        assistant.observe.assert_not_called()

    def test_capture_pause_clears_frame(self):
        feed=Feed(None,None,threading.Lock(),threading.Event())
        feed.frame=(time.monotonic(),b'old')
        with patch('waypoint.capture.feed.WindowCapture') as backend:
            backend.return_value.snapshot.side_effect=RuntimeError('Restore selected game')
            thread=threading.Thread(target=feed.capture_loop); thread.start()
            time.sleep(.12); feed.stop(); thread.join()
        self.assertIsNone(feed.frame)
        with self.assertRaisesRegex(RuntimeError,'recent'): feed.snapshot()
    def test_same_native_frame_is_not_refreshed(self):
        feed=Feed(None,None,threading.Lock(),threading.Event())
        stamp=time.monotonic()
        with patch('waypoint.capture.feed.WindowCapture') as backend:
            backend.return_value.snapshot.return_value=(stamp,b'png')
            thread=threading.Thread(target=feed.capture_loop); thread.start()
            time.sleep(.22); feed.stop(); thread.join()
        self.assertEqual(feed.count,1)
        self.assertEqual(feed.frame[0],stamp)
