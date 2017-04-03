__author__ = 'Preston Sheppard'
import Pathing.wall as wallClass
import math
from Pathing.path import PathObject

def findPath(startPoint, endPoint, wallList):

    wallClass.reset()
    wallClass.generateWalls(wallList)

def run(sets, resolution, angleResolution, advance, branch):
    prunePaths(sets, angleResolution)
    return addPaths(sets, resolution, angleResolution, advance, branch)

def prunePaths(sets, angleResolution):
    for pathObjectList in sets:
        for pathObject in pathObjectList:
            pathObject.prune(angleResolution)

def generateMap(wallList, startPoint, xMin, yMin, xMax, yMax, step=10):
    finalPaths = []
    for x in range(int(xMin / step) + 1, int(xMax / step)):
        for y in range(int(yMin / step) + 1, int(yMax / step)):
            if startPoint != (x * step, y * step):
                finalPaths.append(findPath(startPoint, (x * step, y * step), wallList))
                print(x, y)
    return finalPaths

def getShortestLength(sets):
    shortestLength = None
    for pathObjectList in sets:
        for pathObject in pathObjectList:
            if pathObject.hasFinished:
                length = pathObject.getLength()
                if not shortestLength or length < shortestLength:
                    shortestLength = length
    return shortestLength

def getShortestPath(sets):
    shortestPath = None
    shortestLength = None
    for pathObjectList in sets:
        for pathObject in pathObjectList:
            if pathObject.hasFinished:
                length = pathObject.getLength()
                if not shortestLength or length < shortestLength:
                    shortestPath = pathObject
                    shortestLength = length
    return shortestPath

def generateNodes(walls):
    wallIntersections = {}
    for wall in walls:
        for point in wall:
            if point not in wallIntersections:
                wallIntersections[point] = []

    for sharedPoint in wallIntersections.keys():
        toAdd = []
        for wall in walls:
            if sharedPoint in wall:
                if wall not in wallIntersections[sharedPoint]:
                    toAdd.append(wall)
                else:
                    raise Exception()

        angles = {}
        for wall in toAdd:
            for index, point in enumerate(wall.line):
                if point == sharedPoint:
                    wall = (sharedPoint, wall.line[index - 1])
                    angle = ang(((0, 0), (1, 0)), wall)
                    if angle < 0:
                        angle += math.pi * 2
                    angles[wall] = angle

        ordered = []
        while angles:
            wall = min(angles, key=angles.get)
            ordered.append(wall)
            angles.pop(wall)

        wallIntersections[sharedPoint] = ordered

    nodes = []
    for sharedPoint, walls in wallIntersections.items():
        for index in range(-1, walls.length - 1):
            nodes.append(getSnapPoints(walls, sharedPoint, walls[index], walls[index + 1]))

    return nodes

def getSnapPoints(connectedWalls, sharedPoint, wall1, wall2,  shift=3):
    first = wall1  # closest wall clockwise
    second = wall2  # closest wall counterclockwise
    bisectorAngle = getBisectorAngle(first, second)  # the bisector line of the two walls

    x1 = sharedPoint[0] + math.cos(bisectorAngle) * shift
    y1 = sharedPoint[1] + math.sin(bisectorAngle) * shift
    point1 = (x1, y1)

    angles = {}
    insideLine = (sharedPoint, point1)
    for wall in connectedWalls:
        for index, point in enumerate(wall.line):
            if point == sharedPoint:
                wall = (sharedPoint, wall.line[index - 1])
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
        for index, point in enumerate(wall.line):
            if point == sharedPoint:
                wall = (sharedPoint, wall.line[index - 1])
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

    raise Exception("failed to find snap point")

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