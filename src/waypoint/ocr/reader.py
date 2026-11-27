"""Tesseract CPU OCR through memory pipes, never temporary screenshots."""
import csv,io,os,subprocess,re,hashlib
from pathlib import Path
import cv2
import numpy as np

# Overlapping tiles cover the whole approved window, with exclusions applied
# BEFORE cropping/enlargement. Fractions target a standard game UI layout.
REGIONS={'upper left':(0,0,.52,.55),'upper right':(.48,0,1,.55),
         'lower left':(0,.50,.52,1),'lower right':(.48,.50,1,1)}
EXCLUSIONS={'chat':(0,.65,.27,1),'skill bar':(.29,.83,.71,1)}
LINE_LIMITS={'upper left':24,'upper right':32,'lower left':16,'lower right':24}

def mask_excluded(pixels):
    """Mask only the OCR copy; leave the original frame untouched."""
    masked=pixels.copy();h,w=masked.shape[:2]
    for left,top,right,bottom in EXCLUSIONS.values():
        masked[int(top*h):int(bottom*h),int(left*w):int(right*w)]=255
    return masked

def text_lines(tsv):
    """Filter whole lines, retaining uncertain words rather than deleting them."""
    if len(tsv)>1_000_000: raise ValueError('OCR output exceeded the limit.')
    lines={};geometry={}
    for index,row in enumerate(csv.DictReader(io.StringIO(tsv),delimiter='\t',quoting=csv.QUOTE_NONE)):
        if index>=10000: break
        if None in row or any(value is None for value in row.values()): continue
        try:
            confidence=float(row['conf'])
            if int(row['level'])!=5 or not 0<=confidence<=100: continue
            key=tuple(int(row[k]) for k in ('page_num','block_num','par_num','line_num'))
            word=' '.join(row['text'].split())
        except (KeyError,ValueError,TypeError): continue
        # Isolated punctuation/icons must not consume the useful line budget.
        if word and any(c.isalnum() for c in word):
            lines.setdefault(key,[]).append((word[:120],confidence))
            try:
                x,y,w,h=(int(row[name]) for name in ('left','top','width','height'))
                if w>0 and h>0:
                    previous=geometry.get(key,(x,y,x+w,y+h))
                    geometry[key]=(min(x,previous[0]),min(y,previous[1]),max(x+w,previous[2]),max(y+h,previous[3]))
            except (KeyError,ValueError,TypeError): pass
    # Sparse-text segmentation sometimes splits one heading into nearby blocks.
    # Join only adjacent, vertically aligned fragments using their pixel boxes.
    groups=[]
    for key,words in lines.items():
        box=geometry.get(key);joined=False
        if box:
            for group in groups:
                other=group[1]
                if not other: continue
                height=max(box[3]-box[1],other[3]-other[1])
                gap=max(box[0],other[0])-min(box[2],other[2])
                if abs(box[1]-other[1])<=height*.35 and 0<=gap<=height*2:
                    group[0]=group[0]+words if other[0]<box[0] else words+group[0]
                    group[1]=(min(box[0],other[0]),min(box[1],other[1]),max(box[2],other[2]),max(box[3],other[3]))
                    joined=True;break
        if not joined: groups.append([words,box])
    groups.sort(key=lambda group:(group[1][1],group[1][0]) if group[1] else (0,0))
    output=[];seen=set()
    for words,box in groups:
        text=' '.join(word for word,confidence in words).strip(' \"\u2018\u2019\u201c\u201d')[:120]
        weights=[max(1,sum(c.isalnum() for c in word)) for word,confidence in words]
        score=sum(confidence*weight for (_,confidence),weight in zip(words,weights))/sum(weights)
        # Preserve clocks, but reject scenery fragments and unlabelled numbers.
        meaningful=sum(c.isalpha() for c in text)>=3 or bool(re.fullmatch(r'\d{1,2}:\d{2}(?:\s*[AP]M)?',text,re.I))
        if not meaningful or score<65 or text.casefold() in seen: continue
        seen.add(text.casefold())
        uncertain=any(confidence<45 for word,confidence in words)
        output.append(('[uncertain] ' if uncertain else '')+text)
        if len(output)>=32: break
    return output

class OCRReader:
    def __init__(self,executable):
        path=Path(executable).expanduser().resolve()
        if path.name.casefold()!='tesseract.exe' or not path.is_file():
            raise ValueError('Select an installed tesseract.exe with English language data.')
        if not (path.parent/'tessdata/eng.traineddata').is_file():
            raise ValueError('English OCR data is missing from the tessdata folder beside tesseract.exe.')
        self.executable=str(path)
        self.region_cache={}

    def observe(self,png):
        pixels=cv2.imdecode(np.frombuffer(png,dtype=np.uint8),cv2.IMREAD_GRAYSCALE)
        if pixels is None: raise ValueError('Invalid OCR frame.')
        h,w=pixels.shape
        if w<32 or h<32 or w*h>16_000_000: raise ValueError('Unsupported OCR frame dimensions.')
        pixels=mask_excluded(pixels)
        visible=[];seen=set();reused=0
        cache=getattr(self,'region_cache',{})
        self.region_cache=cache
        for label,(left,top,right,bottom) in REGIONS.items():
            crop=pixels[int(top*h):max(1,int(bottom*h)),int(left*w):max(1,int(right*w))]
            signature=(crop.shape,hashlib.sha256(crop.tobytes()).digest())
            cached=cache.get(label)
            if cached and cached[0]==signature:
                lines=cached[1]
                reused+=1
            else:
                lines=self.read_region(crop)
                cache[label]=(signature,lines)
            for line in lines[:LINE_LIMITS[label]]:
                if line.casefold() in seen: continue
                seen.add(line.casefold());visible.append('OCR '+label+': '+line)
        return dict(map=None,event=None,objective=None,timer=None,player_status=None,
                    visible_text=visible,warnings=[],ocr_regions_processed=len(REGIONS)-reused,
                    ocr_regions_reused=reused,
                    summary='Experimental OCR across the window excluding chat and skill bar; meaning unconfirmed.',
                    confidence=0.0,needs_reasoning=False)

    def read_region(self,crop):
        # Enlarge small UI letters before segmentation. Bound the large
        # center crop separately so it cannot allocate an unbounded image.
        scale=min(2.0,(4_000_000/crop.size)**.5)
        if scale>1:
            crop=cv2.resize(crop,None,fx=scale,fy=scale,interpolation=cv2.INTER_CUBIC)
        ok,encoded=cv2.imencode('.png',crop)
        if not ok: raise ValueError('Could not prepare OCR pixels.')
        # Explicit executable and fixed arguments; no shell or screen text in commands.
        result=subprocess.run([self.executable,'stdin','stdout','--tessdata-dir',
            str(Path(self.executable).parent/'tessdata'),'-l','eng','--psm','11','tsv'],
            input=encoded.tobytes(),capture_output=True,timeout=4,check=False,
            env={**os.environ,'OMP_THREAD_LIMIT':'2'},
            creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
        if result.returncode: raise RuntimeError('OCR engine failed; check the local installation.')
        return text_lines(result.stdout.decode('utf-8',errors='replace'))
