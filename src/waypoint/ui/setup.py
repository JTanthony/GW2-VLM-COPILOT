"""Explicit local file selection; no model download, inference or capture."""
import json
import tkinter as tk
from tkinter import filedialog,messagebox
from waypoint.paths import app_root,data_root
from waypoint.branding import APP_NAME

def configure():
    root=tk.Tk();root.title(APP_NAME+' - Setup');root.geometry('640x430')
    brand_icon=tk.PhotoImage(file=str(app_root()/'assets/branding/gw2-vlm-copilot-32.png'))
    root.iconphoto(True,brand_icon)
    icon_path=str(app_root()/'assets/branding/gw2-vlm-copilot.ico')
    root.iconbitmap(default=icon_path)
    root.after_idle(lambda:root.iconbitmap(icon_path))
    tk.Label(root,text='Set up your local copilot',font=('Segoe UI',14,'bold')).pack(pady=12)
    tk.Label(root,text='Recommended: Gemma 4 12B QAT Q4_0 for chat and vision. The projector lets this model read images; it is NOT the Gemma 3 1B development test model. Other compatible GGUF models may be selected. Setup does not download or run files.',wraplength=600,justify='left').pack(padx=16)
    fields={}
    for name,label,pattern in [('executable','llama.cpp server: llama-server.exe','*.exe'),('model_path','Gemma 4 12B QAT Q4_0: gemma-4-12B-it-QAT-Q4_0.gguf','*.gguf'),('projector_path','12B vision companion: mmproj-gemma-4-12B-it-QAT-BF16.gguf','*.gguf')]:
        row=tk.Frame(root);row.pack(fill='x',padx=16,pady=8)
        tk.Label(row,text=label).pack(anchor='w')
        value=tk.StringVar();fields[name]=value
        tk.Entry(row,textvariable=value).pack(side='left',fill='x',expand=True)
        def pick(v=value,p=pattern):
            selected=filedialog.askopenfilename(parent=root,filetypes=[('Model or executable',p)])
            if selected:v.set(selected)
        tk.Button(row,text='Browse',command=pick).pack(side='right')
    saved=False
    def save():
        nonlocal saved
        values={k:v.get().strip() for k,v in fields.items()}
        from pathlib import Path
        if not all(Path(values[k]).is_file() for k in ('executable','model_path')):
            messagebox.showerror('Missing files','Choose an existing server and model.',parent=root);return
        if values['projector_path'] and not Path(values['projector_path']).is_file():
            messagebox.showerror('Missing projector','Choose an existing projector or leave it blank for text-only use.',parent=root);return
        if not values['projector_path']:values.pop('projector_path')
        values.update(port=17865,gpu_layers='auto',context_length=4096,batch_size=512,physical_batch_size=256)
        directory=data_root()/'config';directory.mkdir(parents=True,exist_ok=True)
        (directory/'inference.local.json').write_text(json.dumps(values,indent=2),encoding='utf-8')
        saved=True;root.destroy()
    tk.Label(root,text='The projector is required for vision. Leave it blank only for text-only chat.',wraplength=600).pack(pady=4)
    tk.Button(root,text='Save and open app',command=save).pack(pady=12)
    root.mainloop();return saved
