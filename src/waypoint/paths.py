"""Source and packaged paths; packaged private state stays per Windows user."""
import os,sys
from pathlib import Path
def app_root():
    return Path(sys.executable).resolve().parent if getattr(sys,'frozen',False) else Path(__file__).resolve().parents[2]
def data_root():
    return Path(os.environ.get('LOCALAPPDATA',Path.home()/'AppData/Local'))/'GW2 VLM COPILOT' if getattr(sys,'frozen',False) else app_root()
