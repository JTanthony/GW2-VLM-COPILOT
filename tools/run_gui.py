import sys
import ctypes
import hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from waypoint.ui.app import main
from waypoint.paths import data_root
from waypoint.branding import APP_NAME

def launch():
    if '--check-package' in sys.argv:
        check_package();return
    if '--smoke' not in sys.argv and ('--setup' in sys.argv or not (data_root()/'config/inference.local.json').exists()):
        from waypoint.ui.setup import configure
        if not configure():return
        if '--setup' in sys.argv:sys.argv.remove('--setup')
    handle=None
    if sys.platform=='win32' and '--smoke' not in sys.argv:
        # Windows releases the mutex if the owning GUI exits or crashes.
        kernel=ctypes.WinDLL('kernel32',use_last_error=True)
        kernel.CreateMutexW.argtypes=[ctypes.c_void_p,ctypes.c_bool,ctypes.c_wchar_p]
        kernel.CreateMutexW.restype=ctypes.c_void_p
        kernel.CloseHandle.argtypes=[ctypes.c_void_p]
        name='Local\\WaypointGUI_'+hashlib.sha256(str(ROOT.resolve()).lower().encode()).hexdigest()[:16]
        handle=kernel.CreateMutexW(None,False,name)
        if not handle: raise ctypes.WinError(ctypes.get_last_error())
        if ctypes.get_last_error()==183:
            kernel.CloseHandle(handle)
            ctypes.windll.user32.MessageBoxW(None,APP_NAME+' is already open. Use the existing window.',APP_NAME,0x40)
            return
    try:
        if sys.platform=='win32': ctypes.windll.user32.SetProcessDPIAware()
        main()
    finally:
        if handle: kernel.CloseHandle(handle)

def check_package():
    import json,tkinter as tk
    from waypoint.paths import app_root
    from waypoint.integrations.credentials import protect
    import numpy,cv2,windows_capture
    root=tk.Tk();root.withdraw()
    for name in ('branding/gw2-vlm-copilot-24.png','branding/gw2-vlm-copilot-32.png','ui/slider-thumb.png'):
        tk.PhotoImage(file=str(app_root()/'assets'/name))
    root.destroy()
    assert protect(protect(b'synthetic-package-check'),decrypt=True)==b'synthetic-package-check'
    target=data_root();target.mkdir(parents=True,exist_ok=True)
    (target/'package-check.json').write_text(json.dumps({'passed':True,'frozen':bool(getattr(sys,'frozen',False)),'python':sys.version,'numpy':numpy.__version__,'opencv':cv2.__version__}),encoding='utf-8')

if __name__=='__main__': launch()
