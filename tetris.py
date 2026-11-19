"""Pocket Blocks • Tk desktop edition."""
import tkinter as tk
from engine import Game, SHAPES, cells

BG, PANEL, INK, MUTED, LIME = '#101719', '#1c282a', '#f1f6e9', '#adbfba', '#ccf477'
COLORS = dict(I='#73d6ce', O='#efcb68', T='#bc9dde', S='#a5d77b', Z='#ee958d', J='#88afe4', L='#edac75', X='#758988')
U = 24


class Arcade:
    def __init__(self, root):
        self.root = root
        root.title('Pocket Blocks | Falling-block arcade')
        root.configure(bg=BG, padx=18, pady=12)
        root.resizable(False, False)
        self.label(root, 'P O C K E T   /   A R C A D E     •     0 1', 10, LIME).pack(anchor='w')
        self.label(root, 'Pocket Blocks', 26, INK).pack(anchor='w')
        body = tk.Frame(root, bg=BG)
        body.pack(pady=8)
        self.field = tk.Canvas(body, width=240, height=480, bg='#121e20', highlightthickness=1, highlightbackground=MUTED)
        self.field.pack(side='left')
        side = tk.Frame(body, bg=BG, padx=14)
        side.pack(side='left', fill='y')
        self.label(side, 'UP NEXT', 10, MUTED).pack(anchor='w')
        self.preview = tk.Canvas(side, width=150, height=68, bg=PANEL, highlightthickness=0)
        self.preview.pack(pady=(3, 12))
        self.stats = self.label(side, '', 14, INK)
        self.stats.pack(anchor='w')
        self.label(side, 'NEW GAME', 10, MUTED).pack(anchor='w', pady=(16, 3))
        for title, mode in [('A  /  Endurance', False), ('B  /  Clear 25', True)]:
            tk.Button(side, text=title, command=lambda m=mode: self.new(m), bg=PANEL, fg=INK, relief='flat', takefocus=False).pack(fill='x', pady=2)
        self.label(side, '← →   Move\n↑ / Z   Rotate\n↓       Soft drop\nSpace   Hard drop\nP       Pause\nR       Restart', 10, MUTED).pack(anchor='w', pady=12)
        root.bind('<KeyPress>', self.key)
        self.timer = None
        self.new(False)

    @staticmethod
    def label(parent, text, size, color):
        return tk.Label(parent, text=text, font=('TkFixedFont', size), bg=BG, fg=color, justify='left')

    def new(self, mode):
        self.g = Game(mode)
        self.paint()
        self.schedule()

    def schedule(self):
        if self.timer is not None:
            self.root.after_cancel(self.timer)
        self.timer = None
        if self.g.state == 'playing':
            self.timer = self.root.after(max(85, 800-70*self.g.level), self.tick)

    def tick(self):
        self.timer = None
        self.g.step()
        self.paint()
        self.schedule()

    def key(self, event):
        k, g = event.keysym.lower(), self.g
        if k == 'r':
            self.new(g.challenge)
            return
        if k == 'p' and g.state in ('playing', 'paused'):
            g.state = 'paused' if g.state == 'playing' else 'playing'
            self.schedule()
        elif g.state != 'playing':
            return
        elif k in ('left', 'right'):
            g.move(1 if k == 'right' else -1, 0)
        elif k in ('up', 'z'):
            g.rotate(k == 'up')
        elif k == 'down':
            g.step(True)
            self.schedule()
        elif k == 'space':
            g.drop()
            self.schedule()
        self.paint()
        return 'break'

    @staticmethod
    def tile(canvas, x, y, color, ghost=False):
        canvas.create_rectangle(x+1, y+1, x+U-1, y+U-1, fill='' if ghost else color, outline=color)
        if not ghost:
            canvas.create_line(x+4, y+U-5, x+4, y+4, x+U-5, y+4, fill=PANEL)

    def paint(self):
        g, f = self.g, self.field
        f.delete('all')
        for y, row in enumerate(g.board):
            for x, val in enumerate(row):
                if val:
                    self.tile(f, x*U, y*U, COLORS[val])
                else:
                    f.create_rectangle(x*U, y*U, x*U+1, y*U+1, outline=PANEL)
        if g.state == 'playing':
            for base, ghost in [(g.landing(), True), (g.y, False)]:
                for x, y in cells(g.shape):
                    self.tile(f, (g.x+x)*U, (base+y)*U, COLORS[g.kind], ghost)
        else:
            f.create_rectangle(0, 196, 240, 284, fill=PANEL, outline=LIME)
            f.create_text(120, 226, text=g.state.upper(), fill=LIME, font=('TkFixedFont', 18))
            f.create_text(120, 255, text='P to resume' if g.state == 'paused' else 'R to play again', fill=INK)
        self.preview.delete('all')
        points = cells(SHAPES[g.next])
        for x, y in points:
            self.tile(self.preview, 75+(x-(1+max(i for i,j in points))/2)*U, 10+(y-min(j for i,j in points))*U, COLORS[g.next])
        mode = 'B / CLEAR 25' if g.challenge else 'A / ENDURANCE'
        self.stats.config(text=f'{mode}\n\n{g.score:07} pts\n{g.lines:03} lines\nLv. {g.level:02}')


if __name__ == '__main__':
    window = tk.Tk()
    Arcade(window)
    window.mainloop()
