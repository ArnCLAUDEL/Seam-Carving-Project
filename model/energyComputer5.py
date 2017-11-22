import numpy
import math
import time

def timer(f):
    def f_timer(self, *args, **kwargs):
        start = time.time()
        res = f(self, *args, **kwargs)
        end = time.time()
        print("Computation time:", end - start)
        return res
    return f_timer

class EnergyComputer:

    def __init__(self, image):
        self.image = image
        self.energyComputed = {}
        self.intensityComputed = {}
        self.count = 0
        self.start, self.end = 0,0
        self.__gx_coords = [(-1,-1), (-1,0), (-1,1), (1,-1), (1,0), (1,1)]
        self.__gy_coords = [(-1,-1), (0,-1), (1,-1), (-1,1), (0,1), (1,1)]

    def inbound(self, x, y):
        return 0 <= x < self.image.w and 0 <= y < self.image.h

    def fitToGrid(self, x, y):
        x = 1 if x <= 0 else (self.image.w - 3 if x >= self.image.w - 3 else x)
        y = 1 if y <= 0 else (self.image.h - 3 if y >= self.image.h - 3 else y)
        return x,y

    @timer
    def stupid_seam_finder(self):
        pe = {"seam_energy":math.inf, "path":[]}
        start1,end1,start2,end2 = float(0),float(0),float(0),float(0)
        fit, e_min, energy = self.fitToGrid, self.energy_min, self.energy
        w,h = self.image.w, self.image.h
        self.count = 0
        for i in range(1, self.image.w -2):
            x, seam_energy, path = i-1, 0, []
            append = path.append
            for j in range(1, h-1):
                y = j
                e1, e2, e3 = energy(x - 1, y), energy(x, y), energy(x + 1, y)
                e = min(e1, e2, e3)
                c = (x + 1, y) if e == e3 else ((x, y) if e == e2 else (x - 1, y))
                seam_energy += e
                append(c)
                x = c[0]
                x = 1 if x <= 0 else (w - 3 if x >= w - 3 else x)
            if pe["seam_energy"] > seam_energy:
                pe = {"seam_energy":seam_energy,"path":path}
        print(self.end - self.start)
        print(end1-start1,"+",end2-start2)
        print(len(self.energyComputed), self.count)
        return pe

    """
        +150ms
    """
    def energy_min(self, x, y):
        e1, e2, e3 = self.energy(x - 1, y), self.energy(x, y), self.energy(x + 1, y)
        e = min(e1, e2, e3)
        c = (x + 1, y) if e == e3 else ((x, y) if e == e2 else (x - 1, y))
        return c,e

    def energy(self, x, y):
        if x == 0 or y == 0:
            return math.inf
        try:
            return self.energyComputed[(x,y)]
        except KeyError:
            pass

        gx, gy = self.g3(x, y, self.__gx_coords), self.g3(x, y, self.__gy_coords)

        res = math.sqrt(gx*gx + gy*gy)
        self.energyComputed[(x,y)] = res
        return res

    def g(self, x, y, c1, c2, c3, c4, c5, c6):
        return self.g2(x, y, c1) + self.g2(x, y, c2) * 2 + self.g2(x, y, c3) - self.g2(x, y, c4) - self.g2(x, y, c5) * 2 - self.g2(x, y, c6)

    def g2(self, x, y, c):
        x2,y2 = x+c[0], y+c[1]

        try:
            res = self.intensityComputed[(x2, y2)]
        except KeyError:
            res = intensity(self.image.get(x2, y2))
            self.intensityComputed[(x2, y2)] = res
        return res

    def g3(self, x, y, c_list):
        v = []
        for c in c_list:
            x2, y2 = x + c[0], y + c[1]
            try:
                res = self.intensityComputed[(x2, y2)]
            except KeyError:
                res = intensity(self.image.get(x2, y2))
                self.intensityComputed[(x2, y2)] = res
            v.append(res)
        return v[0] + v[1] * 2 + v[2] - v[3] - v[4] * 2 - v[5]

    def removeVerticalSeam(self, path, iX=1, iY=0):
        energy = self.energy
        for (x,y) in path:
            for x2 in range(x,self.image.w-2):
                self.energyComputed[(x,y)] = energy(x+iX,y+iY)


def intensity(pixelColors):
    return int(pixelColors[0]) + int(pixelColors[1]) + int(pixelColors[2])
