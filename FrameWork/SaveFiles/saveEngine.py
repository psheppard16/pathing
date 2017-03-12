__author__ = 'python'
import pickle
import os
from FrameWork.SaveFiles.saveFile import SaveFile
class SaveEngine:
    def __init__(self):
        self.NUMBER_OF_SAVES = 3
        self.saveNumber = None
        self.saveSelected = False
        self.save = SaveFile()

    def resetSaves(self):
        self.save = SaveFile()
        for index in range(self.NUMBER_OF_SAVES):
            self.saveCharacter(index)

    def loadChar(self, saveNumber):
        self.saveSelected = True
        self.saveNumber = saveNumber

    def saveCharacter(self, saveNumber):
        pass