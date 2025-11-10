from minesweeper_core import (
    GameBoard, NUM_SAFE_TILES, GRID_SIZE,
    EMPTY_CELL, FLAG_CELL, MINE_CELL,
    set_mine_board, set_num_board
)
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QMessageBox
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import sys

class CellButton(QPushButton):
    def __init__(self, row, col, parent):
        super().__init__()
        self.row = row
        self.col = col
        self.parent = parent
        self.setFixedSize(40, 40)
        self.setFont(QFont("Roboto", 14, QFont.Bold))
        self.setStyleSheet("""         
            QPushButton#empty1 {
                background-color: #dbe0f5;
                border: none;
                font-weight: bold;
            }
            QPushButton#empty1:hover {
                background-color: #cbd3f1;
            }
                           
            QPushButton#empty2 {
                background-color: #bcc5ed;
                border: none;
                font-weight: bold;
            }
            QPushButton#empty2:hover {
                background-color: #acb8e9;
            }
                           
            QPushButton#revealed1 {
                background-color: #eecfc0;
                border: none;
                font-weight: bold;
            }
                           
            QPushButton#revealed2 {
                background-color: #e9bfac;
                border: none;
                font-weight: bold;
            }
                           
            QPushButton#mine {
                background-color: #E06B80;
                border: none;
                font-weight: bold;
            }
        """)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.parent.on_left_click(self.row, self.col)
        elif event.button() == Qt.RightButton:
            self.parent.on_right_click(self.row, self.col)

class MinesweeperGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Minesweeper")
        self.setFixedSize(360, 360)

        self.game_board = GameBoard()
        self.first_click = True
        self.mine_board = None
        self.num_board = None

        self.layout = QGridLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        self.buttons = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                btn = CellButton(i, j, self)
                if (i + j) % 2 == 0:
                    btn.setObjectName("empty1")
                else:
                    btn.setObjectName("empty2")

                btn.style().unpolish(btn)
                btn.style().polish(btn)
                self.layout.addWidget(btn, i, j)
                self.buttons[i][j] = btn

    def on_left_click(self, row, col):
        if self.first_click:
            cell = f"{chr(ord('A')+col)}{row}"
            self.mine_board = set_mine_board(cell)
            self.num_board = set_num_board(self.mine_board)
            self.game_board.start(cell, self.num_board.board)
            self.first_click = False

        result = self.game_board.click(row, col, self.mine_board, self.num_board)
        self.update_buttons()

        if not result:
            self.reveal_mines()
            msg = QMessageBox(self)
            msg.setWindowTitle("Game Over")
            msg.setText("You clicked on a mine! Game Over.")
            msg.setIcon(QMessageBox.NoIcon)  # No sound icon
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            self.reset_game()
        elif self.game_board.counter == NUM_SAFE_TILES:
            self.reveal_mines()
            msg = QMessageBox(self)
            msg.setWindowTitle("You Win!")
            msg.setText("Congratulations! You cleared all safe tiles!")
            msg.setIcon(QMessageBox.NoIcon)  # No sound
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            self.reset_game()

    def on_right_click(self, row, col):
        val = self.game_board.board[row][col]
        if val == FLAG_CELL:
            self.game_board.unflag(row, col)
        elif val == EMPTY_CELL:
            self.game_board.flag(row, col)
        self.update_buttons()

    def update_buttons(self):
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                val = self.game_board.board[i][j]
                btn = self.buttons[i][j]
                if val == EMPTY_CELL:
                    btn.setText("")
                    if (i + j) % 2 == 0:
                        btn.setObjectName("empty1")
                    else:
                        btn.setObjectName("empty2")
                elif val == FLAG_CELL:
                    btn.setText("🚩")
                    # btn.setObjectName("flag")
                elif val == MINE_CELL:
                    btn.setText("M")
                    btn.setObjectName("mine")
                else:
                    btn.setText(str(val))
                    if (i + j) % 2 == 0:
                        btn.setObjectName("revealed1")
                    else:
                        btn.setObjectName("revealed2")

                btn.style().unpolish(btn)
                btn.style().polish(btn)

    def reveal_mines(self):
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if self.mine_board[i][j] == MINE_CELL:
                    self.game_board.board[i][j] = MINE_CELL
        self.update_buttons()

    def reset_game(self):
        self.game_board = GameBoard()
        self.first_click = True
        self.mine_board = None
        self.num_board = None
        self.update_buttons()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MinesweeperGUI()
    window.show()
    sys.exit(app.exec_())
