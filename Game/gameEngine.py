__author__ = 'Preston Sheppard'
import random
import Pathing.pathing as pathing
from Pathing.pathing import Path
import json
import time as tm

class GameEngine:
    def __init__(self, game):
        self.game = game
        self.startPoint = (50, 50)
        self.endPoint = (100, 500)
        self.fullPath = []
        self.wallList = []
        self.nodes = []

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


        self.nodes = pathing.generateNodes(self.startPoint, self.endPoint, self.wallList)
        self.paths = []
        self.paths.extend([Path(self.startPoint, None, self.endPoint, self.nodes, self.paths), Path(self.endPoint, None, self.startPoint, self.nodes, self.paths)])
        self.finalPath = None

    def run(self):
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
                    self.paths.extend([Path(self.startPoint, None, self.endPoint, self.nodes, self.paths), Path(self.endPoint, None, self.startPoint, self.nodes, self.paths)])
                    break
        elif self.game.saveEngine.saveNumber == 1:
            startTime = self.game.frameRateEngine.getTime()
            self.fullPath = pathing.findPath(self.startPoint, self.endPoint, self.wallList)
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
            self.endPoint = (mouseX, mouseY)
            endTime = self.game.frameRateEngine.getTime()
            print("Time:", endTime - startTime)

    def keyReleased(self, event):
        if event.keysym == "a":
            print("a key pressed")

    def keyPressed(self, event):
        if event.keysym == "a":
            print("a key released")




