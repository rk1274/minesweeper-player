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
        cord2 = d[cell[0]]
        cord1 = int(cell[1]) + 3
        self._board[cord1][cord2] = 'F'

    def unflag(self, cell):
        cord2 = d[cell[0]]
        cord1 = int(cell[1]) + 3
        self._board[cord1][cord2] = ' '
    
    def setMine(self, cord1, cord2):
        self._board[cord1][cord2] = 'M'

    def setNumber(self, cord1, cord2, num):
        self._board[cord1][cord2] = num

    def start(self, cell, numboard): 
        cord2 = d[cell[0]] - 1
        cord1 = int(cell[1])
        self._board[cord1 + 3][cord2 + 1] = '-'


        neighboursList = neighbours(cord1, cord2)
        for i in neighboursList:
            if numboard[i[0] + 3][i[1] + 1] == ' ':
                self._board[i[0] + 3][i[1] + 1] = '-'
                self._counter += 1
                for j in neighbours(i[0], i[1]):
                    if j not in neighboursList:
                        neighboursList.append(j)
            else:
                if self._board[i[0] + 3][i[1] + 1] == ' ':
                    self._board[i[0] + 3][i[1] + 1] = numboard[i[0] + 3][i[1] + 1]
                    self._counter += 1


    def click(self, cell, mineBoard, numBoard):
        cord1 = int(cell[1]) + 3
        cord2 = d[cell[0]]
        if mineBoard[cord1][cord2] == 'M':
            self._board[cord1][cord2] = mineBoard[cord1][cord2]
            return False
        elif self._board[cord1][cord2] != ' ':
            return 
        elif numBoard.board[cord1][cord2] != ' ':
            self._board[cord1][cord2] = numBoard.board[cord1][cord2]
            self._counter += 1
            return True
        else:
            cord2 = d[cell[0]] - 1
            cord1 = int(cell[1])
            self._board[cord1 + 3][cord2 + 1] = '-'


            neighboursList = neighbours(cord1, cord2)
            for i in neighboursList:
                if numBoard.board[i[0] + 3][i[1] + 1] == ' ':
                    self._board[i[0] + 3][i[1] + 1] = '-'
                    self._counter += 1
                    for j in neighbours(i[0], i[1]):
                        if j not in neighboursList:
                            neighboursList.append(j)
                else:
                    if self._board[i[0] + 3][i[1] + 1] == ' ':
                        self._board[i[0] + 3][i[1] + 1] = numBoard.board[i[0] + 3][i[1] + 1]
                        self._counter += 1
                

            return True


X = 9
Y = 9
neighbours = lambda x, y : [(x2, y2) for x2 in range(x-1, x+2)
                               for y2 in range(y-1, y+2)
                               if (-1 < x <= X and
                                   -1 < y <= Y and
                                   (x != x2 or y != y2) and
                                   (0 <= x2 <= X) and
                                   (0 <= y2 <= Y))]

def displayBoard(board):
    for i in board:
            if isinstance(i, str):
                print(i)
            else:
                print(''.join(i))

d = {'A':1,'B':2,'C':3,'D':4,'E':5,'F':6,'G':7,'H':8,'I':9}

#initates the mine board
def mineBoard(cell):
    cord1 = int(cell[1]) + 3
    cord2 = d[cell[0]]

    mines = GameBoard()
    c1List = [3,4,5,6,7,8,9,10,11]
    c2List = [1,2,3,4,5,6,7,8,9]

    combinations = [[cord1,cord2]]

    for i in neighbours(cord1 -3, cord2-1):
        combinations.append([i[0]+3, i[1]+1])

    for i in range(10):
        while True:
            c1 = random.choice(c1List)
            c2 = random.choice(c2List)
            if [c1,c2] not in combinations:
                combinations.append([c1,c2])
                break
        mines.setMine(c1, c2)
    
    #displayBoard(mines.board)
    return mines.board

def numbers(board,mineBoard):

    numBoard = GameBoard()
    c1List = [3,4,5,6,7,8,9,10,11]
    c2List = [1,2,3,4,5,6,7,8,9]
    number = 0
    for i in c1List:
        for j in c2List:
            if mineBoard[i][j] != 'M':
                
                if mineBoard[i-1][j-1] == 'M':
                    number+=1
                if mineBoard[i-1][j] == 'M':
                    number+=1
                if mineBoard[i-1][j+1] == 'M':
                    number+=1
                if mineBoard[i][j-1] == 'M':
                    number+=1
                if mineBoard[i][j+1] == 'M':
                    number+=1
                if mineBoard[i+1][j-1] == 'M':
                    number+=1
                if mineBoard[i+1][j] == 'M':
                    number+=1
                if mineBoard[i+1][j+1] == 'M':
                    number+=1

                if number > 0:
                   numBoard.setNumber(i,j,str(number))
                number=0

    ##displayBoard(numBoard.board)
    return numBoard

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

    minesBoard = mineBoard(startCord)
    numboard = numbers(gameBoard,minesBoard)
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


