from .colours import Colours

class MoveTypes: # from left to right direction
    vertical = 'vertical'
    upwards = 'ascending'
    downwards = 'descending'
    horizontal = 'horizontal'

class Board:
    # Initializer / Instance Attributes
    def __init__(self):
        # Initialise the board, a sparse representation allows for a few optimisations at the expense of checking array lengths here and there
        self.columns = [
            [],[],[],[],[],[],[]
        ]
        self.winState = 0
        self.winningMove = (-1,-1)
        self.winningMoveType = ''
        self.debug = False
        self.moveLog = []
    def setDebug(self, debug):
        self.debug = debug
    def getMoveNum(self, moveNum):
        return self.moveLog[moveNum]
    def getLastMove(self):
        if len(self.moveLog)>0:
            return self.moveLog[-1]['colNum']
        else: raise Exception("Someone is requesting the last move when there are no moves yet.")

    def makeMove(self, playerNum, colNum):
        if (self.winState != 0): raise ValueError("Player {} is attempting to move when the game is already won by player {}.".format(playerNum, self.winState))
        if (playerNum != 1 and playerNum != 2): raise ValueError("An invalid player was selected")
        if (type(colNum) != int): raise ValueError("The board didn't understand the requested move ({}).".format(colNum))
        if (colNum<0 or colNum>6): raise ValueError("An invalid column was requested ({}).".format(colNum))
        if (len(self.columns[colNum])>5): raise ValueError("The move attempted to play in a full column ({}).".format(colNum))
        # We seem to have a valid move.
        self.columns[colNum].append(playerNum)
        self.moveLog.append({'playerNum': playerNum, 'colNum': colNum})
        self.checkForWin()
        if (self.winState != 0):
            self.winningMove = (len(self.columns[colNum])-1, colNum);

    def renderBoard(self):
        print(Colours.BLUE+"   ________________"+Colours.CLEAR)
        for rowNum in range(5,-1,-1):
            print(Colours.BOLD+"  "+str(rowNum+1)+Colours.CLEAR+Colours.BLUE+"|"+Colours.CLEAR, end='')
            for colNum in range(0,7):
                piece = self.getDisplayPieceAt(rowNum,colNum)
                print(piece, end='')
                print(" ", end='')
            print(Colours.BLUE+"|"+Colours.CLEAR, flush=True)
        print(Colours.BLUE+"   ================"+Colours.CLEAR)
        print(Colours.BOLD+"    1 2 3 4 5 6 7"+Colours.CLEAR)
        print("")

    def getDisplayPieceAt(self, rowNum, colNum):
        column = self.columns[colNum]
        # print("rowNum: {}, col: {}".format(rowNum, colNum))
        # print(len(column))
        if (len(column)<(rowNum+1)): return Colours.UNDERLINE+'_'+Colours.CLEAR
        elif (column[rowNum]==1): return Colours.YELLOW+"0"+Colours.CLEAR
        else: return Colours.RED+"X"+Colours.CLEAR

    def getPlayerPieceAt(self, rowNum, colNum):
        column = self.columns[colNum]
        if (len(column)<(rowNum+1)): return 0
        else: return column[rowNum]

    def getBoardState(self):
        return self.columns

    def getLegalMoves(self):
        if (self.winState != 0): return []
        legalMoves = []
        for i, column in enumerate(self.columns):
            if (len(column) < 6): legalMoves.append(i)
        return legalMoves

    def checkForWin(self):
        # We don't need to test every square, if we proceed from left to right, bottom to top, 
        #   we only need to check for lines going straight up, lines going up-right, down-right 
        #   and across-right.  We also don't need to check for right-ward lines in columns 4-6 
        #   (zero based) and just check for vertical lines in those columns.
        for rowNum in range(0, 6):
            for colNum in range(0,7):
                if (self.checkVerticalLine(rowNum,colNum)):
                    self.winningMoveType = MoveTypes.vertical
                    self.winningMove=(rowNum,colNum)
                    self.winState = self.getPlayerPieceAt(rowNum,colNum)
                if (self.checkUpwardsLine(rowNum,colNum)):
                    self.winningMoveType = MoveTypes.upwards
                    self.winningMove=(rowNum,colNum)
                    self.winState = self.getPlayerPieceAt(rowNum,colNum)
                if (self.checkDownwardsLine(rowNum,colNum)):
                    self.winningMoveType = MoveTypes.downwards
                    self.winningMove=(rowNum,colNum)
                    self.winState = self.getPlayerPieceAt(rowNum,colNum)
                if (self.checkHorizontalLine(rowNum,colNum)):
                    self.winningMoveType = MoveTypes.horizontal
                    self.winningMove=(rowNum,colNum)
                    self.winState = self.getPlayerPieceAt(rowNum,colNum)
        if (self.winState==0 and len(self.getLegalMoves()) == 0): self.winState = -1 # Stalemate
        return self.winState

    def checkVerticalLine(self, rowNum, colNum):
        if (rowNum>= 3): return False # there isn't enough space for a four line
        column = self.columns[colNum]
        if (len(column) != (rowNum+4)): return False # A winning move from this slot will require the column height to be rowNum+4
        playerNum = self.getPlayerPieceAt(rowNum, colNum)
        if (playerNum==0): return False
        for i in range(rowNum+1,rowNum+4):
            if (column[i]!=playerNum): return False
        return True;
    def checkUpwardsLine(self, rowNum, colNum):
        if (rowNum>= 3): return False # there isn't enough space for a four line
        if (colNum>= 4): return False # there isn't enough space for a four line
        playerNum = self.getPlayerPieceAt(rowNum, colNum)
        if (playerNum==0): return False
        for i in range(1,4):
            if (self.getPlayerPieceAt(rowNum+i, colNum+i)!=playerNum): return False
        return True;
    def checkDownwardsLine(self, rowNum, colNum):
        if (rowNum<= 2): return False # there isn't enough space for a four line
        if (colNum>= 4): return False # there isn't enough space for a four line
        playerNum = self.getPlayerPieceAt(rowNum, colNum)
        if (playerNum==0): return False
        for i in range(1,4):
            if (self.getPlayerPieceAt(rowNum-i, colNum+i)!=playerNum): return False
        return True;
    def checkHorizontalLine(self, rowNum, colNum):
        if (colNum>= 4): return False # there isn't enough space for a four line
        playerNum = self.getPlayerPieceAt(rowNum, colNum)
        if (playerNum==0): return False
        for i in range(1,4):
            if (self.getPlayerPieceAt(rowNum, colNum+i)!=playerNum): return False
        return True;