"""Own CPU player + GPU copilot engines; text/account tests only."""
import argparse,json,socket,sys
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'src'))
from waypoint.inference.engine import Engine
from waypoint.inference.client import Client
from waypoint.assistant.local import Assistant
from waypoint.integrations.accounts import Accounts
from waypoint.integrations.credentials import CredentialStore
from waypoint.storage.resources import Resources
from waypoint.testing.text_sessions import PLAYER_GUIDANCE,run_sessions,title_scenarios,validate_question
from waypoint.testing.catalog import catalog_plans,mix_plans

def test_accounts(mode,game,out):
    if mode=='saved':
        accounts=Accounts(); accounts.select_game(game); accounts.connect('',game)
        return accounts
    accounts=Accounts(CredentialStore(Path(out)/'isolated-credentials'))
    accounts.select_game(game)
    if mode=='dummy':
        accounts.names={1:'Synthetic Trial',2:'Synthetic Explorer'}
        accounts.snapshot={'fetched_at':datetime.now(timezone.utc).isoformat(),'records':[{'id':1,'done':False,'current':10,'max':10},{'id':2,'done':True,'current':5,'max':5}]}
    return accounts

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--sessions',type=int,default=1000); parser.add_argument('--turns',type=int,default=4)
    parser.add_argument('--hours',type=float,default=8); parser.add_argument('--delay',type=float,default=1)
    parser.add_argument('--account-mode',choices=['none','dummy','saved'],default='dummy')
    parser.add_argument('--seed',type=int,default=None,help='Repeat a catalog sampling order using a saved seed')
    parser.add_argument('--game',default='Guild Wars 2'); args=parser.parse_args()
    if args.game!='Guild Wars 2': parser.error('Account/API testing uses Guild Wars 2 only. This batch is focused on GW2 wiki and account progress.')
    if not 1<=args.sessions<=10000 or not 1<=args.turns<=20 or not 0<args.hours<=8 or not 0<=args.delay<=60:
        parser.error('Use 1â€“10000 sessions, 1â€“20 turns, up to 8 hours and 0â€“60 seconds delay.')
    if not (ROOT/'config/player.local.json').is_file():
        from waypoint.ui.player_setup import configure_player
        if not configure_player(ROOT): return 0
    # Validate setup before reports, account access or engine startup.
    for name in ('player','inference'):
        path=ROOT/'config'/f'{name}.local.json'
        if not path.is_file():
            parser.error(f'Missing config/{name}.local.json. Copy config/{name}.example.json to that filename and set your server and model paths. See docs/DEVELOPMENT.md.')
        try:
            config=json.loads(path.read_text('utf-8'))
            for key in ('executable','model_path','port'):
                if key not in config: raise ValueError(f'missing {key}')
            for key in ('executable','model_path'):
                if not (ROOT/config[key]).is_file():
                    raise ValueError(f'{key} does not point to an existing file')
        except (OSError,ValueError,TypeError) as error:
            parser.error(f'Invalid config/{name}.local.json: {error}. See docs/DEVELOPMENT.md.')
    parent=ROOT/'local-data/text-playtests'
    if (parent/'STOP').exists():
        # A new explicit launch resumes only after both previous engines have closed.
        for config_file in ('player.local.json','inference.local.json'):
            port=json.loads((ROOT/'config'/config_file).read_text('utf-8'))['port']
            with socket.socket() as probe:
                probe.settimeout(1)
                if probe.connect_ex(('127.0.0.1',port))==0: parser.error('Previous engines are still active. Let the stop finish before starting another run.')
        (parent/'STOP').unlink()
    out=parent/datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S-%f'); out.mkdir(parents=True)
    accounts=test_accounts(args.account_mode,args.game,out)
    player_config=json.loads((ROOT/'config/player.local.json').read_text('utf-8'))
    copilot_config=json.loads((ROOT/'config/inference.local.json').read_text('utf-8')); copilot_config.pop('projector_path',None)
    from waypoint.version import VERSION
    import hashlib
    review_files=('assistant/research.py','assistant/web_lookup.py','assistant/local.py','inference/budget.py','testing/text_sessions.py')
    source_digest=hashlib.sha256(b''.join((ROOT/'src/waypoint'/name).read_bytes() for name in review_files)).hexdigest()
    (out/'run-info.json').write_text(json.dumps({'app_version':VERSION,'review_code_sha256':source_digest,'account_mode':args.account_mode,'game':accounts.selected_game,'snapshot_time':accounts.snapshot.get('fetched_at') if accounts.snapshot else None,'player_model':'Gemma 3 1B IT Q4_K_M','capture':False,'sessions_limit':args.sessions,'hours_limit':args.hours},indent=2),encoding='utf-8')
    titles=json.loads((ROOT/'src/waypoint/testing/test_titles.json').read_text('utf-8'))
    titles=[title for title in titles if title['game']=='Guild Wars 2']
    plans=title_scenarios(accounts,titles)
    catalog_path=ROOT/'local-data/test-catalog/gw2-public.json'
    if catalog_path.is_file():
        import secrets
        seed=args.seed if args.seed is not None else secrets.randbits(32)
        catalog=json.loads(catalog_path.read_text('utf-8'))
        sampled=[]; excluded=[]
        for plan in catalog_plans(catalog,seed):
            try: validate_question(plan['starter'])
            except ValueError:
                excluded.append({'scenario':plan['name'],'reason':'Existing question privacy/length guard'})
                continue
            sampled.append(plan)
        plans=mix_plans(plans,sampled)
        (out/'catalog-selection.json').write_text(json.dumps({'seed':seed,'catalog_fetched_at':catalog['fetched_at'],
            'coverage':catalog['coverage'],'excluded':excluded,'plans':plans[:args.sessions]},ensure_ascii=False,indent=2),encoding='utf-8')
        print(f'Public catalog enabled: {len(catalog["records"])} names; sampling seed {seed}',flush=True)
        if any(v.get('error') or v.get('missing_ids') for v in catalog['coverage'].values()):
            print('Catalog coverage is partial; see catalog-selection.json for missing IDs or failed categories.',flush=True)
    else:
        print('Public catalog missing; using fixed scenarios. Run tools/refresh_gw2_test_catalog.py to add public names.',flush=True)
    def make_assistant(session):
        game=plans[session%len(plans)]['game']
        resources=Resources(out/'resources'/str(session)); resources.select('my game is '+game)
        # Never carry the connected game's account snapshot into a different title.
        evidence=accounts if game.casefold()==accounts.selected_game.casefold() else Accounts(CredentialStore(out/'unused-credentials'))
        if evidence is not accounts: evidence.select_game(game)
        return Assistant(copilot,resources,evidence,allowed_sources=('Guild Wars 2',))
    print('Report directory: '+str(out),flush=True)
    try:
        with Engine(player_config,ROOT),Engine(copilot_config,ROOT):
            player=Client(f"http://127.0.0.1:{player_config['port']}/v1",model=player_config['alias'],system_guidance=PLAYER_GUIDANCE,temperature=.8,timeout=180)
            copilot=Client(f"http://127.0.0.1:{copilot_config['port']}/v1",timeout=180)
            summary=run_sessions(player,make_assistant,accounts,out,args.sessions,args.turns,args.hours,args.delay,plans=plans)
            return 1 if summary['errors'] else 0
    finally: accounts.disconnect()
if __name__=='__main__': sys.exit(main())
