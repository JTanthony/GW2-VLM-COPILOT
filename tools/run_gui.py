import sys
import ctypes
import hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from waypoint.ui.app import main

def launch():
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
            ctypes.windll.user32.MessageBoxW(None,'Waypoint is already open. Use the existing window.','Waypoint',0x40)
            return
    try:
        if sys.platform=='win32': ctypes.windll.user32.SetProcessDPIAware()
        main()
    finally:
        if handle: kernel.CloseHandle(handle)

if __name__=='__main__': launch()
