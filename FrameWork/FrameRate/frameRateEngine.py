__author__ = 'Preston Sheppard'
import time
from FrameWork.FrameRate.task import Task
class FrameRateEngine:
    def __init__(self, game):
        self.game = game

        self.UPDATE_TIME = .25
        self.nextFrameCalc = 0
        self.tickSum = 0
        self.tickStartTime = 0
        self.renderTime = 1 / 20
        self.renderedFrame = True
        self.requestedFrameRate = 1 / 30
        self.nextTick = 0
        self.tickSpeed = 1 / 30
        self.loadTime = 1
        self.time = 0
        self.startTime = 0
        self.sum = 0
        self.number = 0

        self.taskList = []

    def run(self):
        self.nextTick += self.tickSpeed
        if self.game.saveEngine.save.smoothFrames and False:
            tickTime = self.getTime() - self.tickStartTime #time it takes for the program to run one tick
            if not self.renderedFrame:
                tickTime += self.renderTime
            self.tickSum += tickTime
            if self.getTime() > self.nextFrameCalc:
                self.nextFrameCalc += self.UPDATE_TIME
                if self.getTime() > self.nextTick:
                    catchUpTime = (self.getTime() - self.nextTick) ** .5 / 30
                else:
                    catchUpTime = -(self.nextTick - self.getTime()) ** .5 / 30
                self.tickSpeed = self.tickSum / (self.UPDATE_TIME / self.tickSpeed) + catchUpTime
                self.tickSum = 0
            self.UPDATE_TIME = self.tickSpeed ** .3 #this works but i dont know why; simply multiplying by ten doesnt
            if self.tickSpeed < 1 / 120:
               self.tickSpeed = 1 / 120
        else:
            self.tickSpeed = self.getTime() - self.nextTick

        self.taskList.clear()

    def canRun(self):
        if self.getTime() > self.nextTick:
            self.tickStartTime = self.getTime()
            return True
        else:
            return False

    def getTime(self):
        self.time = time.clock()
        return self.time

    def startTimer(self, taskName):
        self.taskList.append(Task(taskName, self.getTime()))

    def endTimer(self, taskName):
        for task in self.taskList:
            if taskName == task.taskName:
                task.endTask(self.getTime())

    def printDiagnostics(self):
        longestTask = None
        for task in self.taskList:
            if not longestTask or task.runTime > longestTask.runTime:
                longestTask = task
            if task.runTime == 0:
                raise Exception("Task timer for task: (" + str(task.taskName) + ") never ended")

        if longestTask:
            print("frame rate:", str(1 / self.tickSpeed))
            print("Longest task:", longestTask.taskName, "Percent:", str(longestTask.runTime / self.tickSpeed * 100) + "%" , "Time:", str(longestTask.runTime))
        else:
            raise Exception("No tasks have finished")

    def printAllTasks(self):
        tasks = ""
        for task in self.taskList:
            if task.runTime != 0:
                tasks += " " + str(task.taskName) + ": " + str(task.runTime) + ""
            else:
                raise Exception("Task timer for task: (" + str(task.taskName) + ") never ended")
        print(tasks)


