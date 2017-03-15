__author__ = 'Preston Sheppard'
import tkinter
class Window:
    def __init__(self, game):
        self.game = game

        self.width = 1280
        self.height = 720

        #setting up the default settings for window
        self.root = tkinter.Tk()
        self.root.title("Red Shooter")
        self.root.geometry("1280x720")
        self.root.resizable(False, False)
        self.root.bind_all('<KeyPress>', self.keyPressed)
        self.root.bind_all('<KeyRelease>', self.keyReleased)


    def run(self):
        '''
        The main loop for window, runs continually
        and in turn runs, screenEngine, drawingEngine,
        gameEngine, frameRateEngine, and saveEngine
        :return: None
        '''
        self.changeWindowSize(self.game.saveEngine.save.resolution)
        self.root.update()

    def changeWindowSize(self, resolution):
        '''
        takes a resolution in form: "16x9", and if the
        resolution is different from the current resolution,
        it changes the window and screen sizes
        :param resolution: the requested resolution
        :return: None
        '''
        if str(self.width) + 'x' + str(self.height) != self.game.saveEngine.save.resolution:
            self.root.geometry(resolution)
            self.width = self.root.winfo_width()
            self.height = self.root.winfo_height()
            self.game.screenEngine.updateScreens(self.width, self.height)


    def keyPressed(self, event):
        '''
        passes the keyPressed command onto gameEngine for convenience
        :param event: the event object
        :return: None
        '''
        if event.keysym == "Escape":
            self.root.destroy()
        try:
            self.game.gameEngine.keyPressed(event)
        except AttributeError:
            pass

    def keyReleased(self, event):
        '''
        passes the keyReleased command onto gameEngine for convenience
        :param event: the event object
        :return: None
        '''
        try:
            self.game.gameEngine.keyReleased(event)
        except AttributeError:
            pass