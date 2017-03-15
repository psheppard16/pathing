import Game.Pathing.wall as wallClass
from Game.Pathing.path import PathObject
import math
import Game.Pathing.geometry as geo
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

    global toleranceG
    toleranceG = tolerance

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
    reducePaths(sets)
    prunePaths(sets)
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
                    pathObject.eliminate()
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
                        pathObject.eliminate()
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
                        pathObject.eliminate()
                else:
                    pathObject.backtrack(resolution, angleResolution, advance, branch)
                    pathAdded = True

    return not pathAdded

def setStaticVariables():
    PathObject.ADVANCES_TO_TRY = 1000
    PathObject.BRANCHES_TO_TRY = 1000
    PathObject.BACKTRACKS_TO_TRY = 1000
    PathObject.ADVANCE_AMOUNT = 0
    PathObject.BRANCH_AMOUNT = 4
    PathObject.ANGLE_RESOLUTION = 15

    AMOUNT = 100
    PACKING_COEFFICIENT = .907

    MINIMUM = 50
    MAXIMUM = 100000000000000000

    largestDistance = 0
    for pathObjectList1 in PathObject.sets:
        for pathObject1 in pathObjectList1:
            for pathObjectList2 in PathObject.sets:
                for pathObject2 in pathObjectList2:
                    if pathObject2 != pathObject1:
                        newDistance = geo.distanceP(pathObject1.position, pathObject2.position)
                        if newDistance > largestDistance:
                            largestDistance = newDistance

    checkRadius = math.sqrt(PACKING_COEFFICIENT * largestDistance ** 2 / AMOUNT)

    if checkRadius < MINIMUM:
        checkRadius = MINIMUM
    if checkRadius > MAXIMUM:
        checkRadius = MAXIMUM

    PathObject.SLOWER_TOLERANCE = checkRadius - 1
    PathObject.BACKTRACK_TOLERANCE = checkRadius - 1
    PathObject.CONNECTION_TOLERANCE = checkRadius - 1
    PathObject.SNAP_TOLERANCE = checkRadius - 1

    PathObject.RESOLUTION = checkRadius / 2 / math.sin(math.pi / PathObject.ANGLE_RESOLUTION)
    PathObject.END_TOLERANCE = PathObject.RESOLUTION * 2

    if PathObject.ANGLE_RESOLUTION % 2 == 0:
        raise Exception("Angle Resolution=" + str(PathObject.ANGLE_RESOLUTION) + " must be odd")
    if PathObject.ADVANCE_AMOUNT >= int(PathObject.ANGLE_RESOLUTION / 2):
        raise Exception(
            "Advance amount=" + str(PathObject.ADVANCE_AMOUNT) + " must be less than half of Angle Resolution")

def reducePaths(sets):
    for pathObjectList in sets:
        for pathObject in pathObjectList:
            pathObject.reduce()

def prunePaths(sets):
    for pathObjectList in sets:
        for pathObject in pathObjectList:
            pathObject.prune()

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