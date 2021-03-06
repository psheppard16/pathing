import math
import inspect


def lineToPoint(line, point):
    if line[1] == line[0]:
        return distance(line[0][0], line[0][1], point[0], point[1])
    else:
        px = line[1][0] - line[0][0]
        py = line[1][1] - line[0][1]

        something = px * px + py * py

        u = ((point[0] - line[0][0]) * px + (point[1] - line[0][1]) * py) / float(something)

        if u > 1:
            u = 1
        elif u < 0:
            u = 0

        x = line[0][0] + u * px
        y = line[0][1] + u * py

        dx = x - point[0]
        dy = y - point[1]

        dist = math.sqrt(dx * dx + dy * dy)

        return dist


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


def add(v1, v2):
    return v1[0] + v2[0], v1[1] + v2[1]


def sub(v1, v2):
    return v1[0] - v2[0], v1[1] - v2[1]


def unit_vector(v):
    abs = math.sqrt(v[0] ** 2 + v[1] ** 2)
    return v[0] / abs, v[1] / abs


def getSnapPoints(connectedWalls, sharedPoint, insidePoint, shift=.0001):
    if connectedWalls:
        angles = {}
        insideLine = (sharedPoint, insidePoint)
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
        first = ordered[0]  # closest wall clockwise
        second = ordered[-1]  # closest wall counterclockwise
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
    else:
        raise Exception("there must be at least one connected wall")


def liesInTriangle(point, triangle):
    tPoint0 = triangle[0]
    tPoint1 = triangle[1]
    tPoint2 = triangle[2]

    area = (
    (tPoint1[1] - tPoint2[1]) * (tPoint0[0] - tPoint2[0]) + (tPoint2[0] - tPoint1[0]) * (tPoint0[1] - tPoint2[1]))
    if area == 0:
        return False

    alpha = ((tPoint1[1] - tPoint2[1]) * (point[0] - tPoint2[0]) + (tPoint2[0] - tPoint1[0]) * (
    point[1] - tPoint2[1])) / area

    beta = ((tPoint2[1] - tPoint0[1]) * (point[0] - tPoint2[0]) + (tPoint0[0] - tPoint2[0]) * (
    point[1] - tPoint2[1])) / area

    gamma = 1 - alpha - beta

    return alpha > 0 and beta > 0 and gamma > 0


def segmentIntersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    div = det(xdiff, ydiff)
    if div == 0:
        x1 = line2[0][0]
        y1 = line2[0][1]

        x2 = line2[1][0]
        y2 = line2[1][1]
        if line1[1][0] <= x1 <= line1[0][0] or line1[0][0] <= x1 <= line1[1][0]:
            if line1[1][1] <= y2 <= line1[0][1] or line1[0][1] <= y2 <= line1[1][1]:
                return True
        if line1[1][1] <= y1 <= line1[0][1] or line1[0][1] <= y1 <= line1[1][1]:
            if line1[1][0] <= x2 <= line1[0][0] or line1[0][0] <= x2 <= line1[1][0]:
                return True
        return False

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div

    if line1[1][0] < x < line1[0][0] or line1[0][0] < x < line1[1][0]:
        if line2[1][1] < y < line2[0][1] or line2[0][1] < y < line2[1][1]:
            return x, y
    if line1[1][1] < y < line1[0][1] or line1[0][1] < y < line1[1][1]:
        if line2[1][0] < x < line2[0][0] or line2[0][0] < x < line2[1][0]:
            return x, y
    else:
        return None


def lineIntersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    div = det(xdiff, ydiff)
    if div == 0:
        return True

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div

    return x, y


def nthOccurrence(n, element, list):
    """for n>0, returns index or None"""
    seen = 0
    for i, x in enumerate(list):
        if x == element:
            seen += 1
            if seen == n:
                return i


def circleFlood(point, walls, maxLayers=15):
    valid = {}
    centerPixel = getPixel(point)

    if centerPixel in walls:
        valid[centerPixel] = walls[centerPixel]
    else:
        valid[centerPixel] = []

    sig = inspect.signature(getPixel)
    gridSize = sig.parameters['gridSize'].default

    def getEdges(center, layer):
        edge = []
        for i in range(-layer, layer + 1):
            edge.append((center[0] + i, center[1] - layer))
            edge.append((center[0] + i, center[1] + layer))
        for j in range(-layer + 1, layer):
            edge.append((center[0] - layer, center[1] + j))
            edge.append((center[0] + layer, center[1] + j))
        return edge

    added = True
    layer = 1
    while added:
        added = False
        if layer > maxLayers:
            return None
        edge = getEdges(centerPixel, layer)
        for endPixel in edge:
            offLine = 0
            hitWalls = set()
            wallSquares = 0
            endPoint = ((endPixel[0] + .5) * gridSize, (endPixel[1] + .5) * gridSize)
            pixels = bresenham(point, endPoint)
            for toCheck in pixels:
                if toCheck not in edge:
                    if toCheck not in valid:
                        offLine += 1
                    if toCheck in walls:
                        for wall in walls[toCheck]:
                            if centerPixel in walls:
                                if wall not in walls[centerPixel]:
                                    hitWalls.update(wall)
                            else:
                                hitWalls.update(wall)
            if offLine <= 1 :
                if endPixel in walls:
                    valid[endPixel] = walls[endPixel]
                    added = True
                elif len(hitWalls) <= 1:
                    valid[endPixel] = []
                    added = True
        layer += 1
    return valid


