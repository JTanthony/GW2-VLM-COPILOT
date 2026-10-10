"""Windows-user protected credentials; never plaintext or model context."""
import ctypes,hashlib,os
from ctypes import wintypes
from pathlib import Path

class Blob(ctypes.Structure):
    _fields_=[('size',wintypes.DWORD),('data',ctypes.POINTER(ctypes.c_ubyte))]

def protect(data,decrypt=False):
    if os.name!='nt': raise RuntimeError('Saved tokens require Windows protection.')
    buffer=ctypes.create_string_buffer(data); source=Blob(len(data),ctypes.cast(buffer,ctypes.POINTER(ctypes.c_ubyte))); target=Blob()
    crypt=ctypes.WinDLL('crypt32',use_last_error=True); kernel=ctypes.WinDLL('kernel32',use_last_error=True)
    function=crypt.CryptUnprotectData if decrypt else crypt.CryptProtectData
    function.argtypes=[ctypes.POINTER(Blob),ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,wintypes.DWORD,ctypes.POINTER(Blob)]
    function.restype=wintypes.BOOL
    kernel.LocalFree.argtypes=[ctypes.c_void_p]; kernel.LocalFree.restype=ctypes.c_void_p
    # UI_FORBIDDEN, current Windows user scope; never machine-wide protection.
    if not function(ctypes.byref(source),None,None,None,None,1,ctypes.byref(target)):
        raise RuntimeError('Windows could not protect or unlock the saved token.')
    try: return ctypes.string_at(target.data,target.size)
    finally: kernel.LocalFree(target.data)

class CredentialStore:
    def __init__(self,root=None):
        self.root=Path(root) if root is not None else Path(os.environ.get('LOCALAPPDATA',Path.home()/'AppData/Local'))/'Waypoint'/'credentials'
    def path(self,provider):
        return self.root/(hashlib.sha256(provider.encode('utf-8')).hexdigest()+'.dpapi')
    def has(self,provider): return self.path(provider).is_file()
    def save(self,provider,token):
        encrypted=protect(token.encode('utf-8'))
        self.root.mkdir(parents=True,exist_ok=True)
        path=self.path(provider); temp=path.with_suffix('.tmp')
        try: temp.write_bytes(encrypted); temp.replace(path)
        finally: temp.unlink(missing_ok=True)
    def load(self,provider):
        path=self.path(provider)
        if not path.exists(): return None
        if path.stat().st_size>16384: raise RuntimeError('Saved token is invalid. Forget it and enter a new one.')
        try: return protect(path.read_bytes(),decrypt=True).decode('utf-8')
        except Exception: raise RuntimeError('Saved token could not be unlocked. Forget it and enter a new one.') from None
    def forget(self,provider): self.path(provider).unlink(missing_ok=True)
