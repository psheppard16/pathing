__author__ = 'Preston Sheppard'
import random
import Pathing.pathing as pathing
from Pathing.pathing import Path
import json
import time as tm

class GameEngine:
    def __init__(self, game):
        self.game = game
        self.startPoint = (500, 500)
        self.endPoint = (100, 500)
        self.wallList = []
        self.indent = 20

        if self.game.saveEngine.save.wallType == "basic":
            wall = ((150, 300), (300, 150))
            self.wallList.append(wall)
            wall = ((300, 150), (400, 150))
            self.wallList.append(wall)
            wall = ((450, 150), (700, 150))
            self.wallList.append(wall)
            wall = ((300, 500), (400, 230))
            self.wallList.append(wall)
            wall = ((750, 500), (800, 400))
            self.wallList.append(wall)
            wall = ((750, 500), (820, 900))
            self.wallList.append(wall)
            wall = ((600, 400), (500, 300))
            self.wallList.append(wall)
            wall = ((800, 300), (500, 300))
            self.wallList.append(wall)

            wall = ((self.indent, self.indent), (self.game.window.width - self.indent, self.indent)) #these walls bound the screen
            self.wallList.append(wall)
            wall = ((self.game.window.width - self.indent, self.indent), (self.game.window.width - self.indent, self.game.window.height - self.indent))
            self.wallList.append(wall)
            wall = ((self.game.window.width - self.indent, self.game.window.height - self.indent), (self.indent, self.game.window.height - self.indent))
            self.wallList.append(wall)
            wall = ((self.indent, self.game.window.height - self.indent), (self.indent, self.indent))
            self.wallList.append(wall)
        elif self.game.saveEngine.save.wallType == "maze":
            self.wallList = json.load(open("Maze/maze.json"))
            for index, wall in enumerate(self.wallList):
                self.wallList[index] = ((wall[0][0], wall[0][1]), (wall[1][0], wall[1][1]))
        elif self.game.saveEngine.save.wallType == "random":
            # for i in range(5):
            #     x1 = random.randint(0, 1000)
            #     y1 = random.randint(0, 1000)
            #     x2 = random.randint(0, 1000)
            #     y2 = random.randint(0, 1000)
            #     wall = ((x1, y1), (x2, y2))
            #     self.wallList.append(wall)

            offset = 500
            wall1 = ((offset + 0, offset + 0), (offset + 100, offset + 0))
            if random.random() > .5:
                self.wallList.append(wall1)

            wall2 = ((offset + 0, offset + 0), (offset + 100, offset + 100))
            if random.random() > .5:
                self.wallList.append(wall2)

            wall3 = ((offset + 0, offset + 0), (offset + 0, offset + 100))
            if random.random() > .5:
                self.wallList.append(wall3)

            wall4 = ((offset + 0, offset + 0), (offset - 100, offset + 100))
            if random.random() > .5:
                self.wallList.append(wall4)

            wall5 = ((offset + 0, offset + 0), (offset - 100, offset + 0))
            if random.random() > .5:
                self.wallList.append(wall5)

            wall6 = ((offset + 0, offset + 0), (offset - 100, offset - 100))
            if random.random() > .5:
                self.wallList.append(wall6)

            wall7 = ((offset + 0, offset + 0), (offset + 0, offset - 100))
            if random.random() > .5:
                self.wallList.append(wall7)

            wall8 = ((offset + 0, offset + 0), (offset + 100, offset - 100))
            if random.random() > .5:
                self.wallList.append(wall8)

        self.endTime = None
        self.times = []

        self.zones = {}
        zoneSize = 100
        for wall in self.wallList:
            bPoints = bresenham(wall[0], wall[1])
            for point in bPoints:
                    if point in self.zones:
                        self.zones[point].append(wall)
                    else:
                        self.zones[point] = [wall]



        self.fullPath = []
        self.nodes = pathing.generateNodes(self.startPoint, self.endPoint, self.wallList)
        self.paths = []
        self.paths.extend([Path(self.startPoint, None, self.endPoint, self.nodes, self.wallList, self.paths, self.zones)])

    def run(self):
        mouseX = self.game.window.root.winfo_pointerx() - self.game.window.root.winfo_rootx()
        if mouseX > self.game.window.width - self.indent - 1:
            mouseX = self.game.window.width - self.indent - 1
        if mouseX < self.indent + 1:
            mouseX = self.indent + 1
        mouseY = self.game.window.height - (self.game.window.root.winfo_pointery() - self.game.window.root.winfo_rooty())
        if mouseY > self.game.window.height - self.indent - 1:
            mouseY = self.game.window.height - self.indent - 1
        if mouseY < self.indent + 1:
            mouseY = self.indent + 1
        if self.game.saveEngine.saveNumber == 0:
            self.startTime = self.game.frameRateEngine.getTime()
            while self.game.frameRateEngine.getTime() - self.startTime < 1 / 30:
                finalPath = pathing.addPaths(self.paths)
                if finalPath:
                    fullPath = []
                    focus = finalPath
                    while focus:
                        fullPath.append(focus.location)
                        focus = focus.creator
                    self.fullPath = fullPath
                    self.endPoint = (mouseX, mouseY)
                    self.endTime = self.game.frameRateEngine.getTime()
                    time = self.endTime - self.startTime
                    self.times.append(time)
                    sum = 0
                    for time in self.times:
                        sum += time
                    average = sum / len(self.times)
                    print(self.times[-1], average)
                    self.startTime = self.game.frameRateEngine.getTime()

                    self.nodes = pathing.generateNodes(self.startPoint, self.endPoint, self.wallList)
                    self.paths = []
                    self.paths.extend([Path(self.startPoint, None, self.endPoint, self.nodes, self.wallList, self.paths, self.zones)])
                    break
        elif self.game.saveEngine.saveNumber == 1:
            startTime = self.game.frameRateEngine.getTime()
            self.fullPath = pathing.findPath(self.startPoint, self.endPoint, self.wallList)
            self.endPoint = (mouseX, mouseY)
            endTime = self.game.frameRateEngine.getTime()
            print("Time:", endTime - startTime)

    def keyReleased(self, event):
        if event.keysym == "a":
            print("a key pressed")

    def keyPressed(self, event):
        if event.keysym == "a":
            print("a key released")

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

        error -= abs(dy)
        if error < 0:
            coord = (y, x + 1) if is_steep else (x + 1, y)
            points.append(coord)
            y += ystep
            coord = (y, x) if is_steep else (x, y)
            points.append(coord)
            error += dx
    return points


