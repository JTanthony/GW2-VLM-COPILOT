"""Local-only Qwen adapter for the existing GW2 no-account conversation tester."""
import argparse,sys
from pathlib import Path
from waypoint.experiments.ocr_landmarks.qwen import profile,OCRAssistant,TextOnlyClient
from waypoint.assistant.web_lookup import check_wiki_available

ROOT=Path(__file__).resolve().parents[4]
REPORT_FOLDER='text-playtests-qwen'

def main(argv=None):
    args=list(sys.argv[1:] if argv is None else argv)
    parser=argparse.ArgumentParser(description=__doc__,add_help=False)
    if '--stop' in args:
        if args!=['--stop']:parser.error('--stop must be used alone.')
        folder=ROOT/'local-data'/REPORT_FOLDER;folder.mkdir(parents=True,exist_ok=True)
        (folder/'STOP').touch()
        print('Qwen text test stop requested. Active inference will finish before its owned engines close.')
        return 0
    if any(arg=='--account-mode' or arg.startswith('--account-mode=') for arg in args):
        parser.error('This local Qwen launcher is no-account only; it never opens saved account credentials.')
    # Reuse the original scenarios, public catalog, 1B question generation,
    # follow-up checks, wiki retrieval, stop handling and private debrief writer.
    sys.path.insert(0,str(ROOT))
    from tools.run_text_sessions import main as run_existing
    if '--help' in args or '-h' in args:
        return run_existing(args)
    try:config=profile(ROOT)
    except (OSError,ValueError) as error:
        parser.error('Qwen local setup is unavailable: '+str(error))
    print('Local Qwen text test: Gemma 3 1B asks; Qwen 3.5 4B answers. No account, capture or weight training.')
    return run_existing(['--account-mode','none',*args],copilot_profile=config,
        assistant_factory=OCRAssistant,client_factory=TextOnlyClient,
        report_folder=REPORT_FOLDER,copilot_label='Qwen 3.5 4B Q4_K_M (OCR text-only profile)',
        review_files_extra=('ocr/qwen.py',),conflict_ports=(17865,),source_preflight=check_wiki_available)

if __name__=='__main__':sys.exit(main())
