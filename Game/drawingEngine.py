__author__ = 'Preston Sheppard'
import Pathing.pathing as pathing
import Pathing.geometry as geo
from FrameWork.Display.canvasObject import CanvasObject
from Pathing.wall import WallObject
import math
try:
    import pygame
except:
    pass


class DrawingEngine(CanvasObject):
    def __init__(self, game):
        super().__init__(game)
        self.game = game

    def getScreenX(self, x):
        return x

    def getScreenY(self, y):
        return self.game.window.height - y

    def draw(self):
        if self.game.saveEngine.saveNumber == 2:
            length = len(self.game.gameEngine.finalPaths)
            r = 0
            b = 255
            for path in self.game.gameEngine.finalPaths:
                r += 255 / length
                b -= 255 / length
                for iter in range(len(path) - 1):
                    self.showLine(path[iter], path[iter + 1], (r, 0, b), 3, shiftPosition=True)
            for wall in self.game.gameEngine.wallList:
                self.showLine(wall[0], wall[1], (0, 0, 0), 7, shiftPosition=True, rounded=True)
        elif self.game.saveEngine.saveNumber == 0:
            connectedWalls = {}
            for wall in WallObject.wallList:
                for point in wall.line:
                    if point not in connectedWalls:
                        connectedWalls[point] = wall.connections[point] + [wall]

            # snapPoints = []
            # for point, walls in connectedWalls.items():
            #     for angle in range(0,8):
            #         x1 = point[0] + math.cos(math.pi * 2 * angle / 8 + .1) * 20
            #         y1 = point[1] + math.sin(math.pi * 2 * angle / 8 + .1) * 20
            #         snapPoints.append(geo.getSnapPoints(walls, point, (x1, y1), shift=15))
            # for snapPoint in snapPoints:
            #     self.showCircle((snapPoint[0], snapPoint[1]), 10, (0, 255, 255), shiftPosition=True)

            self.showCircle((self.game.gameEngine.endPoint[0], self.game.gameEngine.endPoint[1]), 10, (0, 255, 0),
                            shiftPosition=True)
            self.showCircle((self.game.gameEngine.startPoint[0], self.game.gameEngine.startPoint[1]),
                            self.game.gameEngine.tolerance, (0, 255, 0), shiftPosition=True)

            for wall in self.game.gameEngine.wallList:
                self.showLine(wall[0], wall[1], (0, 0, 0), 7, shiftPosition=True, rounded=True)

            for pathObjectList in self.game.gameEngine.sets:
                for pathObject in pathObjectList:
                    if pathObject.anchorPoint:
                        self.showCircle(pathObject.position, 10, (255, 255, 0),
                                        shiftPosition=True)
                    if pathObject.creator:
                        if pathObject.hasConnected:
                            self.showLine(pathObject.position, pathObject.creator.position, (255, 255, 255), 3,
                                          shiftPosition=True, rounded=True)
                        elif pathObject.hasBacktracked:
                            self.showLine(pathObject.position, pathObject.creator.position, (0, 255, 0), 3,
                                      shiftPosition=True, rounded=True)
                        elif pathObject.hasBranched:
                            self.showLine(pathObject.position, pathObject.creator.position, (0, 0, 255), 3,
                                          shiftPosition=True, rounded=True)
                        elif pathObject.hasAdvanced:
                            self.showLine(pathObject.position, pathObject.creator.position, (255, 255, 0), 3,
                                          shiftPosition=True, rounded=True)
                        else:
                            self.showLine(pathObject.position, pathObject.creator.position, (255, 0, 0), 3,
                                          shiftPosition=True, rounded=True)
            pathToDraw = pathing.getShortestPath(self.game.gameEngine.sets)
            while pathToDraw and pathToDraw.creator:
                self.showLine((pathToDraw.x, pathToDraw.y), (pathToDraw.creator.x, pathToDraw.creator.y), (255, 0, 255),
                              5, shiftPosition=True, rounded=True)
                pathToDraw = pathToDraw.creator
        else:
            self.showCircle((self.game.gameEngine.endPoint[0], self.game.gameEngine.endPoint[1]), 10, (0, 255, 0),
                            shiftPosition=True)
            self.showCircle((self.game.gameEngine.startPoint[0], self.game.gameEngine.startPoint[1]),
                            self.game.gameEngine.tolerance, (0, 255, 0), shiftPosition=True)

            for wall in self.game.gameEngine.wallList:
                self.showLine(wall[0], wall[1], (0, 0, 0), 7, shiftPosition=True, rounded=True)

            pathToDraw = pathing.getShortestPath(self.game.gameEngine.sets)
            while pathToDraw and pathToDraw.creator:
                self.showLine((pathToDraw.x, pathToDraw.y), (pathToDraw.creator.x, pathToDraw.creator.y), (255, 0, 255),
                              5, shiftPosition=True, rounded=True)
                pathToDraw = pathToDraw.creator
