__author__ = 'Preston Sheppard'
from tkinter import *
from FrameWork.Screens.screen import Screen
import json
import Maze.gridSquare as gs

class Options(Screen):
    def __init__(self, game):
        super().__init__(game, "options")
        self.resolutionF = StringVar()
        self.resolutionF.set("Resolution: " + self.game.saveEngine.save.resolution)
        self.resolutionB = Button(self.game.window.root, textvariable=self.resolutionF, command=self.resolution,
                                  bg="#%02x%02x%02x" % (255, 165, 0), font="Helvetica 15 bold", padx=10, pady=10)
        self.resolutionB.pack(in_=self.f, pady=15)

        self.generateB = Button(self.game.window.root, text="Generate New Maze", command=self.generate,
                                  bg="#%02x%02x%02x" % (255, 165, 0), font="Helvetica 15 bold", padx=10, pady=10)
        self.generateB.pack(in_=self.f, pady=15)

        self.mazeSizeL = Label(self.game.window.root, text="Maze Size", bg="#%02x%02x%02x" % (255, 165, 0),
                               font="Helvetica 15 bold", padx=10, pady=10)
        self.mazeSizeL.pack(in_=self.f)
        self.mazeSizeB = Spinbox(self.game.window.root, from_=1, to=5, state="readonly", bg="#%02x%02x%02x" % (255, 165, 0),
                                 font="Helvetica 15 bold")
        self.mazeSizeB.delete(0, "end")
        self.mazeSizeB.pack(in_=self.f)

        self.wallTypeF = StringVar()
        self.wallTypeF.set("Wall Type: " + self.game.saveEngine.save.wallType)
        self.wallTypeB = Button(self.game.window.root, textvariable=self.wallTypeF, command=self.wallType,
                                bg="#%02x%02x%02x" % (255, 165, 0), font="Helvetica 15 bold", padx=10, pady=10)
        self.wallTypeB.pack(in_=self.f, pady=15)

        self.frameF = StringVar()
        if self.game.saveEngine.save.smoothFrames == True:
            self.frameF.set("Smoothed framerate on")
        else:
            self.frameF.set("Smoothed framerates off")
        self.frameB = Button(self.game.window.root, textvariable=self.frameF, command=self.frame,
                             bg="#%02x%02x%02x" % (255, 165, 0), font="Helvetica 15 bold", padx=10, pady=10)
        self.frameB.pack(in_=self.f, pady=15)

        self.accept = Button(self.game.window.root, text="Accept", command=self.accept,
                             bg="#%02x%02x%02x" % (255, 165, 0), font="Helvetica 15 bold", padx=10, pady=10)
        self.accept.pack(in_=self.f, pady=15)

        self.quitB = Button(self.game.window.root, text="Quit", command=self.quit, bg="#%02x%02x%02x" % (255, 0, 0),
                            font="Helvetica 15 bold", padx=10, pady=10)
        self.quitB.pack(in_=self.f, pady=15)

    def quit(self):
        self.game.window.root.destroy()

    def generate(self):
        indent = self.game.gameEngine.indent / 2
        walls = gs.generateSquareMaze(16 * int(self.mazeSizeB.get()), 9 * int(self.mazeSizeB.get()), (self.game.window.height - indent) / 9 / int(self.mazeSizeB.get()), location=(indent/2, indent/2))
        with open('Maze/maze.json', 'w') as outfile:
            json.dump(walls, outfile)

    def setUp(self):
        if self.game.saveEngine.save.smoothFrames == True:
            self.frameF.set("Smoothed framerate on")
        else:
            self.frameF.set("Smoothed framerate off")

        self.resolutionF.set("Resolution: " + self.game.saveEngine.save.resolution)

        self.mazeSizeB.delete(0, "end")
        self.mazeSizeB.insert(0, self.game.saveEngine.save.mazeSize)

        self.wallTypeF.set("Wall Type: " + self.game.saveEngine.save.wallType)

        self.f.pack(side=LEFT)

    def accept(self):
        self.game.saveEngine.save.mazeSize = int(self.mazeSizeB.get())
        self.game.saveEngine.saveCharacter(self.game.saveEngine.saveNumber)
        self.game.screenEngine.rMenu = "mainMenu"

    def wallType(self):
        if self.game.saveEngine.save.wallType == "maze":
            self.game.saveEngine.save.wallType = "basic"
            self.wallTypeF.set("Wall Type: " + "Basic")
        elif self.game.saveEngine.save.wallType == "basic":
            self.game.saveEngine.save.wallType = "random"
            self.wallTypeF.set("Wall Type: " + "Random")
        elif self.game.saveEngine.save.wallType == "random":
            self.game.saveEngine.save.wallType = "maze"
            self.wallTypeF.set("Wall Type: " + "Maze")

    def resolution(self):
        if self.game.saveEngine.save.resolution == "1280x720":
            self.game.saveEngine.save.resolution = "1366x768"
            self.resolutionF.set("Resolution: " + "1366x768")
        elif self.game.saveEngine.save.resolution == "1366x768":
            self.game.saveEngine.save.resolution = "1600x900"
            self.resolutionF.set("Resolution: " + "1600x900")
        elif self.game.saveEngine.save.resolution == "1600x900":
            self.game.saveEngine.save.resolution = "1920x1080"
            self.resolutionF.set("Resolution: " + "1920x1080")
        elif self.game.saveEngine.save.resolution == "1920x1080":
            self.game.saveEngine.save.resolution = "2048x1152"
            self.resolutionF.set("Resolution: " + "2048x1152")
        elif self.game.saveEngine.save.resolution == "2048x1152":
            self.game.saveEngine.save.resolution = "2560x1440"
            self.resolutionF.set("Resolution: " + "2560x1440")
        elif self.game.saveEngine.save.resolution == "2560x1440":
            self.game.saveEngine.save.resolution = "1280x720"
            self.resolutionF.set("Resolution: " + "1280x720")

    def frame(self):
        if self.game.saveEngine.save.smoothFrames:
            self.game.saveEngine.save.smoothFrames = False
            self.frameF.set("Smoothed framerate off")
        else:
            self.game.saveEngine.save.smoothFrames = True
            self.frameF.set("Smoothed framerate on")
