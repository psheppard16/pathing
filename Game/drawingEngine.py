__author__ = 'Preston Sheppard'
import Pathing.pathing as pathing
import Pathing.geometry as geo
from FrameWork.Display.canvasObject import CanvasObject
import inspect
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
        self.showCircle((self.game.gameEngine.endPoint[0], self.game.gameEngine.endPoint[1]), 15, (0, 255, 0),
                        shiftPosition=True)
        self.showCircle((self.game.gameEngine.startPoint[0], self.game.gameEngine.startPoint[1]),
                        15, (0, 255, 0), shiftPosition=True)

        mouseX = self.game.window.root.winfo_pointerx() - self.game.window.root.winfo_rootx()
        if mouseX > self.game.window.width - self.game.gameEngine.indent - 1:
            mouseX = self.game.window.width - self.game.gameEngine.indent - 1
        if mouseX < self.game.gameEngine.indent + 1:
            mouseX = self.game.gameEngine.indent + 1
        mouseY = self.game.window.height - (
        self.game.window.root.winfo_pointery() - self.game.window.root.winfo_rooty())
        if mouseY > self.game.window.height - self.game.gameEngine.indent - 1:
            mouseY = self.game.window.height - self.game.gameEngine.indent - 1
        if mouseY < self.game.gameEngine.indent + 1:
            mouseY = self.game.gameEngine.indent + 1

        sig = inspect.signature(geo.getPixel)
        gridSize = sig.parameters['gridSize'].default
        valid = geo.circleFlood((mouseX, mouseY), self.game.gameEngine.zones)
        if valid:
            for point, walls in valid.items():
                if walls:
                    self.showRectangle((point[0] * gridSize - gridSize * .5, point[1] * gridSize - gridSize * .5), (point[0] * gridSize + gridSize * .5, point[1] * gridSize + gridSize * .5),
                                   (0, 255, 0), shiftPosition=True, secondaryColor=(0, 0, 0), width=2)
                else:
                    self.showRectangle((point[0] * gridSize - gridSize * .5, point[1] * gridSize - gridSize * .5), (point[0] * gridSize + gridSize * .5, point[1] * gridSize + gridSize * .5),
                                   (255, 0, 0), shiftPosition=True, secondaryColor=(0, 0, 0), width=2)


        for nodeList in self.game.gameEngine.nodes.values():
            for node in nodeList:
                self.showCircle((node[0], node[1]), 5, (0, 255, 0), shiftPosition=True)


        for wall in self.game.gameEngine.wallList:
            self.showLine(wall[0], wall[1], (0, 0, 0), 5, shiftPosition=True, rounded=True)

        for path in self.game.gameEngine.paths:
            if path.creator:
                self.showLine(path.location, path.creator.location, (255, 255, 0), 6, shiftPosition=True)


        for index in range(0, len(self.game.gameEngine.fullPath) - 1):
            self.showLine(self.game.gameEngine.fullPath[index], self.game.gameEngine.fullPath[index + 1], (255, 0, 0), 3, shiftPosition=True)


