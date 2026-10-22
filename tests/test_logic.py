"""Automated checks for the game rules and Minimax AI."""

import unittest

from tic_tac_toe.logic import (
    find_best_move,
    get_available_moves,
    get_winner,
    get_winning_line,
    is_draw,
)


class GameLogicTests(unittest.TestCase):
    def test_detects_horizontal_winner_and_line(self) -> None:
        board = ["X", "X", "X", "O", None, "O", None, None, None]
        self.assertEqual(get_winner(board), "X")
        self.assertEqual(get_winning_line(board), (0, 1, 2))

    def test_detects_diagonal_winner(self) -> None:
        board = ["O", "X", "X", "X", "O", None, None, None, "O"]
        self.assertEqual(get_winner(board), "O")
        self.assertEqual(get_winning_line(board), (0, 4, 8))

    def test_detects_draw(self) -> None:
        board = ["X", "O", "X", "X", "O", "O", "O", "X", "X"]
        self.assertIsNone(get_winner(board))
        self.assertTrue(is_draw(board))

    def test_returns_available_cells(self) -> None:
        board = ["X", None, "O", None, "X", None, "O", None, None]
        self.assertEqual(get_available_moves(board), (8, 1, 3, 5, 7))

    def test_ai_takes_a_winning_move(self) -> None:
        board = ["O", "O", None, "X", "X", None, None, None, None]
        self.assertEqual(find_best_move(board), 2)

    def test_ai_blocks_a_human_winning_move(self) -> None:
        board = ["X", "X", None, "O", None, None, None, None, None]
        self.assertEqual(find_best_move(board), 2)

    def test_ai_does_not_modify_the_input_board(self) -> None:
        board = ["X", None, None, None, "O", None, None, None, None]
        original = list(board)
        find_best_move(board)
        self.assertEqual(board, original)

    def test_ai_returns_none_when_game_is_over(self) -> None:
        won = ["X", "X", "X", "O", "O", None, None, None, None]
        full_draw = ["X", "O", "X", "X", "O", "O", "O", "X", "X"]
        self.assertIsNone(find_best_move(won))
        self.assertIsNone(find_best_move(full_draw))

    def test_rejects_invalid_boards_and_marks(self) -> None:
        with self.assertRaises(ValueError):
            get_winner([None, None])
        with self.assertRaises(ValueError):
            find_best_move([None] * 8 + ["Z"])
        with self.assertRaises(ValueError):
            find_best_move([None] * 9, ai_mark="X", human_mark="X")


if __name__ == "__main__":
    unittest.main()
