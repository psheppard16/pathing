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
        self.showCircle((self.game.gameEngine.endPoint[0], self.game.gameEngine.endPoint[1]), 15, (0, 255, 0),
                        shiftPosition=True)
        self.showCircle((self.game.gameEngine.startPoint[0], self.game.gameEngine.startPoint[1]),
                        15, (0, 255, 0), shiftPosition=True)

        valid = circleFlood(self.game.gameEngine.endPoint, self.game.gameEngine.zones)
        if valid:
            for point, walls in valid.items():
                if walls:
                    self.showRectangle((point[0] * 10 - 5, point[1] * 10 - 5), (point[0] * 10 + 5, point[1] * 10 + 5),
                                   (0, 255, 0), shiftPosition=True, secondaryColor=(0, 0, 0), width=2)
                else:
                    self.showRectangle((point[0] * 10 - 5, point[1] * 10 - 5), (point[0] * 10 + 5, point[1] * 10 + 5),
                                   (255, 0, 0), shiftPosition=True, secondaryColor=(0, 0, 0), width=2)


        for wall in self.game.gameEngine.wallList:
            self.showLine(wall[0], wall[1], (0, 0, 0), 5, shiftPosition=True, rounded=True)

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

def bresenham(point1, point2, gridSize=10):
    x1, y1 = (int(round(point1[0] / gridSize)), int(round(point1[1] / gridSize)))
    x2, y2 = (int(round(point2[0] / gridSize)), int(round(point2[1] / gridSize)))
    dx = x2 - x1
    dy = y2 - y1

    # Determine how steep the line is
    is_steep = abs(dy) > abs(dx)

    # Rotate line
    if is_steep:
        x1, y1, x2, y2 = y1, x1, y2, x2

    # Swap start and end points if necessary and store swap state
    if x1 > x2:
        x1, x2, y1, y2 = x2, x1, y2, y1

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

        error -= abs(dy)
        if error < 0:
            coord = (y, x + 1) if is_steep else (x + 1, y)
            points.append(coord)
            y += ystep
            coord = (y, x) if is_steep else (x, y)
            points.append(coord)
            error += dx
    return points

def getLastBresenham(start, end):
    x1, y1 = start
    x2, y2 = end
    dx = x2 - x1
    dy = y2 - y1

    # Determine how steep the line is
    is_steep = abs(dy) > abs(dx)

    # Rotate line
    if is_steep:
        x1, y1, x2, y2 = y1, x1, y2, x2

    # Swap start and end points if necessary and store swap state
    if x1 > x2:
        x1, x2, y1, y2 = x2, x1, y2, y1

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

        error -= abs(dy)
        if error < 0:
            y += ystep
            error += dx
    if points[0] == end:
        return points[1:4]
    elif points[0] == start:
        return points[-5:-2]
    raise Exception("could not find last")

def circleFlood(point, zones, gridSize=10, maxLayers=35):
    start = (int(round(point[0] / gridSize)), int(round(point[1] / gridSize)))
    layer = 0
    valid = {}
    valid[start] = None
    added = True
    while added:
        added = False
        layer += 1
        if layer > maxLayers:
            break
        for i in range(-layer, layer + 1):
            for j in range(-layer, layer + 1):
                if abs(i) == layer or abs(j) == layer:
                    square = (start[0] + i, start[1] + j)
                    pixels = getLastBresenham(start, square)
                    offLine = 0
                    containsWall = 0
                    for toCheck in pixels:
                        if toCheck not in valid:
                            offLine += 1
                        elif valid[toCheck]:
                            containsWall += 1
                    if offLine == 0:
                        if square in zones:
                            added = True
                            valid[square] = zones[square]
                        elif containsWall == 0:
                            added = True
                            valid[square] = []
                    elif containsWall >= 2:
                        if square in zones:
                            valid[square] = zones[square]
    return valid

def drawcircle(center, radius, gridSize=10):
    x0, y0 = (int(round(center[0] / gridSize)), int(round(center[1] / gridSize)))
    x = radius
    y = 0
    err = 0
    pixels = []
    while x >= y:
        pixels.append((x0 + x, y0 + y))
        pixels.append((x0 + y, y0 + x))
        pixels.append((x0 - y, y0 + x))
        pixels.append((x0 - x, y0 + y))
        pixels.append((x0 - x, y0 - y))
        pixels.append((x0 - y, y0 - x))
        pixels.append((x0 + y, y0 - x))
        pixels.append((x0 + x, y0 - y))

        if err <= 0:
            y += 1
            err += 2*y + 1
        if err > 0:
            x -= 1
            err -= 2*x + 1
    return pixels

