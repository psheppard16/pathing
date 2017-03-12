from Game.Maze.gridSquare import GridSquare
import Game.Maze.gridSquare as gs

def generateSquareMaze(mazeWidth, mazeHeight, wallSize):
    start = (0, 0)

    for i in range(mazeWidth): #generates blank grid
        for j in range(mazeHeight):
            GridSquare(i, j)

    focus = start
    while not gs.squaresPathed():
        square = gs.getSquare(focus[0], focus[1])
        if square.hasDirection():
            direction = square.getDirection()
        else:
            square = gs.getPathedSquare()
            if not square:
                break
            focus = (square.xPos, square.yPos)
            direction = square.getDirection()

        if direction == 0:
            if gs.getSquare(focus[0], focus[1] + 1) and not gs.getSquare(focus[0], focus[1] + 1).pathed:
                gs.open(focus[0], focus[1], direction)
                focus = (focus[0], focus[1] + 1)
        elif direction == 1:
            if gs.getSquare(focus[0] + 1, focus[1]) and not gs.getSquare(focus[0] + 1, focus[1]).pathed:
                gs.open(focus[0], focus[1], direction)
                focus = (focus[0] + 1, focus[1])
        elif direction == 2:
            if gs.getSquare(focus[0], focus[1] - 1) and not gs.getSquare(focus[0], focus[1] - 1).pathed:
                gs.open(focus[0], focus[1], direction)
                focus = (focus[0], focus[1] - 1)
        elif direction == 3:
            if gs.getSquare(focus[0] - 1, focus[1]) and not gs.getSquare(focus[0] - 1, focus[1]).pathed:
                gs.open(focus[0], focus[1], direction)
                focus = (focus[0] - 1, focus[1])

    return gs.getWalls(wallSize)





