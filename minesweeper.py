import random

from itertools import product
class GameBoard:
    def __init__(self):
        self._board = [(" +---------+"),
        (" |ABCDEFGHI|"),
        (" +---------+"),
        [("0|"),(" "),(" "),(" "),(" "),(" "),(" "),(" "),(" "),(" "),("|")],
        [("1|"),(" "),(" "),(" "),(" "),(" "),(" "),(" "),(" "),(" "),("|")],
        [("2|"),(" "),(" "),(" "),(" "),(" "),(" "),(" "),(" "),(" "),("|")],
        [("3|"),(" "),(" "),(" "),(" "),(" "),(" "),(" "),(" "),(" "),("|")],
        [("4|"),(" "),(" "),(" "),(" "),(" "),(" "),(" "),(" "),(" "),("|")],
        [("5|"),(" "),(" "),(" "),(" "),(" "),(" "),(" "),(" "),(" "),("|")],
        [("6|"),(" "),(" "),(" "),(" "),(" "),(" "),(" "),(" "),(" "),("|")],
        [("7|"),(" "),(" "),(" "),(" "),(" "),(" "),(" "),(" "),(" "),("|")],
        [("8|"),(" "),(" "),(" "),(" "),(" "),(" "),(" "),(" "),(" "),("|")],
        (" +---------+")
        ]
        self._counter = 0

    @property
    def board(self):
        return self._board

    @property
    def counter(self):
        return self._counter

    def flag(self, cell):
        cord2 = CHAR_TO_NUM_MAPPING[cell[0]]
        cord1 = int(cell[1]) + 3
        self._board[cord1][cord2] = 'F'

    def unflag(self, cell):
        cord2 = CHAR_TO_NUM_MAPPING[cell[0]]
        cord1 = int(cell[1]) + 3
        self._board[cord1][cord2] = ' '
    
    def setMine(self, cord1, cord2):
        self._board[cord1][cord2] = 'M'

    def setNumber(self, cord1, cord2, num):
        self._board[cord1][cord2] = num

    def start(self, cell, numboard): 
        cord1 = int(cell[1]) + Y_OFFSET
        cord2 = CHAR_TO_NUM_MAPPING[cell[0]]

        self.set_island(cord1, cord2, numboard)

    def set_island(self, cord1, cord2, numboard):
        self._board[cord1][cord2] = '-'

        neighboursList = find_neighbours((cord1, cord2))
        for n in neighboursList:
            if numboard[n[0]][n[1]] == ' ':
                self._board[n[0]][n[1]] = '-'
                self._counter += 1

                for new_n in find_neighbours((n[0], n[1])):
                    if new_n not in neighboursList:
                        neighboursList.append(new_n)
            else:
                if self._board[n[0]][n[1]] == ' ':
                    self._board[n[0]][n[1] ] = numboard[n[0]][n[1]]
                    self._counter += 1

    # click ends the game if a mine is clicked. Otherwise sets the tile as the number clicked,
    # or if a blank tile is clicked, reveals the island of blank tiles.
    def click(self, cell, mineBoard, numBoard):
        cord1 = int(cell[1]) + Y_OFFSET
        cord2 = CHAR_TO_NUM_MAPPING[cell[0]]

        if mineBoard[cord1][cord2] == 'M':
            self._board[cord1][cord2] = mineBoard[cord1][cord2]

            return False

        if self._board[cord1][cord2] != ' ':
            # TODO why have u clicked here. show error

            return True
        
        if numBoard.board[cord1][cord2] != ' ':
            self._board[cord1][cord2] = numBoard.board[cord1][cord2]
            self._counter += 1

            return True
        
        self.set_island(cord1, cord2, numBoard)

        return True

def displayBoard(board):
    for i in board:
            if isinstance(i, str):
                print(i)
            else:
                print(''.join(i))

CHAR_TO_NUM_MAPPING = {'A':1,'B':2,'C':3,'D':4,'E':5,'F':6,'G':7,'H':8,'I':9}

