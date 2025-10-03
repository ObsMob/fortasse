# Bomb-Boinger
a simple CLI terminal Minesweeper clone

## Usage: 
1. Download or clone the project.
2. Activate a Virtual Environment. ```"python -m venv venv"``` & ```"source venv/bin/activate" or "venv\Scripts\activate"```
3. Ensure Dependancies are installed ```"pip install -r requirements.txt"``` 
3. Run main.py, e.g. ```"python3 main.py"```

## Dependancies:
- Python-SAT v1.8

## Features:
- Some gameplay options, such as *"Corners Touch = True"* and win tracking.
- Uses Unicode emojis for tile display. 💣🚩
- Standard CLI prompt for navigation and game actions.
- Fully deducible boards, no guessing.

## Future Content:
1. Implementing a GUI to render shapes other than Squares.
2. Basic UI functionality like tracking an "Esc" stroke as "Back", "Quit", or *null* input.
4. More UI functionality in displaying some relevant game "options" during play for reference.
5. Add colored "sections" to the game board, again for more texture.
6. Implement WASD/arrow navigation, with toggle.

## Last Update Added:
1. Reworked Solver to prove deducible boards. Fixed multiple bugs and much more efficient!
2. Holes implemented! Creates "holes" removing random tiles from the game board.
3. Interface now uses an alt-buffer to prevent your terminal from infinite scrolling.

## Known Bugs/Issues:
- When holes is flagged True and Board sizes are relatively large >20, the solver can take an exceptionally long time to find a playable board. For now, can ```Ctrl+C``` out to reduce board size. Fix is in the works.

## Original Creator:
@Obs
http://www.github.com/ObsMob/fortasse