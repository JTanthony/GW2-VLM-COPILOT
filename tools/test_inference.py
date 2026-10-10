"""Run a saved-image test and local answer; always shut down our child engine."""
import argparse,json,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'src'))
from waypoint.inference.engine import Engine
from waypoint.inference.client import Client
from waypoint.assistant.local import Assistant
p=argparse.ArgumentParser(); p.add_argument('--config',default=str(ROOT/'config/inference.local.json')); args=p.parse_args()
c=json.loads(Path(args.config).read_text('utf-8')); report={'valid':False}
try:
    start=time.monotonic()
    with Engine(c,ROOT):
        report['load_seconds']=round(time.monotonic()-start,3)
        assistant=Assistant(Client(f"http://127.0.0.1:{c['port']}/v1"))
        start=time.monotonic(); obs=assistant.observe(ROOT/'tests/fixtures/vision-known-text.png')
        report['observation_seconds']=round(time.monotonic()-start,3); report['observation']=obs; report['valid']=True
        expected={'map':'Queensdale','event':'Defend the bridge','objective':'Protect 3 supply crates','timer':'02:37','player_status':'Alive'}
        report['mismatches']={k:{'expected':v,'observed':obs[k]} for k,v in expected.items() if obs[k]!=v}
        report['test_code_found']=any('BLUE-482' in s for s in obs['visible_text'])
        report['accuracy_passed']=not report['mismatches'] and report['test_code_found']
        start=time.monotonic(); report['answer']=assistant.answer(obs,'What objective and timer are visible?'); report['answer_seconds']=round(time.monotonic()-start,3)
except Exception as exc:
    report['error']=str(exc)
finally:
    out=ROOT/'local-data'; out.mkdir(exist_ok=True); (out/'inference-test.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2)); sys.exit(0 if report.get('valid') and report.get('answer') else 1)
