from tkinter import *
from FrameWork.Screens.screen import Screen
class SaveScreen(Screen):
    def __init__(self, game):
        super().__init__(game, "saveScreen")
        self.save1B = Button(self.game.window.root, text="Debug", command=self.save1, bg="#%02x%02x%02x" % (255, 165, 0), font="Helvetica 15 bold", padx=10, pady=10)
        self.save1B.pack(in_=self.f, pady=25)

        self.save2B = Button(self.game.window.root, text="Final path", command=self.save2, bg="#%02x%02x%02x" % (255, 165, 0), font="Helvetica 15 bold", padx=10, pady=10)
        self.save2B.pack(in_=self.f, pady=25)

        self.save3B = Button(self.game.window.root, text="Generate map", command=self.save3, bg="#%02x%02x%02x" % (255, 165, 0), font="Helvetica 15 bold", padx=10, pady=10)
        self.save3B.pack(in_=self.f, pady=25)

        self.resetB = Button(self.game.window.root, text="reset saves", command=self.resetSaves, bg="#%02x%02x%02x" % (255, 165, 0), font="Helvetica 15 bold", padx=10, pady=10)
        self.resetB.pack(in_=self.f, pady=25)

        self.cancel = Button(self.game.window.root, text="Cancel", command=self.cancel, bg="#%02x%02x%02x" % (255, 165, 0), font="Helvetica 15 bold", padx=10, pady=10)
        self.cancel.pack(in_=self.f, pady=25)

    def save1(self):
        self.game.saveEngine.loadChar(0)
        self.game.screenEngine.rMenu = "mainMenu"

    def save2(self):
        self.game.saveEngine.loadChar(1)
        self.game.screenEngine.rMenu = "mainMenu"

    def save3(self):
        self.game.saveEngine.loadChar(2)
        self.game.screenEngine.rMenu = "mainMenu"

    def resetSaves(self):
        self.game.saveEngine.resetSaves()

    def cancel(self):
        self.game.screenEngine.rMenu = "startScreen"