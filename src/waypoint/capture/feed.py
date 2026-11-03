"""Bounded in-memory capture feed. Capture rate is separate from inference rate."""
import threading,time
from .graphics import WindowCapture
from .progress import ProgressGate

class Feed:
    def __init__(self,target,assistant,inference_lock,question_pending,fps=2,max_width=1280,review_callback=None,frame_callback=None):
        self.review_callback=review_callback
        self.frame_callback=frame_callback
        self.target=target; self.assistant=assistant; self.inference_lock=inference_lock
        self.question_pending=question_pending; self.interval=1/fps; self.max_width=max_width
        self.stop_event=threading.Event(); self.lock=threading.Lock()
        self.frame=None; self.observation=None; self.error=None; self.count=0
        self.vision_error=None; self.analyzing=False
        self.background_reader=None; self.reader_generation=0; self.analysis_seconds=None
        self.ocr_observation=None
        self.threads=[]
    def start(self):
        for fn in (self.capture_loop,self.observe_loop):
            t=threading.Thread(target=fn,daemon=True); self.threads.append(t); t.start()
    def stop(self): self.stop_event.set()
    def set_background_reader(self,reader):
        """Switch only background extraction; discard stale results across modes."""
        with self.lock:
            self.background_reader=reader; self.reader_generation+=1
            self.observation=None; self.vision_error=None; self.analysis_seconds=None
            self.ocr_observation=None
    def ocr_context(self,max_age=15):
        """Review-only text: never expose OCR as verified model context yet."""
        with self.lock:
            if self.ocr_observation and time.monotonic()-self.ocr_observation[0]<=max_age:
                return self.ocr_observation
        return None
    def wait(self):
        for t in self.threads: t.join()
    def snapshot(self,max_age=10):
        with self.lock:
            if self.frame is None or time.monotonic()-self.frame[0]>max_age:
                raise RuntimeError('No recent screen frame. Restore the selected game and wait for new frames, then Send again.')
            return self.frame
    def recent_observation(self,max_age=10):
        with self.lock:
            if self.observation and time.monotonic()-self.observation[0]<=max_age:
                return self.observation[1]
        return None
    def observation_context(self,max_age=90,include_stamp=False):
        with self.lock:
            if self.observation:
                age=time.monotonic()-self.observation[0]
                if age<=max_age: return (self.observation[1],round(age,1),self.observation[0]) if include_stamp else (self.observation[1],round(age,1))
        return (None,None,None) if include_stamp else (None,None)
    def state(self):
        with self.lock:
            now=time.monotonic()
            return {'approved':not self.stop_event.is_set(),'frames_captured':self.count,
                    'frame_age_seconds':round(now-self.frame[0],1) if self.frame else None,
                    'observation_age_seconds':round(now-self.observation[0],1) if self.observation else None,
                    'analyzing':self.analyzing,'capture_error':self.error,'vision_error':self.vision_error}
    def backend_state(self):
        with self.lock:
            return {'background_backend':'ocr' if self.background_reader else 'vlm',
                    'analysis_seconds':self.analysis_seconds}
    def capture_loop(self):
        session=None; seen=None
        try:
            session=WindowCapture(self.target,max_width=self.max_width,fps=1/self.interval)
            session.start()
            while not self.stop_event.is_set():
                try:
                    frame=session.snapshot()
                    new_frame=frame[0]!=seen
                    with self.lock:
                        if frame[0]!=seen:
                            self.frame=frame; self.count+=1; seen=frame[0]
                        self.error=None
                    if new_frame and self.frame_callback: self.frame_callback(*frame)
                except Exception as exc:
                    with self.lock: self.frame=None; self.error=str(exc)
                self.stop_event.wait(.1)
        except Exception as exc:
            with self.lock: self.frame=None; self.error='Window capture failed: '+str(exc)
        finally:
            if session:
                try: session.stop(); session.wait()
                except Exception as exc:
                    with self.lock: self.error='Capture shutdown failed: '+str(exc)
    def observe_loop(self):
        seen=None; next_analysis=0; gate=ProgressGate(); generation=-1
        while not self.stop_event.wait(.1):
            with self.lock: current_generation=self.reader_generation; reader=self.background_reader
            if current_generation!=generation:
                generation=current_generation; gate=ProgressGate(); seen=None; next_analysis=0
            if self.question_pending.is_set(): continue
            if time.monotonic()<next_analysis: continue
            try: stamp,png=self.snapshot(max_age=2)
            except RuntimeError: continue
            if stamp==seen: continue
            with self.inference_lock:
                if self.stop_event.is_set() or self.question_pending.is_set(): continue
                with self.lock:
                    if generation!=self.reader_generation: continue
                # Refresh after waiting: never analyze a frame queued behind a chat request.
                try: stamp,png=self.snapshot(max_age=2)
                except RuntimeError: continue
                # The legacy VLM gate watches tracker/panel pixels; the OCR
                # experiment also reads center/minimap, so sample every 5s.
                if not reader and not gate.due(png,time.monotonic()): continue
                analysis_started=time.monotonic()
                try:
                    with self.lock: self.analyzing=True
                    if self.frame_callback: self.frame_callback(stamp,png)
                    observation=(reader.observe(png) if reader else self.assistant.observe(png,window_title=self.target.title if self.target else '',background=True))
                    with self.lock:
                        if self.stop_event.is_set() or generation!=self.reader_generation: continue
                        if reader: self.ocr_observation=(stamp,observation)
                        else: self.observation=(stamp,observation)
                        self.vision_error=None
                        self.analysis_seconds=round(time.monotonic()-analysis_started,3)
                    if self.review_callback:
                        self.review_callback('ocr_observation' if reader else 'observation',observation=observation,frame_age_seconds=time.monotonic()-stamp,analysis_seconds=round(time.monotonic()-analysis_started,3),frame_stamp=stamp)
                except Exception as exc:
                    with self.lock:
                        if self.stop_event.is_set() or generation!=self.reader_generation: continue
                        self.vision_error=str(exc)
                    if self.review_callback:
                        self.review_callback('ocr_error' if reader else 'vision_error',error_type=type(exc).__name__,analysis_seconds=round(time.monotonic()-analysis_started,3),frame_stamp=stamp)
                finally:
                    with self.lock: self.analyzing=False
                seen=stamp
                next_analysis=time.monotonic()+5
