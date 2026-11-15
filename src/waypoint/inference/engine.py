"""Own one local child engine; never stop another application's model server."""
import json,socket,subprocess,time,sys,ctypes
from pathlib import Path
from waypoint.inference.client import local_http_opener

class EnginePortBusyError(RuntimeError):
    def __init__(self,port):
        self.port=port
        super().__init__(f'Local model port {port} is already in use. Let the existing app or text test finish, or stop it with its own Stop control. No existing engine was reused or stopped.')

class Engine:
    def __init__(self,config,root,*,runtime_dir=None):
        self.config=config; self.root=Path(root); self.process=None; self.log=None
        self.runtime_dir = Path(runtime_dir) if runtime_dir is not None else None
    def start(self):
        c=self.config
        saved_executable = c.get('executable')
        exe = (self.root/saved_executable).resolve() if saved_executable else None
        if (exe is None or not exe.is_file()) and self.runtime_dir is not None:
            bundled_location = self.runtime_dir/'llama-server.exe'
            if bundled_location.is_file():
                exe = bundled_location.resolve()
        if exe is None or not exe.is_file():
            guidance = (
                'Place llama-server.exe and its DLLs in the app runtime folder and click Start engine again. '
                'To use a different folder, reopen the app with --setup and select the server.'
                if getattr(sys, 'frozen', False) else
                'Check the executable path in config/inference.local.json.'
            )
            location = f' at {exe}' if exe is not None else ''
            raise FileNotFoundError(f'Could not find the llama.cpp server{location}. {guidance}')
        paths=[Path(c['model_path'])]
        if c.get('projector_path'): paths.append(Path(c['projector_path']))
        for path in paths:
            if not path.is_file(): raise FileNotFoundError(path)
        port=c['port']
        with socket.socket() as sock:
            if sock.connect_ex(('127.0.0.1',port))==0: raise EnginePortBusyError(port)
        logdir=self.root/'local-data'; logdir.mkdir(exist_ok=True)
        log_path = logdir/('engine.log' if port==17865 else f'engine-{port}.log')
        self.log = log_path.open('w',encoding='utf-8')
        args=[str(exe),'-m',c['model_path'],'--host','127.0.0.1','--port',str(port),'--alias',c.get('alias','waypoint-gemma'),'-c',str(c.get('context_length',4096)),'-ngl',str(c.get('gpu_layers', 'auto')),'--parallel','1','-b',str(c.get('batch_size',512)),'-ub',str(c.get('physical_batch_size',256)),'--reasoning','off','--no-webui']
        if c.get('projector_path'): args.extend(['--mmproj',c['projector_path']])
        if 'threads' in c: args.extend(['--threads',str(c['threads']),'--threads-batch',str(c['threads'])])
        if c.get('kv_offload') is False: args.append('--no-kv-offload')
        if c.get('device'): args.extend(['--device',c['device']])
        if 'flash_attention' in c: args.extend(['--flash-attn',c['flash_attention']])
        if 'cache_type_k' in c: args.extend(['--cache-type-k',c['cache_type_k']])
        if 'cache_type_v' in c: args.extend(['--cache-type-v',c['cache_type_v']])
        if 'gpu_margin_mb' in c: args.extend(['--fit-target',str(c['gpu_margin_mb'])])
        launch_stage = 'prepare the Windows DLL search path'
        try:
            # Resolve the API explicitly, as the Windows GUI launcher does.
            set_dll_directory = None
            if getattr(sys, 'frozen', False) and sys.platform == 'win32':
                kernel = ctypes.WinDLL('kernel32', use_last_error=True)
                set_dll_directory = kernel.SetDllDirectoryW
                set_dll_directory.argtypes = [ctypes.c_wchar_p]
                set_dll_directory.restype = ctypes.c_int
                if not set_dll_directory(None):
                    raise ctypes.WinError(ctypes.get_last_error())
            try:
                launch_stage = 'start the server process'
                self.process = subprocess.Popen(
                    args, executable=str(exe), cwd=exe.parent, stdin=subprocess.DEVNULL,
                    stdout=self.log, stderr=subprocess.STDOUT,
                    creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0),
                )
            finally:
                if set_dll_directory is not None:
                    set_dll_directory(sys._MEIPASS)
        except OSError as error:
            self.log.write(f'Could not {launch_stage} for {exe}: {error!r}\n')
            self.stop()
            raise RuntimeError(f'Windows could not start {exe.name}: unable to {launch_stage}. Details: {log_path}') from error
        except BaseException:
            self.stop()
            raise
        try:
            opener=local_http_opener(); deadline=time.monotonic()+120
            while time.monotonic()<deadline:
                if self.process.poll() is not None: raise RuntimeError(f'Engine exited. Details: {log_path}')
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
