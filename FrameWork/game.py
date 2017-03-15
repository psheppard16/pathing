__author__ = 'Preston Sheppard'
from FrameWork.Screens.screenEngine import ScreenEngine
from FrameWork.FrameRate.frameRateEngine import FrameRateEngine
from FrameWork.SaveFiles.saveEngine import SaveEngine
from FrameWork.Window.window import Window
from Game.gameEngine import GameEngine
from Game.drawingEngine import DrawingEngine
from Game.GameObjects.gameObject import GameObject
class Game:
    def __init__(self):
        #initializing all the screens and engines that run the game

        #do not remove anything
        self.window = Window(self)
        self.frameRateEngine = FrameRateEngine(self)
        self.saveEngine = SaveEngine()
        self.gameEngine = GameEngine(self)
        self.drawingEngine = DrawingEngine(self)
        self.screenEngine = ScreenEngine(self)

        self.window.root.after(1, self.loop)
        self.window.root.mainloop()


    def loop(self):
        '''
        The main loop for game, runs continually
        and in turn runs, screenEngine, drawingEngine,
        gameEngine, frameRateEngine, and saveEngine
        :return: None
        '''
        while True:
            if self.frameRateEngine.canRun():
                self.screenEngine.run()
                self.window.run()
                self.frameRateEngine.run()

                if self.screenEngine.cMenu == "gameEngine":
                    self.window.root.focus_force()
                    self.gameEngine.run()
                    for object in GameObject.gameObjectList:
                        object.run(self.gameEngine)
                    self.drawingEngine.render()