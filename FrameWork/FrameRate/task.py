__author__ = 'Preston Sheppard'
class Task:
    def __init__(self, taskName, startTime):
        self.taskName = taskName
        self.startTime = startTime
        self.runTime = 0

    def endTask(self, endTime):
        self.runTime = endTime - self.startTime

