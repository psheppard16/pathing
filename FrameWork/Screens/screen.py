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
        """
        Sets the width and height of the frame
        :param width: the desired width of the frame
        :param height: the desired height of the frame
        :return: None
        """
        self.f.config(width=width, height=height)

    def setUp(self):
        """
        Sets up the background label, which contains the background
        color or image, and packs the frame
        :return: None
        """
        if self.hasBackground:
            self.backgroundLabel.place(x=0, y=0, relwidth=1, relheight=1)
        self.f.pack(side=LEFT)

    def hide(self):
        """
        Removes the background label and hides the frame
        :return: None
        """
        if self.hasBackground:
            self.backgroundLabel.place(x=10000, y=10000, relwidth=1, relheight=1)
        self.f.pack_forget()
