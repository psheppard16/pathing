__author__ = 'Preston Sheppard'
import math
import Pathing.geometry as geo
class Path:
    def __init__(self, location, creator, endPoint, nodes, walls, paths, zones):
        self.location = location
        self.creator = creator
        self.endPoint = endPoint
        self.nodes = nodes
        self.walls = walls
        self.zones = zones
        self.paths = paths
        self.children = []
        if self.creator:
            self.length = creator.length + geo.distanceP(creator.location, self.location)
        else:
            self.length = 0

        self.paths.append(self)

        self.nodes[geo.getPixel(self.location)].remove(self.location)

        self.connected = self.getSeen()
        self.prepareNext()

    def add(self, gridSize=10):
        next = self.connected.pop(0)
        self.prepareNext()
        if next in self.nodes[geo.getPixel(next, gridSize=gridSize)]:
            return Path(next, self, self.endPoint, self.nodes, self.walls, self.paths, self.zones)

    def setPromisedLength(self):
        self.promisedLength = self.getPromisedLength(self.connected[0])

    def prepareNext(self):
        while self.connected and not self.valid(self.connected[0]):
            self.connected.pop(0)
        if self.connected:
            self.setPromisedLength()
        else:
            self.paths.remove(self)

    def getPromisedLength(self, node):
        return self.length + geo.distanceP(node, self.endPoint) + geo.distanceP(node, self.location)

    def valid(self, node):
        toCheck = self.getZoneWalls(node)
        valid = True
        for wall in toCheck:
            if geo.intersect((self.location, node), wall):
                valid = False
                break
        return valid

    def getZoneWalls(self, node):
        zoneWalls = []
        bPoints = geo.bresenham(self.location, node)
        for point in bPoints:
            if point in self.zones:
                newWalls = self.zones[point]
                zoneWalls = zoneWalls + list(set(newWalls) - set(zoneWalls))
        return zoneWalls

    def getSeen(self, gridSize=10):
        seenPixels = geo.circleFlood(self.location, self.zones, gridSize=gridSize)
        if seenPixels:
            seen = []
            for pixel in seenPixels:
                if pixel in self.nodes:
                    seen.extend(self.nodes[pixel])
            return sorted(seen, key=lambda x: self.getPromisedLength(x))
        else:
            allNodes = []
            for list in self.nodes.values():
                allNodes.extend(list)
            return sorted(allNodes, key=lambda x: self.getPromisedLength(x))

def findPath(startPoint, endPoint, wallList):
    zones = {}
    for wall in wallList:
        bPoints = geo.bresenham(wall[0], wall[1])
        for point in bPoints:
                if point in zones:
                    zones[point].append(wall)
                else:
                    zones[point] = [wall]

    nodes = generateNodes(startPoint, endPoint, wallList)
    paths = []
    paths.append(Path(startPoint, None, endPoint, nodes, wallList, paths, zones))

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
        if path.connected and (not shortest or path.promisedLength < shortest.promisedLength):
            shortest = path
    return shortest

def generateNodes(startPoint, endPoint, walls, gridSize=10):
    nodes = {}
    sharedPoints = []
    for wall in walls:
        for sharedPoint in wall:
            if sharedPoint not in sharedPoints:
                sharedPoints.append(sharedPoint)
                angles = {}
                for wall in walls:
                    if sharedPoint in wall:
                        for index, point in enumerate(wall):
                            if point == sharedPoint:
                                wall = (sharedPoint, wall[index - 1])
                                angle = geo.ang(((0, 0), (1, 0)), wall)
                                if angle < 0:
                                    angle += math.pi * 2
                                angles[wall] = angle

                ordered = []
                while angles:
                    wall = min(angles, key=angles.get)
                    ordered.append(wall)
                    angles.pop(wall)

                for index in range(-1, len(ordered) - 1):
                    if 0 < geo.ang(ordered[index + 1], ordered[index]) < math.pi:
                        node = getNode(ordered, sharedPoint, ordered[index + 1], ordered[index])
                        if node and node not in nodes:
                            pixel = geo.getPixel(node, gridSize=gridSize)
                            if pixel in nodes:
                                nodes[pixel].append(node)
                            else:
                                nodes[pixel] = [node]
                    node = getNode(ordered, sharedPoint, ordered[index], ordered[index])
                    if node and node not in nodes:
                        pixel = geo.getPixel(node, gridSize=gridSize)
                        if pixel in nodes:
                            nodes[pixel].append(node)
                        else:
                            nodes[pixel] = [node]

    pixel = geo.getPixel(startPoint, gridSize=gridSize)
    if pixel in nodes:
        nodes[pixel].append(startPoint)
    else:
        nodes[pixel] = [startPoint]

    pixel = geo.getPixel(endPoint, gridSize=gridSize)
    if pixel in nodes:
        nodes[pixel].append(endPoint)
    else:
        nodes[pixel] = [endPoint]

    return nodes

def getNode(connectedWalls, sharedPoint, wall1, wall2,  shift=.000001):
    first = wall1  # closest wall clockwise
    second = wall2  # closest wall counterclockwise
    bisectorAngle = geo.getBisectorAngle(first, second)  # the bisector line of the two walls

    x1 = sharedPoint[0] + math.cos(bisectorAngle) * shift
    y1 = sharedPoint[1] + math.sin(bisectorAngle) * shift
    point1 = (x1, y1)

    angles = {}
    insideLine = (sharedPoint, point1)
    for wall in connectedWalls:
        for index, point in enumerate(wall):
            if point == sharedPoint:
                wall = (sharedPoint, wall[index - 1])
                angle = geo.ang(insideLine, wall)
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
                angle = geo.ang(insideLine, wall)
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

    return None
