#!/usr/bin/env python3
from c4lib.board import Board
from c4lib.randomBot import RandomBot
from c4lib.humanPlayer import HumanPlayer
from c4lib.colours import Colours

def getPlayOrder(playerNum):
    if (playerNum==1): return '1st'
    else: return '2nd'

print("\nConnect 4 by Quentin\n")
# We instantiate the board and then invite players to play on it
board = Board()
players = [ HumanPlayer(1, board), RandomBot(2, board) ]

# Win detection can be tested by:
# board.makeMove(1,1)
# board.makeMove(2,1)
# board.makeMove(1,1)
# board.makeMove(1,1)
# board.makeMove(1,1)
# board.makeMove(2,2)
# board.makeMove(1,2)
# board.makeMove(1,2)
# board.makeMove(1,3)
# board.makeMove(1,3)
# board.renderBoard()
# board.setDebug(True)
# board.makeMove(1,4)

activePlayer = 1
moveNum = 0
while (board.winState==0):
    board.renderBoard()
    activePlayer = not activePlayer
    players[activePlayer].makeMove()
    print(" Player {} moved in column {}.".format(players[activePlayer].getName(),board.getLastMove()))
    moveNum = moveNum + 1


board.renderBoard()
if (board.winState>0):
    (winningRow, winningCol) = board.winningMove
    winningMoveTypeString = board.winningMoveType
    if (winningMoveTypeString[0] in 'aeiou'): winningMoveTypeString = "an "+winningMoveTypeString
    else: winningMoveTypeString="a "+winningMoveTypeString
    print(" {} playing {} ".format(players[board.winState-1].getName(), getPlayOrder(board.winState))+Colours.BLUE+"wins"+Colours.CLEAR+" by playing col: "+Colours.BOLD+Colours.BLUE+"{}".format(winningCol+1)+Colours.CLEAR+", row: "+Colours.BOLD+Colours.BLUE+"{}".format(winningRow+1)+Colours.CLEAR+" with {} line.".format(winningMoveTypeString))
elif (board.winState==-1): print("The game has tied")
print("\n")
