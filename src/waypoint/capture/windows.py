"""Explicitly selected, window identity checks. No game inputs."""
import ctypes,struct,zlib
from ctypes import wintypes as W
from dataclasses import dataclass
u=ctypes.WinDLL('user32',use_last_error=True); g=ctypes.WinDLL('gdi32',use_last_error=True)
for dll,name,args,result in [
(u,'GetForegroundWindow',[],W.HWND),(u,'GetDC',[W.HWND],W.HDC),(u,'ReleaseDC',[W.HWND,W.HDC],ctypes.c_int),
(u,'IsWindow',[W.HWND],W.BOOL),(u,'IsWindowVisible',[W.HWND],W.BOOL),(u,'IsIconic',[W.HWND],W.BOOL),
(u,'GetClientRect',[W.HWND,ctypes.POINTER(W.RECT)],W.BOOL),(u,'ClientToScreen',[W.HWND,ctypes.POINTER(W.POINT)],W.BOOL),
(u,'GetWindowThreadProcessId',[W.HWND,ctypes.POINTER(W.DWORD)],W.DWORD),
(u,'GetWindowTextLengthW',[W.HWND],ctypes.c_int),(u,'GetWindowTextW',[W.HWND,W.LPWSTR,ctypes.c_int],ctypes.c_int),
(g,'CreateCompatibleDC',[W.HDC],W.HDC),(g,'CreateCompatibleBitmap',[W.HDC,ctypes.c_int,ctypes.c_int],W.HBITMAP),
(g,'SelectObject',[W.HDC,W.HANDLE],W.HANDLE),(g,'DeleteObject',[W.HANDLE],W.BOOL),(g,'DeleteDC',[W.HDC],W.BOOL),
(g,'StretchBlt',[W.HDC,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_int,W.HDC,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_int,W.DWORD],W.BOOL),
(g,'GetDIBits',[W.HDC,W.HBITMAP,W.UINT,W.UINT,ctypes.c_void_p,ctypes.c_void_p,W.UINT],ctypes.c_int)]:
    f=getattr(dll,name); f.argtypes=args; f.restype=result
@dataclass(frozen=True)
class Window:
    handle:int
    pid:int
    title:str

def process_id(handle):
    pid=W.DWORD(); u.GetWindowThreadProcessId(handle,ctypes.byref(pid)); return pid.value

def list_windows():
    result=[]; callback=ctypes.WINFUNCTYPE(W.BOOL,W.HWND,W.LPARAM)
    def visit(hwnd,param):
        if u.IsWindowVisible(hwnd) and not u.IsIconic(hwnd):
            n=u.GetWindowTextLengthW(hwnd)
            if n:
                title=ctypes.create_unicode_buffer(n+1); u.GetWindowTextW(hwnd,title,n+1)
                if title.value!='Waypoint': result.append(Window(hwnd,process_id(hwnd),title.value))
        return True
    cb=callback(visit); u.EnumWindows.argtypes=[callback,W.LPARAM]; u.EnumWindows(cb,0)
    return result

def validate_target(window):
    if not u.IsWindow(window.handle) or process_id(window.handle)!=window.pid: raise RuntimeError('The selected window closed. Select it again.')
    if u.IsIconic(window.handle) or not u.IsWindowVisible(window.handle): raise RuntimeError('Capture paused: restore the selected game window to resume.')

