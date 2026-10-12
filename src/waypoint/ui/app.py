"""Canonical Waypoint GUI. User-approved continuous capture; no Codex relay or microphone."""
import argparse,json,queue,threading,time,traceback,base64,re,sys,webbrowser
from pathlib import Path
import tkinter as tk
from tkinter import font as tkfont,messagebox
from .theme import BG,PANEL,TEXT,MUTED,ACCENT
from .widgets import DarkScrollbar,OvalSlider
from .onboarding import WELCOME
from waypoint.branding import APP_NAME
from waypoint.version import VERSION
from waypoint.updates import check_for_update
from waypoint.paths import app_root,data_root
from waypoint.storage import preferences
from waypoint.capture.windows import list_windows
from waypoint.capture.feed import Feed
from waypoint.inference.engine import Engine
from waypoint.inference.client import Client
from waypoint.assistant.local import Assistant
from waypoint.integrations.accounts import Accounts,connector_for,suggest_games,public_api_for
from waypoint.assistant.routing import is_greeting,needs_screen,force_new_analysis,is_research_request
ROOT=data_root()
ASSETS=app_root()
class App:
    def __init__(self,smoke=False,vision_review=False):
        if vision_review and getattr(sys,'frozen',False):
            raise ValueError('Vision review is available only from the development source launcher.')
        self.smoke=smoke
        self.root=tk.Tk(); self.root.title(APP_NAME); self.root.overrideredirect(True)
        self.root.configure(bg=BG); self.root.minsize(360,300)
        self.brand_icon=tk.PhotoImage(file=str(ASSETS/'assets/branding/gw2-vlm-copilot-32.png'))
        self.header_icon=tk.PhotoImage(file=str(ASSETS/'assets/branding/gw2-vlm-copilot-24.png'))
        self.root.iconphoto(True,self.brand_icon)
        self.root.iconbitmap(str(ASSETS/'assets/branding/gw2-vlm-copilot.ico'))
        self.accounts=Accounts()
        self.settings=preferences.load(ROOT); self.size=max(9,min(20,int(self.settings.get('font_size',10))))
        self.font=tkfont.Font(family='Segoe UI',size=self.size)
        self.role_font=tkfont.Font(family='Segoe UI',size=self.size,weight='bold')
        self.root.geometry('440x580+100+100'); self.root.attributes('-topmost',True)
        self.root.attributes('-alpha',.96); self.events=queue.Queue(); self.engine=None; self.assistant=None
        self.review=None
        if vision_review:
            from waypoint.storage.vision_review import VisionReview
            self.review=VisionReview(ROOT); self.review.set_enabled(True)
        self.feed=None; self.feeds=[]; self.inference_lock=threading.Lock(); self.question_pending=threading.Event(); self.last_vision_status=0
        self.busy=False; self.closing=False; self.cancelled=threading.Event(); self.image=None; self.selected_window=None; self.folded=False
        self.shell=tk.Frame(self.root,bg=BG,highlightbackground='#3d5964',highlightthickness=1); self.shell.pack(fill='both',expand=True)
        header=tk.Frame(self.shell,bg=PANEL,height=36); header.pack(fill='x'); header.pack_propagate(False)
        logo=tk.Label(header,image=self.header_icon,bg=PANEL); logo.pack(side='left',padx=(8,0))
        title=tk.Label(header,text=APP_NAME,bg=PANEL,fg=TEXT,font=('Segoe UI Semibold',10)); title.pack(side='left',padx=(2,10))
        self.button(header,'\u00d7',self.close).pack(side='right'); self.fold_button=self.button(header,'\u25be',self.fold); self.fold_button.pack(side='right',pady=(0,2))
        self.fold_button.configure(font=('Segoe UI', 18),pady=1,)
        self.pin_button=self.button(header,'\u25c6',self.pin); self.pin_button.pack(side='right')
        self.pin_button.configure(fg=ACCENT,activeforeground=ACCENT)
        self.opacity=OvalSlider(header,lambda value:self.root.attributes('-alpha',value/100))
        self.opacity.configure(bg=PANEL)
        self.opacity.pack(side='right',padx=(4,8))
        self.opacity.set(self.settings.get('opacity',96))
        for w in (header,logo,title): w.bind('<ButtonPress-1>',self.drag_start); w.bind('<B1-Motion>',self.drag)
        self.body=tk.Frame(self.shell,bg=BG); self.body.pack(fill='both',expand=True)
        self.body.columnconfigure(0,weight=1); self.body.rowconfigure(2,weight=1)
        toolbar=tk.Frame(self.body,bg=BG); toolbar.grid(row=0,column=0,sticky='ew',padx=8,pady=5)
        self.select_button=self.button(toolbar,'Select window',self.select_window); self.select_button.pack(side='left')
        self.pause_button=self.button(toolbar,'Pause',self.pause_capture); self.pause_button.pack(side='left',padx=3)
        if not getattr(sys,'frozen',False):
            self.recording=tk.BooleanVar(value=vision_review)
            tk.Checkbutton(toolbar,text='Record vision (dev)',variable=self.recording,command=self.toggle_recording,
                           bg=BG,fg=TEXT,selectcolor=PANEL,activebackground=BG,font=('Segoe UI',9)).pack(side='left')
        self.button(toolbar,'A+',lambda:self.resize_text(1)).pack(side='right'); self.button(toolbar,'A\u2212',lambda:self.resize_text(-1)).pack(side='right')
        self.status=tk.Label(self.body,text='Start the local engine, then type a question.',bg=BG,fg=MUTED,font=('Segoe UI',9),wraplength=410,anchor='w',justify='left'); self.status.grid(row=1,column=0,sticky='ew',padx=10)
        box=tk.Frame(self.body,bg=BG); box.grid(row=2,column=0,sticky='nsew',padx=8)
        self.chat=tk.Text(box,bg=BG,fg=TEXT,font=self.font,width=1,height=1,wrap='word',bd=0,state='disabled',highlightthickness=0)
        self.chat.tag_configure('role_waypoint',foreground=ACCENT,font=self.role_font)
        self.chat.tag_configure('role_you',foreground='#ff7272',font=self.role_font)
        self.chat.pack(side='left',fill='both',expand=True); scroll=DarkScrollbar(box,self.chat.yview); scroll.pack(side='right',fill='y'); self.chat.configure(yscrollcommand=scroll.set)
        self.entry=tk.Text(self.body,height=2,width=1,bg=PANEL,fg=TEXT,insertbackground=TEXT,font=('Segoe UI',11),wrap='word',bd=0); self.entry.grid(row=3,column=0,sticky='ew',padx=10,pady=6)
        self.entry.bind('<Return>',self.enter)
        row=tk.Frame(self.body,bg=BG); row.grid(row=4,column=0,sticky='ew',padx=8,pady=4)
        self.connect=self.button(row,'Start engine',self.toggle); self.connect.pack(side='left')
        self.button(row,'Accounts',self.account_window).pack(side='left',padx=(4,0))
        self.send_button=self.button(row,'Send',self.send); self.send_button.pack(side='right')
        self.cancel_button=self.button(row,'Cancel',self.cancel); self.cancel_button.pack(side='right'); self.cancel_button.configure(state='disabled')
        self.update_available=None; self.update_checking=False
        update_row=tk.Frame(self.body,bg=BG); update_row.grid(row=5,column=0,sticky='ew',padx=8,pady=(0,3))
        self.auto_updates=tk.BooleanVar(value=self.settings.get('check_updates_on_launch',True))
        tk.Checkbutton(update_row,text='Check updates on launch',variable=self.auto_updates,bg=BG,fg=MUTED,
                       selectcolor=PANEL,activebackground=BG,font=('Segoe UI',9)).pack(side='left')
        self.update_button=self.button(update_row,'Check updates',self.update_action); self.update_button.pack(side='right')
        self.update_status=tk.Label(self.body,text='',bg=BG,fg=ACCENT,font=('Segoe UI',9),anchor='w',justify='left',wraplength=320)
        self.update_status.grid(row=6,column=0,sticky='ew',padx=10); self.update_status.grid_remove()
        grip=tk.Label(self.shell,text='\u25e2',bg=BG,fg=MUTED,cursor='size_nw_se'); grip.place(relx=1,rely=1,anchor='se')
        grip.bind('<ButtonPress-1>',self.resize_start); grip.bind('<B1-Motion>',self.resize)
        self.body.bind('<Configure>',self.fit_body)
        self.root.bind('<Escape>',lambda e:self.fold()); self.root.protocol('WM_DELETE_WINDOW',self.close)
        self.append('Waypoint',WELCOME)
        if self.review:
            self.append('Waypoint','Development vision recording enabled: '+str(self.review.directory)+'. Frames and visible text are saved locally, up to one hour or 5 GB.')
        self.chat.yview_moveto(0)
        self.root.after(100,self.poll)
        if not smoke and self.auto_updates.get(): self.root.after(1200,lambda:self.check_updates(False))
        if smoke:
            self.root.after(100,lambda:self.resize_text(1)); self.root.after(200,self.fold); self.root.after(300,self.fold); self.root.after(450,self.close)
    def update_action(self):
        if self.update_available:
            webbrowser.open(self.update_available['url'])
        else: self.check_updates(True)
    def check_updates(self,manual=True):
        if self.update_checking or self.closing: return
        self.update_checking=True; self.update_button.configure(state='disabled')
        if manual:
            self.update_status.configure(text='Checking for updates...'); self.update_status.grid()
        def work():
            try: result=check_for_update(); error=False
            except Exception: result=None; error=True
            self.events.put(('update_result',(result,error,manual)))
        threading.Thread(target=work,daemon=True).start()
    def finish_update_check(self,value):
        result,error,manual=value
        self.update_checking=False; self.update_button.configure(state='normal')
        if self.closing: return
        if result:
            self.update_available=result
            self.update_button.configure(text='Download update',fg=ACCENT)
            self.update_status.configure(text='Update available: v'+result['version']+' (installed: v'+VERSION+')')
            self.update_status.grid()
        elif manual:
            self.update_status.configure(text='Could not check updates. Try again later.' if error else 'No newer Windows release available (v'+VERSION+').')
            self.update_status.grid()
    def account_window(self):
        dialog=tk.Toplevel(self.root); dialog.title('Connect your Guild Wars 2 Account'); dialog.geometry('500x390'); dialog.minsize(500,390); dialog.transient(self.root)
        dialog.iconphoto(False,self.brand_icon)
        tk.Label(dialog,text='Connect your Guild Wars 2 Account',font=('Segoe UI Semibold',12)).pack(pady=8)
        tk.Label(dialog,text='Connect your official Guild Wars 2 API key to help your copilot understand your account progress.',wraplength=470,justify='left').pack(padx=12)
        requirements=tk.Label(dialog,text='',wraplength=470,justify='left'); requirements.pack(pady=8,padx=12)
        tk.Label(dialog,text='API key or token',anchor='w').pack(anchor='w',padx=12)
        key=tk.Entry(dialog,show='*',width=55,state='disabled'); key.pack(padx=12)
        tk.Label(dialog,text='Tokens are saved locally with Windows protection after a successful connection. Leave this field blank to use the saved token. Tokens never enter chat.',wraplength=470).pack(pady=6)
        status=tk.Label(dialog,text='Enter your API key, or reconnect using your saved token.',wraplength=470); status.pack(pady=8)
        buttons=tk.Frame(dialog); buttons.pack()
        result=queue.Queue(); running=False; chosen=None
        def choose():
            nonlocal chosen
            chosen='Guild Wars 2'
            requirements.configure(text=self.accounts.select_game(chosen))
            if self.assistant: self.assistant.resources.select('my game is '+chosen)
            key.configure(state='normal'); connect.configure(state='normal')
            update.configure(state='normal' if self.accounts.key else 'disabled')
            status.configure(text='Saved token available. Click Connect to reconnect, or enter a replacement.' if self.accounts.has_saved(chosen) else 'Enter your API key, then Connect.')
        def request(refresh=False):
            nonlocal running
            if running or not chosen: return
            value=key.get().strip(); key.delete(0,'end'); running=True
            connect.configure(state='disabled'); update.configure(state='disabled'); key.configure(state='disabled')
            status.configure(text='Updating your account progress...')
            def worker():
                try: result.put(self.accounts.refresh() if refresh else self.accounts.connect(value,chosen,remember=True))
                except Exception as exc: result.put(str(exc))
            threading.Thread(target=worker,daemon=True).start()
        def disconnect():
            self.accounts.disconnect(); status.configure(text='Account disconnected. You can still use window vision and saved goals.')
            if not running: key.configure(state='normal' if chosen and connector_for(chosen) else 'disabled'); key.delete(0,'end')
        def forget():
            if running or not chosen: return
            try:
                self.accounts.forget(chosen); key.configure(state='normal' if connector_for(chosen) else 'disabled'); key.delete(0,'end')
                update.configure(state='disabled'); status.configure(text='Saved token removed and account disconnected. Enter a token to connect again.')
            except OSError: status.configure(text='Could not remove the saved token. Try again.')
        def poll_account():
            nonlocal running
            if not dialog.winfo_exists(): return
            try:
                text=result.get_nowait(); status.configure(text=text); running=False
                supported=bool(chosen and connector_for(chosen))
                key.configure(state='normal' if supported else 'disabled'); connect.configure(state='normal' if supported else 'disabled')
                update.configure(state='normal' if self.accounts.key else 'disabled')
            except queue.Empty: pass
            dialog.after(100,poll_account)
        connect=tk.Button(buttons,text='Connect',command=request,state='disabled'); connect.pack(side='left',padx=4)
        update=tk.Button(buttons,text='Refresh',command=lambda:request(True),state='disabled'); update.pack(side='left',padx=4)
        tk.Button(buttons,text='Disconnect',command=disconnect).pack(side='left',padx=4)
        tk.Button(dialog,text='Forget saved token',command=forget).pack(pady=8)
        choose()
        dialog.after(100,poll_account)
    def fit_body(self,event):
        self.status.configure(wraplength=max(200,event.width-20))
        self.entry.configure(height=2 if event.height<360 else 3)
    def button(self,parent,text,command):
        return tk.Button(parent,text=text,command=command,bg=PANEL,fg=TEXT,activebackground='#304550',activeforeground=TEXT,relief='flat',bd=0,padx=8,pady=2,font=('Segoe UI',10))
    def drag_start(self,e): self.drag_offset=(e.x_root-self.root.winfo_x(),e.y_root-self.root.winfo_y())
    def drag(self,e): self.root.geometry(f'+{e.x_root-self.drag_offset[0]}+{e.y_root-self.drag_offset[1]}')
    def resize_start(self,e): self.resize_origin=(e.x_root,e.y_root,self.root.winfo_width(),self.root.winfo_height())
    def resize(self,e):
        if not self.folded:
            x,y,w,h=self.resize_origin; self.root.geometry(f'{max(360,w+e.x_root-x)}x{max(300,h+e.y_root-y)}')
    def resize_text(self,delta): self.size=max(9,min(20,self.size+delta)); self.font.configure(size=self.size); self.role_font.configure(size=self.size)
    def pin(self):
        active=not bool(self.root.attributes('-topmost'))
        self.root.attributes('-topmost',active)
        self.pin_button.configure(fg=ACCENT if active else MUTED,activeforeground=ACCENT if active else MUTED)
    def fold(self):
        if not self.folded:
            self.expanded=self.root.geometry(); self.body.pack_forget(); self.root.minsize(320,36); self.root.geometry('320x36'); self.fold_button.configure(text='\u25b8')
        else:
            self.body.pack(fill='both',expand=True); self.root.minsize(360,300); self.root.geometry(self.expanded); self.fold_button.configure(text='\u25be')
        self.folded=not self.folded
    def select_window(self):
        if self.busy: return
        windows=list_windows()
        dialog=tk.Toplevel(self.root); dialog.title(APP_NAME+' - Select window'); dialog.iconphoto(False,self.brand_icon); dialog.iconbitmap(str(ASSETS/'assets/branding/gw2-vlm-copilot.ico')); dialog.geometry('500x300'); dialog.attributes('-topmost',True)
        tk.Label(dialog,text=APP_NAME,image=self.header_icon,compound='left',font=('Segoe UI Semibold',10)).pack(anchor='w',padx=10,pady=(8,0))
        tk.Label(dialog,text='Choose the game/application window for continuous local vision.',wraplength=470).pack(pady=8)
        choices=tk.Listbox(dialog,exportselection=False); choices.pack(fill='both',expand=True,padx=10)
        for window in windows: choices.insert('end',window.title)
        def confirm():
            indexes=choices.curselection()
            if not indexes: return
            target=windows[indexes[0]]
            if not messagebox.askyesno('Approve capture',f'Allow continuous screenshots of {target.title} at up to 2 FPS?\n\nCapture continues while you use other apps. Minimize the game to pause; restore it to resume. The model analyzes the latest frame at its own speed. Pause stops capture and clears approval. Screenshots stay in memory.',parent=dialog): return
            self.stop_feed(); self.selected_window=target; dialog.destroy(); self.start_feed()
            self.append('Waypoint',f'Selected {target.title}. Keep that window restored to continue vision, even while using other apps. Then type a question and Send. Pause stops vision and clears this selection.')
            self.status.configure(text='Capture approved \u00b7 '+target.title)
        tk.Button(dialog,text='Confirm window',command=confirm).pack(pady=8)
        dialog.transient(self.root); dialog.grab_set()
    def start_feed(self):
        if self.selected_window and self.assistant and not self.feed:
            self.feed=Feed(self.selected_window,self.assistant,self.inference_lock,self.question_pending,max_width=self.engine.config.get('capture_max_width',1280) if self.engine else 1280,review_callback=self.record_review if not getattr(sys,'frozen',False) else None,frame_callback=self.record_frame if not getattr(sys,'frozen',False) else None)
            self.feeds.append(self.feed); self.feed.start()
    def toggle_recording(self):
        if getattr(sys,'frozen',False): return
        try:
            if self.review is None:
                from waypoint.storage.vision_review import VisionReview
                self.review=VisionReview(ROOT)
            self.review.set_enabled(self.recording.get())
            self.append('Waypoint','Development recording '+('ON: frames and chat saved locally, up to one hour or 5 GB. '+str(self.review.directory) if self.review.enabled else 'OFF. Existing recordings remain locally.'))
        except OSError:
            self.recording.set(False); self.append('Waypoint','Could not start development recording.')
    def record_frame(self,stamp,png):
        if self.review is None: return
        try: return self.review.save_frame(stamp,png)
        except OSError:
            self.review.set_enabled(False)
            self.events.put(('review_error','Development recording stopped: storage limit or file-write failure.'))
    def record_review(self,kind,**values):
        if self.review is None: return
        try: self.review.record(kind,**values)
        except OSError:
            self.review.set_enabled(False)
            self.events.put(('review_error','Local review logging stopped because the file could not be written or reached its size limit.'))
    def view_frame(self):
        if not self.feed: self.append('Waypoint','Select and approve a window first.'); return
        try: stamp,png=self.feed.snapshot(max_age=90)
        except RuntimeError as exc: self.append('Waypoint',str(exc)); return
        dialog=tk.Toplevel(self.root); dialog.title('Captured frame \u2014 model input'); dialog.attributes('-topmost',True)
        tk.Label(dialog,text=f'Actual captured frame \u00b7 {time.monotonic()-stamp:.0f} seconds old \u00b7 nothing saved').pack()
        photo=tk.PhotoImage(data=base64.b64encode(png))
        # Show the original pixels in a scrollable view, avoiding a second resize of small UI text.
        canvas=tk.Canvas(dialog,width=min(1000,photo.width()),height=min(650,photo.height()))
        xscroll=tk.Scrollbar(dialog,orient='horizontal',command=canvas.xview); xscroll.pack(side='bottom',fill='x')
        yscroll=tk.Scrollbar(dialog,command=canvas.yview); yscroll.pack(side='right',fill='y')
        canvas.pack(fill='both',expand=True); canvas.configure(xscrollcommand=xscroll.set,yscrollcommand=yscroll.set,scrollregion=(0,0,photo.width(),photo.height()))
        canvas.create_image(0,0,image=photo,anchor='nw'); dialog.photo=photo
    def stop_feed(self):
        if self.feed: self.feed.stop(); self.feed=None
    def pause_capture(self):
        self.stop_feed(); self.selected_window=None; self.cancelled.set()
        self.status.configure(text='Capture paused \u00b7 window approval cleared')
        if self.busy: self.cancel()
    def append(self,role,text):
        self.chat.configure(state='normal')
        tag={'Waypoint':'role_waypoint','You':'role_you'}.get(role)
        self.chat.insert('end',(APP_NAME if role=='Waypoint' else role)+'\n',(tag,) if tag else ())
        self.chat.insert('end',text+'\n\n',())
        self.chat.see('end'); self.chat.configure(state='disabled')
    def lock(self,busy):
        self.busy=busy; state='disabled' if busy else 'normal'
        for widget in (self.connect,self.send_button,self.select_button): widget.configure(state=state)
        self.cancel_button.configure(state='normal' if busy and self.assistant else 'disabled')
    def toggle(self):
        if self.busy: return
        self.lock(True); self.status.configure(text='Stopping engine\u2026' if self.engine else 'Loading local model\u2026')
        def work():
            try:
                if self.engine:
                    self.stop_feed()
                    for feed in self.feeds: feed.wait()
                    self.feeds.clear(); self.engine.stop(); self.events.put(('stopped',None))
                else:
                    config=json.loads((ROOT/'config/inference.local.json').read_text('utf-8')); engine=Engine(config,ROOT); engine.start()
                    self.events.put(('started',(engine,Assistant(Client(f"http://127.0.0.1:{config['port']}/v1"),accounts=self.accounts,allowed_sources=('Guild Wars 2',)))))
            except Exception as exc: self.events.put(('error',str(exc)))
        threading.Thread(target=work,daemon=True).start()
    def enter(self,e):
        if e.state & 1: return
        self.send(); return 'break'
    def send(self):
        if self.busy: return
        question=self.entry.get('1.0','end-1c').strip()
        if re.search(r'(?i)\b[0-9a-f]{8}(?:-[0-9a-f]{4}){2}-[0-9a-f-]{20,}\b',question):
            self.entry.delete('1.0','end'); self.append('Waypoint','API keys belong in the private Accounts field. This message was not sent to the model.'); self.account_window(); return
        if re.search(r'(?i)\b(connect|link|add)\b.{0,45}\b(account|api)\b',question):
            self.entry.delete('1.0','end'); self.append('You',question); self.account_window(); return
        if not self.assistant: self.status.configure(text='Start the engine first.'); return
        if not question or len(question)>2000: self.status.configure(text='Enter a question of 1\u20132000 characters.'); return
        if self.selected_window is None and any(term in question.lower() for term in ('watch ', 'capture ', 'vision test')):
            self.append('You',question); self.entry.delete('1.0','end'); self.select_window(); return
        target=self.selected_window; image=self.image; assistant=self.assistant; self.cancelled.clear(); self.lock(True)
        self.append('You',question); self.entry.delete('1.0','end'); self.status.configure(text='Preparing a local answer\u2026')
        feed=self.feed
        self.question_pending.set()
        def work():
            observation=None; age=None; observation_stamp=None
            try:
                if self.cancelled.is_set(): self.events.put(('cancelled',None)); return
                # Freeze the most recent approved frame before waiting for active inference.
                frame=None
                if target and needs_screen(question) and not is_greeting(question) and not is_research_request(question):
                    try:
                        if feed: frame=feed.snapshot()
                        elif needs_screen(question): raise RuntimeError('Vision is not running. Select the window and start the engine.')
                    except RuntimeError:
                        if needs_screen(question): raise
                question_frame=frame
                if question_frame is None and feed and self.review:
                    try: question_frame=feed.snapshot()
                    except RuntimeError: pass
                if question_frame: self.record_frame(*question_frame)
                self.record_review('question',question=question,frame_stamp=question_frame[0] if question_frame else None)
                with self.inference_lock:
                    if self.cancelled.is_set(): self.events.put(('cancelled',None)); return
                    if frame:
                        stamp,png=frame
                        self.events.put(('progress','Analyzing screen and answering\u2026'))
                        observation,age,observation_stamp=feed.observation_context(max_age=10,include_stamp=True) if feed and not force_new_analysis(question) else (None,None,None)
                        if observation is None:
                            self.record_frame(stamp,png); observation_stamp=stamp
                            observation=assistant.observe(png,window_title=target.title if target else '',question=question); age=time.monotonic()-stamp
                        if self.cancelled.is_set(): self.events.put(('cancelled',None)); return
                        answer=assistant.answer(observation,question,window_title=target.title if target else '',progress=lambda text:self.events.put(('progress',text)),observation_age=age)
                    elif image:
                        observation=assistant.observe(image)
                        answer=assistant.answer(observation,question)
                    else:
                        observation,age,observation_stamp=feed.observation_context(include_stamp=True) if feed and not is_greeting(question) and not is_research_request(question) else (None,None,None)
                        if observation is not None:
                            answer=assistant.answer(observation,question,window_title=target.title if target else '',progress=lambda text:self.events.put(('progress',text)),observation_age=age)
                        else:
                            research_observation,_=feed.observation_context() if feed and is_research_request(question) else (None,None)
                            answer=assistant.chat(question,window_title=target.title if target else '',progress=lambda text:self.events.put(('progress',text)),vision_state=feed.state() if feed else {'approved':bool(target)},research_observation=research_observation)
                if not self.cancelled.is_set():
                    self.record_review('answer',question=question,answer=answer,observation=observation,frame_age_seconds=age,frame_stamp=observation_stamp)
                self.events.put(('cancelled',None) if self.cancelled.is_set() else ('answer',answer))
            except Exception as exc:
                self.record_review('answer_error',question=question,error_type=type(exc).__name__,frame_stamp=observation_stamp)
                log=ROOT/'local-data/gui-errors.log'; log.parent.mkdir(exist_ok=True)
                with log.open('a',encoding='utf-8') as out: out.write(traceback.format_exc()+'\n')
                self.events.put(('cancelled',None) if self.cancelled.is_set() else ('error',str(exc)))
            finally: self.question_pending.clear()
        self.status.configure(text='Waiting for local model\u2026')
        threading.Thread(target=work,daemon=True).start()
    def cancel(self): self.cancelled.set(); self.cancel_button.configure(state='disabled'); self.status.configure(text='Cancelling: current request finishes, then its result is discarded.')
    def poll(self):
        try:
            while True:
                kind,value=self.events.get_nowait()
                if kind=='update_result': self.finish_update_check(value); continue
                if kind=='review_error':
                    if hasattr(self,'recording'): self.recording.set(False)
                    self.append('Waypoint',value); continue
                if kind=='progress': self.status.configure(text=value); continue
                if kind=='started': self.engine,self.assistant=value; self.connect.configure(text='Stop engine'); self.status.configure(text='Local engine ready.'); self.start_feed()
                elif kind=='stopped': self.engine=None; self.assistant=None; self.connect.configure(text='Start engine'); self.status.configure(text='Engine stopped.')
                elif kind=='answer': self.append('Waypoint',value); self.status.configure(text='Answer ready \u00b7 local inference')
                elif kind=='cancelled': self.status.configure(text='Cancelled. No answer added.')
                elif kind=='error': self.status.configure(text='Error: '+value); self.append('Waypoint','Could not answer: '+value)
                self.lock(False)
        except queue.Empty: pass
        if self.feed and not self.busy:
            state=self.feed.state(); age=state['observation_age_seconds']
            detail=f'last analyzed frame {age:.0f}s old' if age is not None else ('analyzing first frame\u2026' if state['analyzing'] else 'waiting for game frames')
            self.status.configure(text=(state['vision_error'] or state['capture_error'] or f"Vision \u00b7 {state['frames_captured']} frames \u00b7 "+detail)[:180])
        if time.monotonic()-self.last_vision_status>=1:
            state=self.feed.state() if self.feed else {'approved':False}
            state['updated_at']=time.time()
            try: preferences.save_status(ROOT,state)
            except OSError: pass
            self.last_vision_status=time.monotonic()
        if self.closing and not self.busy:
            if self.engine:
                self.toggle(); return self.root.after(100,self.poll)
            self.root.destroy(); return
        self.root.after(100,self.poll)
    def close(self):
        if self.closing: return
        self.closing=True; self.cancelled.set(); self.stop_feed()
        if not self.smoke: preferences.save(ROOT,{'font_size':self.size,'opacity':self.opacity.value,'check_updates_on_launch':self.auto_updates.get()})
        self.status.configure(text='Closing after local work and engine shutdown\u2026')
    def run(self): self.root.mainloop()
def main():
    p=argparse.ArgumentParser(); p.add_argument('--smoke',action='store_true')
    if not getattr(sys,'frozen',False): p.add_argument('--vision-review',action='store_true',help='Development frame recording and diagnostics')
    args=p.parse_args(); App(smoke=args.smoke,vision_review=getattr(args,'vision_review',False)).run()
if __name__=='__main__': main()
