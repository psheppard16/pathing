__author__ = 'Preston Sheppard'
from tkinter import *
from FrameWork.Screens.screen import Screen
class Instructions(Screen):
    def __init__(self, game):
        super().__init__(game, "instructions")
        instructions = """Objective:
This project is a simple implementation of a pathing algorithm
Display:
The thick orange line is either the final path, or the current fastest path that the
algorithm has found
Red Lines are lines that have not advanced, branched, or backtracked
Blue lines have advanced, but have not branched or backtracked
Green lines have advanced and branched, but have not backtracked
White lines have advanced, branched, and backtracked. All lines eventually turn white
Controls:
Move the mouse around to change the location to path to
"""

        self.descriptionL = Label(self.game.window.root, text=instructions, justify=CENTER, bg="#%02x%02x%02x" % (121, 202, 249), compound=CENTER, wraplength=self.game.window.width // 1.25, font="Helvetica 15 bold")
        self.descriptionL.pack(in_=self.f, side=TOP, pady=10)

        self.cancel = Button(self.game.window.root, text="Cancel", command=self.cancel, bg="#%02x%02x%02x" % (255, 165, 0), font="Helvetica 15 bold", padx=10, pady=10)
        self.cancel.pack(in_=self.f, pady=15)

        self.quitB = Button(self.game.window.root, text="Quit", command=self.quit, bg="#%02x%02x%02x" % (255, 0, 0), font="Helvetica 15 bold", padx=10, pady=10)
        self.quitB.pack(in_=self.f, pady=15)

    def quit(self):
        self.game.window.root.destroy()

    def cancel(self):
        if self.game.saveEngine.saveSelected:
            self.game.screenEngine.rMenu = "mainMenu"
        else:
            self.game.screenEngine.rMenu = "startScreen"
