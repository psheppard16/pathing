import math
import Game.Pathing.geometry as geo
from Game.Pathing.wall import WallObject
class PathObject():
    def __init__(self, x, y, creator, tolerance=None, sets=None, targetPoint=None, hasConnected=False, hasAdvanced=False, hasBacktracked=False,
                 hasBranched=False, hasFinished=False, anchorPoint=None, hasSplit=False):
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
        self.hasSplit = hasSplit

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

    def reduce(self):
        if self.creator and self.creator.creator and not self.hasBeenEliminated:
            if not self.creator.hasBeenEliminated and not self.creator.creator.hasBeenEliminated:
                point1 = self.position
                point2 = self.creator.position
                point3 = self.creator.creator.position

                intersectedWalls = []
                for wall in WallObject.wallList:
                    if wall.intersects((point1, point3)):
                        intersectedWalls.append(wall)

                if not intersectedWalls:
                    self.creator.children.remove(self)
                    self.creator = self.creator.creator
                    self.creator.children.append(self)
                else:
                    blockingWalls = {}
                    lengths = {}

                    while intersectedWalls: #generate blocking walls kosherly maybe
                        wall = intersectedWalls.pop(0)
                        for point in wall.line:
                            if point not in blockingWalls and geo.liesInTriangle(point, (point1, point2, point3)):
                                blockingWalls[point] = wall.connections[point] + [wall]
                                lengths[point] = geo.distanceP(point1, point) + geo.distanceP(point3, point)
                                intersectedWalls.extend(wall.connections[point])

                    while blockingWalls:
                        anchorPoint = min(lengths, key=lengths.get)
                        connectedWalls = blockingWalls.pop(anchorPoint)
                        lengths.pop(anchorPoint)
                        if anchorPoint != self.creator.anchorPoint:
                            snapPoints = geo.getSnapPoints(connectedWalls, anchorPoint, self.position)
                            for snapPoint in snapPoints:
                                valid = True
                                for wall in connectedWalls:
                                    if wall.intersects((point1, snapPoint)) or wall.intersects((snapPoint, point3)):
                                        valid = False
                                if valid:
                                    new = PathObject(snapPoint[0], snapPoint[1], self.creator.creator, anchorPoint=anchorPoint)
                                    if new and not new.hasBeenEliminated:
                                        self.creator.graft(new, includeSelf=False)

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
                        if geo.distanceP(pathObject.position, self.position) < tolerance:
                            toCopy = pathObject
                            copy = toCopy.copy(self, hasConnected=True, hasBranched=True, hasAdvanced=True, hasBacktracked=True)
                            while copy and not copy.hasBeenEliminated:
                                toCopy = pathObject.creator
                                copy = toCopy.copy(copy, hasConnected=True, hasBranched=True, hasAdvanced=True, hasBacktracked=True)

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
                if geo.distanceP(self.position, pointToCheck.position) < tolerance and not self.hasFinished:
                    self.eliminate()
                    break
                pointToCheck = pointToCheck.creator

    def removeSlowerPaths(self, tolerance):
        if not self.hasBeenEliminated:
            objectsToEliminate = []
            for pathObject in self.pathObjectList:
                if pathObject != self:
                    if geo.distanceP(self.position, pathObject.position) < tolerance:
                        length1 = self.getPromisedLength()
                        length2 = pathObject.getPromisedLength()
                        if self.anchorPoint and pathObject.anchorPoint:
                            pass
                            if pathObject.anchorPoint == self.anchorPoint:
                                if length1 >= length2:
                                    reachable = True
                                    for wall in WallObject.wallList:
                                        if wall.intersects((self.position, pathObject.position)):
                                            reachable = False
                                            break
                                    if reachable:
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
                    pathObject = objectsToEliminate.pop()
                    reachable = True
                    for wall in WallObject.wallList:
                        if wall.intersects((self.position, pathObject.position)):
                            reachable = False
                            break
                    if reachable:
                        pathObject.eliminate()

    def finishPath(self, tolerance):
        if self.hasFinished:
            raise Exception(str(self) + " already finished")
        if self.hasBeenEliminated:
            raise Exception(str(self) + " has been eliminated")
        if geo.distanceP(self.position, self.targetPoint) < tolerance * 2:
            PathObject(self.targetPoint[0], self.targetPoint[1], self, hasConnected=True, hasAdvanced=True,
                       hasBacktracked=True, hasBranched=True, hasFinished=True, anchorPoint=self.targetPoint)

    def copy(self, creator, hasConnected=None, hasAdvanced=None, hasBacktracked=None, hasBranched=None, hasFinished=None, hasSplit=None):
        return PathObject(self.x, self.y, creator,
                        hasConnected= hasConnected if hasConnected else self.hasConnected,
                        hasAdvanced= hasAdvanced if hasAdvanced else self.hasAdvanced,
                        hasBacktracked= hasBacktracked if hasBacktracked else self.hasBacktracked,
                        hasBranched= hasBranched if hasBranched else self.hasBranched,
                        hasFinished= hasFinished if hasFinished else self.hasFinished,
                        anchorPoint= self.anchorPoint,
                        hasSplit= hasSplit if hasSplit else self.hasSplit)

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

    def split(self, wall):
        if not self.hasSplit and not self.hasBeenEliminated:
            connectedWalls = wall.connections1
            for wall1 in connectedWalls:
                wall1 = wall.line
            points = geo.getSnapPoints(connectedWalls, wall.point1, (self.x, self.y))
            for point in points:
                self.hasSplit = True
                PathObject(point[0], point[1], self, anchorPoint=wall.point1, hasSplit=True)

            connectedWalls = wall.connections2
            for wall1 in connectedWalls:
                wall1 = wall.line
            points = geo.getSnapPoints(connectedWalls, wall.point2, (self.x, self.y))
            for point in points:
                self.hasSplit = True
                PathObject(point[0], point[1], self, anchorPoint=wall.point2, hasSplit=True)
