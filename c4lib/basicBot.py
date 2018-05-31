from random import randint
from copy import deepcopy
from .player import Player

# Instantiate with a difficulty value, this is the number of move steps to look up, 
#   a number larger than 42 is pointless (maximum number of moves) but will not 
#   actually do much beyond giving you something to do while waiting for the 
#   heat-death of the universe.  3 or 4 are the practical limits, 2 is quick enough to be comfortable.
class BasicBot(Player):
    def __init__(self, playerNum, board, lookupRange = 3):
        Player.__init__(self, playerNum, board)
        self.lookupRange = lookupRange

    def getName(self):
        return "ThinkingBot"

    def chooseMove(self):
        moves = self.board.getLegalMoves()
        if (len(moves)==0): raise Exception("We are asked to move but there are no legal moves, perhaps the game has been won or drawn already.")
        return self.__selectFromMoves(moves)

    # Select from the available moves
    def __selectFromMoves(self, moves):
        bestMoves = []
        bestUtility = -1
        for candidate in moves:
            utility = self.__calculateUtility(candidate, self.board)
            if (utility > bestUtility):                
                bestMoves = [candidate]
                bestUtility = utility
            elif (utility==bestUtility): bestMoves.append(candidate)
        if (len(bestMoves)>1):
            return bestMoves[randint(0,len(bestMoves)-1)]
        else: return bestMoves[0]

    # Calculate a utility value in range of 0 - 100 with 0 being a losing move and 100 being a winning move, tie is 50 (as is a totally neutral position), 
    #   if we found nothing compelling within our lookup range then we apply some heuristics to evaluate the board position for that play.
    # This is essentially a simplified min/max tree with capped iterations (lookup range or how far ahead to reason).
    # We evaluate plays in alternating steps from each perspective, assigning maximum utility to wins and minimum utility to losses.
    # We use some simple heuristics to assign partial utility to plays that don't generate a win or loss within our lookup range.

    # Although not implemented, this can be optimised by storing the reasoned tree as a dynamic playbook and after the opponent's play;
    #   identify the tree branch being used, discard the rest and use the reasoning time to further expand that tree, starting from it's bottom level
    def __calculateUtility(self, candidate, board, recursionLevel = 0):
        # Swap player perspective if necessary
        if (recursionLevel%2==0): currentPlayerNum = self.playerNum
        else: currentPlayerNum = (self.playerNum%2)+1
        
        # clone the board
        boardClone = deepcopy(board)
        # make the candidate move
        boardClone.makeMove(currentPlayerNum,candidate)
        # evaluate the win state
        # if won, return 100
        winState = boardClone.winState
        if (winState == currentPlayerNum):
            return 100 # A win
        if (winState == -1): return 50; # A tie

        # If we can't win in the next move, think harder (unless we've thought too hard already)
        if (recursionLevel>self.lookupRange):
            bias = self.__applyHeuristics(boardClone, currentPlayerNum);
            utility = 50+(50*bias);
            return utility
        # evalute the possible moves, from the alternate perspective and calculate a utility based on what we find
        return self.__calculateUtilityFromMoves(boardClone, recursionLevel+1)

    # Select from the available moves
    def __calculateUtilityFromMoves(self, boardClone, recursionLevel):
        bestMoves = []
        bestUtility = -1
        for candidate in boardClone.getLegalMoves():
            utility = self.__calculateUtility(candidate, boardClone, recursionLevel)
            if (utility > bestUtility):
                bestMoves = [candidate]
                bestUtility = utility
            elif (utility==bestUtility): bestMoves.append(candidate)
        
        if (recursionLevel%2==0): return bestUtility
        else: return (100-bestUtility)

    # we apply a board-state based heuristic here
    def __applyHeuristics(self, boardClone, currentPlayerNum):
        # A simple heuristic is to prefer moves in the centre of the board
        (moveRow, moveCol) = boardClone.getLastMoveRowCol();
        centreHeuristic = 3-abs(3-moveCol)
        if (moveRow == 2 or moveRow == 3): centreHeuristic = centreHeuristic + 1

        # We also prefer to move next to an existing piece of ours
        groupingHeuristic = 0
        # vertical lines
        if (boardClone.getPlayerPieceAt(moveRow-1,moveCol) == currentPlayerNum): groupingHeuristic=groupingHeuristic+1
        if (boardClone.getPlayerPieceAt(moveRow-2,moveCol) == currentPlayerNum): groupingHeuristic=groupingHeuristic+1
        
        # horizontal lines
        if (boardClone.getPlayerPieceAt(moveRow,moveCol-1) == currentPlayerNum): groupingHeuristic=groupingHeuristic+1
        if (boardClone.getPlayerPieceAt(moveRow,moveCol+1) == currentPlayerNum): groupingHeuristic=groupingHeuristic+1
        
        # ascending lines
        if (boardClone.getPlayerPieceAt(moveRow-2,moveCol-2) == currentPlayerNum): groupingHeuristic=groupingHeuristic+1
        if (boardClone.getPlayerPieceAt(moveRow-1,moveCol-1) == currentPlayerNum): groupingHeuristic=groupingHeuristic+1
        if (boardClone.getPlayerPieceAt(moveRow+1,moveCol+1) == currentPlayerNum): groupingHeuristic=groupingHeuristic+1
        if (boardClone.getPlayerPieceAt(moveRow+2,moveCol+2) == currentPlayerNum): groupingHeuristic=groupingHeuristic+1
        
        # descending lines
        if (boardClone.getPlayerPieceAt(moveRow+2,moveCol-2) == currentPlayerNum): groupingHeuristic=groupingHeuristic+1
        if (boardClone.getPlayerPieceAt(moveRow+1,moveCol-1) == currentPlayerNum): groupingHeuristic=groupingHeuristic+1
        if (boardClone.getPlayerPieceAt(moveRow-1,moveCol+1) == currentPlayerNum): groupingHeuristic=groupingHeuristic+1
        if (boardClone.getPlayerPieceAt(moveRow-2,moveCol+2) == currentPlayerNum): groupingHeuristic=groupingHeuristic+1
        
        return (centreHeuristic+groupingHeuristic)/11
