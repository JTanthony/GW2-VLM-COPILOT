"""Local file selection for the simulated player; no inference or downloads."""
import json
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox
from waypoint.branding import APP_NAME

def save_player_config(project, executable, model):
    executable, model = Path(executable), Path(model)
    if not executable.is_file() or executable.name.lower() != 'llama-server.exe':
        raise ValueError('Choose an existing llama-server.exe, with its downloaded DLLs alongside it.')
    if not model.is_file() or model.suffix.lower() != '.gguf':
        raise ValueError('Choose the downloaded Gemma 3 1B GGUF model.')
    config = dict(executable=str(executable.resolve()), model_path=str(model.resolve()),
                  port=17866, alias='waypoint-test-player', gpu_layers=0, device='none',
                  kv_offload=False, context_length=2048, threads=2,
                  batch_size=256, physical_batch_size=128)
    directory = Path(project)/'config'
    directory.mkdir(parents=True, exist_ok=True)
    (directory/'player.local.json').write_text(json.dumps(config, indent=2), encoding='utf-8')

def configure_player(project, smoke=False):
    root = tk.Tk()
    root.title(APP_NAME + ' - Tester setup')
    root.geometry('640x340')
    icon = tk.PhotoImage(file=str(Path(project)/'assets/branding/gw2-vlm-copilot-32.png'))
    root.iconphoto(True, icon)
    tk.Label(root, text='Set up the simulated player', font=('Segoe UI',14,'bold')).pack(pady=12)
    tk.Label(root, text='Select your downloaded llama.cpp server and Gemma 3 1B IT Q4_K_M model. '
             'The 1B model generates test questions; the app\'s configured model answers. '
             'No vision projector is needed here. This setup does not download files or train model weights.',
             wraplength=600, justify='left').pack(padx=16)
    fields = {}
    for key, label, pattern in [('executable','llama.cpp server: llama-server.exe','*.exe'),
                                ('model','Player model: gemma-3-1b-it-Q4_K_M.gguf','*.gguf')]:
        row = tk.Frame(root); row.pack(fill='x', padx=16, pady=8)
        tk.Label(row,text=label).pack(anchor='w')
        value = tk.StringVar(); fields[key] = value
        tk.Entry(row,textvariable=value).pack(side='left',fill='x',expand=True)
        def pick(v=value,p=pattern):
            selected = filedialog.askopenfilename(parent=root,filetypes=[('Local file',p)])
            if selected: v.set(selected)
        tk.Button(row,text='Browse',command=pick).pack(side='right')
    saved = False
    def save():
        nonlocal saved
        try:
            save_player_config(project, fields['executable'].get().strip(), fields['model'].get().strip())
        except (ValueError,OSError) as error:
            messagebox.showerror('Tester setup',str(error),parent=root); return
        saved = True; root.destroy()
    tk.Button(root,text='Save and start tests',command=save).pack(pady=12)
    if smoke: root.after(150,root.destroy)
    root.mainloop()
    return saved
