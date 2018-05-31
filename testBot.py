#!/usr/bin/env python3
from c4lib.board import Board
from c4lib.randomBot import RandomBot
from c4lib.basicBot import BasicBot
from c4lib.abpBot import ABpBot
from c4lib.humanPlayer import HumanPlayer
from c4lib.colours import Colours

def getPlayOrder(playerIndex):
    if (playerIndex==0): return '1st'
    else: return '2nd'

print("\nConnect 4 by Quentin\n")
# We instantiate the board and then invite players to play on it
board = Board()
bot1 = ABpBot(1, board, 6)
bot2 = BasicBot(2, board, 2)
players = [ bot1, bot2 ]
"""
  6|_ X _ _ _ _ _ |
  5|_ 0 _ _ _ _ _ |
  4|_ X X _ X _ _ |
  3|_ X 0 X X _ _ |
  2|_ 0 0 X 0 X 0 |
  1|0 X 0 X 0 0 0 |
   ================
    0 1 2 3 4 5 6
"""

board.makeMove(1,0)
board.makeMove(2,1)
board.makeMove(1,1)
board.makeMove(2,1)
board.makeMove(2,1)
board.makeMove(1,1)
board.makeMove(2,1)
board.makeMove(1,2)
board.makeMove(1,2)
board.makeMove(1,2)
board.makeMove(2,2)
board.makeMove(2,3)
board.makeMove(2,3)
board.makeMove(2,3)
board.makeMove(1,4)
board.makeMove(1,4)
board.makeMove(2,4)
board.makeMove(2,4)
board.makeMove(1,5)
board.makeMove(1,6)
board.makeMove(1,6)
board.makeMove(2,5)
board.renderBoard()

bot1.move()
print(" Bot moved in column {}.".format(board.getLastMove()+1))
board.renderBoard()
if (board.winState>0):
    (winningRow, winningCol) = board.winningMove
    winningMoveTypeString = board.winningMoveType
    if (winningMoveTypeString[0] in 'aeiou'): winningMoveTypeString = "an "+winningMoveTypeString
    else: winningMoveTypeString="a "+winningMoveTypeString
    print(" {} playing {} ".format(players[board.winState-1].getName(), getPlayOrder(board.winState))+Colours.BLUE+"wins"+Colours.CLEAR+" by playing col: "+Colours.BOLD+Colours.BLUE+"{}".format(winningCol+1)+Colours.CLEAR+", row: "+Colours.BOLD+Colours.BLUE+"{}".format(winningRow+1)+Colours.CLEAR+" with {} line.".format(winningMoveTypeString))
elif (board.winState==-1): print("The game has tied")
print("\n")
