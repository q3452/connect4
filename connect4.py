#!/usr/bin/env python3
from c4lib.board import Board
from c4lib.randomBot import RandomBot
from c4lib.basicBot import BasicBot
from c4lib.abpBot import ABpBot
from c4lib.humanPlayer import HumanPlayer
from c4lib.colours import Colours
from random import randint
import time

def getPlayOrder(playerIndex):
    if (playerIndex==0): return '1st'
    else: return '2nd'

print("\nConnect 4 by Quentin\n")

# We instantiate the board and then invite players to play on it
board = Board()

coinToss = randint(0,1)
playerNum = coinToss+1
otherPlayerNum = (not coinToss)+1
players = [ None, None ]
players[coinToss] = ABpBot(playerNum, board, 7)
players[not coinToss] = HumanPlayer(otherPlayerNum, board)

# The game loop is here, we toggle the active player rather than performing both turns in the same loop
playerIndex = 0
moveNum = 0
while (board.winState==0):
    board.renderBoard()
    startThinking = time.time()
    players[playerIndex].move()
    stopThinking = time.time()
    print("{:.3g}s Player {} ({}) moved in column {}.".format(stopThinking-startThinking, players[playerIndex].getName(),getPlayOrder(playerIndex),(board.getLastMove()+1)))
    moveNum = moveNum + 1
    playerIndex = not playerIndex

board.renderBoard()
if (board.winState>0):
    (winningRow, winningCol) = board.winningMove
    winningMoveTypeString = board.winningMoveType
    if (winningMoveTypeString[0] in 'aeiou'): winningMoveTypeString = "an "+winningMoveTypeString
    else: winningMoveTypeString="a "+winningMoveTypeString
    print(" {} playing {} ".format(players[board.winState-1].getName(), getPlayOrder(board.winState))+Colours.BLUE+"wins"+Colours.CLEAR+" by playing col: "+Colours.BOLD+Colours.BLUE+"{}".format(winningCol+1)+Colours.CLEAR+", row: "+Colours.BOLD+Colours.BLUE+"{}".format(winningRow+1)+Colours.CLEAR+" with {} line.".format(winningMoveTypeString))
elif (board.winState==-1): print("The game has tied")
print("\n")
