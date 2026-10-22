"""Tkinter user interface for the Tic-Tac-Toe game."""

import tkinter as tk

from .logic import find_best_move, get_winner, get_winning_line, is_draw

BACKGROUND = "#F3F5F9"
CARD = "#FFFFFF"
TEXT = "#1F2937"
MUTED = "#667085"
X_COLOR = "#2563EB"
O_COLOR = "#D9465F"
ACCENT = "#176B5B"
HIGHLIGHT = "#DDF3E8"
EMPTY_DISABLED = "#EDF0F5"


class TicTacToeApp:
    """Manage the board, round status, score, and computer turn."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Tic-Tac-Toe | Simple AI")
        self.root.configure(bg=BACKGROUND)
        self.root.resizable(False, False)
        self.root.geometry("430x700")

        self.board: list[str | None] = [None] * 9
        self.scores = {"X": 0, "draw": 0, "O": 0}
        self.game_over = False
        self.computer_thinking = False
        self.pending_computer_move: str | None = None
        self.buttons: list[tk.Button] = []
        self.score_labels: dict[str, tk.Label] = {}
        self.winning_cells: tuple[int, ...] = ()

        self._build_layout()
        self._render_board()
        self._update_scores()

    def _build_layout(self) -> None:
        """Create the title, score, board, and game controls."""
        card = tk.Frame(self.root, bg=CARD, padx=26, pady=24)
        card.pack(fill="both", expand=True, padx=22, pady=22)

        tk.Label(
            card,
            text="Tic-Tac-Toe",
            bg=CARD,
            fg=TEXT,
            font=("Segoe UI", 23, "bold"),
        ).pack()
        tk.Label(
            card,
            text="Play against a simple, unbeatable AI",
            bg=CARD,
            fg=MUTED,
            font=("Segoe UI", 10),
        ).pack(pady=(3, 16))

        scores = tk.Frame(card, bg=CARD)
        scores.pack(fill="x", pady=(0, 16))
        for column, (key, title) in enumerate(
            (("X", "YOU"), ("draw", "DRAWS"), ("O", "COMPUTER"))
        ):
            panel = tk.Frame(scores, bg=BACKGROUND, padx=10, pady=8)
            panel.grid(row=0, column=column, sticky="ew", padx=4)
            scores.grid_columnconfigure(column, weight=1)
            tk.Label(
                panel,
                text=title,
                bg=BACKGROUND,
                fg=MUTED,
                font=("Segoe UI", 8, "bold"),
            ).pack()
            score_label = tk.Label(
                panel,
                text="0",
                bg=BACKGROUND,
                fg=X_COLOR if key == "X" else O_COLOR if key == "O" else TEXT,
                font=("Segoe UI", 15, "bold"),
            )
            score_label.pack(pady=(2, 0))
            self.score_labels[key] = score_label

        self.status_label = tk.Label(
            card,
            text="Your turn — choose a square.",
            bg=CARD,
            fg=ACCENT,
            font=("Segoe UI", 11, "bold"),
            height=2,
        )
        self.status_label.pack(fill="x", pady=(0, 10))

        board_frame = tk.Frame(card, bg=BACKGROUND, padx=4, pady=4)
        board_frame.pack()
        for row in range(3):
            board_frame.grid_rowconfigure(row, minsize=98, weight=1)
            board_frame.grid_columnconfigure(row, minsize=98, weight=1)
        for index in range(9):
            button = tk.Button(
                board_frame,
                text=" ",
                bg=CARD,
                activebackground="#E8EEF8",
                fg=TEXT,
                activeforeground=TEXT,
                disabledforeground=TEXT,
                relief=tk.FLAT,
                borderwidth=0,
                font=("Segoe UI", 27, "bold"),
                command=lambda cell=index: self._play_human_move(cell),
            )
            button.grid(
                row=index // 3,
                column=index % 3,
                sticky="nsew",
                padx=4,
                pady=4,
            )
            self.buttons.append(button)

        controls = tk.Frame(card, bg=CARD)
        controls.pack(fill="x", pady=(18, 0))
        tk.Button(
            controls,
            text="New game",
            command=self._new_game,
            bg=ACCENT,
            activebackground="#115647",
            fg="#FFFFFF",
            activeforeground="#FFFFFF",
            relief=tk.FLAT,
            borderwidth=0,
            font=("Segoe UI", 10, "bold"),
            padx=18,
            pady=10,
            cursor="hand2",
        ).pack(side="left", expand=True, fill="x", padx=(0, 5))
        tk.Button(
            controls,
            text="Reset score",
            command=self._reset_score,
            bg=BACKGROUND,
            activebackground="#E8ECF2",
            fg=TEXT,
            activeforeground=TEXT,
            relief=tk.FLAT,
            borderwidth=0,
            font=("Segoe UI", 10, "bold"),
            padx=18,
            pady=10,
            cursor="hand2",
        ).pack(side="left", expand=True, fill="x", padx=(5, 0))

        tk.Label(
            card,
            text="You are X  •  Computer is O",
            bg=CARD,
            fg=MUTED,
            font=("Segoe UI", 9),
        ).pack(pady=(16, 0))

    def _play_human_move(self, index: int) -> None:
        """Accept a legal human move and schedule the computer's response."""
        if self.game_over or self.computer_thinking or self.board[index] is not None:
            return

        self.board[index] = "X"
        if self._check_round_end():
            return

        self.computer_thinking = True
        self.status_label.config(text="Computer is thinking…", fg=MUTED)
        self._render_board()
        self.pending_computer_move = self.root.after(250, self._play_computer_move)

    def _play_computer_move(self) -> None:
        """Choose and place the computer's best move."""
        self.pending_computer_move = None
        if self.game_over:
            return

        move = find_best_move(self.board, ai_mark="O", human_mark="X")
        if move is None:
            self.computer_thinking = False
            self._finish_round("draw")
            return

        self.board[move] = "O"
        self.computer_thinking = False
        self._render_board()
        if not self._check_round_end():
            self.status_label.config(text="Your turn — choose a square.", fg=ACCENT)

    def _check_round_end(self) -> bool:
        """Finish the round if someone has won or the board is full."""
        winner = get_winner(self.board)
        if winner is not None:
            self._finish_round(winner)
            return True
        if is_draw(self.board):
            self._finish_round("draw")
            return True
        return False

    def _finish_round(self, result: str) -> None:
        """Show the result, highlight a win, and update the score."""
        self.game_over = True
        self.computer_thinking = False
        if result in self.scores:
            self.scores[result] += 1
        line = get_winning_line(self.board)
        self.winning_cells = line or ()

        if result == "X":
            message, color = "You win! Nice game.", X_COLOR
        elif result == "O":
            message, color = "The computer wins. Try again!", O_COLOR
        else:
            message, color = "It's a draw. Start a new game to play again.", TEXT

        self.status_label.config(text=message, fg=color)
        self._update_scores()
        self._render_board()

    def _new_game(self) -> None:
        """Start a fresh round while keeping the score."""
        self._cancel_pending_move()
        self.board = [None] * 9
        self.game_over = False
        self.computer_thinking = False
        self.winning_cells = ()
        self.status_label.config(text="Your turn — choose a square.", fg=ACCENT)
        self._render_board()

    def _reset_score(self) -> None:
        """Clear the score and start a fresh round."""
        self._new_game()
        self.scores = {"X": 0, "draw": 0, "O": 0}
        self._update_scores()

    def _cancel_pending_move(self) -> None:
        """Cancel a scheduled computer move when a round is restarted."""
        if self.pending_computer_move is not None:
            self.root.after_cancel(self.pending_computer_move)
            self.pending_computer_move = None

    def _update_scores(self) -> None:
        """Refresh the three score counters."""
        for key, label in self.score_labels.items():
            label.config(text=str(self.scores[key]))

    def _render_board(self) -> None:
        """Refresh cell labels, colors, and availability after each turn."""
        for index, button in enumerate(self.buttons):
            mark = self.board[index]
            foreground = X_COLOR if mark == "X" else O_COLOR if mark == "O" else TEXT
            background = HIGHLIGHT if index in self.winning_cells else CARD
            if mark is None and self.computer_thinking:
                background = EMPTY_DISABLED
                foreground = MUTED

            disabled = self.game_over or self.computer_thinking or mark is not None
            button.config(
                text=mark or " ",
                bg=background,
                fg=foreground,
                disabledforeground=foreground,
                state=tk.DISABLED if disabled else tk.NORMAL,
            )
