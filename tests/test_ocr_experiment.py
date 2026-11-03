import sys,threading,time,subprocess,unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import MagicMock,patch
import cv2,numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from waypoint.experiments.ocr_landmarks.reader import OCRReader,text_lines,REGIONS,EXCLUSIONS,mask_excluded
from waypoint.capture.feed import Feed

TSV='level\tpage_num\tblock_num\tpar_num\tline_num\tconf\ttext\n5\t1\t1\t1\t1\t95\tDragon\n5\t1\t1\t1\t1\t96\tVigil\n5\t1\t1\t1\t2\t20\tWrong\n'

class OCRTests(unittest.TestCase):
    def test_ui_toggle_installs_reader_and_off_restores_vision(self):
        from waypoint.ui.app import App
        app=App.__new__(App)
        app.ocr_enabled=MagicMock();app.ocr_enabled.get.return_value=True
        app.qwen_ocr=MagicMock();app.qwen_ocr.get.return_value=False
        app.ocr_executable=__file__;app.feed=MagicMock();app.ocr_label=MagicMock()
        app.status=MagicMock();app.show_ocr_readings=MagicMock()
        reader=MagicMock()
        with patch('waypoint.experiments.ocr_landmarks.reader.OCRReader',return_value=reader):
            app.toggle_ocr()
        app.feed.set_background_reader.assert_called_with(reader)
        app.show_ocr_readings.assert_called_once()
        app.ocr_enabled.get.return_value=False;app.toggle_ocr()
        app.feed.set_background_reader.assert_called_with(None)
        self.assertIsNone(app.ocr_reader)

    def test_cancelled_setup_does_not_change_existing_feed(self):
        from waypoint.ui.app import App
        app=App.__new__(App);app.ocr_executable='';app.root=MagicMock()
        app.ocr_enabled=MagicMock();app.ocr_enabled.get.return_value=True
        app.feed=MagicMock()
        with patch('waypoint.ui.app.filedialog.askopenfilename',return_value=''):
            app.toggle_ocr()
        app.ocr_enabled.set.assert_called_once_with(False)
        app.feed.set_background_reader.assert_not_called()

    def test_confidence_filter_preserves_lines_without_claiming_meaning(self):
        self.assertEqual(text_lines(TSV),['Dragon Vigil'])
        self.assertEqual(text_lines('bad header\ninvalid'),[])
        with self.assertRaises(ValueError): text_lines('x'*1_000_001)

    def test_engine_requires_real_path_and_language_data(self):
        with TemporaryDirectory() as folder:
            executable=Path(folder)/'tesseract.exe'; executable.touch()
            with self.assertRaises(ValueError): OCRReader(executable)
            (Path(folder)/'tessdata').mkdir(); (Path(folder)/'tessdata/eng.traineddata').touch()
            self.assertEqual(OCRReader(executable).executable,str(executable.resolve()))

    def test_full_window_tiles_use_memory_pipes_bounded_threads_and_no_semantic_guesses(self):
        reader=OCRReader.__new__(OCRReader);reader.executable='C:/OCR/tesseract.exe'
        png=cv2.imencode('.png',np.zeros((1080,1920),dtype=np.uint8))[1].tobytes()
        with patch('waypoint.experiments.ocr_landmarks.reader.subprocess.run',return_value=MagicMock(returncode=0,stdout=TSV.encode())) as run:
            result=reader.observe(png)
        self.assertEqual(run.call_count,4)
        for call,rect in zip(run.call_args_list,REGIONS.values()):
            self.assertEqual(call.args[0][1:3],['stdin','stdout'])
            self.assertNotIn('shell',call.kwargs)
            self.assertEqual(call.kwargs['env']['OMP_THREAD_LIMIT'],'2')
            self.assertEqual(call.kwargs['timeout'],4)
            pixels=cv2.imdecode(np.frombuffer(call.kwargs['input'],dtype=np.uint8),0)
            left,top,right,bottom=rect
            self.assertEqual(pixels.shape,(2*(int(bottom*1080)-int(top*1080)),2*(int(right*1920)-int(left*1920))))
        self.assertIsNone(result['map']); self.assertIsNone(result['event'])
        self.assertEqual(len(result['visible_text']),1)  # Overlap deduplicated.

    def test_chat_and_skill_pixels_are_removed_before_any_ocr_crop(self):
        pixels=np.full((100,200),17,dtype=np.uint8)
        masked=mask_excluded(pixels)
        for left,top,right,bottom in EXCLUSIONS.values():
            self.assertTrue(np.all(masked[int(top*100):int(bottom*100),int(left*200):int(right*200)]==255))
        self.assertTrue(np.all(pixels==17))
        self.assertEqual(masked[5,5],17)  # Map title retained.
        self.assertEqual(masked[90,190],17)  # Minimap retained.
        self.assertEqual(masked[68,48],255)  # Larger Oct 24 chat header.
        self.assertEqual(masked[90,62],255)  # Left edge of expanded skill bar.
        coverage=np.zeros_like(pixels)
        for left,top,right,bottom in REGIONS.values():
            coverage[int(top*100):int(bottom*100),int(left*200):int(right*200)]=1
        self.assertTrue(np.all(coverage))

    def test_literal_quotes_cannot_merge_tsv_rows_into_numeric_garbage(self):
        header=TSV.splitlines()[0]+'\n'
        rows='5\t1\t1\t1\t1\t95\t"\n5\t1\t1\t1\t2\t95\tDesert Highlands\n'
        self.assertEqual(text_lines(header+rows),['Desert Highlands'])
        self.assertEqual(text_lines(header+'5\t1\t1\t1\t1\t95\tText\textra\n'),[])

    def test_low_confidence_word_is_marked_not_silently_removed_from_name(self):
        sample=TSV.replace('95\tDragon','95\tAbandoned').replace('96\tVigil','35\tNecklace')
        self.assertEqual(text_lines(sample),['[uncertain] Abandoned Necklace'])

    def test_noise_does_not_hide_event_after_watch_list(self):
        header=TSV.splitlines()[0]+'\n'
        rows=[f'5\t1\t1\t1\t{i+1}\t95\t{text}\n' for i,text in enumerate(['=','@','Wx','4','Token Collector','Powered Up','Escort ogres through the mountains'])]
        self.assertEqual(text_lines(header+''.join(rows)),['Token Collector','Powered Up','Escort ogres through the mountains'])

    def test_adjacent_heading_fragments_merge_using_coordinates(self):
        header='level\tpage_num\tblock_num\tpar_num\tline_num\tconf\ttext\tleft\ttop\twidth\theight\n'
        rows=['5\t1\t2\t1\t1\t95\tEarned\t92\t10\t45\t20\n',
              '5\t1\t3\t1\t1\t95\tMastery Point\t0\t10\t85\t20\n',
              '5\t1\t4\t1\t1\t95\tSeparate label\t400\t10\t80\t20\n']
        self.assertEqual(text_lines(header+''.join(rows)),['Mastery Point Earned','Separate label'])

    def test_failure_does_not_run_a_model_fallback(self):
        reader=OCRReader.__new__(OCRReader);reader.executable='C:/OCR/tesseract.exe'
        png=cv2.imencode('.png',np.zeros((100,100),dtype=np.uint8))[1].tobytes()
        with patch('waypoint.experiments.ocr_landmarks.reader.subprocess.run',side_effect=subprocess.TimeoutExpired('ocr',4)):
            with self.assertRaises(subprocess.TimeoutExpired): reader.observe(png)
        with self.assertRaises(ValueError): reader.observe(b'invalid')

    def test_review_readings_never_become_model_observations_and_off_clears_them(self):
        feed=Feed(None,MagicMock(),threading.Lock(),threading.Event())
        feed.frame=(time.monotonic(),b'fixture')
        reader=MagicMock();reader.observe.return_value={'visible_text':['OCR tracker: Dragon Vigil']}
        feed.set_background_reader(reader)
        feed.review_callback=lambda *args,**kwargs:feed.stop()
        worker=threading.Thread(target=feed.observe_loop);worker.start();worker.join(2)
        feed.stop();worker.join(2)
        self.assertFalse(worker.is_alive()); self.assertIsNotNone(feed.ocr_context())
        self.assertEqual(feed.observation_context(),(None,None))
        feed.assistant.observe.assert_not_called()
        feed.set_background_reader(None)
        self.assertIsNone(feed.ocr_context());self.assertEqual(feed.backend_state()['background_backend'],'vlm')

    def test_switch_discards_inflight_ocr_result(self):
        feed=Feed(None,MagicMock(),threading.Lock(),threading.Event())
        feed.frame=(time.monotonic(),b'fixture')
        def switch(png):
            feed.set_background_reader(None);feed.stop()
            return {'visible_text':['stale']}
        reader=MagicMock();reader.observe.side_effect=switch
        feed.set_background_reader(reader)
        worker=threading.Thread(target=feed.observe_loop);worker.start();worker.join(2)
        feed.stop();worker.join(2)
        self.assertFalse(worker.is_alive());self.assertIsNone(feed.ocr_context())
        self.assertEqual(feed.observation_context(),(None,None))

if __name__=='__main__':unittest.main()
