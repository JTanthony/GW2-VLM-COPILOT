"""Compatibility import; production runtime is waypoint.ocr.qwen."""
import sys
from waypoint.ocr import qwen as _runtime
sys.modules[__name__]=_runtime
