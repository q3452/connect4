#!/usr/bin/env python3
from c4lib.board import Board
from c4lib.randomBot import RandomBot
#from lib.randomBot import *

print("\nConnect 4 by Quentin Serrurier\n")
# We instantiate the board and then invite players to play on it
board = Board()
randomBot1 = RandomBot(1, board)
randomBot2 = RandomBot(2, board)

while (board.winState==0):
    randomBot1.makeMove()
    if (board.winState!=0): break
    randomBot2.makeMove()
if (board.winState>0):
    (winningRow, winningCol) = board.winningMove
    print(" Player {} wins by playing col: {}, row: {} for a {} line.".format(board.winState, winningCol+1, winningRow+1, board.winningMoveType))
elif (board.winState==-1): print("The game has tied")

board.renderBoard()


# columns are zero based
# board.makeMove(1, 5)
# board.makeMove(2, 5)
# board.makeMove(1, 5)
# board.makeMove(2, 3)
# board.makeMove(1, 4)
# board.makeMove(2, 3)
# board.makeMove(1, 4)
# board.makeMove(2, 4)
# board.makeMove(1, 4)
# board.makeMove(2, 3)
# board.makeMove(1, 3)
# board.makeMove(2, 2)
# board.makeMove(1, 3)
# board.makeMove(2, 4)
# board.makeMove(1, 3)
# board.makeMove(2, 4)
# board.makeMove(1, 2)
# board.makeMove(2, 2)
# board.makeMove(1, 1)
# board.makeMove(2, 2)
# board.makeMove(1, 0)
# board.makeMove(2, 1)
# board.makeMove(1, 1)
# board.makeMove(2, 6)
# board.makeMove(1, 6)
#board.setDebug(True)
#print(board.getLegalMoves())

# print("Playing {} in column {}".format(playerNum, colNum+1))
# print("board: ")