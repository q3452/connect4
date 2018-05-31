from random import randint
from .player import Player

class RandomBot(Player):

    def chooseMove(self):
        moves = self.board.getLegalMoves()
        if (len(moves)==0): raise Exception("We are asked to move but there are no legal moves, perhaps the game has been won or drawn already.")
        return moves[randint(0,len(moves)-1)]

    def getName(self):
        return "RandomBot"
