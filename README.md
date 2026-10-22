# Tic-Tac-Toe with Simple AI

A small, beginner-friendly Python game for a human player to play Tic-Tac-Toe against the computer. The interface is built with Tkinter, which is included with most standard Python installations. The project has no third-party dependencies.

## Features

- Play as **X** against the computer as **O**.
- The computer uses Minimax to choose a move and will not lose when it plays correctly.
- The game detects wins and draws, and highlights the winning row.
- **New game** starts another round and keeps the score. **Reset score** clears the score and starts a new round.
- Moves are checked before they are accepted, so a filled square cannot be played again and a finished round cannot be changed.
- The code separates the game rules, user interface, and automated checks.

## Project structure

```text
tic_tac_toe_ai/
├── main.py                  # Starts the application
├── README.md                # Setup, instructions, and project notes
├── tic_tac_toe/
│   ├── __init__.py
│   ├── logic.py              # Rules, board checks, and Minimax AI
│   └── ui.py                 # Tkinter window and controls
└── tests/
    └── test_logic.py         # Checks for rules and AI decisions
```

There is no `requirements.txt` because the project only uses Python's standard library.

## Requirements

- Python 3.10 or newer
- A Python installation that includes Tkinter

## Run the game

1. Open the `tic_tac_toe_ai` folder in Visual Studio Code.
2. If prompted, install Microsoft's **Python** extension and choose a Python interpreter (Python 3.10 or newer).
3. Open `main.py` and select **Run Python File** in the top-right corner.

You can also open VS Code's integrated terminal in this folder and run:

```text
python main.py
```

On some Windows installations, use `py main.py` if the `python` command is not available. On macOS or Linux, use `python3 main.py` if needed.

Click any empty square to place **X**. The computer will respond as **O**. Choose **New game** to play another round.

## Run the checks

From the project folder, run:

```text
python -m unittest discover -s tests -v
```

## How the AI works

Minimax looks ahead at the possible moves until it reaches a win, loss, or draw. It treats the computer's turns as choices that should improve its result and the human's turns as choices that try to make the computer's result worse. It assigns scores to those outcomes and picks the move with the best score. Tic-Tac-Toe has a small board, so the computer can check every possible continuation quickly. This is a search algorithm, not a trained machine-learning model.

## Main files

- **`main.py`** — the file to run to open the game.
- **`tic_tac_toe/ui.py`** — the window, board, score display, and buttons.
- **`tic_tac_toe/logic.py`** — win/draw checks and the computer's Minimax strategy.
- **`tests/test_logic.py`** — automated checks for the rules and AI.
