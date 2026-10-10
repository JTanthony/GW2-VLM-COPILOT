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
from waypoint.testing.text_sessions import PLAYER_GUIDANCE,run_sessions,title_scenarios

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--sessions',type=int,default=1000); parser.add_argument('--turns',type=int,default=4)
    parser.add_argument('--hours',type=float,default=8); parser.add_argument('--delay',type=float,default=1)
    parser.add_argument('--account-mode',choices=['dummy','saved'],default='dummy')
    parser.add_argument('--game',default='Guild Wars 2'); args=parser.parse_args()
    if args.game!='Guild Wars 2': parser.error('Account/API testing uses Guild Wars 2 only. This batch is focused on GW2 wiki and account progress.')
    if not 1<=args.sessions<=10000 or not 1<=args.turns<=20 or not 0<args.hours<=8 or not 0<=args.delay<=60:
        parser.error('Use 1â€“10000 sessions, 1â€“20 turns, up to 8 hours and 0â€“60 seconds delay.')
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
    if args.account_mode=='saved':
        accounts=Accounts(); accounts.select_game(args.game)
        # Normal app credential use only: no token is printed, logged or passed to either model.
        accounts.connect('',args.game)
    else:
        accounts=Accounts(CredentialStore(out/'dummy-credentials')); accounts.select_game(args.game)
        if args.game!='Guild Wars 2': parser.error('Dummy progress fixture currently uses the GW2 adapter. Choose saved mode for another supported adapter.')
        accounts.names={1:'Synthetic Trial',2:'Synthetic Explorer'}
        accounts.snapshot={'fetched_at':datetime.now(timezone.utc).isoformat(),'records':[{'id':1,'done':False,'current':10,'max':10},{'id':2,'done':True,'current':5,'max':5}]}
    player_config=json.loads((ROOT/'config/player.local.json').read_text('utf-8'))
    copilot_config=json.loads((ROOT/'config/inference.local.json').read_text('utf-8')); copilot_config.pop('projector_path',None)
    (out/'run-info.json').write_text(json.dumps({'account_mode':args.account_mode,'game':accounts.selected_game,'snapshot_time':accounts.snapshot.get('fetched_at') if accounts.snapshot else None,'player_model':'Gemma 3 1B IT Q4_K_M','capture':False,'sessions_limit':args.sessions,'hours_limit':args.hours},indent=2),encoding='utf-8')
    titles=json.loads((ROOT/'src/waypoint/testing/test_titles.json').read_text('utf-8'))
    titles=[title for title in titles if title['game']=='Guild Wars 2']
    plans=title_scenarios(accounts,titles)
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
