__author__ = 'Preston Sheppard'
import random
class GridSquare:
    xSize = 16
    ySize = 9
    gridSquares = [[None for i in range(9)] for j in range(16)]
    def __init__(self, xPos, yPos):
        self.xPos = xPos
        self.yPos = yPos
        self.pathed = False
        self.walls = [True, True, True, True]
        self.directions = [0, 1, 2, 3]
        GridSquare.gridSquares[xPos][yPos] = self
        
    def open(self, direction):
        ###0###
        #3###1#
        ###2###
        self.walls[direction] = False
        self.pathed = True
        try:
            if direction == 0 and getSquare(self.xPos, self.yPos + 1):
                square = getSquare(self.xPos, self.yPos + 1)
                square.walls[2] = False
                square.pathed = True
                square.directions.remove(2)
            elif direction == 1 and getSquare(self.xPos + 1, self.yPos):
                square = getSquare(self.xPos + 1, self.yPos)
                square.walls[3] = False
                square.pathed = True
                square.directions.remove(3)
            elif direction == 2 and getSquare(self.xPos, self.yPos - 1):
                square = getSquare(self.xPos, self.yPos - 1)
                square.walls[0] = False
                square.pathed = True
                square.directions.remove(0)
            elif direction == 3 and getSquare(self.xPos - 1, self.yPos):
                square = getSquare(self.xPos - 1, self.yPos)
                square.walls[1] = False
                square.pathed = True
                square.directions.remove(1)
        except IndexError:
            pass

    def getDirection(self):
        try:
            direction = random.choice(self.directions)
            self.directions.remove(direction)
            return direction
        except IndexError:
            return None

    def hasDirection(self):
        if self.directions:
            return True
        else:
            return False

def open(xPos, yPos, direction):
    GridSquare.gridSquares[xPos][yPos].open(direction)

def getWalls(wallSize):
    wallList = []
    for squareList in GridSquare.gridSquares:
        for square in squareList:
            if square.walls[0]:
                wallList.append(((square.xPos * wallSize, (square.yPos + 1) * wallSize), ((square.xPos + 1) * wallSize, (square.yPos + 1) * wallSize)))
            if square.walls[1]:
                wallList.append((((square.xPos + 1) * wallSize, (square.yPos + 1) * wallSize), ((square.xPos + 1) * wallSize, square.yPos * wallSize)))
            if square.walls[2]:
                wallList.append(((square.xPos * wallSize, square.yPos * wallSize), ((square.xPos + 1) * wallSize, square.yPos * wallSize)))
            if square.walls[3]:
                wallList.append(((square.xPos * wallSize, (square.yPos + 1) * wallSize), (square.xPos * wallSize, square.yPos * wallSize)))
    return wallList

def squaresPathed():
    for squareList in GridSquare.gridSquares:
        for square in squareList:
            if not square.pathed:
                return False
    return True

def getSquare(xPos, yPos):
    if xPos < 0:
        return None
    if yPos < 0:
        return None
    if xPos >= GridSquare.xSize:
        return None
    if yPos >= GridSquare.ySize:
        return None
    return GridSquare.gridSquares[xPos][yPos]

def getPathedSquare():
    candidates = []
    for squareList in GridSquare.gridSquares:
        for square in squareList:
            if square.pathed and square.hasDirection():
                candidates.append(square)
    if candidates:
        return random.choice(candidates)
    else:
        return None

