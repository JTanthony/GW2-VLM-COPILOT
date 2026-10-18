"""Developer-only crop candidates for already-recorded frames; no disk writes."""
import cv2
import numpy as np

REGIONS={'map':(0,0,.30,.23),'tracker':(.76,0,1,.62),'panel':(.25,.13,.82,.85)}

def crop_panel(png,region):
    if region not in REGIONS: raise ValueError('Choose map, tracker or panel.')
    pixels=cv2.imdecode(np.frombuffer(png,dtype=np.uint8),cv2.IMREAD_COLOR)
    if pixels is None: raise ValueError('Invalid recorded image.')
    height,width=pixels.shape[:2]
    if width<100 or height<100: raise ValueError('Frame too small for region comparison.')
    left,top,right,bottom=REGIONS[region]
    crop=pixels[int(height*top):int(height*bottom),int(width*left):int(width*right)]
    ok,encoded=cv2.imencode('.png',crop)
    if not ok: raise ValueError('Could not encode crop.')
    return encoded.tobytes()
