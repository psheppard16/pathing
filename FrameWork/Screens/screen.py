__author__ = 'Preston Sheppard'
from tkinter import *
from PIL import ImageTk
class Screen:
    screenList = []
    def __init__(self, game, name, backgroundPath="none"):
        self.game = game

        self.name = name

        self.f = Frame(self.game.window.root, bg="blue", width=self.game.window.width, height=self.game.window.width)
        self.f.pack_propagate(0)

        if backgroundPath == "none":
            self.hasBackground = False
        else:
            self.hasBackground = True
            self.backgroundImage= ImageTk.PhotoImage(file=backgroundPath)
            self.backgroundLabel = Label(self.game.window.root, image=self.backgroundImage)
        Screen.screenList.append(self)

    def update(self, width, height):
        self.f.config(width=width, height=height)

    def setUp(self):
        if self.hasBackground:
            self.backgroundLabel.place(x=0, y=0, relwidth=1, relheight=1)
        self.f.pack(side=LEFT)

    def hide(self):
        if self.hasBackground:
            self.backgroundLabel.place(x=10000, y=10000, relwidth=1, relheight=1)
        self.f.pack_forget()
