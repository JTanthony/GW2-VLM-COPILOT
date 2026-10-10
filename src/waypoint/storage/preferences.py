import json
from pathlib import Path
def load(root):
    try:
        data=json.loads((Path(root)/'local-data/ui-settings.json').read_text('utf-8'))
        if not isinstance(data,dict): data={}
        reset=Path(root)/'local-data/chat-font-reset.json'
        if reset.exists():
            data['font_size']=10
            reset.unlink()
        return data
    except (OSError,ValueError): return {}
def save(root,data):
    directory=Path(root)/'local-data'; directory.mkdir(exist_ok=True)
    temp=directory/'ui-settings.tmp'; temp.write_text(json.dumps(data),encoding='utf-8'); temp.replace(directory/'ui-settings.json')

def save_status(root,data):
    directory=Path(root)/'local-data'; directory.mkdir(exist_ok=True)
    temp=directory/'vision-status.tmp'; temp.write_text(json.dumps(data),encoding='utf-8'); temp.replace(directory/'vision-status.json')
