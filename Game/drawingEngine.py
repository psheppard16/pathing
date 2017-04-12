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
        # for wall in self.game.gameEngine.wallList:
        #     bPoints = bresenham(wall[0], wall[1])
        #     for point in bPoints:
        #         self.showRectangle((point[0] * 100, point[1] * 100), (point[0] * 100 + 100, point[1] * 100 + 100),
        #                            (165, 255, 165), shiftPosition=True, secondaryColor=(0, 0, 0), width=2)
        #
        for index in range(0, len(self.game.gameEngine.fullPath) - 1):
            bPoints = bresenham(self.game.gameEngine.fullPath[index], self.game.gameEngine.fullPath[index + 1])
            for point in bPoints:
                self.showRectangle((point[0] * 100, point[1] * 100), (point[0] * 100 + 100, point[1] * 100 + 100),
                                   (255, 165, 165), shiftPosition=True, secondaryColor=(0, 0, 0), width=2)

        # for index in range(0, len(self.game.gameEngine.fullPath) - 1):
        #     bPoints = bresenham(self.game.gameEngine.fullPath[index], self.game.gameEngine.fullPath[index + 1])
        #     for point in bPoints:
        #         self.showCircle((point[0] * 100, point[1] * 100), 10, (255, 165, 0), shiftPosition=True)


        self.showCircle((self.game.gameEngine.endPoint[0], self.game.gameEngine.endPoint[1]), 15, (0, 255, 0),
                        shiftPosition=True)
        self.showCircle((self.game.gameEngine.startPoint[0], self.game.gameEngine.startPoint[1]),
                        15, (0, 255, 0), shiftPosition=True)

        for wall in self.game.gameEngine.wallList:
            self.showLine(wall[0], wall[1], (0, 0, 0), 5, shiftPosition=True, rounded=True)

        # for node in self.game.gameEngine.nodes:
        #     self.showCircle(node, 5, (0, 255, 0), shiftPosition=True)

        for path in self.game.gameEngine.paths:
            if path.creator:
                self.showLine(path.location, path.creator.location, (255, 255, 0), 6, shiftPosition=True)


        for index in range(0, len(self.game.gameEngine.fullPath) - 1):
            self.showLine(self.game.gameEngine.fullPath[index], self.game.gameEngine.fullPath[index + 1], (255, 0, 0), 3, shiftPosition=True)


def switch_octant_to_zero(octant, x, y):
   if octant == 0: return (x, y)
   if octant == 1: return (y, x)
   if octant == 2: return (y, -x)
   if octant == 3: return (-x, y)
   if octant == 4: return (-x, -y)
   if octant == 5: return (-y, -x)
   if octant == 6: return (-y, x)
   if octant == 7: return (x, -y)

def switch_octant_from_zero(octant, x, y):
   if octant == 0: return (x, y)
   if octant == 1: return (y, x)
   if octant == 2: return (-y, x)
   if octant == 3: return (-x, y)
   if octant == 4: return (-x, -y)
   if octant == 5: return (-y, -x)
   if octant == 6: return (y, -x)
   if octant == 7: return (x, -y)

def get_octant(A, B):
    dx, dy = B[0] - A[0], B[1] - A[1]
    octant = 0
    if dy < 0:
        dx, dy = -dx, -dy  # rotate by 180 degrees
        octant += 4
    if dx < 0:
        dx, dy = dy, -dx  # rotate clockwise by 90 degrees
        octant += 2
    if dx < dy:
        # no need to rotate now
        octant += 1
    return octant

def bresenham(point1, point2, gridSize=100):
    x1, y1 = (int(point1[0] / gridSize), int(point1[1] / gridSize))
    x2, y2 = (int(point2[0] / gridSize), int(point2[1] / gridSize))
    dx = x2 - x1
    dy = y2 - y1

    # Determine how steep the line is
    is_steep = abs(dy) > abs(dx)

    # Rotate line
    if is_steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    # Swap start and end points if necessary and store swap state
    swapped = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        swapped = True

    # Recalculate differentials
    dx = x2 - x1
    dy = y2 - y1

    # Calculate error
    error = int(dx / 2.0)
    ystep = 1 if y1 < y2 else -1

    # Iterate over bounding box generating points between start and end
    y = y1
    points = []
    for x in range(x1, x2 + 1):
        coord = (y, x) if is_steep else (x, y)
        points.append(coord)

        coord = (y, x + 1) if is_steep else (x, y + 1)
        points.append(coord)

        coord = (y, x - 1) if is_steep else (x, y - 1)
        points.append(coord)

        error -= abs(dy)
        if error < 0:
            y += ystep
            error += dx
    return points