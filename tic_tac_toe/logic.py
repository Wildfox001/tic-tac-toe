"""Game rules and a small Minimax AI for Tic-Tac-Toe."""

from collections.abc import Sequence
from math import inf
from typing import Final

Mark = str | None

WINNING_LINES: Final[tuple[tuple[int, int, int], ...]] = (
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
)

# Center and corners are checked first when equally good moves are available.
MOVE_ORDER: Final[tuple[int, ...]] = (4, 0, 2, 6, 8, 1, 3, 5, 7)


def _validate_board(board: Sequence[Mark]) -> None:
    """Raise a clear error if a board does not contain nine valid cells."""
    if len(board) != 9:
        raise ValueError("A Tic-Tac-Toe board must contain exactly 9 cells.")
    if any(cell not in (None, "X", "O") for cell in board):
        raise ValueError('Each cell must contain None, "X", or "O".')


def get_winner(board: Sequence[Mark]) -> str | None:
    """Return the winning mark, or None when there is no winner yet."""
    _validate_board(board)
    for first, second, third in WINNING_LINES:
        mark = board[first]
        if mark is not None and mark == board[second] == board[third]:
            return mark
    return None


def get_winning_line(board: Sequence[Mark]) -> tuple[int, int, int] | None:
    """Return the three winning cell indexes, if a player has won."""
    _validate_board(board)
    for line in WINNING_LINES:
        first, second, third = line
        mark = board[first]
        if mark is not None and mark == board[second] == board[third]:
            return line
    return None


def get_available_moves(board: Sequence[Mark]) -> tuple[int, ...]:
    """Return the indexes of empty cells in the preferred move order."""
    _validate_board(board)
    return tuple(index for index in MOVE_ORDER if board[index] is None)


def is_draw(board: Sequence[Mark]) -> bool:
    """Return True when the board is full and nobody has won."""
    _validate_board(board)
    return get_winner(board) is None and all(cell is not None for cell in board)


def find_best_move(
    board: Sequence[Mark], ai_mark: str = "O", human_mark: str = "X"
) -> int | None:
    """Choose the AI's best legal move using the Minimax algorithm.

    The search checks every possible continuation. It gives the AI a higher
    score for a quick win and prefers delaying a loss when a draw is impossible.
    The input board is copied, so this function never changes the caller's board.
    """
    _validate_board(board)
    if ai_mark not in ("X", "O") or human_mark not in ("X", "O"):
        raise ValueError('Player marks must be "X" or "O".')
    if ai_mark == human_mark:
        raise ValueError("The AI and human must use different marks.")

    if get_winner(board) is not None:
        return None

    working_board = list(board)
    available_moves = get_available_moves(working_board)
    if not available_moves:
        return None

    def score_position(is_ai_turn: bool, depth: int) -> int:
        winner = get_winner(working_board)
        if winner == ai_mark:
            return 10 - depth
        if winner == human_mark:
            return depth - 10
        if all(cell is not None for cell in working_board):
            return 0

        if is_ai_turn:
            best_score = -inf
            for move in get_available_moves(working_board):
                working_board[move] = ai_mark
                score = score_position(False, depth + 1)
                working_board[move] = None
                best_score = max(best_score, score)
            return int(best_score)

        best_score = inf
        for move in get_available_moves(working_board):
            working_board[move] = human_mark
            score = score_position(True, depth + 1)
            working_board[move] = None
            best_score = min(best_score, score)
        return int(best_score)

    best_move: int | None = None
    best_score = -inf
    for move in available_moves:
        working_board[move] = ai_mark
        score = score_position(False, 1)
        working_board[move] = None
        if score > best_score:
            best_score = score
            best_move = move

    return best_move
