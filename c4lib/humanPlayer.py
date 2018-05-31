from .player import Player
from .colours import Colours

class HumanPlayer(Player):
    def __init__(self, playerNum, board):
        Player.__init__(self, playerNum, board)
        # Get our name
        self.name = input("Please enter a name for human player {}: ".format(playerNum))

    def chooseMove(self):
        moves = self.board.getLegalMoves()
        moveStr = (',').join([self.__convertZeroBaseToOneBaseString(x) for x in moves])
        move = self.queryMove(moveStr)
        while (not move in moves):
            print(Colours.RED+"That was not a valid column number, please try again.\a"+Colours.CLEAR)
            move = self.queryMove(moveStr)
        return move

    def queryMove(self, moveStr):
        print("\nLegal moves: "+Colours.BOLD+Colours.BLUE+"{}".format(moveStr)+Colours.CLEAR)
        try:
            move = int(input("Please choose from the above moves: "))
            return (move-1) # convert one base to zero base
        except ValueError:
            return -1

    def getName(self):
        return self.name

    def __convertZeroBaseToOneBaseString(self, x):
        return str(x+1)
