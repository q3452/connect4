#!/usr/bin/env python3
from c4lib.board import *
#from lib.randomBot import *

print("\nConnect 4 by Quentin Serrurier")
board = Board()



# columns are zero based
board.makeMove(1, 5)
board.makeMove(2, 5)
board.makeMove(1, 5)
board.makeMove(1, 4)
board.makeMove(1, 4)
board.makeMove(2, 4)
board.makeMove(1, 4)
board.makeMove(2, 3)
board.makeMove(2, 3)
board.makeMove(2, 3)
board.makeMove(1, 3)
board.makeMove(1, 3)
board.makeMove(2, 2)
board.makeMove(1, 2)
board.makeMove(2, 2)
board.makeMove(2, 2)
board.makeMove(2, 1)
board.makeMove(1, 1)
board.makeMove(1, 1)
board.makeMove(1, 0)
board.makeMove(2, 4)
board.makeMove(1, 6)
board.makeMove(1, 6)
board.makeMove(1, 4)
board.renderBoard()


# print("Playing {} in column {}".format(playerNum, colNum+1))
# print("board: ")