def getPixel(point, gridSize=13):
    return (int(point[0] / gridSize), int(point[1] / gridSize))


def switch_octant_to_zero(octant, point):
    x = point[0]
    y = point[1]
    if octant == 1: return (x, y)
    if octant == 2: return (y, x)
    if octant == 3: return (y, -x)
    if octant == 4: return (-x, y)
    if octant == 5: return (-x, -y)
    if octant == 6: return (-y, -x)
    if octant == 7: return (-y, x)
    if octant == 8: return (x, -y)
    raise Exception("not a valid octant")


def switch_octant_from_zero(octant, point):
    x = point[0]
    y = point[1]
    if octant == 1: return (x, y)
    if octant == 2: return (y, x)
    if octant == 3: return (-y, x)
    if octant == 4: return (-x, y)
    if octant == 5: return (-x, -y)
    if octant == 6: return (-y, -x)
    if octant == 7: return (y, -x)
    if octant == 8: return (x, -y)
    raise Exception("not a valid octant")


def get_octant(A, B):
    x, y = (B[0] - A[0]), (B[1] - A[1])
    octant = [([1, 2], [8, 7]), ([4, 3], [5, 6])][x < 0][y < 0][abs(x) < abs(y)]
    return octant


def bresenhamOld(point1, point2):
    x1, y1 = getPixel(point1)
    x2, y2 = getPixel(point2)
    dx = x2 - x1
    dy = y2 - y1

    sig = inspect.signature(getPixel)
    gridSize = sig.parameters['gridSize'].default
    y1Error = point1[1] - y1 * gridSize
    y2Error = point2[1] - y2 * gridSize
    x1Error = point1[0] - x1 * gridSize
    x2Error = point2[0] - x2 * gridSize

    # Determine how steep the line is
    is_steep = abs(dy) > abs(dx)

    # Rotate line
    if is_steep:
        x1Error, y1Error = y1Error, x1Error
        x2Error, y2Error = y2Error, x2Error
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    # Swap start and end points if necessary and store swap state
    swapped = False
    if x1 > x2:
        x1Error, x2Error = x2Error, x1Error
        y1Error, y2Error = y2Error, y1Error
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
    startError = y1Error
    endError = y2Error
    startShiftError = x1Error
    endShiftError = x2Error
    for x in range(x1, x2 + 1):
        coord = (y, x) if is_steep else (x, y)
        points.append(coord)

        error -= abs(dy)
        if error < 0:
            errorSlope = (endError - startError) / (x2 - x1 - startShiftError / gridSize + endShiftError / gridSize)
            change = (x - x1 - startShiftError)
            if startError + change * errorSlope > 0:
                coord = (y, x + 1) if is_steep else (x + 1, y)
                points.append(coord)
            else:
                coord = (y + ystep, x) if is_steep else (x, y + ystep)
                points.append(coord)
            y += ystep
            error += dx
    return points


def bresenham(point1, point2):
    octant = get_octant(point1, point2)
    point1 = switch_octant_to_zero(octant, point1)
    point2 = switch_octant_to_zero(octant, point2)
    shift = switch_octant_to_zero(octant, (.5, .5))
    x1, y1 = getPixel(point1)
    x2, y2 = getPixel(point2)
    slope = (point2[1] - point1[1]) / (point2[0] - point1[0])
    sig = inspect.signature(getPixel)
    gridSize = sig.parameters['gridSize'].default
    points = []
    lastX = x1
    for y in range(y1 + int(.5 + shift[1]), y2 + int(.5 + shift[1])):
        x = (y * gridSize - point1[1]) / slope + point1[0]
        xPixel = int(x / gridSize)
        points.append((xPixel, y - int(.5 + shift[1])))
        for x in range(lastX, xPixel):
            points.append((x, y - int(.5 + shift[1])))
        lastX = xPixel
    for x in range(lastX, x2 + 1):
        points.append((x, y2))
    return [switch_octant_from_zero(octant, point) for point in points]


def bresenhamCircle(center, radius):
    x0, y0 = getPixel(center)
    x = radius
    y = 0
    err = 0
    pixels = []
    while x >= y:
        pixels.append((x0 + x, y0 + y))
        pixels.append((x0 + y, y0 + x))
        pixels.append((x0 - y, y0 + x))
        pixels.append((x0 - x, y0 + y))
        pixels.append((x0 - x, y0 - y))
        pixels.append((x0 - y, y0 - x))
        pixels.append((x0 + y, y0 - x))
        pixels.append((x0 + x, y0 - y))

        if err <= 0:
            y += 1
            err += 2*y + 1
        if err > 0:
            x -= 1
            err -= 2*x + 1
    return pixels