import math


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


def getSnapPoints(connectedWalls, sharedPoint, insidePoint, shift=3):
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


def circleFlood(point, walls, gridSize=10, maxLayers=35):
    start = (int(round(point[0] / gridSize)), int(round(point[1] / gridSize)))
    layer = 0
    valid = {}
    valid[start] = None
    added = True
    while added:
        added = False
        layer += 1
        if layer > maxLayers:
            return None
        for i in range(-layer, layer + 1):
            for j in range(-layer, layer + 1):
                if abs(i) == layer or abs(j) == layer:
                    square = (start[0] + i, start[1] + j)
                    pixels = getLastBresenham(start, square, getRange=3)
                    offLine = 0
                    hitWalls = set()
                    for toCheck in pixels:
                        if toCheck not in valid:
                            offLine += 1
                        if toCheck in walls:
                            for wall in walls[toCheck]:
                                hitWalls.update(wall)
                    if offLine == 1 and len(hitWalls) <= 8:
                        added = True
                        if square in walls:
                            valid[square] = walls[square]
                        else:
                            valid[square] = []

    return valid


def getPixel(point, gridSize=10):
    return (int(round(point[0] / gridSize)), int(round(point[1] / gridSize)))


def getLastBresenham(start, end, getRange=5):
    x1, y1 = start
    x2, y2 = end
    dx = x2 - x1
    dy = y2 - y1

    # Determine how steep the line is
    is_steep = abs(dy) > abs(dx)

    # Rotate line
    if is_steep:
        x1, y1, x2, y2 = y1, x1, y2, x2

    # Swap start and end points if necessary and store swap state
    if x1 > x2:
        x1, x2, y1, y2 = x2, x1, y2, y1

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
            y += ystep
            error += dx
    # if points[0] == end:
    #     return points[1: 1 + getRange]
    # elif points[0] == start:
    #     return points[-2 - getRange:-2]
    return points
    #raise Exception("could not find last")


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
    x1, y1 = getPixel(point1, gridSize=gridSize)
    x2, y2 = getPixel(point2, gridSize=gridSize)
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


def bresenhamCircle(center, radius, gridSize=10):
    x0, y0 = (int(round(center[0] / gridSize)), int(round(center[1] / gridSize)))
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