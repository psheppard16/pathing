import Pathing.geometry as geo
import math
from Pathing.wall import WallObject
import itertools
class PathObject():
    def __init__(self, x, y, creator, tolerance=None, sets=None, targetPoint=None, hasConnected=False, hasAdvanced=False, hasBacktracked=False,
                 hasBranched=False, hasFinished=False, anchorPoint=None):
        self.x = x
        self.y = y
        self.position = (x, y)
        self.creator = creator
        self.children = []
        self.hasAdvanced = hasAdvanced
        self.hasBranched = hasBranched
        self.hasBacktracked = hasBacktracked
        self.hasBeenEliminated = False
        self.hasFinished = hasFinished
        self.hasConnected = hasConnected
        self.anchorPoint = anchorPoint

        if self.creator:
            self.sets = self.creator.sets
            self.tolerance = self.creator.tolerance

            self.pathObjectList = self.creator.pathObjectList
            self.pathObjectList.append(self)
            self.targetPoint = creator.targetPoint
            self.creator.children.append(self)

            self.removeBackTracks(self.tolerance)

            self.removeIntersectingPaths(WallObject.wallList)

            self.removeSlowerPaths(self.tolerance)

            self.simplify()

            self.connect(self.tolerance)
        else:
            if targetPoint is None:
                raise Exception(
                    "A point without a creator must either be a start point or endpoint (startPoint=True/False)")
            if tolerance is None:
                raise Exception(
                    "A point without a creator must have a value for tolerance")
            if sets is None:
                raise Exception(
                    "A point without a creator must have a value for sets")

            self.tolerance = tolerance

            self.sets = sets
            self.pathObjectList = [self]
            self.sets.append(self.pathObjectList)

            self.targetPoint = targetPoint
            self.anchorPoint = (self.x, self.y)
            self.hasSnapped = True
        if not self.hasFinished and not self.hasBeenEliminated:
            self.finishPath(self.tolerance)

    def simplify(self):
        intersectedWalls = self.reduce()
        if intersectedWalls and not self.creator.anchorPoint:
            self.snap(intersectedWalls)

    def reduce(self):
        if self.creator and self.creator.creator and not self.hasBeenEliminated:
            point1 = self.position
            point3 = self.creator.creator.position

            intersectedWalls = []
            for wall in WallObject.wallList:
                if wall.intersects((point1, point3)):
                    intersectedWalls.append(wall)

            if intersectedWalls:
                return intersectedWalls
            else:
                self.creator.children.remove(self)
                self.creator = self.creator.creator
                self.creator.children.append(self)

    def snap(self, intersectedWalls):
        point1 = self.position
        point2 = self.creator.position
        point3 = self.creator.creator.position
        connectedWalls = {}

        for wall in WallObject.wallList:
            for point in wall.line:
                if point not in connectedWalls and geo.liesInTriangle(point, (point1, point2, point3)):
                    connectedWalls[point] = wall.connections[point] + [wall]
                    intersectedWalls.extend(wall.connections[point])

        pathAdded = False
        nodesToTry = 1
        while not pathAdded and nodesToTry < 2:
            lengths = {}
            permutaions = itertools.permutations(connectedWalls, nodesToTry)
            for permutaion in permutaions:
                length = 0
                lastPoint = point1
                for point in permutaion:
                    length += geo.distanceP(point, lastPoint)
                    lastPoint = point
                length += geo.distanceP(lastPoint, point3)
                lengths[permutaion] = length

            while lengths and not pathAdded:
                permutaion = min(lengths, key=lengths.get)
                lengths.pop(permutaion)
                last = self.creator.creator
                for anchorPoint in permutaion:
                    if (last and not last.hasBeenEliminated or last is self.creator.creator):
                        connected = connectedWalls[anchorPoint]
                        snapPoint = geo.getSnapPoints(connected, anchorPoint, self.creator.position, shift=3)
                        last = PathObject(snapPoint[0], snapPoint[1], last, anchorPoint=anchorPoint)
                    else:
                        break
                if last and not last.hasBeenEliminated:
                    self.creator.graft(last, includeSelf=False)
                    pathAdded = True
            nodesToTry += 1

    def getLength(self):
        length = 0
        pathObject = self
        while pathObject.creator:
            length += geo.distanceP(pathObject.position, pathObject.creator.position)
            pathObject = pathObject.creator
        return length

    def getPromisedLength(self):
        length = self.getLength()
        distanceToEndPoint = geo.distanceP(self.position, self.targetPoint)
        return length + distanceToEndPoint

    def connect(self, tolerance):
        if not self.hasConnected and not self.hasBeenEliminated:
            for pathObjectList in self.sets:
                if self not in pathObjectList:
                    for pathObject in pathObjectList:
                        if pathObject.creator and geo.lineToPoint((pathObject.position, pathObject.creator.position), self.position) < tolerance:
                            toCopy = pathObject
                            copy = self
                            while copy and not copy.hasBeenEliminated and toCopy:
                                copy = toCopy.copy(copy, hasConnected=True, hasBranched=True, hasAdvanced=True, hasBacktracked=True)
                                toCopy = toCopy.creator
                            self.hasAdvanced = True
                            self.hasBranched = True
                            self.hasBacktracked = True
                            pathObject.hasAdvanced = True
                            pathObject.hasBranched = True
                            pathObject.hasBacktracked = True

    def advance(self, resolution, angleResolution, advance):
        if self.hasAdvanced:
            raise Exception(str(self) + " already advanced")
        if self.hasBeenEliminated:
            raise Exception(str(self) + " has been eliminated")
        self.hasAdvanced = True
        startAngle = math.atan2(self.targetPoint[1] - self.y, self.targetPoint[0] - self.x)
        for step in range(-advance, advance + 1):
            angle = startAngle + step * math.pi * 2 / angleResolution
            PathObject(self.x + math.cos(angle) * resolution,
                       self.y + math.sin(angle) * resolution, self)

    def branch(self, resolution, angleResolution, advance, branch):
        if not self.hasAdvanced:
            raise Exception(str(self) + " has not advanced yet")
        if self.hasBranched:
            raise Exception(str(self) + " already branched")
        if self.hasBeenEliminated:
            raise Exception(str(self) + " has been eliminated")
        self.hasBranched = True
        startAngle = math.atan2(self.targetPoint[1] - self.y, self.targetPoint[0] - self.x)
        for step in range(advance + 1, angleResolution - advance):
            if step < advance + branch + 1 or step >= angleResolution - advance - branch:
                angle = startAngle + step * math.pi * 2 / angleResolution
                PathObject(self.x + math.cos(angle) * resolution,
                           self.y + math.sin(angle) * resolution, self)

    def backtrack(self, resolution, angleResolution, advance, branch):
        if not self.hasAdvanced:
            raise Exception(str(self) + " has not advanced yet")
        if not self.hasBranched:
            raise Exception(str(self) + " has not branched yet")
        if self.hasBacktracked:
            raise Exception(str(self) + " already backtracked")
        if self.hasBeenEliminated:
            raise Exception(str(self) + " has been eliminated")
        self.hasBacktracked = True
        startAngle = math.atan2(self.targetPoint[1] - self.y, self.targetPoint[0] - self.x)
        for step in range(advance + branch + 1, angleResolution - advance - branch):
            angle = startAngle + step * math.pi * 2 / angleResolution
            PathObject(self.x + math.cos(angle) * resolution,
                       self.y + math.sin(angle) * resolution, self)

    def eliminate(self):
        if self.hasBeenEliminated:
            raise Exception("object has already been eliminated")

        if not self.creator:
            raise Exception("cannot eliminate the start or end point")

        while self.children:
            self.children[0].eliminate()

        self.pathObjectList.remove(self)

        self.creator.children.remove(self)

        self.hasBeenEliminated = True

        del self

    def removeIntersectingPaths(self, wallList):
        if not self.creator:
            raise Exception("Path must be a child in order to remove intersecting paths")
        if not self.hasBeenEliminated:
            for wall in wallList:
                if wall.intersects((self.position, self.creator.position)):
                    self.eliminate()
                    break

    def removeBackTracks(self, tolerance):
        if not self.creator:
            raise Exception("Path must be a child in order to remove backtracks")
        if not self.hasBeenEliminated:
            pointToCheck = self.creator
            while pointToCheck.creator:
                if geo.lineToPoint((pointToCheck.position, pointToCheck.creator.position), self.position) < tolerance and not self.hasFinished and not self.hasConnected:
                    self.eliminate()
                    break
                pointToCheck = pointToCheck.creator

    def removeSlowerPaths(self, tolerance):
        if not self.hasBeenEliminated:
            objectsToEliminate = []
            for pathObject in self.pathObjectList:
                if pathObject != self and self.creator != pathObject:
                    if geo.distanceP(self.position, pathObject.position) < tolerance:
                        reachable = True
                        for wall in WallObject.wallList:
                            if wall.intersects((self.position, pathObject.position)):
                                reachable = False
                                break
                        if reachable:
                            length1 = self.getPromisedLength()
                            length2 = pathObject.getPromisedLength()
                            if self.anchorPoint and pathObject.anchorPoint:
                                if pathObject.anchorPoint == self.anchorPoint:
                                    if length1 >= length2:
                                            self.eliminate()
                                            break  # break so path doesnt delete itself twice
                                    if length1 < length2:
                                        objectsToEliminate.append(pathObject)
                            elif not self.anchorPoint and not pathObject.anchorPoint:
                                if length1 >= length2:
                                    self.eliminate()
                                    break
                                if length1 < length2 and not self.creator.hasBacktracked:   # only delete existing objects if path isnt a backtrack
                                    objectsToEliminate.append(pathObject)                   # this avoids overwriting identical paths after all paths
                                                                                        # are almost resolved

            if not self.hasBeenEliminated and objectsToEliminate:
                while objectsToEliminate:  # delete objects after to avoid iterating while deleting
                    objectsToEliminate.pop().eliminate()

    def prune(self, angleResolution):
        if not self.hasBeenEliminated and self.creator and not self.anchorPoint:
            if self.children: #eliminate paths which have not reduced properly
                self.eliminate()
            else: #eliminated paths which are surrounded by valid paths
                left = False
                right = False
                for pathObject in self.pathObjectList:
                    if pathObject != self and pathObject.creator == self.creator:
                        if geo.lineToPoint((pathObject.position, pathObject.creator.position), self.position) < self.tolerance:
                            angle = geo.ang((self.creator.position, self.position), (pathObject.creator.position, pathObject.position))
                            if -math.pi * 2 / angleResolution < angle < 0:
                                left = True
                            elif math.pi * 2 / angleResolution > angle > 0:
                                right = True
                            elif angle == 0:
                                left = True
                                right = True
                            if left and right:
                                self.eliminate()
                                break

    def finishPath(self, tolerance):
        if self.hasFinished:
            raise Exception(str(self) + " already finished")
        if self.hasBeenEliminated:
            raise Exception(str(self) + " has been eliminated")
        if geo.distanceP(self.position, self.targetPoint) < tolerance * 2:
            PathObject(self.targetPoint[0], self.targetPoint[1], self, hasConnected=True, hasAdvanced=True,
                       hasBacktracked=True, hasBranched=True, hasFinished=True, anchorPoint=self.targetPoint)

    def copy(self, creator, hasConnected=None, hasAdvanced=None, hasBacktracked=None, hasBranched=None, hasFinished=None):
        return PathObject(self.x, self.y, creator,
                        hasConnected= hasConnected if hasConnected else self.hasConnected,
                        hasAdvanced= hasAdvanced if hasAdvanced else self.hasAdvanced,
                        hasBacktracked= hasBacktracked if hasBacktracked else self.hasBacktracked,
                        hasBranched= hasBranched if hasBranched else self.hasBranched,
                        hasFinished= hasFinished if hasFinished else self.hasFinished,
                        anchorPoint= self.anchorPoint)

    def copyChildren(self, creator):
        cousins = []
        for pathObject in self.children:
            copy = pathObject.copy(creator)
            cousins.append((pathObject, copy))
        return cousins

    def graft(self, creator, includeSelf=True):
        if creator and not creator.hasBeenEliminated:
            if includeSelf:
                selfCopy = self.copy(creator)
                if selfCopy and not selfCopy.hasBeenEliminated:
                    cousins = self.copyChildren(selfCopy)
                    while cousins:
                        pair = cousins.pop()
                        original = pair[0]
                        copy = pair[1]
                        if copy and not copy.hasBeenEliminated:
                            cousins.extend(original.copyChildren(copy))
            else:
                creators = self.copyChildren(creator)
                while creators:
                    pair = creators.pop()
                    origional = pair[0]
                    cousin = pair[1]
                    if cousin and not cousin.hasBeenEliminated:
                        creators.extend(origional.copyChildren(cousin))