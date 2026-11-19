# Pocket Blocks

A keyboard-driven falling-block game for the desktop, written in Python with Tkinter. Play an endless score chase or tackle a short obstacle course. No game assets, network access, or pip packages are required.

## Run

With Python 3.8+ and a graphical desktop, run these commands from the repository root:

```sh
python3 -m tkinter  # optional: check that Tk opens a window
python3 tetris.py
```

On Windows, use `py` instead of `python3`. If Tkinter is missing on Ubuntu/Debian, install `python3-tk` for the system Python. A headless terminal can run the tests but cannot display the game.

## Play

The game opens in **A / Endurance**. Complete horizontal rows to remove them; every ten lines raises the level and speeds up gravity until it reaches its cap. **B / Clear 25** starts with four rows of scattered blocks: clear 25 lines to win. Click either mode button to start a fresh board. If the next piece cannot enter, the game ends.

| Key | Action |
| --- | --- |
| Left / Right | Slide one column |
| Up / Z | Rotate clockwise / counterclockwise |
| Down | Soft drop (1 point per cell) |
| Space | Drop to the outlined landing position and lock (2 points per cell) |
| P / R | Pause or resume / restart current mode |

Clearing one, two, three, or four rows at once awards 40, 100, 300, or 1,200 points respectively, multiplied by the level before the clear plus one.

## Research and design

[Nintendo’s Game Boy overview](https://www.nintendo.com/en-gb/Games/Game-Boy/TETRIS--275924.html) contrasts A-Type’s accelerating endurance play with B-Type’s 25-line objective and obstacles. That distinction drives the two modes here: the same placement decisions serve either a long-term score or a finite target. [MobyGames’ account of the 1989 release](https://www.mobygames.com/game/42121/tetris/) describes the seven four-block shapes and horizontal line clears retained in both modes.

This is an independent interpretation, not an emulator or an official Nintendo product. It uses a 10×20 field, shuffled seven-piece bags, a landing outline, and instant hard drop. The challenge uses a fixed obstacle depth rather than the original height selector. All visuals are drawn with Tk; no Nintendo graphics or music are included.

## Development

`engine.py` holds the board, collision, rotation, scoring and mode rules. `tetris.py` handles drawing, keyboard input and the Tk gravity timer. Run the headless rule tests with `python3 -m unittest -v`.
