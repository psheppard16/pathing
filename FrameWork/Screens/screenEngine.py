__author__ = 'Preston Sheppard'
from Game.gameEngine import GameEngine
from FrameWork.Screens.screen import Screen
from FrameWork.Screens.options import Options
from FrameWork.Screens.mainMenu import MainMenu
from FrameWork.Screens.instructions import Instructions
from FrameWork.Screens.saveScreen import SaveScreen
from FrameWork.Screens.startScreen import StartScreen
from Game.GameObjects.gameObject import GameObject
class ScreenEngine:
    def __init__(self, game):
        self.game = game
        self.cMenu = "null"
        self.rMenu = "startScreen"
        StartScreen(self.game)
        Instructions(self.game)
        Options(self.game)
        MainMenu(self.game)
        SaveScreen(self.game)

    def run(self):
        self.switchScreen()

    def switchScreen(self):
        if self.cMenu != self.rMenu:
            self.updateScreens(self.game.window.width, self.game.window.height)
            self.clearWindow()
            switchedScreen = False
            for screen in Screen.screenList:
                if self.rMenu == screen.name:
                    switchedScreen = True
                    screen.setUp()
                    break
            if self.rMenu == "gameEngine":
                GameObject.gameObjectList.clear()
                self.game.gameEngine = GameEngine(self.game)
                switchedScreen = True
            if switchedScreen:
                self.cMenu = self.rMenu
            else:
                raise Exception("Screen name not found")

    def clearWindow(self):
        for screen in Screen.screenList:
            screen.hide()

    def updateScreens(self, width, height):
        for screen in Screen.screenList:
            screen.update(width, height)