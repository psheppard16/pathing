__author__ = 'Preston Sheppard'
import math
class Path:
    def __init__(self, location, creator, endPoint, nodes, paths):
        self.location = location
        self.creator = creator
        self.endPoint = endPoint
        self.nodes = nodes
        self.paths = paths
        self.children = []

        self.paths.append(self)
        self.candidates = nodes[location][:]
        del self.nodes[self.location]
        if self.creator:
            self.length = creator.length + distanceP(creator.location, self.location)
        else:
            self.length = 0
        self.setPromisedLength()

    def add(self):
        next = self.getNext()
        if next:
            new = Path(next, self, self.endPoint, self.nodes, self.paths)
            self.children.append(new)
            return new

    def setPromisedLength(self):
        if self.candidates:
            self.promisedLength = self.length + \
                distanceP(self.candidates[0], self.endPoint) + \
                distanceP(self.candidates[0], self.location)

    def getNext(self):
        next = self.candidates.pop(0)
        self.setPromisedLength()
        if next in self.nodes:
            return next
        else:
            return None

def findPath(startPoint, endPoint, wallList):
    nodes = generateNodes(startPoint, endPoint, wallList)
    paths = []
    paths.append(Path(startPoint, None, endPoint, nodes, paths))

    finalPath = None
    while not finalPath:
        finalPath = addPaths(paths)

    fullPath = []
    focus = finalPath
    while focus:
        fullPath.append(focus.location)
        focus = focus.creator
    return fullPath

def addPaths(paths):
    pathToAdvance = getPromisingPath(paths)
    if pathToAdvance:
        new = pathToAdvance.add()
        if new and new.location == pathToAdvance.endPoint:
            return new
    else:
        raise Exception("failed to find path")

def getPromisingPath(paths):
    shortest = None
    for path in paths:
        if path.candidates and (not shortest or path.promisedLength < shortest.promisedLength):
            shortest = path
    return shortest

def generateNodes(startPoint, endPoint, walls):
    nodes = {}
    for wall in walls:
        for sharedPoint in wall:
            if sharedPoint not in nodes:
                toAdd = []
                for wall in walls:
                    if sharedPoint in wall:
                        toAdd.append(wall)

                angles = {}
                for wall in toAdd:
                    for index, point in enumerate(wall):
                        if point == sharedPoint:
                            wall = (sharedPoint, wall[index - 1])
                            angle = ang(((0, 0), (1, 0)), wall)
                            if angle < 0:
                                angle += math.pi * 2
                            angles[wall] = angle

                ordered = []
                while angles:
                    wall = min(angles, key=angles.get)
                    ordered.append(wall)
                    angles.pop(wall)

                for index in range(-1, len(ordered) - 1):
                    if 0 < ang(ordered[index + 1], ordered[index]) < math.pi:
                        nodes[getNodes(ordered, sharedPoint, ordered[index + 1], ordered[index])] = []
                    nodes[getNodes(ordered, sharedPoint, ordered[index], ordered[index])] = []

    nodes[startPoint] = []
    nodes[endPoint] = []

    for node1 in nodes.keys():
        connected = {}
        for node2 in nodes.keys():
            valid = True
            for wall in walls:
                if intersect((node1, node2), wall):
                    valid = False
                    break
            if valid:
                connected[node2] = distanceP(node2, endPoint) + distanceP(node1, node2)
        ordered = []  # order the walls based on angle to insideLine
        while connected:
            wall = min(connected, key=connected.get)
            ordered.append(wall)
            connected.pop(wall)
        nodes[node1] = ordered
    return nodes

def getNodes(connectedWalls, sharedPoint, wall1, wall2,  shift=.01):
    first = wall1  # closest wall clockwise
    second = wall2  # closest wall counterclockwise
    bisectorAngle = getBisectorAngle(first, second)  # the bisector line of the two walls

    x1 = sharedPoint[0] + math.cos(bisectorAngle) * shift
    y1 = sharedPoint[1] + math.sin(bisectorAngle) * shift
    point1 = (x1, y1)

    angles = {}
    insideLine = (sharedPoint, point1)
    for wall in connectedWalls:
        for index, point in enumerate(wall):
            if point == sharedPoint:
                wall = (sharedPoint, wall[index - 1])
                angle = ang(insideLine, wall)
                if angle < 0:
                    angle += math.pi * 2
                angles[wall] = angle
    ordered = []  # order the walls based on angle to insideLine
    while (angles):
        wall = min(angles, key=angles.get)
        ordered.append(wall)
        angles.pop(wall)
    first1 = ordered[0]  # closest wall clockwise
    second1 = ordered[-1]  # closest wall counterclockwise
    if first1 == first and second1 == second:
        return point1

    x2 = sharedPoint[0] - math.cos(bisectorAngle) * shift
    y2 = sharedPoint[1] - math.sin(bisectorAngle) * shift
    point2 = (x2, y2)
    angles = {}
    insideLine = (sharedPoint, point2)
    for wall in connectedWalls:
        for index, point in enumerate(wall):
            if point == sharedPoint:
                wall = (sharedPoint, wall[index - 1])
                angle = ang(insideLine, wall)
                if angle < 0:
                    angle += math.pi * 2
                angles[wall] = angle
    ordered = []  # order the walls based on angle to insideLine
    while (angles):
        wall = min(angles, key=angles.get)
        ordered.append(wall)
        angles.pop(wall)
    first2 = ordered[0]  # closest wall clockwise
    second2 = ordered[-1]  # closest wall counterclockwise
    if first2 == first and second2 == second:
        return point2

    return (0, 0)
    #raise Exception("failed to find snap point")

def getBisectorAngle(line1, line2):
    x1 = line1[0][0] - line1[1][0]
    y1 = line1[0][1] - line1[1][1]
    x2 = line2[0][0] - line2[1][0]
    y2 = line2[0][1] - line2[1][1]

    theta_1 = math.atan2(y1, x1)
    theta_2 = math.atan2(y2, x2)

    return (theta_1 + theta_2) / 2

def ang(lineA, lineB):
    x1 = lineA[1][0] - lineA[0][0]
    y1 = lineA[1][1] - lineA[0][1]

    x2 = lineB[1][0] - lineB[0][0]
    y2 = lineB[1][1] - lineB[0][1]

    detV = det((x1, y1), (x2, y2))
    dotV = dot((x1, y1), (x2, y2))
    return math.atan2(detV, dotV)

def det(a, b):
    return a[0] * b[1] - a[1] * b[0]

def dot(vA, vB):
    return vA[0] * vB[0] + vA[1] * vB[1]

def ccw(a, b, c):
    return (c[1] - a[1]) * (b[0] - a[0]) > (b[1] - a[1]) * (c[0] - a[0])

def intersect(line1, line2):
    a = line1[0]
    b = line1[1]
    c = line2[0]
    d = line2[1]
    return ccw(a,c,d) != ccw(b,c,d) and ccw(a,b,c) != ccw(a,b,d)

def distanceP(point1, point2):
    return distance(point1[0], point1[1], point2[0], point2[1])

def distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)