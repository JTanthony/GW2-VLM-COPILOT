"""GW2 account form checks: hidden UI, no engine, capture or network."""
import sys,unittest,tkinter as tk
from pathlib import Path
from unittest.mock import MagicMock
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from waypoint.ui.app import App
from waypoint.integrations.accounts import Accounts
class AccountFormTests(unittest.TestCase):
    def setUp(self):
        self.root=tk.Tk();self.root.withdraw();self.addCleanup(self.root.destroy)
        self.app=App.__new__(App);self.app.root=self.root;self.app.brand_icon=tk.PhotoImage(width=1,height=1)
        self.store=MagicMock();self.store.has.return_value=True
        self.app.accounts=Accounts(self.store);self.app.assistant=None;self.app.account_window()
        self.dialog=next(w for w in self.root.winfo_children() if isinstance(w,tk.Toplevel));self.dialog.withdraw()
        self.widgets=[]
        def collect(w):
            for child in w.winfo_children():self.widgets.append(child);collect(child)
        collect(self.dialog)
    def test_fixed_game_and_private_empty_field(self):
        self.assertEqual(self.app.accounts.selected_game,'Guild Wars 2')
        self.assertEqual(self.dialog.title(),'Connect your Guild Wars 2 Account')
        fields=[w for w in self.widgets if isinstance(w,tk.Entry)]
        self.assertEqual(len(fields),1);self.assertEqual(fields[0].get(),'');self.assertEqual(fields[0].cget('show'),'*')
        self.store.load.assert_not_called()
        self.assertFalse(any(isinstance(w,tk.Listbox) for w in self.widgets))
        self.assertFalse(any(isinstance(w,tk.Button) and w.cget('text')=='Use game' for w in self.widgets))
    def test_forget_saved_token(self):
        next(w for w in self.widgets if isinstance(w,tk.Button) and w.cget('text')=='Forget saved token').invoke()
        self.store.forget.assert_called_once_with('Guild Wars 2')
