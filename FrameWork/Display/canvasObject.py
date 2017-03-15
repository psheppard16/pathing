__author__ = 'Preston Sheppard'
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
        if platform.system() == "Windows":
            os.environ['SDL_VIDEODRIVER'] = 'windib'
            self.usePygame = True
            self.display = pygame.display.set_mode((self.game.window.width, self.game.window.height))
            self.display.fill((255, 255, 255))
            pygame.display.init()
            pygame.font.init()
        else:
            self.usePygame = False
            self.canvas = Canvas(self.game.window.root, bg="white", width=self.game.window.width, height = self.game.window.height)
            self.canvas.pack(in_=self.f)

        self.customDrawLayer = 0
        self.backgroundColor = (121, 202, 249)
        self.tkImageList = [] #images must maintain a reference in order to appear on the canvas

    def render(self):
        self.clear()
        self.game.frameRateEngine.startTimer("draw canvas")

        customDrawn = False
        objectsNotDrawn = True
        layerToDraw = 0
        while objectsNotDrawn:
            objectsNotDrawn = False
            for object in GameObject.gameObjectList:
                if object.layer == layerToDraw:
                    object.draw(self)
                    object.drawn = True
                elif object.drawn == False:
                    objectsNotDrawn = True
            layerToDraw += 1
            if layerToDraw == self.customDrawLayer:
                self.draw()
                customDrawn = True
        for object in GameObject.gameObjectList:
            object.drawn = False
        if not customDrawn:
            self.draw()

        self.game.frameRateEngine.endTimer("draw canvas")
        self.updateCanvas()
        
    def clear(self):
        self.game.frameRateEngine.startTimer("clear canvas")
        if self.usePygame:
            self.display.fill(self.backgroundColor)
        else:
            self.canvas.delete("all")
            self.canvas.create_rectangle(0, 0, self.game.window.width, self.game.window.height, fill = "#%02x%02x%02x" % self.backgroundColor)
            self.tkImageList.clear()
        self.game.frameRateEngine.endTimer("clear canvas")
        
    def updateCanvas(self):
        self.game.frameRateEngine.startTimer("update canvas")
        if self.usePygame:
            pygame.display.update()
            self.game.window.root.update() #must update while in canvas in pygame but not in tkinter
        else:
            self.canvas.update()
        self.game.frameRateEngine.endTimer("update canvas")

    @abstractmethod
    def draw(self):
        pass

    def showRectangle(self, position1, position2, color, secondaryColor=(0,0,0), width=0, shiftPosition=False):
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
                    pygame.draw.rect(self.display, secondaryColor, ((int(x1), int(y1)), (int(x2 - x1), int(y2 - y1))), int(width))
            else:
                tk_rgb = "#%02x%02x%02x" % color
                secondary_tk_rgb = "#%02x%02x%02x" % secondaryColor
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=tk_rgb, width=width, outline=secondary_tk_rgb)

    def showLine(self, position1, position2, color, width, shiftPosition=False):
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
            else:
                tk_rgb = "#%02x%02x%02x" % color
                self.canvas.create_line(x1, y1, x2, y2, fill=tk_rgb, width=int(width))

    def showText(self, text, position, color, fontName="Times", fontSize=12, bold=False, italic=False, anchorCenter=False, shadowWidth=0, secondaryColor=(0, 0, 0), outlineWidth=0, shiftPosition=False):
        if shiftPosition:
            if self.usePygame:
                if outlineWidth!= 0:
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
                        self.display.blit(screenText, (int(self.getScreenX(position[0] - textW / 2 + x)), int(self.getScreenY(position[1] - textH / 2 + y))))
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
                        self.display.blit(screenText, (int(self.getScreenX(position[0] - textW / 2 + shift)), int(self.getScreenY(position[1] - textH / 2))))
                font = pygame.font.SysFont(fontName, fontSize, bold, italic)
                screenText = font.render(text, 1, color)
                if anchorCenter:
                    textW = screenText.get_width()
                    textH = screenText.get_height()
                else:
                    textW = 0
                    textH = 0
                self.display.blit(screenText, (int(self.getScreenX(position[0] - textW / 2)), int(self.getScreenY(position[1] - textH / 2))))
            else:
                tk_rgb = "#%02x%02x%02x" % color
                fontString = fontName + " " + str(fontSize)
                if bold:
                    fontString += " bold"
                if italic:
                    fontString += " italic"
                if anchorCenter:
                    if outlineWidth!= 0:
                        secondary_tk_rgb = "#%02x%02x%02x" % secondaryColor
                        for angle in range(0, 361, int(8 / math.sqrt(outlineWidth)) + 1):
                            x = outlineWidth * math.sin(angle)
                            y = outlineWidth * math.cos(angle)
                            self.canvas.create_text(int(self.getScreenX(position[0] + x)), int(self.getScreenY(position[1] + y)), fill=secondary_tk_rgb, font=fontString, text=text)
                    elif shadowWidth != 0:
                        secondary_tk_rgb = "#%02x%02x%02x" % secondaryColor
                        for shift in range(shadowWidth):
                            self.canvas.create_text(int(self.getScreenX(position[0] + shift)), int(self.getScreenY(position[1])), fill=secondary_tk_rgb, font=fontString, text=text)
                    self.canvas.create_text(int(self.getScreenX(position[0])), int(self.getScreenY(position[1])), fill=tk_rgb, font=fontString, text=text)
                else:
                    if outlineWidth!= 0:
                        secondary_tk_rgb = "#%02x%02x%02x" % secondaryColor
                        for angle in range(0, 361, int(8 / math.sqrt(outlineWidth)) + 1):
                            x = outlineWidth * math.sin(angle)
                            y = outlineWidth * math.cos(angle)
                            self.canvas.create_text(int(self.getScreenX(position[0] + x)), int(self.getScreenY(position[1] + y)), fill=secondary_tk_rgb, font=fontString, text=text, anchor=NW)
                    elif shadowWidth != 0:
                        secondary_tk_rgb = "#%02x%02x%02x" % secondaryColor
                        for shift in range(shadowWidth):
                            self.canvas.create_text(int(self.getScreenX(position[0] + shift)), int(self.getScreenY(position[1])), fill=secondary_tk_rgb, font=fontString, text=text, anchor=NW)
                    self.canvas.create_text(int(self.getScreenX(position[0])), int(self.getScreenY(position[1])), fill=tk_rgb, font=fontString, text=text, anchor=NW)
        else:
            if self.usePygame:
                if outlineWidth!= 0:
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
                        self.display.blit(screenText, (int(position[0] - textW / 2) + x, int(position[1] - textH / 2) + y))
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
                        self.display.blit(screenText, (int(position[0] - textW / 2) + shift, int(position[1] - textH / 2)))
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
                    if outlineWidth!= 0:
                        secondary_tk_rgb = "#%02x%02x%02x" % secondaryColor
                        for angle in range(0, 361, int(8 / math.sqrt(outlineWidth)) + 1):
                            x = outlineWidth * math.sin(angle)
                            y = outlineWidth * math.cos(angle)
                            self.canvas.create_text(position[0] + x, position[1] + y, fill=secondary_tk_rgb, font=fontString, text=text)
                    elif shadowWidth != 0:
                        secondary_tk_rgb = "#%02x%02x%02x" % secondaryColor
                        for shift in range(shadowWidth):
                            self.canvas.create_text(position[0] + shift, position[1], fill=secondary_tk_rgb, font=fontString, text=text)
                    self.canvas.create_text(position[0], position[1], fill=tk_rgb, font=fontString, text=text)
                else:
                    if outlineWidth!= 0:
                        secondary_tk_rgb = "#%02x%02x%02x" % secondaryColor
                        for angle in range(0, 361, int(8 / math.sqrt(outlineWidth)) + 1):
                            x = outlineWidth * math.sin(angle)
                            y = outlineWidth * math.cos(angle)
                            self.canvas.create_text(position[0] + x, position[1] + y, fill=secondary_tk_rgb, font=fontString, text=text, anchor=NW)
                    elif shadowWidth != 0:
                        secondary_tk_rgb = "#%02x%02x%02x" % secondaryColor
                        for shift in range(shadowWidth):
                            self.canvas.create_text(position[0] + shift, position[1], fill=secondary_tk_rgb, font=fontString, text=text, anchor=NW)
                    self.canvas.create_text(position[0], position[1], fill=tk_rgb, font=fontString, text=text, anchor=NW)

    def showImage(self, image, position, anchorCenter=False, shiftPosition=False):
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

    def showPolygon(self, pointList, color, position=(0, 0), shiftPosition=False):
        #doesnt work for bigger than screen polygons
            #should be easy fix, do in form of rectangle
        points = []

        for index in range(len(pointList)):
            if shiftPosition:
                points.append((int(self.getScreenX(pointList[index][0] + position[0])), int(self.getScreenY(pointList[index][1] + position[1]))))
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
                pygame.draw.polygon(self.display, (0, 0, 0), points, 2)
            else:
                tk_rgb = "#%02x%02x%02x" % color
                self.canvas.create_polygon(points, outline='black', fill=tk_rgb, width=2)

    def showCircle(self, position, radius, color, width=0, secondaryColor=(0, 0, 0), shiftPosition=False):
        if shiftPosition:
            width = int(self.getScreenX(width) - self.getScreenX(0) + 1)
            radius = int(self.getScreenX(radius) - self.getScreenX(0) + 1)
            x = int(self.getScreenX(position[0]))
            y = int(self.getScreenY(position[1]))
        else:
            width = int(width + 1)
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
                    secondary_tk_rgb = "#%02x%02x%02x" % secondaryColor
                    self.canvas.create_oval(x - radius, y - radius,
                                            x + radius, y + radius, fill=tk_rgb, width=width, outline=secondary_tk_rgb)
            except ValueError:
                pass

    def setBackgroundColor(self, color):
        self.backgroundColor = color

    def setDrawLayer(self, layer):
        self.customDrawLayer = layer

    def update(self, width, height):
        self.f.config(width=self.game.window.width, height=self.game.window.width)
        if self.usePygame:
            self.diplay = pygame.display.set_mode((self.game.window.width, self.game.window.height))
        else:
            self.canvas.config(width=self.game.window.width, height=self.game.window.height)

    def scaleImage(self, image, scale):
        newWidth = image.size[0] * scale
        wPercent = (newWidth/float(image.size[0]))
        hSize = int((float(image.size[1])*float(wPercent)))
        scaledImage = image.resize((int(newWidth), int(hSize)), PIL.Image.ANTIALIAS)
        return scaledImage

    def rotate(self, image, angle):
        if self.usePygame:
            return pygame.transform.rotate(image, angle)
        else:
            return self.rotatePIL(image, angle)

    def rotatePIL(self, image, angle):
        startSize = image.size
        imageString = image.convert('RGBA')
        rotatedImage = imageString.rotate(angle, expand=0).resize(startSize)
        finalImage = Image.new("RGBA", startSize, (255, 255, 255, 0))
        finalImage.paste(rotatedImage, (0, 0), rotatedImage)
        return finalImage

    def convertToDisplayFormat(self, image):
        if self.usePygame:
            imageBytes = image.convert('RGBA').tobytes("raw", 'RGBA')
            convertedImage = pygame.image.fromstring(imageBytes, image.size, 'RGBA')
        else:
            convertedImage = image
        return convertedImage

    def manipulateImage(self, image, scale, angle):
        scaledImage = self.scaleImage(image, scale)
        rotatedImage = self.rotatePIL(scaledImage, angle)
        finalImage = self.convertToDisplayFormat(rotatedImage)
        return finalImage

    @abstractmethod
    def getScreenX(self, x):
        pass

    @abstractmethod
    def getScreenY(self, y):
        pass