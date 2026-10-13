import sys,unittest
from pathlib import Path
import cv2
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from waypoint.capture.progress import ProgressGate

def png(image):
    return cv2.imencode('.png',image)[1].tobytes()

class ProgressTests(unittest.TestCase):
    def test_unchanged_skipped_but_periodically_refreshed(self):
        gate=ProgressGate(); image=png(np.zeros((200,400),dtype=np.uint8))
        self.assertTrue(gate.due(image,0))
        self.assertFalse(gate.due(image,10))
        self.assertTrue(gate.due(image,60))

    def test_tracker_change_triggers_but_combat_hud_does_not(self):
        gate=ProgressGate(); image=np.zeros((200,400),dtype=np.uint8)
        gate.due(png(image),0)
        image[180:,:]=255
        self.assertFalse(gate.due(png(image),5))
        image[:100,320:]=255
        self.assertTrue(gate.due(png(image),10))

    def test_invalid_image_keeps_existing_error_path(self):
        self.assertTrue(ProgressGate().due(b'bad image',0))
