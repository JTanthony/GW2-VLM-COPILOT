"""Opt-in source-development recording; excluded from Windows releases."""
import json,re,threading,time
from uuid import uuid4
from datetime import datetime,timezone,timedelta
from pathlib import Path

KEY = re.compile(r'(?i)\b[0-9a-f]{8}(?:-[0-9a-f]{4}){2}-[0-9a-f-]{20,}\b')
SECRET = re.compile(r'(?i)(bearer\s+|(?:api[_ -]?key|access[_ -]?token|password)\s*[:=]\s*)[^\s,;]+')

def clean(value):
    if isinstance(value,str):
        return SECRET.sub(lambda m:m.group(1)+'[redacted]',KEY.sub('[redacted]',value))
    if isinstance(value,dict):
        return {k:clean(v) for k,v in value.items()
                if not any(term in k.lower() for term in ('token','password','secret','credential','image','png','base64','snapshot'))}
    if isinstance(value,(tuple,list)): return [clean(v) for v in value]
    if value is None or isinstance(value,(int,float,bool)): return value
    return None

class VisionReview:
    def __init__(self,root):
        self.directory=Path(root)/'local-data/vision-review'
        self.path=None; self.enabled=False; self.lock=threading.Lock()
        self.frames={}; self.frame_bytes=0; self.started=0
    def set_enabled(self,enabled):
        with self.lock:
            if enabled:
                self.directory.mkdir(parents=True,exist_ok=True)
                self.path=self.directory/(datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S-%f')+'-'+uuid4().hex+'.jsonl')
                self.frames={}; self.frame_bytes=0; self.started=time.monotonic()
            self.enabled=enabled
    def save_frame(self,stamp,png):
        with self.lock:
            if not self.enabled: return None
            if stamp in self.frames: return self.frames[stamp]
            if time.monotonic()-self.started>3600 or self.frame_bytes+len(png)>5_000_000_000:
                self.enabled=False
                raise OSError('Development recording reached its one-hour or 5 GB limit.')
            folder=self.path.with_suffix(''); folder.mkdir(exist_ok=True)
            filename=f'frame-{len(self.frames)+1:06d}.png'
            (folder/filename).write_bytes(png)
            relative=folder.name+'/'+filename
            self.frames[stamp]=relative; self.frame_bytes+=len(png)
            captured=datetime.now(timezone.utc)-timedelta(seconds=max(0,time.monotonic()-stamp))
            with self.path.open('a',encoding='utf-8') as out:
                out.write(json.dumps({'kind':'frame','captured_at':captured.isoformat(),'frame_file':relative,'frame_stamp':stamp})+'\n')
            return relative
    def record(self,kind,*,question=None,answer=None,observation=None,frame_age_seconds=None,analysis_seconds=None,error_type=None,frame_stamp=None):
        with self.lock:
            if not self.enabled: return
            record=clean(dict(timestamp=datetime.now(timezone.utc).isoformat(),kind=kind,
                              question=question,answer=answer,observation=observation,
                              frame_age_seconds=frame_age_seconds,analysis_seconds=analysis_seconds,error_type=error_type,
                              frame_stamp=frame_stamp,frame_file=self.frames.get(frame_stamp)))
            if self.path.exists() and self.path.stat().st_size>20_000_000:
                self.enabled=False
                raise OSError('Review log reached 20 MB. Enable it again to start a new file.')
            with self.path.open('a',encoding='utf-8') as out:
                out.write(json.dumps(record,ensure_ascii=False)+'\n')
