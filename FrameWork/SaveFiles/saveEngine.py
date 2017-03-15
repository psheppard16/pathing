__author__ = 'Preston Sheppard'
import pickle
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
        filePath = "FrameWork/SaveFiles/saveFile" + str(saveNumber)
        try:
            with open(filePath, 'rb') as input:
                self.save = pickle.load(input)
        except EOFError and FileNotFoundError:
            raise Exception("File not found")

    def saveCharacter(self, saveNumber):
        filePath = "FrameWork/SaveFiles/saveFile" + str(saveNumber)
        try:
            with open(filePath, 'wb') as output:
                pickle.dump(self.save, output, pickle.HIGHEST_PROTOCOL)
        except EOFError and FileNotFoundError:
            raise Exception("File not found")