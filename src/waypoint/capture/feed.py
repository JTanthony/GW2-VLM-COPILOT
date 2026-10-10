"""Bounded in-memory capture feed. Capture rate is separate from inference rate."""
import threading,time
from .graphics import WindowCapture

class Feed:
    def __init__(self,target,assistant,inference_lock,question_pending,fps=2,max_width=1280):
        self.target=target; self.assistant=assistant; self.inference_lock=inference_lock
        self.question_pending=question_pending; self.interval=1/fps; self.max_width=max_width
        self.stop_event=threading.Event(); self.lock=threading.Lock()
        self.frame=None; self.observation=None; self.error=None; self.count=0
        self.vision_error=None; self.analyzing=False
        self.threads=[]
    def start(self):
        for fn in (self.capture_loop,self.observe_loop):
            t=threading.Thread(target=fn,daemon=True); self.threads.append(t); t.start()
    def stop(self): self.stop_event.set()
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
    def observation_context(self,max_age=90):
        with self.lock:
            if self.observation:
                age=time.monotonic()-self.observation[0]
                if age<=max_age: return self.observation[1],round(age,1)
        return None,None
    def state(self):
        with self.lock:
            now=time.monotonic()
            return {'approved':not self.stop_event.is_set(),'frames_captured':self.count,
                    'frame_age_seconds':round(now-self.frame[0],1) if self.frame else None,
                    'observation_age_seconds':round(now-self.observation[0],1) if self.observation else None,
                    'analyzing':self.analyzing,'capture_error':self.error,'vision_error':self.vision_error}
    def capture_loop(self):
        session=None; seen=None
        try:
            session=WindowCapture(self.target,max_width=self.max_width,fps=1/self.interval)
            session.start()
            while not self.stop_event.is_set():
                try:
                    frame=session.snapshot()
                    with self.lock:
                        if frame[0]!=seen:
                            self.frame=frame; self.count+=1; seen=frame[0]
                        self.error=None
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
        seen=None; next_analysis=0
        while not self.stop_event.wait(.1):
            if self.question_pending.is_set(): continue
            if time.monotonic()<next_analysis: continue
            try: stamp,png=self.snapshot(max_age=2)
            except RuntimeError: continue
            if stamp==seen: continue
            with self.inference_lock:
                if self.stop_event.is_set() or self.question_pending.is_set(): continue
                try:
                    with self.lock: self.analyzing=True
                    observation=self.assistant.observe(png,window_title=self.target.title if self.target else '')
                    with self.lock: self.observation=(stamp,observation); self.vision_error=None
                except Exception as exc:
                    with self.lock: self.vision_error=str(exc)
                finally:
                    with self.lock: self.analyzing=False
                seen=stamp
                next_analysis=time.monotonic()+3
