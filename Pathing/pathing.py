__author__ = 'Preston Sheppard'
import math
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
            self.length = creator.length + distanceP(creator.location, self.location)
        else:
            self.length = 0

        self.paths.append(self)
        self.nodes.remove(self.location)

        self.connected = sorted(self.nodes, key=lambda x: self.getPromisedLength(x))
        self.prepareNext()

    def add(self):
        if self.connected:
            next = self.connected.pop(0)
            self.prepareNext()
            if next in self.nodes:
                return Path(next, self, self.endPoint, self.nodes, self.walls, self.paths, self.zones)

    def setPromisedLength(self):
        if self.connected:
            self.promisedLength = self.getPromisedLength(self.connected[0])

    def prepareNext(self):
        while self.connected and not self.valid(self.connected[0]):
            self.connected.pop(0)
        self.setPromisedLength()

    def getPromisedLength(self, node):
        return self.length + distanceP(node, self.endPoint) + distanceP(node, self.location)

    def valid(self, node):
        toCheck = self.getZoneWalls(node)
        valid = True
        for wall in toCheck:
            if intersect((self.location, node), wall):
                valid = False
                break
        return valid

    def getZoneWalls(self, node):
        zoneWalls = []
        bPoints = bresenham(self.location, node)
        for point in bPoints:
            if point in self.zones:
                newWalls = self.zones[point]
                zoneWalls = zoneWalls + list(set(newWalls) - set(zoneWalls))
        return zoneWalls

def switch_octant_to_zero(octant, x, y):
   if octant == 0: return (x, y)
   if octant == 1: return (y, x)
   if octant == 2: return (y, -x)
   if octant == 3: return (-x, y)
   if octant == 4: return (-x, -y)
   if octant == 5: return (-y, -x)
   if octant == 6: return (-y, x)
   if octant == 7: return (x, -y)

def switch_octant_from_zero(octant, x, y):
   if octant == 0: return (x, y)
   if octant == 1: return (y, x)
   if octant == 2: return (-y, x)
   if octant == 3: return (-x, y)
   if octant == 4: return (-x, -y)
   if octant == 5: return (-y, -x)
   if octant == 6: return (y, -x)
   if octant == 7: return (x, -y)

def get_octant(A, B):
    dx, dy = B[0] - A[0], B[1] - A[1]
    octant = 0
    if dy < 0:
        dx, dy = -dx, -dy  # rotate by 180 degrees
        octant += 4
    if dx < 0:
        dx, dy = dy, -dx  # rotate clockwise by 90 degrees
        octant += 2
    if dx < dy:
        # no need to rotate now
        octant += 1
    return octant

def bresenham(point1, point2, gridSize=10):
    x1, y1 = (int(round(point1[0] / gridSize)), int(round(point1[1] / gridSize)))
    x2, y2 = (int(round(point2[0] / gridSize)), int(round(point2[1] / gridSize)))
    dx = x2 - x1
    dy = y2 - y1

    # Determine how steep the line is
    is_steep = abs(dy) > abs(dx)

    # Rotate line
    if is_steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    # Swap start and end points if necessary and store swap state
    swapped = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        swapped = True

    # Recalculate differentials
    dx = x2 - x1
    dy = y2 - y1

    # Calculate error
    error = int(dx / 2.0)
    ystep = 1 if y1 < y2 else -1

    # Iterate over bounding box generating points between start and end
    y = y1
    points = []
    for x in range(x1, x2 + 1):
        coord = (y, x) if is_steep else (x, y)
        points.append(coord)

        error -= abs(dy)
        if error < 0:
            coord = (y, x + 1) if is_steep else (x + 1, y)
            points.append(coord)
            y += ystep
            coord = (y, x) if is_steep else (x, y)
            points.append(coord)
            error += dx
    return points

def findPath(startPoint, endPoint, wallList):
    zones = {}
    for wall in wallList:
        bPoints = bresenham(wall[0], wall[1])
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

def generateNodes(startPoint, endPoint, walls):
    nodes = []
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
                        node = getNode(ordered, sharedPoint, ordered[index + 1], ordered[index])
                        if node and node not in nodes:
                            nodes.append(node)
                    node = getNode(ordered, sharedPoint, ordered[index], ordered[index])
                    if node and node not in nodes:
                        nodes.append(node)

    nodes.append(startPoint)
    nodes.append(endPoint)

    return nodes

def getNode(connectedWalls, sharedPoint, wall1, wall2,  shift=.1):
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

    return None

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