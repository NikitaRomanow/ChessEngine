class GameState():
    def __init__(self):
        # each piece has 2 characters, 1st is a color, 2nd is a type
        # "--" represents an empty space
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]

        self.moveFunctions = {"p": self.getPawnMoves,
                              "R": self.getRookMoves,
                              "N": self.getKnightMoves,
                              "B": self.getBishopMoves,
                              "Q": self.getQueenMoves,
                              "K": self.getKingMoves}

        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7,4)
        self.blackKingLocation = (0,4)
        self.checkMate = False
        self.staleMate = False


    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove #switch turns
        #update king location
        if move.pieceMoved == "wK":
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == "bK":
            self.blackKingLocation = (move.endRow, move.endCol)

    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
            if move.pieceMoved == "wK":
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == "bK":
                self.blackKingLocation = (move.startRow, move.startCol)

    def getValidMoves(self):

        #1. generate all possible moves

        moves = self.getAllPossibleMoves()

        #2. for each move make a move

        for i in range(len(moves)-1, -1, -1): #when removing from a list we go backwards
            self.makeMove(moves[i])
            self.whiteToMove = not self.whiteToMove

            if self.inCheck():
                moves.remove(moves[i]) #4. if they attack your king it's not a valid move
            self.whiteToMove = not self.whiteToMove
            self.undoMove()
            if len(moves) == 0: #either checkmate or stalemate
                if self.inCheck():
                    self.checkMate = True
                else:
                    self.staleMate = True
            else:
                self.checkMate = False
                self.staleMate = False

        return moves


    def inCheck(self):
        if self.whiteToMove:
            print("1self.whiteToMove")
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])

        else:
            print(self.whiteToMove)
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])



    def squareUnderAttack(self, row, col):
        self.whiteToMove = not self.whiteToMove #switch turn
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove

        for move in oppMoves:
            if move.endRow == row and move.endCol == col:
                return True
        return False




    def getAllPossibleMoves(self):
        moves = []
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                turn = self.board[row][col][0]
                if (turn == "w" and self.whiteToMove) or (turn == "b" and not self.whiteToMove):
                    piece = self.board[row][col][1]
                    self.moveFunctions[piece](row, col, moves)
        return moves

    """
    Desctibing the possibilities of pieces moves
    """

    def getPawnMoves(self, row, col, moves):
        if self.whiteToMove: #white pawns moves
            if self.board[row-1][col] == "--": #1 sqare move
                moves.append(Move((row, col),(row-1, col), self.board))
                if row == 6 and self.board[row-2][col] == "--": #2square move
                    moves.append(Move((row, col), (row - 2, col), self.board))

            if col-1 >= 0 : #check for not go away off board by capture left
                if self.board[row-1][col-1][0] == "b": #if there enemy piece
                    moves.append(Move((row, col), (row - 1, col-1), self.board))

            if col+1 <= 7 : #check for not go away off board by capture right
                if self.board[row-1][col+1][0] == "b": #if there enemy piece
                    moves.append(Move((row, col), (row - 1, col+1), self.board))




        else: #black pawns moves
            if self.board[row+1][col] == "--": #1 sqare move
                moves.append(Move((row, col), (row+1, col), self.board))
                if row == 1 and self.board[row+2][col] == "--": #2square move
                    moves.append(Move((row, col), (row + 2, col), self.board))

            if col-1 >= 0 : #check for not go away off board by capture left
                if self.board[row+1][col-1][0] == "w": #if there enemy piece
                    moves.append(Move((row, col), (row + 1, col-1), self.board))

            if col+1 <= 7 : #check for not go away off board by capture right
                if self.board[row+1][col+1][0] == "w": #if there enemy piece
                    moves.append(Move((row, col), (row + 1, col+1), self.board))


    def getRockMoves(self,row,col,moves):
        pass

    def getKnightMoves(self, row, col, moves):
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        allyColor = "w" if self.whiteToMove else "b"
        for m in knightMoves:
            endRow = row + m[0]
            endCol = col + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor: #empty or enemy piece
                    moves.append(Move((row, col), (endRow, endCol), self.board))


    def getBishopMoves(self, row, col, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = row + d[0] * i
                endCol = col + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((row, col), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((row, col), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break

    def getQueenMoves(self, row, col, moves):
        self.getRookMoves(row, col, moves)
        self.getBishopMoves(row, col, moves)

    def getKingMoves(self, row, col, moves):
        kingMoves = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        allyColor = "w" if self.whiteToMove else "b"
        for i in range(8):
            endRow = row + kingMoves[i][0]
            endCol = col + kingMoves[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:  # empty or enemy piece
                    moves.append(Move((row, col), (endRow, endCol), self.board))


class Move():

    #maps keys to values

    ranksToRows = {
        "1": 7, "2": 6, "3": 5, "4": 4,
        "5": 3, "6": 2, "7": 1, "8": 0
    }
    rowsToRanks = {v:k for k,v in ranksToRows.items()}

    filseToCols = {
        "a": 0, "b": 1, "c": 2, "d": 3,
        "e": 4, "f": 5, "g": 6, "h": 7
    }

    colsToFiles = {v:k for k,v in filseToCols.items()}

    def __init__(self,startSq,endSq,board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow*1000 + self.startCol*100 + self.endRow*10 + self.endCol

    def __eq__(self,other):
        if isinstance(other,Move):
            return self.moveID == other.moveID
        return False
        
    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self,row,col):
        return self.colsToFiles[col] + self.rowsToRanks[row]