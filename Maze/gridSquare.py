__author__ = 'Preston Sheppard'
import random
class GridSquare:
    def __init__(self, xPos, yPos):
        self.xPos = xPos
        self.yPos = yPos
        self.pathed = False
        self.walls = [True, True, True, True]
        self.directions = [0, 1, 2, 3]
        
    def open(self, direction, gridSquares):
        ###0###
        #3###1#
        ###2###
        self.walls[direction] = False
        self.pathed = True
        try:
            if direction == 0 and getSquare(self.xPos, self.yPos + 1, gridSquares):
                square = getSquare(self.xPos, self.yPos + 1, gridSquares)
                square.walls[2] = False
                square.pathed = True
                square.directions.remove(2)
            elif direction == 1 and getSquare(self.xPos + 1, self.yPos, gridSquares):
                square = getSquare(self.xPos + 1, self.yPos, gridSquares)
                square.walls[3] = False
                square.pathed = True
                square.directions.remove(3)
            elif direction == 2 and getSquare(self.xPos, self.yPos - 1, gridSquares):
                square = getSquare(self.xPos, self.yPos - 1, gridSquares)
                square.walls[0] = False
                square.pathed = True
                square.directions.remove(0)
            elif direction == 3 and getSquare(self.xPos - 1, self.yPos, gridSquares):
                square = getSquare(self.xPos - 1, self.yPos, gridSquares)
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

def open(xPos, yPos, direction, gridSquares):
    gridSquares[xPos][yPos].open(direction, gridSquares)

def getWalls(wallSize, gridSquares, location):
    wallList = []
    for squareList in gridSquares:
        for square in squareList:
            if square.walls[0]:
                wallList.append(((square.xPos * wallSize + location[0], (square.yPos + 1) * wallSize + location[1]), ((square.xPos + 1) * wallSize + location[0], (square.yPos + 1) * wallSize + location[1])))
            if square.walls[1]:
                wallList.append((((square.xPos + 1) * wallSize + location[0], (square.yPos + 1) * wallSize + location[1]), ((square.xPos + 1) * wallSize + location[0], square.yPos * wallSize + location[1])))
            if square.walls[2]:
                wallList.append(((square.xPos * wallSize + location[0], square.yPos * wallSize + location[1]), ((square.xPos + 1) * wallSize + location[0], square.yPos * wallSize + location[1])))
            if square.walls[3]:
                wallList.append(((square.xPos * wallSize + location[0], (square.yPos + 1) * wallSize + location[1]), (square.xPos * wallSize + location[0], square.yPos * wallSize + location[1])))

    removed = True
    while removed:
        removed = False
        for wall1 in wallList:  # remove duplicate walls
            duplicate = False
            for wall2 in wallList:
                if wall1 == wall2:
                    if duplicate:
                        wallList.remove(wall2)
                        removed = True
                    else:
                        duplicate = True

    return wallList

def squaresPathed(gridSquares):
    for squareList in gridSquares:
        for square in squareList:
            if not square.pathed:
                return False
    return True

def getSquare(xPos, yPos, gridSquares):
    if xPos < 0:
        return None
    if yPos < 0:
        return None
    if xPos >= len(gridSquares):
        return None
    if yPos >= len(gridSquares[0]):
        return None
    return gridSquares[xPos][yPos]

def getPathedSquare(gridSquares):
    candidates = []
    for squareList in gridSquares:
        for square in squareList:
            if square.pathed and square.hasDirection():
                candidates.append(square)
    if candidates:
        return random.choice(candidates)
    else:
        return None

def generateSquareMaze(mazeWidth, mazeHeight, wallSize, location=(0,0)):
    start = (0, 0)

    gridSquares = [[None for i in range(mazeHeight)] for j in range(mazeWidth)]
    for i in range(mazeWidth): #generates blank grid
        for j in range(mazeHeight):
            gridSquares[i][j] = GridSquare(i, j)

    focus = start
    while not squaresPathed(gridSquares):
        square = getSquare(focus[0], focus[1], gridSquares)
        if square.hasDirection():
            direction = square.getDirection()
        else:
            square = getPathedSquare(gridSquares)
            if not square:
                break
            focus = (square.xPos, square.yPos)
            direction = square.getDirection()

        if direction == 0:
            if getSquare(focus[0], focus[1] + 1, gridSquares) and not getSquare(focus[0], focus[1] + 1, gridSquares).pathed:
                open(focus[0], focus[1], direction, gridSquares)
                focus = (focus[0], focus[1] + 1)
        elif direction == 1:
            if getSquare(focus[0] + 1, focus[1], gridSquares) and not getSquare(focus[0] + 1, focus[1], gridSquares).pathed:
                open(focus[0], focus[1], direction, gridSquares)
                focus = (focus[0] + 1, focus[1], gridSquares)
        elif direction == 2:
            if getSquare(focus[0], focus[1] - 1, gridSquares) and not getSquare(focus[0], focus[1] - 1, gridSquares).pathed:
                open(focus[0], focus[1], direction, gridSquares)
                focus = (focus[0], focus[1] - 1, gridSquares)
        elif direction == 3:
            if getSquare(focus[0] - 1, focus[1], gridSquares) and not getSquare(focus[0] - 1, focus[1], gridSquares).pathed:
                open(focus[0], focus[1], direction, gridSquares)
                focus = (focus[0] - 1, focus[1], gridSquares)

    return getWalls(wallSize, gridSquares, location)
