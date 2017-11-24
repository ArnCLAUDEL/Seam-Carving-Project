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
    def stupid_seam_finder(self, b=True):

        #path_energy: minimal path
        pe = {"seam_energy":math.inf, "path":[]}

        #functions calls in local variables for better efficiency
        energy = self.energy

        #width and height in local variables for better efficiency
        w,h = self.image.w, self.image.h

        if b:
            pe = self.computeHorizontal(pe, energy, w, h)
        else:
            pe = self.computeVertical(pe, energy, w, h)

        print(self.end - self.start)
        print(len(self.energyComputed), self.count)
        return pe

    def computeVertical(self, pe, energy, w, h):
        for i in range(0, w -2):
            x = i
            #current energy and path
            seam_energy, path = 0, []
            append = path.append

            for j in range(1, h-1):
                y = j
                e1, e2, e3 = energy(x -1, y), energy(x,y), energy(x +1, y)
                e = min(e1, e2, e3)
                x = x +1 if e == e3 else x if e == e2 else x -1
                seam_energy += e
                append((x,y))
                x = 1 if x <= 0 else (w - 3 if x >= w - 3 else x)

            if pe["seam_energy"] > seam_energy:
                pe = {"seam_energy":seam_energy,"path":path}
        return pe

    def computeHorizontal(self, pe, energy, w, h):
        for i in range(0, h -2):
            y = i
            #current energy and path
            seam_energy, path = 0, []
            append = path.append

            for j in range(1, w-1):
                x = j
                e1, e2, e3 = energy(x, y-1), energy(x,y), energy(x, y+1)
                e = min(e1, e2, e3)
                y = y +1 if e == e3 else y if e == e2 else y -1
                seam_energy += e
                append((x,y))
                y = 1 if y <= 0 else (self.image.h - 3 if y >= self.image.h - 3 else y)

            if pe["seam_energy"] > seam_energy:
                pe = {"seam_energy":seam_energy,"path":path}
        return pe

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

    def removeVerticalSeam(self, path, c=(1,0)):
        energy = self.energy
        iX,iY = c[0], c[1]
        for (x,y) in path:
            for x2 in range(x,self.image.w-2):
                self.energyComputed[(x,y)] = energy(x+iX,y+iY)


def intensity(pixelColors):
    return int(pixelColors[0]) + int(pixelColors[1]) + int(pixelColors[2])
