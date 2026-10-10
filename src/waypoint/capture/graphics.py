"""HWND-only Windows Graphics Capture. No desktop fallback or disk images."""
import threading,time
import cv2
from windows_capture import WindowsCapture
from .windows import validate_target

class WindowCapture:
    def __init__(self,target,max_width=1280,fps=2):
        self.target=target; self.max_width=max_width; self.interval=1/fps
        self.lock=threading.Lock(); self.frame=None; self.error=None
        self.closed=False; self.control=None; self.last_frame=0
        # Exact approved HWND; never a title substring or whole monitor.
        self.capture=WindowsCapture(window_hwnd=target.handle,monitor_index=None,
                                    cursor_capture=False,minimum_update_interval=round(1000/fps))
        self.capture.frame_handler=self.on_frame
        self.capture.closed_handler=self.on_closed
    def start(self):
        validate_target(self.target)
        self.control=self.capture.start_free_threaded()
    def on_frame(self,frame,control):
        try:
            validate_target(self.target)
            now=time.monotonic()
            if now-self.last_frame<self.interval: return
            pixels=frame.frame_buffer[:,:,:3]
            height,width=pixels.shape[:2]
            if width<1 or height<1: raise RuntimeError('Waiting for game frames.')
            if width>self.max_width:
                pixels=cv2.resize(pixels,(self.max_width,max(1,round(height*self.max_width/width))),interpolation=cv2.INTER_AREA)
            ok,encoded=cv2.imencode('.png',pixels)
            if not ok: raise RuntimeError('Could not encode the game frame.')
            validate_target(self.target)
            with self.lock:
                self.frame=(now,encoded.tobytes()); self.error=None; self.last_frame=now
        except Exception as exc:
            with self.lock: self.frame=None; self.error=str(exc)
    def on_closed(self):
        with self.lock: self.closed=True; self.frame=None
    def snapshot(self):
        try: validate_target(self.target)
        except RuntimeError:
            with self.lock: self.frame=None
            raise
        with self.lock:
            if self.closed: raise RuntimeError('The selected window closed. Select it again.')
            if self.error: raise RuntimeError(self.error)
            if not self.frame or time.monotonic()-self.frame[0]>3:
                raise RuntimeError('Waiting for new game frames. Restore the game if minimized.')
            return self.frame
    def stop(self):
        if self.control and not self.control.is_finished(): self.control.stop()
    def wait(self):
        if self.control: self.control.wait()
