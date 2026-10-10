"""Own one local child engine; never stop another application's model server."""
import json,socket,subprocess,time
from pathlib import Path
from urllib.request import build_opener,ProxyHandler
from waypoint.inference.client import NoRedirect
class Engine:
    def __init__(self,config,root):
        self.config=config; self.root=Path(root); self.process=None; self.log=None
    def start(self):
        c=self.config
        exe=(self.root/c['executable']).resolve()
        paths=[exe,Path(c['model_path'])]
        if c.get('projector_path'): paths.append(Path(c['projector_path']))
        for path in paths:
            if not path.is_file(): raise FileNotFoundError(path)
        port=c['port']
        with socket.socket() as sock:
            if sock.connect_ex(('127.0.0.1',port))==0: raise RuntimeError('A local engine is already using the Waypoint port. Close other Waypoint windows with ×, then reopen one window. No existing engine was stopped.')
        logdir=self.root/'local-data'; logdir.mkdir(exist_ok=True)
        self.log=(logdir/('engine.log' if port==17865 else f'engine-{port}.log')).open('w',encoding='utf-8')
        args=[str(exe),'-m',c['model_path'],'--host','127.0.0.1','--port',str(port),'--alias',c.get('alias','waypoint-gemma'),'-c',str(c.get('context_length',4096)),'-ngl',str(c.get('gpu_layers', 'auto')),'--parallel','1','-b',str(c.get('batch_size',512)),'-ub',str(c.get('physical_batch_size',256)),'--reasoning','off','--no-webui']
        if c.get('projector_path'): args.extend(['--mmproj',c['projector_path']])
        if 'threads' in c: args.extend(['--threads',str(c['threads']),'--threads-batch',str(c['threads'])])
        if c.get('kv_offload') is False: args.append('--no-kv-offload')
        if c.get('device'): args.extend(['--device',c['device']])
        if 'flash_attention' in c: args.extend(['--flash-attn',c['flash_attention']])
        if 'cache_type_k' in c: args.extend(['--cache-type-k',c['cache_type_k']])
        if 'cache_type_v' in c: args.extend(['--cache-type-v',c['cache_type_v']])
        if 'gpu_margin_mb' in c: args.extend(['--fit-target',str(c['gpu_margin_mb'])])
        try:
            self.process=subprocess.Popen(args,cwd=exe.parent,stdout=self.log,stderr=subprocess.STDOUT,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
            opener=build_opener(ProxyHandler({}),NoRedirect()); deadline=time.monotonic()+120
            while time.monotonic()<deadline:
                if self.process.poll() is not None: raise RuntimeError('Engine exited; inspect local-data/engine.log.')
                try:
                    with opener.open(f'http://127.0.0.1:{port}/health',timeout=2) as r:
                        if json.load(r).get('status')=='ok': return
                except OSError: pass
                time.sleep(.25)
            raise TimeoutError('Engine loading timed out.')
        except BaseException:
            self.stop(); raise
    def stop(self):
        if self.process and self.process.poll() is None:
            self.process.terminate()
            try: self.process.wait(timeout=10)
            except subprocess.TimeoutExpired: self.process.kill(); self.process.wait(timeout=5)
        if self.log: self.log.close()
    def __enter__(self): self.start(); return self
    def __exit__(self,*args): self.stop()
