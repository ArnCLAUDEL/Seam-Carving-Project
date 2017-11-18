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

    def inbound(self, x, y):
        return 0 <= x < self.image.w and 0 <= y < self.image.h

    def fitToGrid(self, x, y):
        x,x = max(1, x),min(self.image.w-3, x)
        y,y = max(1,y),max(self.image.h-3, y)
        return x,y

    @timer
    def stupid_seam_finder(self):
        pe = {"seam_energy":math.inf, "path":[]}
        start1,end1 = 0,0
        start2, end2= 0, 0
        for i in range(1, self.image.w -2):
            x = i-1
            seam_energy = 0
            path = []
            for j in range(1, self.image.h -1):
                y = j
                c,e = self.energy_min(x, y)
                seam_energy += e
                path.append(c)
                x = c[0]
                x = self.fitToGrid(x,y)[0]
            if pe["seam_energy"] > seam_energy:
                pe["seam_energy"] = seam_energy
                pe["path"] = path
        print(end1-start1," + ",end2 - start2)
        return pe

    """
        +150ms
    """
    def energy_min(self, x, y):
        e1, e2, e3 = self.energy(x - 1, y), self.energy(x, y), self.energy(x + 1, y)
        e = min(e1, e2, e3)
        if e == e3:
            c = (x + 1, y)
        elif e == e2:
            c = (x, y)
        else:
            c = (x - 1, y)
        return c,e

    def energy(self, x, y):
        if x == 0 or y == 0:
            return math.inf
        try:
            res = self.energyComputed[(x,y)]
            return res
        except KeyError:
            pass

        gx = self.g(x, y, (-1,-1), (-1,0), (-1,1)) - self.g(x, y, (1,-1), (1,0), (1,1))
        gy = self.g(x, y, (-1,-1), (0,-1), (1,-1)) - self.g(x, y, (-1,1), (0,1), (1,1))

        res = math.sqrt(gx*gx + gy*gy)
        self.energyComputed[(x,y)] = res
        return res
    
    def g(self, x, y, c1, c2, c3):
        return self.g2(x, y, c1) + self.g2(x, y, c2) * 2 + self.g2(x, y, c3)

    def g2(self, x, y, c):
        x2,y2 = x +c[0],y +c[1]

        res = self.intensityComputed.get((x2,y2),-1)
        if res < 0 :
            res = intensity(self.image.get(x2, y2))
            self.intensityComputed[(x2, y2)] = res
        return res
    
    def removeVerticalSeam(self, path):
        for (x,y) in path:
            for x2 in range(x,self.image.w-2):
                self.energyComputed[(x,y)] = self.energy(x+1,y)
            self.energyComputed[(x-1,y)] = self.energy(x-1,y)


def intensity(pixelColors):
    return int(pixelColors[0]) + int(pixelColors[1]) + int(pixelColors[2])
