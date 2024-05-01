import numpy as np

class Board():
    def __init__(self,matrix):
        self.rows = 6
        self.columns = 7
        self.matrix = np.zeros((self.rows,self.columns))
        for i in range(self.columns ):
            for j in range(self.rows):
                self.matrix[j][i] = matrix[j][i]
        self.winner = False

    def playerInput(self, piece, col):
        for r in range(self.rows - 1, -1, -1):
            if self.matrix[r][col] == 0:
                self.matrix[r][col] = piece
                break

    def checkHorizontal(self, piece):
        for row in range(self.rows):
            for col in range(self.columns - 3):
                if (self.matrix[row][col] == piece and self.matrix[row][col + 1] == piece and self.matrix[row][
                    col + 2] == piece and self.matrix[row][col + 3] == piece):
                    return True

    def checkVertical(self, piece):
        for col in range(self.columns):
            for row in range(self.rows - 3):
                if (self.matrix[row][col] == piece and self.matrix[row + 1][col] == piece and self.matrix[row + 2][
                    col] == piece and self.matrix[row + 3][col] == piece):
                    return True

    def checkD1(self, piece):
        for col in range(self.columns - 3):
            for row in range(self.rows - 3):
                if (self.matrix[row][col] == piece and self.matrix[row + 1][col + 1] == piece and self.matrix[row + 2][
                    col + 2] == piece and self.matrix[row + 3][col + 3] == piece):
                    return True



    def checkD2(self, piece):
        for col in range(self.columns - 3):
            for row in range(3, self.rows):
                if (self.matrix[row][col] == piece and self.matrix[row - 1][col + 1] == piece and self.matrix[row - 2][
                    col + 2] == piece and self.matrix[row - 3][col + 3] == piece):
                    return True

    def checkWin(self, piece):
        if (self.checkHorizontal(piece) or self.checkVertical(piece) or self.checkD1(piece) or self.checkD2(piece)):
            return True

    def print(self):
        print(self.matrix)

    def getValidInputs(self):
        inputs = []
        for n in range(self.columns):
            if self.matrix[0][n] == 0:
                inputs.append(n)
        return inputs

    def generateChildren(self,piece):
        inputs = self.getValidInputs()
        boards = []
        for n in inputs:
            b = Board(self.matrix)
            b.playerInput(piece,n)
            boards.append(b)
        return boards,inputs

    def potenetialHorizontal(self,piece,pieceI):
        if(self.checkWin(pieceI)):
            return -1000
        elif self.checkWin(piece):
            return 1000
        else:
            score = 0
            tempL = []
            for row in range(self.rows):
                for col in range(self.columns - 3):
                    tempL = [self.matrix[row][col] , self.matrix[row][col + 1] , self.matrix[row][col + 2] , self.matrix[row][col + 3]]
                    if tempL.count(pieceI) == 0:
                        if tempL.count(piece) > 1:
                            score += tempL.count(piece)
                    elif tempL.count(piece) == 0:
                        if tempL.count(pieceI) > 1:
                            score -= tempL.count(pieceI)

            return score

    def potenetialVertical(self,piece,pieceI):
        if (self.checkWin(pieceI)):
            return -1000
        elif self.checkWin(piece):
            return 1000
        else:
            score = 0
            tempL = []
            for col in range(self.columns):
                for row in range(self.rows - 3):
                    tempL = [self.matrix[row][col], self.matrix[row + 1][col], self.matrix[row + 2][col],
                             self.matrix[row + 3][col]]
                    if tempL.count(pieceI) == 0:
                        if tempL.count(piece) > 1:
                            score += tempL.count(piece)
                    elif tempL.count(piece) == 0:
                        if tempL.count(pieceI) > 1:
                            score -= tempL.count(pieceI)

            return score

    def potenetialD1(self,piece,pieceI):
        if (self.checkWin(pieceI)):
            return -1000
        elif self.checkWin(piece):
            return 1000
        else:
            score = 0
            tempL = []
            for col in range(self.columns - 3):
                for row in range(self.rows - 3):
                    tempL = [self.matrix[row][col],self.matrix[row + 1][col + 1],self.matrix[row + 2][col + 2],self.matrix[row + 3][col + 3]]
                    if tempL.count(pieceI) == 0:

                        if tempL.count(piece) > 1:
                            score += tempL.count(piece)
                    elif tempL.count(piece) == 0:

                        if tempL.count(pieceI) > 1:
                            score -= tempL.count(pieceI)

            return score

    def potentialD2(self,piece,pieceI):
        if (self.checkWin(pieceI)):
            return -1000
        elif self.checkWin(piece):
            return 1000
        else:
            score = 0
            tempL = []
            for col in range(self.columns - 3):
                for row in range(3, self.rows):
                    tempL = [self.matrix[row][col],self.matrix[row - 1][col + 1],self.matrix[row - 2][
                        col + 2],self.matrix[row - 3][col + 3]]
                    if tempL.count(pieceI) == 0:
                        if tempL.count(piece) > 1:
                            score += tempL.count(piece)
                    elif tempL.count(piece) == 0:
                        if tempL.count(pieceI) > 1:
                            score -= tempL.count(pieceI)

            return score

    def getScore(self,piece,pieceI):
        a = self.potentialD2(piece,pieceI)
        b = self.potenetialHorizontal(piece,pieceI)
        c = self.potenetialD1(piece,pieceI)
        d = self.potenetialVertical(piece,pieceI)

        return a+b+c+d










