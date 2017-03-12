__author__ = 'python'
import math
import random

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
            if False:
                longest = 0
                for path in self.game.gameEngine.finalPaths:
                    dist = self.distance(path[0][0], path[0][1], path[-1][0], path[-1][1])
                    if dist > longest:
                        longest = dist

                for path in self.game.gameEngine.finalPaths:
                    length = self.distance(path[0][0], path[0][1], path[-1][0], path[-1][1])
                    r = (length / longest) * 255
                    b = 255 - (length / longest) * 255
                    for iter in range(len(path) - 1):
                        self.showLine(path[iter], path[iter + 1], (r, 0, b), 3, shiftPosition=True)
                for wall in self.game.gameEngine.wallList:
                    self.showLine(wall[0], wall[1], (0, 0, 0), 7, shiftPosition=True)
            elif True:
                length = len(self.game.gameEngine.finalPaths)
                r = 0
                b = 255
                for path in self.game.gameEngine.finalPaths:
                    r += 255 / length
                    b -= 255 / length
                    for iter in range(len(path) - 1):
                        self.showLine(path[iter], path[iter + 1], (r, 0, b), 3, shiftPosition=True)
                for wall in self.game.gameEngine.wallList:
                    self.showLine(wall[0], wall[1], (0, 0, 0), 7, shiftPosition=True)
            else:
                colors = []
                for path in self.game.gameEngine.finalPaths:
                    colors.append((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

                for path in self.game.gameEngine.finalPaths:
                    for iter in range(len(path) - 1):
                        self.showLine(path[iter], path[iter + 1], colors[self.game.gameEngine.finalPaths.index(path)], 3, shiftPosition=True)
                for wall in self.game.gameEngine.wallList:
                    self.showLine(wall[0], wall[1], (0, 0, 0), 7, shiftPosition=True)
        else:
            self.showCircle((self.game.gameEngine.endPoint[0], self.game.gameEngine.endPoint[1]), 10, (0, 255, 0), shiftPosition=True)
            self.showCircle((self.game.gameEngine.startPoint[0], self.game.gameEngine.startPoint[1]), pathing.toleranceG, (0, 255, 0), shiftPosition=True)

            for pathObjectList in pathing.setsG:
                for pathObject in pathObjectList:
                    if pathObject.anchorPoint:
                        self.showCircle((pathObject.anchorPoint[0], pathObject.anchorPoint[1]), 10, (255, 255, 0), shiftPosition=True)


            for wall in self.game.gameEngine.wallList:
                self.showLine(wall[0], wall[1], (0, 0, 0), 7, shiftPosition=True)

            for pathObjectList in pathing.setsG:
                for pathObject in pathObjectList:
                    if pathObject.creator:
                        # if pathObject.hasConnected:
                        #     self.showLine((pathObject.x, pathObject.y), (pathObject.creator.x, pathObject.creator.y), (0, 0, 255), 3, shiftPosition=True)
                        if pathObject.hasBranched:
                            self.showLine((pathObject.x, pathObject.y), (pathObject.creator.x, pathObject.creator.y), (0, 255, 0), 3, shiftPosition=True)
                        elif pathObject.hasAdvanced:
                            self.showLine((pathObject.x, pathObject.y), (pathObject.creator.x, pathObject.creator.y), (0, 0, 255), 3, shiftPosition=True)
                        else:
                            self.showLine((pathObject.x, pathObject.y), (pathObject.creator.x, pathObject.creator.y), (255, 0, 0), 3, shiftPosition=True)

            pathToDraw = pathing.getShortestPath(pathing.setsG)
            while pathToDraw and pathToDraw.creator:
                self.showLine((pathToDraw.x, pathToDraw.y), (pathToDraw.creator.x, pathToDraw.creator.y), (255, 165, 0), 5, shiftPosition=True)
                pathToDraw = pathToDraw.creator

    def distance(self, x1, y1, x2, y2):
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)






