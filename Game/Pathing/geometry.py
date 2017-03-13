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
    x2 = lineB[1][0] - lineB[0][0]

    y1 = lineA[1][1] - lineA[0][1]
    y2 = lineB[1][1] - lineB[0][1]

    dot = x1 * x2 + y1 * y2  # dot product
    det = x1 * y2 - y1 * x2  # determinant
    angle = math.atan2(det, dot)  # atan2(y, x) or atan2(sin, cos)
    return angle

def getBisectorAngle(line1, line2):
    sharedPoint = lineIntersection(line1, line2)

    if sharedPoint is True:
        return ang(((0, 0), (1, 0)), line1) + math.pi / 2
    else:
        secondPoint1 = line1[0] if not (
        int(line1[0][0]) == int(sharedPoint[0]) and int(line1[0][1]) == int(sharedPoint[1])) else line1[1]
        secondPoint2 = line2[0] if not (
        int(line2[0][0]) == int(sharedPoint[0]) and int(line2[0][1]) == int(sharedPoint[1])) else line2[1]

    x1 = secondPoint1[0] - sharedPoint[0]
    y1 = secondPoint1[1] - sharedPoint[1]

    x2 = secondPoint2[0] - sharedPoint[0]
    y2 = secondPoint2[1] - sharedPoint[1]

    theta_1 = math.atan2(y1, x1)
    theta_2 = math.atan2(y2, x2)

    middle_theta = (theta_1 + theta_2) / 2
    return middle_theta

def det(a, b):
    return a[0] * b[1] - a[1] * b[0]

def dot(vA, vB):
    return vA[0] * vB[0] + vA[1] * vB[1]

def getSnapPoints(connectedWalls, sharedPoint, insidePoint, shift=3):
    if len(connectedWalls) > 1:
        angledWalls = []
        insideLine = (sharedPoint, insidePoint)
        for wall in connectedWalls:
            for index, point in enumerate(wall.line):
                if point == sharedPoint:
                    angledWalls.append((wall, ang(insideLine, (sharedPoint, wall.line[index - 1]))))

        ordered = []  # order the walls based on angle to insideLine
        while (angledWalls):
            smallest = None
            for wallAndAngle in angledWalls:
                if not smallest:
                    smallest = wallAndAngle
                else:
                    if wallAndAngle[1] < smallest[1]:
                        smallest = wallAndAngle
            ordered.append(angledWalls.pop(angledWalls.index(smallest)))

        first = ordered[0][0]  # closest wall clockwise
        second = ordered[-1][0]  # closest wall counterclockwise

        bisectorAngle = getBisectorAngle(first.line, second.line)  # the bisector line of the two walls
        x1 = sharedPoint[0] - math.cos(bisectorAngle) * shift
        y1 = sharedPoint[1] - math.sin(bisectorAngle) * shift

        x2 = sharedPoint[0] + math.cos(bisectorAngle) * shift
        y2 = sharedPoint[1] + math.sin(bisectorAngle) * shift

        return (x1, y1), (x2, y2)
    elif len(connectedWalls) == 1:
        if connectedWalls[0].point1 == sharedPoint:
            secondPoint = connectedWalls[0].point2
        else:
            secondPoint = connectedWalls[0].point1
        run = sharedPoint[0] - secondPoint[0]
        rise = sharedPoint[1] - secondPoint[1]

        wallAngle = math.atan2(rise, run)
        x1 = sharedPoint[0] + math.cos(wallAngle) * shift
        y1 = sharedPoint[1] + math.sin(wallAngle) * shift

        return (x1, y1),
    else:
        raise Exception("there must be at least one connected wall")

def liesInTriangle(point, triangle):
    tPoint0 = triangle[0]
    tPoint1 = triangle[1]
    tPoint2 = triangle[2]

    area = ((tPoint1[1] - tPoint2[1]) * (tPoint0[0] - tPoint2[0]) + (tPoint2[0] - tPoint1[0]) * (tPoint0[1] - tPoint2[1]))
    if area == 0:
        return False

    alpha = ((tPoint1[1] - tPoint2[1]) * (point[0] - tPoint2[0]) + (tPoint2[0] - tPoint1[0]) * (point[1] - tPoint2[1])) / area

    beta = ((tPoint2[1] - tPoint0[1]) * (point[0] - tPoint2[0]) + (tPoint0[0] - tPoint2[0]) * (point[1] - tPoint2[1])) / area

    gamma = 1 - alpha - beta

    return alpha > 0 and beta > 0  and gamma > 0

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
    for i,x in enumerate(list):
        if x==element:
            seen += 1
            if seen==n:
                return i