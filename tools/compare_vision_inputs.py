"""Compare full/cropped saved UI on an already-running loopback engine."""
import argparse,json,sys,time
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from waypoint.inference.client import Client
from waypoint.inference.validation import BACKGROUND_PROMPT,BACKGROUND_SCHEMA,validate_observation
from waypoint.testing.vision_inputs import crop_panel

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--frame',type=Path,required=True)
    parser.add_argument('--region',choices=('map','tracker','panel'),required=True)
    parser.add_argument('--base-url',default='http://127.0.0.1:17865/v1')
    parser.add_argument('--repeats',type=int,choices=range(1,4),default=2)
    args=parser.parse_args()
    full=args.frame.read_bytes()
    if len(full)>10_000_000: raise ValueError('Frame exceeds inference image limit.')
    crop=crop_panel(full,args.region)
    client=Client(args.base_url)
    focus={'map':'Read the map completion title and icon-labeled counters.',
           'tracker':'Read the current event and its own labeled counters; keep story and hearts separate.',
           'panel':'Read the open vendor/tooltip or achievement panel. Currency icons may be unknown; never guess gold.'}[args.region]
    records=[]
    for repeat in range(args.repeats):
        # Alternate order to expose warm-up/order effects instead of pretending
        # a single warm cropped request is a controlled speed comparison.
        candidates=[('full',full),('crop',crop)]
        if repeat%2: candidates.reverse()
        for label,image in candidates:
            started=time.monotonic()
            record={'repeat':repeat+1,'input':label,'image_bytes':len(image)}
            try:
                raw=client.complete(BACKGROUND_PROMPT+'\nTask: '+focus,image=image,schema=BACKGROUND_SCHEMA,max_tokens=384)
                record['observation']=validate_observation(raw)
            except Exception as exc: record['error_type']=type(exc).__name__
            record['seconds']=round(time.monotonic()-started,3);records.append(record)
            print(label,record['seconds'],'seconds',record.get('error_type','completed'),flush=True)
    directory=ROOT/'local-data/vision-benchmarks';directory.mkdir(parents=True,exist_ok=True)
    output=directory/(datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S-%f')+'.json')
    output.write_text(json.dumps({'source_frame':str(args.frame.resolve()),'region':args.region,
        'note':'Manual factual scoring required. Same-frame comparison; no account data, capture, or model training.',
        'records':records},indent=2),encoding='utf-8')
    print('Private comparison report:',output)

if __name__=='__main__':main()
