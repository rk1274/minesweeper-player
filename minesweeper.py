import random

CHAR_TO_NUM_MAPPING = {'A':0,'B':1,'C':2,'D':3,'E':4,'F':5,'G':6,'H':7,'I':8}
GRID_SIZE = 9
FLAG_CELL = 'F'
MINE_CELL = 'M'
EMPTY_CELL = ' '
PLAIN_CELL = '-'

class GameBoard:
    def __init__(self):
        self._board = [[EMPTY_CELL for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self._counter = 0

    @property
    def board(self):
        return self._board

    @property
    def counter(self):
        return self._counter

    def flag(self, cell):
        row, col = get_cords_from_cell(cell)
        self._board[row][col] = FLAG_CELL

    def unflag(self, cell):
        row, col = get_cords_from_cell(cell)
        if self._board[row][col] == FLAG_CELL:
            self._board[row][col] = EMPTY_CELL
    
    def setMine(self, row, col):
        self._board[row][col] = MINE_CELL

    def setNumber(self, row, col, num):
        self._board[row][col] = num

    def start(self, cell, numboard): 
        row, col = get_cords_from_cell(cell)
        self.set_island(row, col, numboard)

    def set_island(self, row, col, numboard):
        self._board[row][col] = PLAIN_CELL

        neighboursList = find_neighbours((row, col))
        for n in neighboursList:
            if numboard[n[0]][n[1]] == EMPTY_CELL:
                self._board[n[0]][n[1]] = PLAIN_CELL
                self._counter += 1

                for new_n in find_neighbours((n[0], n[1])):
                    if new_n not in neighboursList:
                        neighboursList.append(new_n)
            else:
                if self._board[n[0]][n[1]] == EMPTY_CELL:
                    self._board[n[0]][n[1]] = numboard[n[0]][n[1]]
                    self._counter += 1

    def click(self, cell, mineBoard, numBoard):
        row, col = get_cords_from_cell(cell)

        if mineBoard[row][col] == MINE_CELL:
            self._board[row][col] = MINE_CELL
            return False

        if self._board[row][col] != EMPTY_CELL:
            return True
        
        if numBoard.board[row][col] != EMPTY_CELL:
            self._board[row][col] = numBoard.board[row][col]
            self._counter += 1
            return True
        
        self.set_island(row, col, numBoard.board)
        return True

def display_board(board):
    print("   " + " ".join("ABCDEFGHI"))
    print("  +" + "-" * 17 + "+")

    for i, row in enumerate(board):
        print(f"{i} |" + " ".join(row) + "|")
        
    print("  +" + "-" * 17 + "+")

def get_cords_from_cell(cell):
    col = CHAR_TO_NUM_MAPPING[cell[0].upper()]
    row = int(cell[1])
    return row, col

def set_mine_board(cell):
    row, col = get_cords_from_cell(cell)
    mine_board = GameBoard()

    combinations = find_neighbours((row, col))
    combinations.append((row, col))

    for _ in range(10):
        while True:
            r = random.randint(0, 8)
            c = random.randint(0, 8)
            if (r, c) not in combinations:
                combinations.append((r, c))
                break

        mine_board.setMine(r, c)
    
    return mine_board.board
 
def set_num_board(mine_board):
    num_board = GameBoard()

    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            if mine_board[x][y] == MINE_CELL:
                continue

            num_nearby_mines = 0
            neighbours = find_neighbours((x, y))
            for n in neighbours:
                if mine_board[n[0]][n[1]] == MINE_CELL:
                    num_nearby_mines += 1

            if num_nearby_mines > 0:
                num_board.setNumber(x, y, str(num_nearby_mines))

    return num_board

def find_neighbours(pos):
    """Return all valid neighbouring (row, col) positions around a given cell."""
    row, col = pos
    neighbours = []

    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0:
                continue  # skip the cell itself

            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < GRID_SIZE and 0 <= new_col < GRID_SIZE:
                neighbours.append((new_row, new_col))

    return neighbours

def coordinateCheck(cord):
    try:
        if cord[0].upper() in CHAR_TO_NUM_MAPPING and int(cord[1]) in range(0, 9) and len(cord) == 2:
            return True
        else:
            print("[error] please enter in the format 'A2'")
            return False
    except:
        print("[error] please enter in the format 'A2'")
        return False

def inputChecker(input):
    try:
        if input[0] in ['F','U','C'] and input[2].upper() in CHAR_TO_NUM_MAPPING and int(input[3]) in range(0, 9) and len(input) == 5:
            return True
        else:
            print("[error] please enter in the format 'F[A2]'")
            return False
    except:
        return False

def begin_game(game_board):
    display_board(game_board.board)
    start_cord = input("----> Please enter your first coordinate: ")
    while coordinateCheck(start_cord) != True:
        start_cord = input("----> Please enter your first coordinate: ")
        coordinateCheck(start_cord)

    mine_board = set_mine_board(start_cord)
    num_board = set_num_board(mine_board)
    game_board.start(start_cord, num_board.board)

    display_board(game_board.board)
    return mine_board, num_board

def turn(game_board, mine_board, num_board):
    result = True
    user_input = input("----> Please enter your move: ")
    while inputChecker(user_input) != True:
        user_input = input("----> Please enter your move: ")
        inputChecker(user_input)

    print(user_input[2:4])
    if user_input[0] == 'F':
        game_board.flag(user_input[2:4])
    elif user_input[0] == 'U':
        game_board.unflag(user_input[2:4])
    else:
        result = game_board.click(user_input[2:4], mine_board, num_board)

    return result

if __name__ == "__main__":
    print('''
    +========================+
    | WELCOME TO MINESWEEPER |
    +========================+
    | the aim of this game   |
    | is to flag all the     |
    | mines and clear all    |
    | safe tiles!!           |
    +========================+
    | to flag a cell:        |
    |   F[A0]                |
    | to unflag a cell:      |
    |   U[A0]                |
    | to click a cell:       | 
    |   C[A0]                |
    +========================+
    
    +========================+
    |      GOOD LUCK !       |
    +========================+
       ''')
    game_board = GameBoard()
    
    mines_board, num_board = begin_game(game_board)
    display_board(game_board.board)
    print(game_board.counter)
    
    while True:
        result = turn(game_board, mines_board, num_board)
        display_board(game_board.board)

        if result == False:
            print('Game Over')
            break

        if game_board.counter == 71:
            print('you win!!')
            break
