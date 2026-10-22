"""Start the Tic-Tac-Toe game."""

import tkinter as tk

from tic_tac_toe.ui import TicTacToeApp


def main() -> None:
    """Create the application window and start Tkinter's event loop."""
    root = tk.Tk()
    TicTacToeApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
