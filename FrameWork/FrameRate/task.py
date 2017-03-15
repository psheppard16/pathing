__author__ = 'Preston Sheppard'
class Task:
    def __init__(self, taskName, startTime):
        self.taskName = taskName
        self.startTime = startTime
        self.runTime = 0

    def endTask(self, endTime):
        """
        Sets the runtime for this task to the total
        time that it has been running
        :param endTime: the time the task ended
        :return: None
        """
        self.runTime = endTime - self.startTime

