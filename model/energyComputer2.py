import numpy
import math
import time

class EnergyData:
    def __init__(self, se, c, previousED):
        self.se = se
        self.c = c
        self.previousED = previousED

class EnergyComputer:
    def __init__(self, image):
        self.image = image
        self.energyComputed = {}
        self.intensityComputed = {}
        self.ec2 = {(i,j):EnergyData(0,(i,j),None) for i in range(0,image.w) for j in range(0,image.h)}

    def inbound(self, x, y):
        return (x >= 0 and x < self.image.w
                and y >= 0 and y < self.image.h)

    def fitToGrid(self, x, y):
        x = max(1, x)
        x = min(self.image.w - 3, x)
        y = max(1, y)
        y = max(self.image.h - 3, y)
        return (x, y)

    def timer(f):
        def f_timer(self, *args, **kwargs):
            start = time.time()
            res = f(self, *args, **kwargs)
            end = time.time()
            print("Computation time:", end - start)
            return res
        return f_timer

    def stupid_seam_finder(self):
        pe = {"seam_energy": 0, "path": []}
        for i in range(1, self.image.h - 2):
            y = i
            for j in range(1, self.image.w - 2):
                x = j
                e = self.energy(x,y)

                se1 = self.energy(x - 1, y)
                se2 = self.energy(x, y)
                se3 = self.energy(x + 1, y)
                d = {se1: (x - 1, y), se2: (x, y), se3: (x + 1, y)}
                se_min = min(se1, se2, se3)
                se = se_min + e
                ed = EnergyData(se, (x,y), self.ec2[d[se_min]])
                self.ec2[(x,y)] = ed

        print(self.getMinimalSeam())
        return pe

    def getMinimalSeam(self):
        ed = EnergyData(math.inf, None, None)
        for i in range(0,self.image.w-1):
            ed2 = self.ec2[(i,self.image.h-1)]
            if( ed2.se < ed.se):
                ed = ed2
        path = []
        while(ed.previousED != None):
            path.append(ed.c)
            ed = ed.previousED
        return path

    def energy(self, x, y):
        if x == 0 or y == 0:
            return math.inf
        try:
            res = self.energyComputed[(x, y)]
            return res
        except KeyError:
            pass

        gx = self.g(x, y, (-1, -1), (-1, 0), (-1, 1))
        gx -= self.g(x, y, (1, -1), (1, 0), (1, 1))

        gy = self.g(x, y, (-1, -1), (0, -1), (1, -1))
        gy -= self.g(x, y, (-1, 1), (0, 1), (1, 1))

        res = math.sqrt(gx * gx + gy * gy)
        # res = gx*gx + gy*gy
        self.energyComputed[(x, y)] = res
        return res

    def g(self, x, y, c1, c2, c3):
        return self.g2(x, y, c1) + self.g2(x, y, c2) * 2 + self.g2(x, y, c3)

    def g2(self, x, y, c):
        x2 = x + c[0]
        y2 = y + c[1]
        try:
            return self.intensityComputed[(x2, y2)]
        except KeyError:
            res = intensity(self.image.get(x2, y2))
            self.intensityComputed[(x2, y2)] = res
            return res

    def removeVerticalSeam(self, path):
        for (x, y) in path:
            for x2 in range(x, self.image.w - 2):
                self.energyComputed[(x, y)] = self.energy(x + 1, y)
                self.energyComputed[(x - 1, y)] = self.energy(x - 1, y)


def intensity(pixelColors):
    return int(pixelColors[0]) + int(pixelColors[1]) + int(pixelColors[2])
