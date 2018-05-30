from random import randint
from .player import Player

class RandomBot(Player):

    def makeMove(self):
        moves = self.board.getLegalMoves()
        if (len(moves)==0): raise Exception("We are asked to move but there are no legal moves, perhaps the game has been won or drawn already.")
        move = randint(0,len(moves)-1)
        self.board.makeMove(self.playerNum,moves[move])
