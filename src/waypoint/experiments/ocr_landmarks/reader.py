"""Compatibility import; production runtime is waypoint.ocr.reader."""
import sys
from waypoint.ocr import reader as _runtime
sys.modules[__name__]=_runtime
