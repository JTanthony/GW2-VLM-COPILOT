import tkinter as tk
from pathlib import Path
from waypoint.paths import app_root
from .theme import BG,PANEL,TEXT,MUTED,ACCENT

class DarkScrollbar(tk.Canvas):
    """Draw our own track because Windows ignores native scrollbar colors."""
    def __init__(self, parent, command):
        super().__init__(parent, width=10, bg=BG, bd=0, highlightthickness=0)
        self.command = command
        self.first, self.last = 0.0, 1.0
        self.drag = None
        self.bind('<Configure>', lambda event: self.redraw())
        self.bind('<Button-1>', self.press)
        self.bind('<B1-Motion>', self.move)
        self.bind('<ButtonRelease-1>', lambda event: setattr(self, 'drag', None))
        self.bind('<MouseWheel>', lambda event: self.command('scroll', -int(event.delta / 120), 'units'))

    def set(self, first, last):
        self.first, self.last = float(first), float(last)
        self.redraw()

    def geometry(self):
        height = max(1, self.winfo_height())
        size = min(height, max(24, (self.last - self.first) * height))
        limit = max(0, 1 - (self.last - self.first))
        top = self.first / limit * (height - size) if limit else 0
        return height, size, limit, top

    def redraw(self):
        self.delete('all')
        if self.last - self.first < .999:
            _, size, _, top = self.geometry()
            self.create_rectangle(2, top, 8, top + size, fill='#3d5964', outline='')

    def press(self, event):
        height, size, limit, top = self.geometry()
        if top <= event.y <= top + size:
            self.drag = (event.y, self.first)
        elif height > size:
            self.command('moveto', max(0, min(limit, (event.y - size / 2) / (height - size) * limit)))

    def move(self, event):
        height, size, limit, _ = self.geometry()
        if self.drag and height > size:
            y, first = self.drag
            self.command('moveto', max(0, min(limit, first + (event.y - y) / (height - size) * limit)))


class OvalSlider(tk.Canvas):
    """Compact pill track with a circular, draggable thumb."""
    def __init__(self, parent, command):
        super().__init__(parent, width=66, height=20, bg=BG, bd=0,
                         highlightthickness=0, cursor='hand2', takefocus=True)
        self.command = command
        self.value = 96
        self.thumb = tk.PhotoImage(file=str(app_root() / 'assets/ui/slider-thumb.png'))
        self.bind('<Button-1>', self.choose)
        self.bind('<B1-Motion>', self.choose)
        self.bind('<Left>', lambda event: self.set(self.value - 1))
        self.bind('<Right>', lambda event: self.set(self.value + 1))
        self.bind('<Home>', lambda event: self.set(55))
        self.bind('<End>', lambda event: self.set(100))

    def set(self, value):
        self.value = max(55, min(100, float(value)))
        self.delete('all')
        x = 8 + (self.value - 55) / 45 * 50
        # Overlapping circles and a rectangle form an oval-ended track.
        for left, right, color in ((8, 58, '#40515b'),):
            self.create_oval(left - 3, 7, left + 3, 13, fill=color, outline='')
            self.create_rectangle(left, 7, right, 13, fill=color, outline='')
            self.create_oval(right - 3, 7, right + 3, 13, fill=color, outline='')
        self.create_image(x, 10, image=self.thumb)
        self.command(self.value)

    def choose(self, event):
        self.focus_set()
        self.set(55 + (event.x - 8) / 50 * 45)


