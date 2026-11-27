"""First-run resource downloads and existing-file setup for Gemma or Qwen."""
import json
import queue
import threading
import time
import webbrowser
from pathlib import Path
import tkinter as tk
from tkinter import filedialog,messagebox,ttk
from waypoint.paths import app_root,data_root
from waypoint.branding import APP_NAME
from waypoint.storage import preferences
from waypoint.storage.downloads import RESOURCES, DownloadCancelled, install_resource

LLAMA_RELEASE_URL = 'https://github.com/ggml-org/llama.cpp/releases/tag/b12387'
LLAMA_DOWNLOAD_LABEL = 'Download llama.cpp Windows x64 (CUDA 12) and CUDA 12.4 DLLs'
LLAMA_FOLDER_HELP = (
    'Choose Windows x64 (CUDA 12.4) and the matching CUDA 12.4 DLLs. '
    'Extract both ZIPs and place all files in \\GW2-VLM-COPILOT\\runtime. '
)


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
    root=tk.Tk();root.title(APP_NAME+' - Setup');root.geometry('760x760')
    root.minsize(720,760)
    brand_icon=tk.PhotoImage(file=str(app_root()/'assets/branding/gw2-vlm-copilot-32.png'))
    root.iconphoto(True,brand_icon)
    icon_path=str(app_root()/'assets/branding/gw2-vlm-copilot.ico')
    root.iconbitmap(default=icon_path);root.after_idle(lambda:root.iconbitmap(icon_path))
    style=ttk.Style(root)
    style.theme_use('clam')
    style.configure('Download.Horizontal.TProgressbar',background='#39bbaa',troughcolor='#e0e5e8')
    tk.Label(root,text='Set up your local copilot',font=('Segoe UI',16,'bold')).pack(anchor='w',padx=20,pady=(18,6))
    tk.Label(root,text='Choose your AI, then download the resources you need or select existing files.',
             font=('Segoe UI',10),wraplength=690,justify='left').pack(anchor='w',padx=20)
    resource_root=data_root()
    existing=preferences.load(resource_root)
    try:
        configuration=json.loads((resource_root/'config/inference.local.json').read_text('utf-8'))
    except (OSError,ValueError):
        configuration={}
    model_paths={key:existing.get(key+'_model_path','') for key in ('gemma','qwen')}
    configured_family=configuration.get('model_family','gemma')
    if configured_family in model_paths and not model_paths[configured_family]:
        model_paths[configured_family]=configuration.get('model_path','')
    for resource in RESOURCES:
        if resource.key in model_paths and not Path(model_paths[resource.key]).is_file():
            candidate=resource_root/resource.folder/resource.filename
            if candidate.is_file():model_paths[resource.key]=str(candidate)
    selected=existing.get('selected_model',configured_family)
    family=tk.StringVar(value=selected if selected in model_paths else 'gemma')
    choices=tk.Frame(root);choices.pack(fill='x',padx=20,pady=12)
    controls=[]
    for text,value in [('4B Qwen (OCR)', 'qwen'),('12B Gemma QAT (vision)','gemma')]:
        control=tk.Radiobutton(choices,text=text,value=value,variable=family)
        control.pack(side='left',padx=(0,16));controls.append(control)
    notebook=ttk.Notebook(root)
    notebook.pack(fill='both',expand=True,padx=20,pady=(0,8))
    downloads=tk.Frame(notebook)
    locations=tk.Frame(notebook)
    notebook.add(downloads,text='Downloads')
    notebook.add(locations,text='File locations')
    checks={};bars={};statuses={}
    tk.Label(downloads,text='Server and CUDA downloads are for NVIDIA GPUs. Select each resource to include.',
             wraplength=660,justify='left',fg='#4d5961').pack(anchor='w',padx=12,pady=(12,6))
    for resource in RESOURCES:
        row=tk.Frame(downloads);row.pack(fill='x',padx=12,pady=3)
        selected=resource.key in ('server','cuda',family.get()) or (resource.key=='projector' and family.get()=='gemma')
        checks[resource.key]=tk.BooleanVar(value=selected)
        control=tk.Checkbutton(row,text=resource.label,variable=checks[resource.key],anchor='w',font=('Segoe UI',10))
        control.grid(row=0,column=0,sticky='w');controls.append(control)
        tk.Button(row,text='Source',command=lambda url=resource.source:webbrowser.open(url),
                  relief='flat',fg='#137c73',cursor='hand2').grid(row=0,column=1,sticky='e')
        bars[resource.key]=ttk.Progressbar(row,maximum=100,style='Download.Horizontal.TProgressbar')
        bars[resource.key].grid(row=1,column=0,columnspan=2,sticky='ew',pady=(2,0))
        statuses[resource.key]=tk.StringVar(value=f'{resource.size/1_000_000_000:.2f} GB download')
        tk.Label(row,textvariable=statuses[resource.key],fg='#4d5961',anchor='w',font=('Segoe UI',9)).grid(row=2,column=0,columnspan=2,sticky='w')
        row.columnconfigure(0,weight=1)
    tk.Label(downloads,text='ZIPs are extracted automatically. Model files are placed in Models.\n'
             'Resources are checked against their published SHA-256 checksums.',
             wraplength=660,justify='left',fg='#4d5961').pack(anchor='w',padx=12,pady=(8,3))
    tk.Label(downloads,text='Download location  '+str(resource_root),wraplength=660,justify='left',
             fg='#4d5961',font=('Segoe UI',9)).pack(anchor='w',padx=12)
    fields={};labels={};entries={};buttons={}
    server=resource_root/'runtime/llama-b12387/llama-server.exe'
    if not server.is_file():server=app_root()/'runtime/llama-server.exe'
    defaults={'executable':configuration.get('executable',str(server) if server.is_file() else ''),
              'model_path':model_paths[family.get()],
              'projector_path':existing.get('gemma_projector_path',configuration.get('projector_path','')),
              'ocr_folder':str(Path(existing['ocr_executable']).parent) if existing.get('ocr_executable') else ''}
    if not Path(defaults['executable']).is_file() and server.is_file():
        defaults['executable']=str(server)
    if not Path(defaults['projector_path']).is_file():
        projector=resource_root/'Models'/RESOURCES[-1].filename
        if projector.is_file():defaults['projector_path']=str(projector)
    if not defaults['ocr_folder'] and Path('C:/Program Files/Tesseract-OCR/tesseract.exe').is_file():
        defaults['ocr_folder']='C:/Program Files/Tesseract-OCR'
    for name,label,pattern in [('executable','llama.cpp server: llama-server.exe','*.exe'),('model_path','Model GGUF','*.gguf'),('projector_path','Gemma vision companion (optional for chat)','*.gguf'),('ocr_folder','Tesseract OCR installation folder',None)]:
        row=tk.Frame(locations);row.pack(fill='x',padx=12,pady=10)
        labels[name]=tk.Label(row,text=label);labels[name].pack(anchor='w')
        value=tk.StringVar(value=defaults[name]);fields[name]=value
        entries[name]=tk.Entry(row,textvariable=value);entries[name].pack(side='left',fill='x',expand=True)
        controls.append(entries[name])
        def pick(v=value,p=pattern):
            selected=filedialog.askdirectory(parent=root,title='Choose installed Tesseract OCR folder') if p is None else filedialog.askopenfilename(parent=root,initialdir=str(app_root()/'Models') if (app_root()/'Models').is_dir() else str(app_root()),filetypes=[('Model or executable',p)])
            if selected:v.set(selected)
        buttons[name]=tk.Button(row,text='Browse',command=pick);buttons[name].pack(side='right');controls.append(buttons[name])
    tk.Button(locations,text='Download Tesseract OCR for Windows',
              command=lambda:webbrowser.open('https://github.com/UB-Mannheim/tesseract/wiki')).pack(anchor='w',padx=12,pady=(10,4))
    ocr_help=tk.StringVar()
    tk.Label(locations,textvariable=ocr_help,wraplength=660,justify='left',fg='#4d5961').pack(anchor='w',padx=12,pady=4)
    tk.Label(downloads,textvariable=ocr_help,wraplength=660,justify='left',fg='#4d5961').pack(anchor='w',padx=12,pady=(8,4))
    current_family=family.get()
    def refresh(*_,selection_changed=True):
        nonlocal current_family
        if selection_changed:
            model_paths[current_family]=fields['model_path'].get()
            current_family=family.get()
            fields['model_path'].set(model_paths[current_family])
            checks['qwen'].set(current_family=='qwen')
            checks['gemma'].set(current_family=='gemma')
            checks['projector'].set(current_family=='gemma')
        qwen=family.get()=='qwen'
        labels['model_path'].configure(text='Qwen 3.5 4B Q4_K_M GGUF' if qwen else 'Gemma 4 12B QAT Q4_0 GGUF')
        for name,enabled in [('projector_path',not qwen),('ocr_folder',qwen)]:
            entries[name].configure(state='normal' if enabled else 'disabled');buttons[name].configure(state='normal' if enabled else 'disabled')
        ocr_help.set('Qwen reads screen text with Tesseract. Install Tesseract with English data, then choose its folder in File locations.'
                     if qwen else 'For screen vision, select the matching Gemma vision companion. The main model supports chat on its own.')
    family.trace_add('write',refresh);refresh(selection_changed=False)
    saved=False
    working=False
    closing=False
    cancel=threading.Event()
    events=queue.Queue()
    message=tk.StringVar(value='Choose resources, then click Download selected.')
    tk.Label(root,textvariable=message,wraplength=700,justify='left',fg='#4d5961').pack(anchor='w',padx=20,pady=4)
    actions=tk.Frame(root);actions.pack(fill='x',padx=20,pady=(4,16))
    def set_working(value):
        nonlocal working
        working=value
        for control in controls:
            control.configure(state='disabled' if value else 'normal')
        download_button.configure(state='disabled' if value else 'normal')
        save_button.configure(state='disabled' if value else 'normal')
        cancel_button.configure(state='normal' if value else 'disabled')
        if not value:refresh(selection_changed=False)
    def start_downloads():
        selected=[resource for resource in RESOURCES if checks[resource.key].get()]
        if not selected:
            message.set('Select at least one resource to download.')
            return
        cancel.clear();set_working(True)
        message.set('Downloading to '+str(resource_root))
        def work():
            try:
                for resource in selected:
                    events.put(('progress',resource.key,'Starting',0,resource.size))
                    last_update=0
                    def progress(phase,completed,total):
                        nonlocal last_update
                        now=time.monotonic()
                        if now-last_update>=.1 or completed==total:
                            events.put(('progress',resource.key,phase,completed,total))
                            last_update=now
                    try:
                        path=install_resource(resource,resource_root,cancel,progress)
                        events.put(('ready',resource.key,str(path)))
                    except DownloadCancelled as error:
                        events.put(('stopped',resource.key,str(error)))
                        break
                    except Exception as error:
                        events.put(('stopped',resource.key,'Download failed. '+str(error)))
                        break
            finally:
                events.put(('finished',))
        threading.Thread(target=work,daemon=True).start()
    def poll():
        while not events.empty():
            event=events.get_nowait();kind=event[0]
            if kind=='progress':
                _,key,phase,completed,total=event
                bars[key]['value']=100*completed/max(1,total)
                statuses[key].set(f'{phase}  {completed/1_000_000:,.0f} / {total/1_000_000:,.0f} MB')
            elif kind=='ready':
                _,key,path=event
                bars[key]['value']=100;statuses[key].set('Ready')
                if key=='server':fields['executable'].set(path)
                elif key=='projector':fields['projector_path'].set(path)
                elif key in model_paths:
                    model_paths[key]=path
                    if family.get()==key:fields['model_path'].set(path)
                message.set('Completed resources are ready. Check File locations, then Save and open app.')
            elif kind=='stopped':
                statuses[event[1]].set(event[2]);message.set(event[2])
            elif kind=='finished':
                set_working(False)
                if closing:
                    root.destroy()
                    return
        root.after(100,poll)
    def save():
        nonlocal saved
        try:config,settings=setup_values({k:v.get() for k,v in fields.items()},family.get())
        except ValueError as error:
            notebook.select(locations)
            messagebox.showerror('Missing files',str(error),parent=root);return
        directory=resource_root/'config';directory.mkdir(parents=True,exist_ok=True)
        temporary=directory/'inference.local.json.tmp'
        temporary.write_text(json.dumps(config,indent=2),encoding='utf-8')
        temporary.replace(directory/'inference.local.json')
        model_paths[family.get()]=fields['model_path'].get()
        previous=preferences.load(resource_root)
        previous.update({key+'_model_path':path for key,path in model_paths.items() if path})
        previous.update(settings)
        previous['gemma_projector_path']=fields['projector_path'].get()
        preferences.save(resource_root,previous)
        saved=True;root.destroy()
    def close():
        nonlocal closing
        if working:
            closing=True;cancel.set()
            message.set('Cancelling downloads before closing...')
        else:root.destroy()
    download_button=tk.Button(actions,text='Download selected',command=start_downloads)
    download_button.pack(side='left')
    cancel_button=tk.Button(actions,text='Cancel downloads',command=cancel.set,state='disabled')
    cancel_button.pack(side='left',padx=8)
    save_button=tk.Button(actions,text='Save and open app',command=save)
    save_button.pack(side='right')
    root.protocol('WM_DELETE_WINDOW',close)
    root.after(100,poll)
    root.mainloop();return saved
