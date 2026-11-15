"""Compatibility import; production runtime is waypoint.ocr.nearby."""
import sys
from waypoint.ocr import nearby as _runtime
sys.modules[__name__]=_runtime
