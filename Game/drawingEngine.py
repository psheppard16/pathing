__author__ = 'Preston Sheppard'
import Game.Pathing.pathing as pathing
from FrameWork.Display.canvasObject import CanvasObject
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
        else:
            self.showCircle((self.game.gameEngine.endPoint[0], self.game.gameEngine.endPoint[1]), 10, (0, 255, 0),
                            shiftPosition=True)
            self.showCircle((self.game.gameEngine.startPoint[0], self.game.gameEngine.startPoint[1]),
                            self.game.gameEngine.tolerance, (0, 255, 0), shiftPosition=True)

            for wall in self.game.gameEngine.wallList:
                self.showLine(wall[0], wall[1], (0, 0, 0), 7, shiftPosition=True, rounded=True)

            for pathObjectList in pathing.setsG:
                for pathObject in pathObjectList:
                    if pathObject.anchorPoint:
                        self.showCircle((pathObject.anchorPoint[0], pathObject.anchorPoint[1]), 10, (255, 255, 0),
                                        shiftPosition=True)
                    if pathObject.creator:
                        if pathObject.hasBranched:
                            self.showLine(pathObject.position, pathObject.creator.position, (0, 255, 0), 3,
                                          shiftPosition=True, rounded=True)
                        elif pathObject.hasAdvanced:
                            self.showLine(pathObject.position, pathObject.creator.position, (0, 0, 255), 3,
                                          shiftPosition=True, rounded=True)
                        else:
                            self.showLine(pathObject.position, pathObject.creator.position, (255, 0, 0), 3,
                                          shiftPosition=True, rounded=True)

            pathToDraw = pathing.getShortestPath(pathing.setsG)
            while pathToDraw and pathToDraw.creator:
                self.showLine((pathToDraw.x, pathToDraw.y), (pathToDraw.creator.x, pathToDraw.creator.y), (255, 165, 0),
                              5, shiftPosition=True, rounded=True)
                pathToDraw = pathToDraw.creator
