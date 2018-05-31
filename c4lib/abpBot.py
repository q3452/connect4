from random import randint
from copy import deepcopy
from .player import Player

def otherPlayer(playerNum):
    newPlayerNum = (not(playerNum-1))+1
    return newPlayerNum

# This is an upgrade to the basic bot which uses a simplified min/max tree.  This uses MinMax with Alpha/Beta Pruning to reduce the search space.
# This lets this bot look much further ahead than the basic version, up to about 9ply can be searched in reasonable time, compared to about 4 with BasicBot.
# Various online resources were used for reference and inspiration but mostly the wikipedia on A/B pruning and a relevent stack-exchange question with non-functional code.
# https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning
# https://stackoverflow.com/questions/19963555/alpha-beta-pruning-python-algorithm
# 
# A weakness of the bot is that it assumes that the opponent plays perfectly, which means that in positions where the opponent CAN win, it will assume that it CAN'T 
# and play randomly from what appear to it to be equally bad options rather than trying to stay alive as long as possible (which would let the opponent make a mistake).
# This can lead to some counter-intuitive plays which is actually because it knows that it could force a loss if it were on the other side and it considered all defeat 
# to be equal.  This could probably be fixed by preferring later defeats to immediate ones.

class ABpBot(Player):
    def __init__(self, playerNum, board, lookupRange = 7):
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
        alpha = float('-infinity')
        for move in moves:
            board.makeMove(self.playerNum, move)
            if( board.winState == self.playerNum ): alpha = float('infinity')
            else: alpha = -self.alphaBetaSearch(board, alpha, float('infinity'), self.lookupRange - 1, otherPlayer(self.playerNum))
            board.unmakeMove()
            if( alpha > bestUtility ):
                bestUtility = alpha
                bestMoves = [move]
            elif( alpha == bestUtility ): bestMoves.append(move)
        return bestMoves[randint(0,len(bestMoves)-1)]

    def alphaBetaSearch(self, board, alpha, beta, lookupRange, playerNum):
        if lookupRange == 0:
            return self.__applyHeuristics(board, playerNum)
        moves = board.getLegalMoves()
        for move in moves:
            board.makeMove(playerNum, move)
            if( board.winState == self.playerNum ): utility = float('infinity')
            else: utility = -self.alphaBetaSearch(board, -beta, -alpha, lookupRange - 1, otherPlayer(playerNum))
            board.unmakeMove()
            if( utility >= beta ):
                return beta
            if( utility > alpha ):
                alpha = utility
        return alpha

    # we apply a board-state based heuristic here
    def __applyHeuristics(self, boardClone, currentPlayerNum):
        if (boardClone.winState == 0): return 0
        # A simple heuristic is to prefer pieces in the centre of the board
        centreHeuristic = 0
        for colNum in range(2,5):
            for rowNum in range(0,4):
                if( boardClone.getPlayerPieceAt(rowNum,colNum)==currentPlayerNum ):
                    centreHeuristic = centreHeuristic + 1

        (moveRow, moveCol) = boardClone.getLastMoveRowCol();

        # We also prefer to minimise clustering of opponent's pieces, this might encourage our bot to aggressively disrupt opponent's lines
        groupingHeuristic = 12 # Count down since this is actually the opponent's move
        otherPlayerNum = otherPlayer(currentPlayerNum)
        # vertical lines
        if (boardClone.getPlayerPieceAt(moveRow-1,moveCol) == otherPlayerNum): groupingHeuristic=groupingHeuristic-1
        if (boardClone.getPlayerPieceAt(moveRow-2,moveCol) == otherPlayerNum): groupingHeuristic=groupingHeuristic-1
        
        # horizontal lines
        if (boardClone.getPlayerPieceAt(moveRow,moveCol-1) == otherPlayerNum): groupingHeuristic=groupingHeuristic-1
        if (boardClone.getPlayerPieceAt(moveRow,moveCol+1) == otherPlayerNum): groupingHeuristic=groupingHeuristic-1
        
        # ascending lines
        if (boardClone.getPlayerPieceAt(moveRow-2,moveCol-2) == otherPlayerNum): groupingHeuristic=groupingHeuristic-1
        if (boardClone.getPlayerPieceAt(moveRow-1,moveCol-1) == otherPlayerNum): groupingHeuristic=groupingHeuristic-1
        if (boardClone.getPlayerPieceAt(moveRow+1,moveCol+1) == otherPlayerNum): groupingHeuristic=groupingHeuristic-1
        if (boardClone.getPlayerPieceAt(moveRow+2,moveCol+2) == otherPlayerNum): groupingHeuristic=groupingHeuristic-1
        
        # descending lines
        if (boardClone.getPlayerPieceAt(moveRow+2,moveCol-2) == otherPlayerNum): groupingHeuristic=groupingHeuristic-1
        if (boardClone.getPlayerPieceAt(moveRow+1,moveCol-1) == otherPlayerNum): groupingHeuristic=groupingHeuristic-1
        if (boardClone.getPlayerPieceAt(moveRow-1,moveCol+1) == otherPlayerNum): groupingHeuristic=groupingHeuristic-1
        if (boardClone.getPlayerPieceAt(moveRow-2,moveCol+2) == otherPlayerNum): groupingHeuristic=groupingHeuristic-1
        
        utility = centreHeuristic+groupingHeuristic
        return utility
