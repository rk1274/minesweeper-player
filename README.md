# Minesweeper player (GUI and terminal)

A modern, graphical version of the classic **Minesweeper** game built with **PyQt5** in Python.

This repository contains both the GUI version of Minesweeper and the original text-based core logic. You can also run a standalone executable without installing Python.

## Running the GUI Version

You can simply run the minesweeper.exe if using windows.

Alternatively you'll need to have **Python 3.7+** and **PyQt5** installed.

Install PyQt5 using pip:
```bash
pip install PyQt5
```

Then simply run:
```bash
python minesweeper_gui.py
```

## Running the Core (Text-based) Version

The core version is interactive in the terminal:
```bash
python minesweeper_core.py
```
Follow the on-screen instructions:
- Flag a cell: F[A0]
- Unflag a cell: U[A0]
- Click a cell: C[A0]