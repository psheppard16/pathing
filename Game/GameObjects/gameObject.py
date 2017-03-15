__author__ = 'Preston Sheppard'
import math
from abc import ABCMeta, abstractmethod
class GameObject(metaclass=ABCMeta):
    gameObjectList = []
    def __init__(self, game, x, y, xVel=0, yVel=0, layer=0):
        #import is called on init to avoid circular imports
        from FrameWork.game import Game

        #formatting errors
        if not isinstance(game, Game):
            raise Exception(str(game) + " is not an instance of the class Game. You must provide a game object")
        if layer < 0 or not isinstance(layer, int):
            raise Exception("layer must be a positive integer")
        if not isinstance(x, int) and not isinstance(x, float):
            raise Exception("x position must be a number")
        if not isinstance(y, int) and not isinstance(y, float):
            raise Exception("y position must be a number")
        if not isinstance(xVel, int) and not isinstance(xVel, float):
            raise Exception("x velocity must be a number")
        if not isinstance(yVel, int) and not isinstance(yVel, float):
            raise Exception("y velocity must be a number")

        #game is required in order to have access to the framerate
        self.game = game

        #initializing variables
        self.xVel = xVel
        self.yVel = yVel
        self.x = x
        self.y = y
        self.xForce = 0
        self.yForce = 0

        #layer is the layer in which an object is drawn on the canvas
        #low numbers are drawn first
        self.layer = layer

        #game objects add themselves to the gameObjectList for convenience
        GameObject.gameObjectList.append(self)

    def move(self):
        """
        move calculates the objects new position and applies
        forces correctly
        :return: None
        """
        self.x += self.getXDisplacement(self.game.frameRateEngine.tickSpeed)
        self.y += self.getYDisplacement(self.game.frameRateEngine.tickSpeed)
        self.xVel += self.xForce * self.game.frameRateEngine.tickSpeed
        self.yVel += self.yForce * self.game.frameRateEngine.tickSpeed
        self.xForce = 0
        self.yForce = 0

    def accelerate(self, xForce, yForce):
        """
        Applies a force to the object which changes its
        x and y velocities
        :param xForce: the x component of the force
        :param yForce: the y component of the force
        :return:
        """
        if not isinstance(xForce, int) and not isinstance(xForce, float):
            raise Exception("x force must be a number")
        if not isinstance(yForce, int) and not isinstance(yForce, float):
            raise Exception("y force must be a number")
        self.xForce += xForce
        self.yForce += yForce

    def setSpeed(self, xVel, yVel):
        """
        sets the velocity of the object
        :param xVel: the new x velocity
        :param yVel: the new y velocity
        :return: None
        """
        if not isinstance(xVel, int) and not isinstance(xVel, float):
            raise Exception("x velocity must be a number")
        if not isinstance(yVel, int) and not isinstance(yVel, float):
            raise Exception("y velocity must be a number")
        self.yVel = yVel
        self.xVel = xVel

    def setPosition(self, xPos, yPos):
        """
        sets the position of an object
        :param xPos: the new x position
        :param yPos: the new y position
        :return: None
        """
        if not isinstance(xPos, int) and not isinstance(xPos, float):
            raise Exception("x position must be a number")
        if not isinstance(yPos, int) and not isinstance(yPos, float):
            raise Exception("y position must be a number")
        self.x = xPos
        self.y = yPos

    def shiftPosition(self, xShift, yShift):
        """
        shifts the position of an object by a desired amount
        :param xShift: the shift in the x direction
        :param yShift: the shift in the y direction
        :return: None
        """
        if not isinstance(xShift, int) and not isinstance(xShift, float):
            raise Exception("x shift must be a number")
        if not isinstance(yShift, int) and not isinstance(yShift, float):
            raise Exception("y shift must be a number")
        self.x += xShift
        self.y += yShift

    def getXVel(self):
        """
        gets the x velocity
        :return: the x velocity
        """
        return self.xVel

    def getYVel(self):
        """
        gets the y velocity
        :return: the y velocity
        """
        return self.yVel

    def getSpeed(self):
        """
        gets the speed of the object
        :return: the speed of the object
        """
        return math.sqrt(self.yVel ** 2 + self.xVel ** 2)

    def getXDisplacement(self, seconds):
        """
        This method predicts the x displacement of the object based on the
        current forces that are being applied
        :param seconds: number of seconds ahead the prediction is
        :return: the x displacement
        """
        if not isinstance(seconds, int) and not isinstance(seconds, float):
            raise Exception("seconds must be a number")
        return self.getXVel() * seconds + math.copysign(.5 * self.xForce * seconds ** 2, self.xForce)

    def getYDisplacement(self, seconds):
        """
        This method predicts the y displacement of the object based on the
        current forces that are being applied
        :param seconds: number of seconds ahead the prediction is
        :return: the y displacement
        """
        if not isinstance(seconds, int) and not isinstance(seconds, float):
            raise Exception("seconds must be a number")
        return self.getYVel() * seconds + math.copysign(.5 * self.yForce * seconds ** 2, self.yForce)

    def getAngle(self):
        """
        gets the angle that the object is traveling
        :return: the angle in radians
        """
        return math.atan2(self.getYVel(), self.getXVel())

    def distanceToSelf(self, x, y):
        """
        calculates how far away a point is from this object
        :param x: x location of the point
        :param y: y location of the point
        :return: the distance
        """
        if not isinstance(x, int) and not isinstance(x, float):
            raise Exception("x position must be a number")
        if not isinstance(y, int) and not isinstance(y, float):
            raise Exception("y position must be a number")
        xD = self.x - x
        yD = self.y - y
        return math.sqrt(xD ** 2 + yD ** 2)

    @abstractmethod
    def draw(self, drawingEngine):
        """
        for every gameObject, draw is called every tick by the CanvasObject class automatically.
        Layering and order are also carried out automatically, with every non-gameObject
        being drawn in a single layer, (specified by the user in drawingEngine). The method
        draws a red circle of radius 100 by default.

        THIS METHOD MUST BE OVERWRITTEN

        :param drawingEngine: the drawingEngine created by game
        :return: None
        """
        drawingEngine.showCircle((self.x, self.y), 100, (255, 0, 0))

    @abstractmethod
    def run(self, gameEngine):
        """
        for every gameObject, run is called every tick by the Game class automatically.
        They are run in an arbitrary order strictly after gameEngines run command is called.
        The method calls move by default

        THIS METHOD MUST BE OVERWRITTEN

        :param gameEngine: the gameEngine created by game
        :return: None
        """
        self.move()