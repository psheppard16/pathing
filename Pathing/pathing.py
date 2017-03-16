__author__ = 'Preston Sheppard'
import Pathing.wall as wallClass
import math

from Pathing.path import PathObject

toleranceG = 100
setsG = []

def findPath(startPoint, endPoint, wallList, resolution=50, angleResolution=11):
    resolution = resolution
    angleResolution = angleResolution
    advance = 0  # amount on either side of the first, so a value of one produces 3 paths
    branch = int(angleResolution / 2)
    tolerance = math.sin(math.pi / angleResolution) * resolution * 2 - 1

    if angleResolution % 2 == 0:
        raise Exception("Angle Resolution=" + str(angleResolution) + " must be odd")
    if advance >= int(angleResolution / 2):
        raise Exception("Advance amount=" + str(advance) + " must be less than half of Angle Resolution")

    sets = []
    global setsG
    setsG = sets

    wallClass.reset()
    wallClass.generateWalls(wallList)

    createStartingPoints(startPoint, endPoint, sets, tolerance)

    done = False
    while not done:
        done = run(sets, resolution, angleResolution, advance, branch)

    shortestPath = getShortestPath(sets)

    if not shortestPath:
        print("could not find a path between those two points")
    else:
        unarrangedpath = [shortestPath]

        focus = shortestPath
        while focus.creator:
            focus = focus.creator
            unarrangedpath.append(focus)

        arrangedPath = []
        if shortestPath.targetPoint == startPoint:
            while unarrangedpath:
                pathObject = unarrangedpath.pop()
                arrangedPath.append((pathObject.x, pathObject.y))
        else:
            for pathObject in unarrangedpath:
                arrangedPath.append((pathObject.x, pathObject.y))

        return arrangedPath

def run(sets, resolution, angleResolution, advance, branch):
    prunePaths(sets, angleResolution)
    return addPaths(sets, resolution, angleResolution, advance, branch)

def addPaths(sets, resolution, angleResolution, advance, branch):
    pathAdded = False
    shortestLength = getShortestLength(sets)
    candidates = getUnadvancedPaths(sets)

    for pathObject in candidates:
        if not pathObject.hasAdvanced and not pathObject.hasBeenEliminated:
            if shortestLength:
                if pathObject.getPromisedLength() <= shortestLength:
                    pathObject.advance(resolution, angleResolution, advance)
                    pathAdded = True
                else:
                    pathObject.advanced = True
                    pathObject.branched = True
                    pathObject.backtracked = True
            else:
                pathObject.advance(resolution, angleResolution, advance)
                pathAdded = True

    if not pathAdded:
        candidates = getUnbranchedPaths(sets)
        for pathObject in candidates:
            if pathObject.hasAdvanced and not pathObject.hasBranched and not pathObject.hasBeenEliminated:
                if shortestLength:
                    if pathObject.getPromisedLength() <= shortestLength:
                        pathObject.branch(resolution, angleResolution, advance, branch)
                        pathAdded = True
                    else:
                        pathObject.advanced = True
                        pathObject.branched = True
                        pathObject.backtracked = True
                else:
                    pathObject.branch(resolution, angleResolution, advance, branch)
                    pathAdded = True

    if not pathAdded:
        candidates = getUnbacktrackedPaths(sets)
        for pathObject in candidates:
            if pathObject.hasAdvanced and pathObject.hasBranched and not pathObject.hasBacktracked and not pathObject.hasBeenEliminated:
                if shortestLength:
                    if pathObject.getPromisedLength() <= shortestLength:
                        pathObject.backtrack(resolution, angleResolution, advance, branch)
                        pathAdded = True
                    else:
                        pathObject.advanced = True
                        pathObject.branched = True
                        pathObject.backtracked = True
                else:
                    pathObject.backtrack(resolution, angleResolution, advance, branch)
                    pathAdded = True

    return not pathAdded

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

def createStartingPoints(startPoint, endPoint, sets, tolerance):
    PathObject(startPoint[0], startPoint[1], None, sets=sets, tolerance=tolerance, targetPoint=endPoint, hasAdvanced=True, hasBranched=True, hasBacktracked=True)
    PathObject(endPoint[0], endPoint[1], None, sets=sets, tolerance=tolerance, targetPoint=startPoint)

def getUnadvancedPaths(sets):
    points = []
    for pathObjectList in sets:
        for pathObject in pathObjectList:
            if pathObject and not pathObject.hasBeenEliminated and not pathObject.hasAdvanced:
                points.append(pathObject)
    orderedPoints = []
    while points:
        smallestPromise = 100000000000
        mostPromisingPath = None
        for pathObject in points:
            promisedLength = pathObject.getPromisedLength()
            if promisedLength < smallestPromise:
                mostPromisingPath = pathObject
                smallestPromise = promisedLength
        orderedPoints.append(mostPromisingPath)
        points.remove(mostPromisingPath)
    return orderedPoints

def getUnbranchedPaths(sets):
    points = []
    for pathObjectList in sets:
        for pathObject in pathObjectList:
            if pathObject and not pathObject.hasBeenEliminated and not pathObject.hasBranched:
                points.append(pathObject)
    orderedPoints = []
    while points:
        smallestPromise = 100000000000
        mostPromisingPath = None
        for pathObject in points:
            promisedLength = pathObject.getPromisedLength()
            if promisedLength < smallestPromise:
                mostPromisingPath = pathObject
                smallestPromise = promisedLength
        orderedPoints.append(mostPromisingPath)
        points.remove(mostPromisingPath)
    return orderedPoints

def getUnbacktrackedPaths(sets):
    points = []
    for pathObjectList in sets:
        for pathObject in pathObjectList:
            if pathObject and not pathObject.hasBeenEliminated and not pathObject.hasBacktracked:
                points.append(pathObject)
    orderedPoints = []
    while points:
        smallestPromise = 100000000000
        mostPromisingPath = None
        for pathObject in points:
            promisedLength = pathObject.getPromisedLength()
            if promisedLength < smallestPromise:
                mostPromisingPath = pathObject
                smallestPromise = promisedLength
        orderedPoints.append(mostPromisingPath)
        points.remove(mostPromisingPath)
    return orderedPoints