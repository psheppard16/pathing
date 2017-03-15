__author__ = 'Preston Sheppard'
import math
class Wall:
    def __init__(self, x1, y1, x2, y2):
        self.cap1 = (x1, y1)
        self.cap2 = (x2, y2)

    def crossesWall(self, pX1, pY1, pX2, pY2):
        return self.intersect((pX1, pY1), (pX2, pY2), self.cap1, self.cap2)

    def line(self, p1, p2):
        A = (p1[1] - p2[1])
        B = (p2[0] - p1[0])
        C = (p1[0]*p2[1] - p2[0]*p1[1])
        return A, B, -C

    def ccw(self, A,B,C):
            return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

    # Return true if line segments AB and CD intersect
    def intersect(self, A,B,C,D):
        if self.ccw(A,C,D) != self.ccw(B,C,D) and self.ccw(A,B,C) != self.ccw(A,B,D):
            return self.angle(A, B, C, D)
        else:
            return False

    def dot(self, vA, vB):
        return vA[0]*vB[0]+vA[1]*vB[1]

    def angle(self, A, B, C, D):
        lineA = (A, B)
        lineB = (C, D)
        # Get nicer vector form
        vA = [(lineA[0][0]-lineA[1][0]), (lineA[0][1]-lineA[1][1])]
        vB = [(lineB[0][0]-lineB[1][0]), (lineB[0][1]-lineB[1][1])]
        # Get dot prod
        dot_prod = self.dot(vA, vB)
        # Get magnitudes
        magA = self.dot(vA, vA)**0.5
        magB = self.dot(vB, vB)**0.5
        # Get cosine value
        cos_ = dot_prod/magA/magB
        # Get angle in radians and then convert to degrees
        angle = math.acos(dot_prod/magB/magA)
        # Basically doing angle <- angle mod 360
        ang_deg = math.degrees(angle)%360

        if ang_deg-180>=0:
            # As in if statement
            return 360 - ang_deg
        else:

            return ang_deg

    def getTuple(self):
        return self.cap1, self.cap2