# set_mine_board initates the mine board. Ensures that the first cell clicked and its neighbours are not mines.
def set_mine_board(cell):
    cord1 = int(cell[1]) + Y_OFFSET
    cord2 = CHAR_TO_NUM_MAPPING[cell[0]]

    mine_board = GameBoard()

    combinations = find_neighbours((cord1, cord2))
    combinations.append((cord1, cord2))

    for _ in range(10):
        while True:
            c1 = random.choice(X_INDEXES)
            c2 = random.choice(Y_INDEXES)
            if (c1,c2) not in combinations:
                combinations.append((c1,c2))
                break

        mine_board.setMine(c1, c2)
    
    return mine_board.board

X_INDEXES = [3,4,5,6,7,8,9,10,11]
Y_INDEXES = [1,2,3,4,5,6,7,8,9]
Y_OFFSET = 3

def numbers(mine_board):
    num_board = GameBoard()

    for x in X_INDEXES:
        for y in Y_INDEXES:
            if mine_board[x][y] == 'M':
                continue

            num_mines = 0
            neighbours = find_neighbours((x,y))
            for n in neighbours:
                if mine_board[n[0]][n[1]] == 'M':
                    num_mines+=1

            if num_mines > 0:
                num_board.setNumber(x, y, str(num_mines))

    return num_board

# finds the valid neighbours of a tile (excluding tiles out of bounds)
def find_neighbours(t):
    x, y = t
    potential = [(i, j) for i in range(x - 1, x + 2) for j in range(y - 1, y + 2)]
    potential.remove((x, y))

    neighbours = [
        (i, j)
        for i, j in potential
        if i in X_INDEXES and j in Y_INDEXES
    ]

    return neighbours

def coordinateCheck(cord):
    try:
        if cord[0] in ['A','B','C','D','E','F','G','H','I'] and int(cord[1]) in range(0, 9) and len(cord) == 2:
            return True
        else:
              print("[error] please enter in the format 'A2'")
              return False
    except:
        print("[error] please enter in the format 'A2'")
        return False

def inputChecker(input):
    try:
        if input[0] in ['F','U','C'] and input[2] in ['A','B','C','D','E','F','G','H','I'] and int(input[3]) in range(0, 9) and len(input) == 5:
            return True
        else:
            print("[error] please enter in the format 'F[A2]'")
            return False
    except:
        return False

def beginGame(gameBoard):
    displayBoard(gameBoard.board)

    startCord = input("----> Please enter your first coordinate: ")
    while coordinateCheck(startCord) != True:
        startCord = input("----> Please enter your first coordinate: ")
        coordinateCheck(startCord)

    minesBoard = set_mine_board(startCord)
    numboard = numbers(minesBoard)
    gameBoard.start(startCord,numboard.board)

    displayBoard(gameBoard.board)

    return minesBoard, numboard

def turn(gameBoard, minesBoard, numboard):
    result = True
    userInput = input("----> Please enter your move: ")
    while inputChecker(userInput) != True:
        userInput = input("----> Please enter your move: ")
        inputChecker(userInput)

    print(userInput[2:4])
    if userInput[0] == 'F':
        gameBoard.flag(userInput[2:4])
    elif userInput[0] == 'U':
        gameBoard.unflag(userInput[2:4])
    else:
        result = gameBoard.click(userInput[2:4], minesBoard, numboard)

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
    gameBoard = GameBoard()
    
    minesBoard, numBoard = beginGame(gameBoard)
    ## displayBoard(minesBoard)
    displayBoard(gameBoard.board)
    print(gameBoard.counter)
    
    while True:
        result = turn(gameBoard, minesBoard, numBoard)
        displayBoard(gameBoard.board)
        if result == False:
            print('Game Over')
            break
        elif gameBoard.counter == 71:
            print('you win!!')
            break
        
        
        