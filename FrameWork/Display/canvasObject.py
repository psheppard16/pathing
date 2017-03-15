import math
from PIL import Image, ImageTk
import PIL

try:
    import pygame
except:
    pass
from tkinter import Canvas, NW
import os
import platform
from FrameWork.Screens.screen import Screen
from Game.GameObjects.gameObject import GameObject
from abc import ABCMeta, abstractmethod


class CanvasObject(Screen, metaclass=ABCMeta):
    def __init__(self, game):
        super().__init__(game, "gameEngine")
        os.environ['SDL_WINDOWID'] = str(self.f.winfo_id())
        if False:# platform.system() == "Windows":
            os.environ['SDL_VIDEODRIVER'] = 'windib'
            self.usePygame = True
            self.display = pygame.display.set_mode((self.game.window.width, self.game.window.height))
            self.display.fill((255, 255, 255))
            pygame.display.init()
            pygame.font.init()
        else:
            self.usePygame = False
            self.canvas = Canvas(self.game.window.root, bg="white", width=self.game.window.width,
                                 height=self.game.window.height)
            self.canvas.pack(in_=self.f)

        self.customDrawLayer = None
        self.backgroundColor = (121, 202, 249)
        self.tkImageList = []  # images must maintain a reference in order to appear on the canvas

    def render(self):
        """
        Clears screen
        draws all gameObjects at the appropriate layer,
        and then calls the draw method at the customDrawLayer,
        or last if not specified
        updates the canvas depending on whether using pygame
        :return: None
        """
        self.clear()
        self.game.frameRateEngine.startTimer("draw canvas")

        objectList = GameObject.gameObjectList[:]
        customDrawn = False
        layerToDraw = 0
        while len(objectList) != 0:
            for object in objectList:
                if object.layer == layerToDraw:
                    object.draw(self)
                    objectList.remove(object)
            layerToDraw += 1
            if layerToDraw == self.customDrawLayer:
                self.draw()
                customDrawn = True
        if not customDrawn:
            self.draw()

        self.game.frameRateEngine.endTimer("draw canvas")
        self.updateCanvas()

    def clear(self):
        """
        clears the screen and fills it with the background color
        :return: None
        """
        self.game.frameRateEngine.startTimer("clear canvas")
        if self.usePygame:
            self.display.fill(self.backgroundColor)
        else:
            self.canvas.delete("all")
            self.canvas.create_rectangle(0, 0, self.game.window.width, self.game.window.height,
                                         fill="#%02x%02x%02x" % self.backgroundColor)
            self.tkImageList.clear()
        self.game.frameRateEngine.endTimer("clear canvas")

    def updateCanvas(self):
        """
        updates the canvas with the proper method
        based on whether pygame is being used or tkinter
        :return: None
        """
        self.game.frameRateEngine.startTimer("update canvas")
        if self.usePygame:
            pygame.display.update()
            self.game.window.root.update()  # must update while in canvas in pygame but not in tkinter
        else:
            self.canvas.update()
        self.game.frameRateEngine.endTimer("update canvas")

    @abstractmethod
    def draw(self):
        """
        abstract method to be overwritten by the draw method in drawingEngine
        :return: None
        """
        pass

    def showRectangle(self, position1, position2, color, secondaryColor=(0, 0, 0), width=0, shiftPosition=False):
        """
        Wrapper method for tkinter and pygame showRectangle methods

        :param position1: The first bounding point for the rectangle
        :param position1: the second point
        :param color: the color of the rectangle in rgb
        :param width: the width of the outline of the rectangle
        :param shiftPosition: whether to call the abstract method
        shift position on the passed coordinates. Default: False
        :param secondaryColor: the color of the outline in rgb. Default: black

        :return: None
        """
        show = True
        if shiftPosition:
            x1 = int((self.getScreenX(position1[0])))
            y1 = int((self.getScreenY(position1[1])))
            x2 = int((self.getScreenX(position2[0])))
            y2 = int((self.getScreenY(position2[1])))
        else:
            x1 = int(position1[0])
            y1 = int(position1[1])
            x2 = int(position2[0])
            y2 = int(position2[1])

        if x1 > self.game.window.width:
            show = False
        if x2 < 0:
            show = False
        if y1 > self.game.window.height:
            show = False
        if y2 < 0:
            show = False

        if show:
            if self.usePygame:
                pygame.draw.rect(self.display, color, ((int(x1), int(y1)), (int(x2 - x1), int(y2 - y1))))
                if width != 0:
                    pygame.draw.rect(self.display, secondaryColor, ((int(x1), int(y1)), (int(x2 - x1), int(y2 - y1))),
                                     int(width))
            else:
                tk_rgb = "#%02x%02x%02x" % color
                secondary_tk_rgb = "#%02x%02x%02x" % secondaryColor
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=tk_rgb, width=width, outline=secondary_tk_rgb)

    def showLine(self, position1, position2, color, width, shiftPosition=False, rounded=False):
        """
        Wrapper method for tkinter and pygame showLine methods

        :param position1: the first point of the line
        :param position1: the second point
        :param color: the color of the line in rgb
        :param width: the width of the line
        :param shiftPosition: whether to call the abstract method
        shift position on the passed coordinates. Default: False
        :param rounded: whether to round the ends of the lines. Default:False

        :return: None
        """
        show = False
        if shiftPosition:
            x1 = int((self.getScreenX(position1[0])))
            y1 = int((self.getScreenY(position1[1])))
            x2 = int((self.getScreenX(position2[0])))
            y2 = int((self.getScreenY(position2[1])))
        else:
            x1 = int(position1[0])
            y1 = int(position1[1])
            x2 = int(position2[0])
            y2 = int(position2[1])

        if x1 < self.game.window.width and x1 > 0:
            if y1 < self.game.window.height and y1 > 0:
                show = True
        if x2 < self.game.window.width and x2 > 0:
            if y2 < self.game.window.height and y2 > 0:
                show = True

        if show:
            if self.usePygame:
                pygame.draw.line(self.display, color, (x1, y1), (x2, y2), int(width))
                if rounded:
                    pygame.draw.circle(self.diplay, color, (x2, y2), width / 2)
                    pygame.draw.circle(self.diplay, color, position2, width / 2)
            else:
                tk_rgb = "#%02x%02x%02x" % color
                self.canvas.create_line(x1, y1, x2, y2, fill=tk_rgb, width=int(width))
                if rounded:
                    self.canvas.create_oval(x1 - width / 2, y1 - width / 2,
                                            x1 + width / 2, y1 + width / 2, fill=tk_rgb, outline="")
                    self.canvas.create_oval(x2 - width / 2, y2 - width / 2,
                                            x2 + width / 2, y2 + width / 2, fill=tk_rgb, outline="")

    def showText(self, text, position, color, fontName="Times", fontSize=12, bold=False, italic=False,
                 anchorCenter=False, shadowWidth=0, secondaryColor=(0, 0, 0), outlineWidth=0, shiftPosition=False):
        """
        Wrapper method for tkinter and pygame showText methods

        :param position: the position of the upper right hand corner of the
        text if anchorCenter is false, if true, the center of text
        :param text: the text to display
        :param color: the color of the text in rgb
        :param secondaryColor: the color of the outline or shadow of the text in rgb. Default: black
        :param shiftPosition: whether to call the abstract method
        shift position on the passed coordinates. Default: False
        :param anchorCenter: whether to display text at center of
        passed coordinates or from the upper right corner. Default: False
        :param fontSize: default: 12
        :param bold: default: False
        :param italic: default: False
        :param outlineWidth: default:0
        :param shadowWidth: default: 0
        :param fontName: default: "Times"

        :return: None
        """

        if shiftPosition:
            if self.usePygame:
                if outlineWidth != 0:
                    font = pygame.font.SysFont(fontName, fontSize, bold, italic)
                    screenText = font.render(text, 1, secondaryColor)
                    if anchorCenter:
                        textW = screenText.get_width()
                        textH = screenText.get_height()
                    else:
                        textW = 0
                        textH = 0

                    for angle in range(0, 361, int(8 / math.sqrt(outlineWidth)) + 1):
                        x = outlineWidth * math.sin(angle)
                        y = outlineWidth * math.cos(angle)
                        self.display.blit(screenText, (int(self.getScreenX(position[0] - textW / 2 + x)),
                                                       int(self.getScreenY(position[1] - textH / 2 + y))))
                elif shadowWidth != 0:
                    font = pygame.font.SysFont(fontName, fontSize, bold, italic)
                    screenText = font.render(text, 1, secondaryColor)
                    if anchorCenter:
                        textW = screenText.get_width()
                        textH = screenText.get_height()
                    else:
                        textW = 0
                        textH = 0
                    for shift in range(shadowWidth):
                        self.display.blit(screenText, (int(self.getScreenX(position[0] - textW / 2 + shift)),
                                                       int(self.getScreenY(position[1] - textH / 2))))
                font = pygame.font.SysFont(fontName, fontSize, bold, italic)
                screenText = font.render(text, 1, color)
                if anchorCenter:
                    textW = screenText.get_width()
                    textH = screenText.get_height()
                else:
                    textW = 0
                    textH = 0
                self.display.blit(screenText, (
                int(self.getScreenX(position[0] - textW / 2)), int(self.getScreenY(position[1] - textH / 2))))
            else:
                tk_rgb = "#%02x%02x%02x" % color
                fontString = fontName + " " + str(fontSize)
                if bold:
                    fontString += " bold"
                if italic:
                    fontString += " italic"
                if anchorCenter:
                    if outlineWidth != 0:
                        secondary_tk_rgb = "#%02x%02x%02x" % secondaryColor
                        for angle in range(0, 361, int(8 / math.sqrt(outlineWidth)) + 1):
                            x = outlineWidth * math.sin(angle)
                            y = outlineWidth * math.cos(angle)
                            self.canvas.create_text(int(self.getScreenX(position[0] + x)),
                                                    int(self.getScreenY(position[1] + y)), fill=secondary_tk_rgb,
                                                    font=fontString, text=text)
                    elif shadowWidth != 0:
                        secondary_tk_rgb = "#%02x%02x%02x" % secondaryColor
                        for shift in range(shadowWidth):
                            self.canvas.create_text(int(self.getScreenX(position[0] + shift)),
                                                    int(self.getScreenY(position[1])), fill=secondary_tk_rgb,
                                                    font=fontString, text=text)
                    self.canvas.create_text(int(self.getScreenX(position[0])), int(self.getScreenY(position[1])),
                                            fill=tk_rgb, font=fontString, text=text)
                else:
                    if outlineWidth != 0:
                        secondary_tk_rgb = "#%02x%02x%02x" % secondaryColor
                        for angle in range(0, 361, int(8 / math.sqrt(outlineWidth)) + 1):
                            x = outlineWidth * math.sin(angle)
                            y = outlineWidth * math.cos(angle)
                            self.canvas.create_text(int(self.getScreenX(position[0] + x)),
                                                    int(self.getScreenY(position[1] + y)), fill=secondary_tk_rgb,
                                                    font=fontString, text=text, anchor=NW)
                    elif shadowWidth != 0:
                        secondary_tk_rgb = "#%02x%02x%02x" % secondaryColor
                        for shift in range(shadowWidth):
                            self.canvas.create_text(int(self.getScreenX(position[0] + shift)),
                                                    int(self.getScreenY(position[1])), fill=secondary_tk_rgb,
                                                    font=fontString, text=text, anchor=NW)
                    self.canvas.create_text(int(self.getScreenX(position[0])), int(self.getScreenY(position[1])),
                                            fill=tk_rgb, font=fontString, text=text, anchor=NW)
        else:
            if self.usePygame:
                if outlineWidth != 0:
                    font = pygame.font.SysFont(fontName, fontSize, bold, italic)
                    screenText = font.render(text, 1, secondaryColor)
                    if anchorCenter:
                        textW = screenText.get_width()
                        textH = screenText.get_height()
                    else:
                        textW = 0
                        textH = 0

                    for angle in range(0, 361, int(8 / math.sqrt(outlineWidth)) + 1):
                        x = outlineWidth * math.sin(angle)
                        y = outlineWidth * math.cos(angle)
                        self.display.blit(screenText,
                                          (int(position[0] - textW / 2) + x, int(position[1] - textH / 2) + y))
                elif shadowWidth != 0:
                    font = pygame.font.SysFont(fontName, fontSize, bold, italic)
                    screenText = font.render(text, 1, secondaryColor)
                    if anchorCenter:
                        textW = screenText.get_width()
                        textH = screenText.get_height()
                    else:
                        textW = 0
                        textH = 0
                    for shift in range(shadowWidth):
                        self.display.blit(screenText,
                                          (int(position[0] - textW / 2) + shift, int(position[1] - textH / 2)))
                font = pygame.font.SysFont(fontName, fontSize, bold, italic)
                screenText = font.render(text, 1, color)
                if anchorCenter:
                    textW = screenText.get_width()
                    textH = screenText.get_height()
                else:
                    textW = 0
                    textH = 0
                self.display.blit(screenText, (int(position[0] - textW / 2), int(position[1] - textH / 2)))
            else:
                tk_rgb = "#%02x%02x%02x" % color
                fontString = fontName + " " + str(fontSize)
                if bold:
                    fontString += " bold"
                if italic:
                    fontString += " italic"
                if anchorCenter:
                    if outlineWidth != 0:
                        secondary_tk_rgb = "#%02x%02x%02x" % secondaryColor
                        for angle in range(0, 361, int(8 / math.sqrt(outlineWidth)) + 1):
                            x = outlineWidth * math.sin(angle)
                            y = outlineWidth * math.cos(angle)
                            self.canvas.create_text(position[0] + x, position[1] + y, fill=secondary_tk_rgb,
                                                    font=fontString, text=text)
                    elif shadowWidth != 0:
                        secondary_tk_rgb = "#%02x%02x%02x" % secondaryColor
                        for shift in range(shadowWidth):
                            self.canvas.create_text(position[0] + shift, position[1], fill=secondary_tk_rgb,
                                                    font=fontString, text=text)
                    self.canvas.create_text(position[0], position[1], fill=tk_rgb, font=fontString, text=text)
                else:
                    if outlineWidth != 0:
                        secondary_tk_rgb = "#%02x%02x%02x" % secondaryColor
                        for angle in range(0, 361, int(8 / math.sqrt(outlineWidth)) + 1):
                            x = outlineWidth * math.sin(angle)
                            y = outlineWidth * math.cos(angle)
                            self.canvas.create_text(position[0] + x, position[1] + y, fill=secondary_tk_rgb,
                                                    font=fontString, text=text, anchor=NW)
                    elif shadowWidth != 0:
                        secondary_tk_rgb = "#%02x%02x%02x" % secondaryColor
                        for shift in range(shadowWidth):
                            self.canvas.create_text(position[0] + shift, position[1], fill=secondary_tk_rgb,
                                                    font=fontString, text=text, anchor=NW)
                    self.canvas.create_text(position[0], position[1], fill=tk_rgb, font=fontString, text=text,
                                            anchor=NW)

    def showImage(self, image, position, anchorCenter=False, shiftPosition=False):
        """
        Wrapper method for tkinter and pygame showImage methods

        :param image: the Pillow image to be displayed
        :param position: the position of the upper right hand corner of the
        text if anchorCenter is false, if true, the center of text
        :param anchorCenter: whether to display text at center of
        passed coordinates or from the upper right corner. Default: False
        :param shiftPosition: whether to call the abstract method
        shift position on the passed coordinates. Default: False

        :return: None
        """
        if self.usePygame:
            imageW = image.get_width()
            imageH = image.get_height()
        else:
            imageW, imageH = image.size

        if shiftPosition:
            x = int(self.getScreenX(position[0]))
            y = int(self.getScreenY(position[1]))
        else:
            x = int(position[0])
            y = int(position[1])

        show = True
        if x > self.game.window.width:
            show = False
        if x + imageW < 0:
            show = False
        if y > self.game.window.height:
            show = False
        if y + imageH < 0:
            show = False

        if self.usePygame:
            if not anchorCenter:
                imageW = 0
                imageH = 0
        else:
            if anchorCenter:
                imageW = 0
                imageH = 0

        if show:
            if self.usePygame:
                self.display.blit(image, (x - imageW / 2, y - imageH / 2))
            else:
                image = ImageTk.PhotoImage(image)
                self.tkImageList.append(image)
                self.canvas.create_image((x + imageW / 2, y + imageH / 2), image=image)

    def showPolygon(self, pointList, color, position=(0, 0), shiftPosition=False, secondaryColor=(0, 0, 0), width=0):
        """
        Wrapper method for tkinter and pygame showPolygon methods
        doesnt not display polygons that are bigger than the screen

        :param pointList: list of points to be displayed
        :param position: the vector to shift all points in pointList by,
        this value is affected by shiftPosition. Default: (0,0)
        :param color: the color of the polygon in rgb
        :param width: the width of the outline. Default: 0
        :param secondaryColor: the color of the outline of the polygon in rgb. Default: black
        :param shiftPosition: whether to call the abstract method
        shift position on the passed coordinates. Default: False

        :return: None
        """

        points = []

        for index in range(len(pointList)):
            if shiftPosition:
                points.append((int(self.getScreenX(pointList[index][0] + position[0])),
                               int(self.getScreenY(pointList[index][1] + position[1]))))
            else:
                points.append((int(pointList[index][0] + position[0]), int(pointList[index][1] + position[1])))

        show = False
        for point in pointList:
            if not show:
                if point[0] < self.game.window.width and point[0] > 0:
                    if point[1] < self.game.window.height and point[1] > 0:
                        show = True
        if show:
            if self.usePygame:
                pygame.draw.polygon(self.display, color, points)
                if width:
                    pygame.draw.polygon(self.display, secondaryColor, points, width)
            else:
                tk_rgb = "#%02x%02x%02x" % color
                secondary_tk_rgb = "#%02x%02x%02x" % secondaryColor
                self.canvas.create_polygon(points, outline=secondary_tk_rgb, fill=tk_rgb, width=width)

    def showCircle(self, position, radius, color, width=0, secondaryColor=(0, 0, 0), shiftPosition=False):
        """
        Wrapper method for tkinter and pygame showCircle methods

        :param the center position of the circle
        :param color: the color of the circle in rgb
        :param width: the width of the outline. Default: 0
        :param secondaryColor: the color of the outline of the circle in rgb. Default: black
        :param shiftPosition: whether to call the abstract method
        shift position on the passed coordinates. Default: False

        :return: None
        """

        if shiftPosition:
            width = self.getScreenX(width) - self.getScreenX(0)
            radius = self.getScreenX(radius) - self.getScreenX(0)
            x = int(self.getScreenX(position[0]))
            y = int(self.getScreenY(position[1]))
        else:
            width = int(width)
            radius = int(radius + 1)
            x = int(position[0])
            y = int(position[1])

        show = True
        if x - radius / 2 > self.game.window.width:
            show = False
        if x + radius / 2 < 0:
            show = False
        if y - radius / 2 > self.game.window.height:
            show = False
        if y + radius / 2 < 0:
            show = False

        if show:
            try:
                if self.usePygame:
                    pygame.draw.circle(self.display, color, (x, y), radius)
                    if int(width) != 0:
                        pygame.draw.circle(self.display, secondaryColor, (x, y), radius, width)
                else:
                    tk_rgb = "#%02x%02x%02x" % color
                    if width:
                        secondary_tk_rgb = "#%02x%02x%02x" % secondaryColor
                    else:
                        secondary_tk_rgb = ""
                    self.canvas.create_oval(x - radius, y - radius,
                                            x + radius, y + radius, fill=tk_rgb, width=width, outline=secondary_tk_rgb)
            except ValueError:
                pass

    def setBackgroundColor(self, color):
        """
        sets the color of the background
        :param color: the desired background color
        :return: None
        """
        self.backgroundColor = color

    def setDrawLayer(self, layer):
        """
        sets the layer at which the draw method is called
        :param layer: the desired layer
        :return: None
        """
        self.customDrawLayer = layer

    def getBackgroundColor(self):
        """
        gets the color of the background
        :return: the background color
        """
        return self.backgroundColor

    def getDrawLayer(self):
        """
        gets the layer at which the draw method is called
        :return: the draw layer
        """
        return self.customDrawLayer

    def update(self, width, height):
        """
        sets the width and height of the canvas
        :param width: the desired width
        :param height: the desired height
        :return: None
        """
        self.f.config(width=width, height=height)
        if self.usePygame:
            self.diplay = pygame.display.set_mode((width, height))
        else:
            self.canvas.config(width=width, height=height)

    def scaleImage(self, image, scale):
        """
        scales an image by the given amout
        :param image: a Pillow image
        :param scale: the amount to scale the image
        :return: the scaled Pillow image
        """
        newWidth = image.size[0] * scale
        wPercent = (newWidth / float(image.size[0]))
        hSize = int((float(image.size[1]) * float(wPercent)))
        scaledImage = image.resize((int(newWidth), int(hSize)), PIL.Image.ANTIALIAS)
        return scaledImage

    def rotate(self, image, angle):
        """
        rotates an image by the given angle in degrees
        :param image: a Pillow image
        :param angle: the angle in degrees
        :return: the rotated Pillow image
        """
        if self.usePygame:
            return pygame.transform.rotate(image, angle)
        else:
            return self.rotatePIL(image, angle)

    def rotatePIL(self, image, angle):
        """
        wrapper method for the imageString.rotate() method
        which properly handles transparent pixels and large images
        :param image: a Pillow image
        :param angle: the angle in degrees
        :return: the rotated Pillow image
        """
        startSize = image.size
        imageString = image.convert('RGBA')
        rotatedImage = imageString.rotate(angle, expand=0).resize(startSize)
        finalImage = Image.new("RGBA", startSize, (255, 255, 255, 0))
        finalImage.paste(rotatedImage, (0, 0), rotatedImage)
        return finalImage

    def convertToDisplayFormat(self, image):
        """
        converts image to the proper format depending on
        whether you are using pygame
        :param image: a Pillow image
        :return: A pygame image if using pygame, a Pillow otherwise
        """
        if self.usePygame:
            imageBytes = image.convert('RGBA').tobytes("raw", 'RGBA')
            convertedImage = pygame.image.fromstring(imageBytes, image.size, 'RGBA')
        else:
            convertedImage = image
        return convertedImage

    def manipulateImage(self, image, scale, angle):
        """
        wrapper method to scale, rotate, and convert an image
        :param image: a Pillow image
        :param scale: the amount to scale the image
        :param angle: the angle in degrees
        :return: A pygame image if using pygame, a Pillow otherwise
        """
        scaledImage = self.scaleImage(image, scale)
        rotatedImage = self.rotatePIL(scaledImage, angle)
        finalImage = self.convertToDisplayFormat(rotatedImage)
        return finalImage

    @abstractmethod
    def getScreenX(self, x):
        """
        abstract method to be overwritten by drawingEngine.
        Called by all draw methods when shiftPosition=True
        :param x: an x coordinate
        :return: x
        """
        return x

    @abstractmethod
    def getScreenY(self, y):
        """
        abstract method to be overwritten by drawingEngine.
        Called by all draw methods when shiftPosition=True
        :param y: an y coordinate
        :return: y
        """
        return y
