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


def ang(lineA, lineB):
    x1 = lineA[1][0] - lineA[0][0]
    y1 = lineA[1][1] - lineA[0][1]

    x2 = lineB[1][0] - lineB[0][0]
    y2 = lineB[1][1] - lineB[0][1]

    detV = det((x1, y1), (x2, y2))
    dotV = dot((x1, y1), (x2, y2))
    return math.atan2(detV, dotV)


def getBisectorAngle(line1, line2):
    x1 = line1[0][0] - line1[1][0]
    y1 = line1[0][1] - line1[1][1]
    x2 = line2[0][0] - line2[1][0]
    y2 = line2[0][1] - line2[1][1]

    theta_1 = math.atan2(y1, x1)
    theta_2 = math.atan2(y2, x2)

    return (theta_1 + theta_2) / 2


def det(a, b):
    return a[0] * b[1] - a[1] * b[0]


def dot(vA, vB):
    return vA[0] * vB[0] + vA[1] * vB[1]


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


def distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def distanceP(point1, point2):
    return distance(point1[0], point1[1], point2[0], point2[1])


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
