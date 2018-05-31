from abc import ABCMeta, abstractmethod
class Player(metaclass=ABCMeta):
    # Initializer / Instance Attributes
    def __init__(self, playerNum, board):
        self.playerNum = playerNum
        self.board = board
        
    def move(self):
        move = self.chooseMove()
        self.board.makeMove(self.playerNum,move)

# The getName and chooseMove methods should be reimplemented for child classes
    @abstractmethod
    def getName(self):
        # Return a string identifying the player
        pass

    @abstractmethod
    def chooseMove(self):
        # Return a legal move (column number as int in the range 0-6)
        pass
