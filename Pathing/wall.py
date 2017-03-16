import Pathing.geometry as geo
class WallObject():
    wallList = []
    rawList = []
    def __init__(self, line):
        self.line = ((line[0][0], line[0][1]), (line[1][0], line[1][1]))
        self.point1 = self.line[0]
        self.point2 = self.line[1]
        self.connections = {self.point1: [], self.point2: []}

    def intersects(self, segment):
        return geo.segmentIntersection(self.line, segment)

    def getConnected(self):
        return self.connections[self.point1] + self.connections[self.point1]

def generateWalls(walls):
    WallObject.rawList = walls
    for wall in walls:
        WallObject.wallList.append(WallObject(wall))
    for wall1 in WallObject.wallList:
        for point1 in wall1.line:
            for wall2 in WallObject.wallList:
                if wall1 is not wall2:
                    for point2 in wall2.line:
                        if point1 == point2:
                            wall1.connections[point1].append(wall2)

def reset():
    WallObject.wallList = []
    WallObject.rawList = []