"""In-memory change gate; no OCR, screen writes, or notification permission."""
import cv2
import numpy as np

class ProgressGate:
    def __init__(self, refresh_seconds=60):
        self.previous=None
        self.last_analysis=None
        self.refresh_seconds=refresh_seconds

    def due(self, png, now):
        pixels=cv2.imdecode(np.frombuffer(png,dtype=np.uint8),cv2.IMREAD_GRAYSCALE)
        if pixels is None:
            return True  # Let the existing inference path report invalid input.
        h,w=pixels.shape
        # Standard GW2 tracker and achievement-panel areas. Full model input is
        # retained: custom layouts still receive a periodic refresh.
        regions=(pixels[:max(1,int(h*.55)),int(w*.78):],
                 pixels[int(h*.18):max(1,int(h*.73)),:max(1,int(w*.44))])
        signature=np.concatenate([cv2.resize(region,(64,64)).flatten() for region in regions])
        changed=self.previous is None or np.mean(np.abs(signature.astype(float)-self.previous.astype(float)))>=8
        refresh=self.last_analysis is None or now-self.last_analysis>=self.refresh_seconds
        if changed or refresh:
            self.previous=signature
            self.last_analysis=now
            return True
        return False
