__author__ = 'Preston Sheppard'
from tkinter import *
from FrameWork.Screens.screen import Screen
class MainMenu(Screen):
    def __init__(self, game):
        super().__init__(game, "mainMenu")
        self.startB = Button(self.game.window.root, text="Start", command=self.start, bg="#%02x%02x%02x" % (255, 165, 0), font="Helvetica 15 bold", padx=10, pady=10)
        self.startB.pack(in_=self.f, pady=15)

        self.instructionsB = Button(self.game.window.root, text="Instructions", command=self.instructions, bg="#%02x%02x%02x" % (255, 165, 0), font="Helvetica 15 bold", padx=10, pady=10)
        self.instructionsB.pack(in_=self.f, pady=15)

        self.optionsB = Button(self.game.window.root, text="Options", command=self.options, bg="#%02x%02x%02x" % (255, 165, 0), font="Helvetica 15 bold", padx=10, pady=10)
        self.optionsB.pack(in_=self.f, pady=15)

        self.quitB = Button(self.game.window.root, text="Quit", command=self.quit, bg="#%02x%02x%02x" % (255, 0, 0), font="Helvetica 15 bold", padx=10, pady=10)
        self.quitB.pack(in_=self.f, pady=15)

    def quit(self):
        self.game.window.root.destroy()

    def options(self):
        self.game.screenEngine.rMenu = "options"

    def start(self):
        self.game.screenEngine.rMenu = "gameEngine"

    def instructions(self):
        self.game.screenEngine.rMenu = "instructions"