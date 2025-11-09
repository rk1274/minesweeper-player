import unittest
from minesweeper import GameBoard, coordinateCheck, inputChecker, numbers, set_mine_board, CHAR_TO_NUM_MAPPING

class TestMinesweeper(unittest.TestCase):
    def setUp(self):
        self.game = GameBoard()

    def test_flag_and_unflag(self):
        self.game.flag("A0")
        self.assertEqual(self.game.board[3][1], "F")
        self.game.unflag("A0")
        self.assertEqual(self.game.board[3][1], " ")

    def test_set_mine(self):
        self.game.setMine(3, 1)
        self.assertEqual(self.game.board[3][1], "M")

    def test_set_number(self):
        self.game.setNumber(3, 1, "2")
        self.assertEqual(self.game.board[3][1], "2")

    def test_coordinate_check_valid(self):
        self.assertTrue(coordinateCheck("A0"))
        self.assertTrue(coordinateCheck("I8"))

    def test_coordinate_check_invalid(self):
        self.assertFalse(coordinateCheck("J0"))
        self.assertFalse(coordinateCheck("A9"))
        self.assertFalse(coordinateCheck("AA"))
        self.assertFalse(coordinateCheck(""))

    def test_input_checker_valid(self):
        self.assertTrue(inputChecker("F[A0]"))
        self.assertTrue(inputChecker("U[I8]"))
        self.assertTrue(inputChecker("C[B3]"))

    def test_input_checker_invalid(self):
        self.assertFalse(inputChecker("Z[A0]"))
        self.assertFalse(inputChecker("F[J0]"))
        self.assertFalse(inputChecker("C[A9]"))
        self.assertFalse(inputChecker("F[A00]"))

    def test_numbers_no_mines(self):
        board = self.game.board
        mines = GameBoard().board
        numboard = numbers(self.game, mines)
        # No mines means all empty (no numbers)
        found_numbers = any(
            isinstance(row, list) and any(cell.isdigit() for cell in row)
            for row in numboard.board
        )
        self.assertFalse(found_numbers)

    def test_mineBoard_generates_mines(self):
        mines = set_mine_board("A0")
        mine_count = sum(
            1 for row in mines if isinstance(row, list) for cell in row if cell == "M"
        )
        self.assertEqual(mine_count, 10)  # always generates 10 mines

    def test_click_on_mine_returns_false(self):
        mines = GameBoard()
        mines.setMine(3, 1)
        numBoard = GameBoard()
        result = self.game.click("A0", mines.board, numBoard)
        self.assertFalse(result)

    def test_click_on_safe_returns_true(self):
        numBoard = GameBoard()
        numBoard.setNumber(3, 1, "1")
        mines = GameBoard()
        result = self.game.click("A0", mines.board, numBoard)
        self.assertTrue(result)
        self.assertEqual(self.game.board[3][1], "1")

if __name__ == "__main__":
    unittest.main()
