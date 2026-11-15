"""Explicit local setup for Gemma vision or Qwen OCR; no downloads or capture."""
import json
from pathlib import Path
import tkinter as tk
from tkinter import filedialog,messagebox
from waypoint.paths import app_root,data_root
from waypoint.branding import APP_NAME
from waypoint.storage import preferences


def setup_values(values,family):
    values={key:str(value).strip() for key,value in values.items()}
    if family not in ('gemma','qwen'):raise ValueError('Choose Gemma or Qwen.')
    if not all(Path(values.get(key,'')).is_file() for key in ('executable','model_path')):
        raise ValueError('Choose an existing llama-server.exe and model GGUF.')
    config={key:values[key] for key in ('executable','model_path')}
    config.update(model_family=family,port=17865,gpu_layers='auto',context_length=4096,batch_size=512,physical_batch_size=256)
    saved={'selected_model':family,family+'_model_path':values['model_path']}
    if family=='gemma':
        projector=values.get('projector_path','')
        if projector and not Path(projector).is_file():raise ValueError('Choose an existing vision companion or leave it blank for chat only.')
        if projector:config['projector_path']=projector
        saved['gemma_projector_path']=projector
    else:
        folder=Path(values.get('ocr_folder',''))
        if not (folder/'tesseract.exe').is_file() or not (folder/'tessdata/eng.traineddata').is_file():
            raise ValueError('Choose the installed Tesseract folder containing tesseract.exe and tessdata/eng.traineddata.')
        saved['ocr_executable']=str(folder/'tesseract.exe')
    return config,saved


def configure():
    root=tk.Tk();root.title(APP_NAME+' - Setup');root.geometry('660x570')
    root.minsize(640,570)
    brand_icon=tk.PhotoImage(file=str(app_root()/'assets/branding/gw2-vlm-copilot-32.png'))
    root.iconphoto(True,brand_icon)
    icon_path=str(app_root()/'assets/branding/gw2-vlm-copilot.ico')
    root.iconbitmap(default=icon_path);root.after_idle(lambda:root.iconbitmap(icon_path))
    tk.Label(root,text='Set up your local copilot',font=('Segoe UI',14,'bold')).pack(pady=12)
    tk.Label(root,text='Choose your local server and model. Qwen uses Tesseract to read screen text; Gemma uses its matching vision companion. Files stay on your computer. Setup does not download or run them.',wraplength=620,justify='left').pack(padx=16)
    family=tk.StringVar(value='gemma')
    choices=tk.Frame(root);choices.pack(fill='x',padx=16,pady=8)
    for text,value in [('4B Qwen (OCR)', 'qwen'),('12B Gemma QAT (vision)','gemma')]:
        tk.Radiobutton(choices,text=text,value=value,variable=family).pack(side='left')
    fields={};labels={};entries={};buttons={}
    for name,label,pattern in [('executable','llama.cpp server: llama-server.exe','*.exe'),('model_path','Model GGUF','*.gguf'),('projector_path','Gemma vision companion (optional for chat)','*.gguf'),('ocr_folder','Tesseract OCR installation folder',None)]:
        row=tk.Frame(root);row.pack(fill='x',padx=16,pady=7)
        labels[name]=tk.Label(row,text=label);labels[name].pack(anchor='w')
        value=tk.StringVar();fields[name]=value
        entries[name]=tk.Entry(row,textvariable=value);entries[name].pack(side='left',fill='x',expand=True)
        def pick(v=value,p=pattern):
            selected=filedialog.askdirectory(parent=root,title='Choose installed Tesseract OCR folder') if p is None else filedialog.askopenfilename(parent=root,initialdir=str(app_root()/'Models') if (app_root()/'Models').is_dir() else str(app_root()),filetypes=[('Model or executable',p)])
            if selected:v.set(selected)
        buttons[name]=tk.Button(row,text='Browse',command=pick);buttons[name].pack(side='right')
    def refresh(*_):
        qwen=family.get()=='qwen'
        labels['model_path'].configure(text='Qwen 3.5 4B Q4_K_M GGUF' if qwen else 'Gemma 4 12B QAT Q4_0 GGUF')
        for name,enabled in [('projector_path',not qwen),('ocr_folder',qwen)]:
            entries[name].configure(state='normal' if enabled else 'disabled');buttons[name].configure(state='normal' if enabled else 'disabled')
    family.trace_add('write',refresh);refresh()
    saved=False
    def save():
        nonlocal saved
        try:config,settings=setup_values({k:v.get() for k,v in fields.items()},family.get())
        except ValueError as error:
            messagebox.showerror('Missing files',str(error),parent=root);return
        directory=data_root()/'config';directory.mkdir(parents=True,exist_ok=True)
        (directory/'inference.local.json').write_text(json.dumps(config,indent=2),encoding='utf-8')
        previous=preferences.load(data_root());previous.update(settings);preferences.save(data_root(),previous)
        saved=True;root.destroy()
    tk.Label(root,text='Qwen needs Tesseract with English data. Gemma needs its matching companion for images. You can switch models later in Settings.',wraplength=620,justify='left').pack(padx=16,pady=8)
    tk.Button(root,text='Save and open app',command=save).pack(pady=10)
    root.mainloop();return saved
