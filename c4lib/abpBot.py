from random import randint
from copy import deepcopy
from .player import Player

def otherPlayer(playerNum):
    newPlayerNum = (not(playerNum-1))+1
    return newPlayerNum

class ABpBot(Player):
    def __init__(self, playerNum, board, lookupRange = 3):
        Player.__init__(self, playerNum, board)
        self.lookupRange = lookupRange
        self.debug = False

    def getName(self):
        return "ABpBot"

    def chooseMove(self):
        moves = self.board.getLegalMoves()
        if( len(moves)==0 ): raise Exception("We are asked to move but there are no legal moves, perhaps the game has been won or drawn already.")
        return self.__selectFromMoves(moves)

    # Select from the available moves
    def __selectFromMoves(self, moves):
        board = deepcopy(self.board)
        bestMoves = []
        bestUtility = float('-infinity')
        alpha = float('infinity')
        for move in moves:
            self.debug = (move==3)
            board.makeMove(self.playerNum, move)
            alpha = -self.alphaBeta(board, float('-infinity'), alpha, self.lookupRange - 1, otherPlayer(self.playerNum))
            print("Base utility for {} is {}".format(move, alpha))
            board.unmakeMove()
            if( alpha > bestUtility ):
                bestUtility = alpha
                bestMoves = [move]
            elif( alpha == bestUtility ): bestMoves.append(move)
        print("Best moves:", bestMoves)
        return bestMoves[randint(0,len(bestMoves)-1)]

    def alphaBeta(self, board, alpha, beta, lookupRange, playerNum):
        otherPlayerNum = otherPlayer(playerNum)
        if (board.winState==otherPlayerNum): return alpha

        if lookupRange == 0:
            return self.__applyHeuristics(board, playerNum)
        moves = board.getLegalMoves()
        for move in moves:
            board.makeMove(playerNum, move)
            utility = -self.alphaBeta(board, -beta, -alpha, lookupRange - 1, otherPlayerNum)
            board.unmakeMove()
            if( utility >= beta ):
                return beta
            if( utility > alpha ):
                alpha = utility
        return alpha

    # we apply a board-state based heuristic here
    def __applyHeuristics(self, boardClone, currentPlayerNum):
        if (boardClone.winState == currentPlayerNum): return 999
        if (boardClone.winState == 0): return 0
        # A simple heuristic is to prefer pieces in the centre of the board
        centreHeuristic = 0
        for colNum in range(2,5):
            for rowNum in range(0,4):
                if( boardClone.getPlayerPieceAt(rowNum,colNum)==currentPlayerNum ):
                    centreHeuristic = centreHeuristic + 1

        (moveRow, moveCol) = boardClone.getLastMoveRowCol();
        # centreHeuristic = 3-abs(3-moveCol)
        # if (moveRow == 2 or moveRow == 3): centreHeuristic = centreHeuristic + 1

        # We also prefer to move next to an existing piece of ours
        groupingHeuristic = 12 # Count down since this is actually the opponent's move
        # vertical lines
        if (boardClone.getPlayerPieceAt(moveRow-1,moveCol) == currentPlayerNum): groupingHeuristic=groupingHeuristic-1
        if (boardClone.getPlayerPieceAt(moveRow-2,moveCol) == currentPlayerNum): groupingHeuristic=groupingHeuristic-1
        
        # horizontal lines
        if (boardClone.getPlayerPieceAt(moveRow,moveCol-1) == currentPlayerNum): groupingHeuristic=groupingHeuristic-1
        if (boardClone.getPlayerPieceAt(moveRow,moveCol+1) == currentPlayerNum): groupingHeuristic=groupingHeuristic-1
        
        # ascending lines
        if (boardClone.getPlayerPieceAt(moveRow-2,moveCol-2) == currentPlayerNum): groupingHeuristic=groupingHeuristic-1
        if (boardClone.getPlayerPieceAt(moveRow-1,moveCol-1) == currentPlayerNum): groupingHeuristic=groupingHeuristic-1
        if (boardClone.getPlayerPieceAt(moveRow+1,moveCol+1) == currentPlayerNum): groupingHeuristic=groupingHeuristic-1
        if (boardClone.getPlayerPieceAt(moveRow+2,moveCol+2) == currentPlayerNum): groupingHeuristic=groupingHeuristic-1
        
        # descending lines
        if (boardClone.getPlayerPieceAt(moveRow+2,moveCol-2) == currentPlayerNum): groupingHeuristic=groupingHeuristic-1
        if (boardClone.getPlayerPieceAt(moveRow+1,moveCol-1) == currentPlayerNum): groupingHeuristic=groupingHeuristic-1
        if (boardClone.getPlayerPieceAt(moveRow-1,moveCol+1) == currentPlayerNum): groupingHeuristic=groupingHeuristic-1
        if (boardClone.getPlayerPieceAt(moveRow-2,moveCol+2) == currentPlayerNum): groupingHeuristic=groupingHeuristic-1
        
        utility = centreHeuristic+groupingHeuristic
        return utility
