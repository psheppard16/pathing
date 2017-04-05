__author__ = 'Preston Sheppard'
import Pathing.pathing as pathing
import Pathing.geometry as geo
from FrameWork.Display.canvasObject import CanvasObject
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
        for node, connected in self.game.gameEngine.nodes.items():
            self.showCircle(node, 5, (0, 255, 0), shiftPosition=True)
            for node2 in connected:
                self.showLine(node, node2, (255, 255, 0), 9, shiftPosition=True)
        for path in self.game.gameEngine.paths:
            if path.creator:
                self.showLine(path.location, path.creator.location, (255, 0, 0), 6, shiftPosition=True)
        for index in range(0, len(self.game.gameEngine.fullPath) - 1):
            self.showLine(self.game.gameEngine.fullPath[index], self.game.gameEngine.fullPath[index + 1], (0, 255, 255), 3, shiftPosition=True)

        self.showCircle((self.game.gameEngine.endPoint[0], self.game.gameEngine.endPoint[1]), 15, (0, 255, 0),
                        shiftPosition=True)
        self.showCircle((self.game.gameEngine.startPoint[0], self.game.gameEngine.startPoint[1]),
                        15, (0, 255, 0), shiftPosition=True)

        for wall in self.game.gameEngine.wallList:
            self.showLine(wall[0], wall[1], (0, 0, 0), 7, shiftPosition=True, rounded=True)
