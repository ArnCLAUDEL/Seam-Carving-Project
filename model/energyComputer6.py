import numpy
import math
import time

def timer(f):
    def f_timer(self, *args, **kwargs):
        start = time.time()
        res = f(self, *args, **kwargs)
        end = time.time()
        print(f , "done in", round((end - start),2), "s")
        return res
    return f_timer

class EnergyComputer:

    # Utils

    # Inbound check
    #   0 <= x < self.image.w and 0 <= y < self.image.h

    #  Fit to grid
    #   x = 1 if x <= 0 else (self.image.w - 3 if x >= self.image.w - 3 else x)
    #   y = 1 if y <= 0 else (self.image.h - 3 if y >= self.image.h - 3 else y)

    def __init__(self, image):
        self.image = image

        self.intensityComputed = [[-1 for y in range(self.image.h)] for x in range(self.image.w)]
        self.energyComputed = [[math.inf for y in range(self.image.h)] for x in range(self.image.w)]
        self.verticalPathGrid = [[(0,0) for y in range(self.image.h)] for x in range(self.image.w)]

        #Coordinates used to compute gradient
        self.__gx_coords = [(-1,-1), (-1,0), (-1,1), (1,-1), (1,0), (1,1)]
        self.__gy_coords = [(-1,-1), (0,-1), (1,-1), (-1,1), (0,1), (1,1)]

        self.compute_energies()

    @timer
    def stupid_seam_finder(self, b=True):
        pe = self.findVerticalPath()
        return pe
        path = pe["path"]
        print(len(path))

        for p in path:
            print(p)

    def findVerticalPath(self):
        self.compute_path()
        pe = {"energy": math.inf, "path": []}

        for x in range(1,self.image.w):
            p = self.verticalPathGrid[x][1]
            path = [(x,1)]
            energy = 0
            for y in range(1,self.image.h-2):
                energy = energy + self.energyComputed[p[0]][p[1]]
                path.append(p)
                p = self.verticalPathGrid[p[0]][p[1]]
            if energy < pe["energy"]:
                pe["energy"] = energy
                pe["path"] = path
        return pe

    @timer
    def removeVerticalSeam(self, path, c=(1,0)):
        energy = self.energy
        iX,iY = c[0], c[1]
        for (x,y) in path:
            for i in range(x,self.image.w-2):
                self.energyComputed[x][y] = energy(x+iX,y+iY)
        #self.compute_path()

    def compute_path(self):
        #Function calls and variables in local variables for better efficiency
        energyComputed = self.energyComputed
        pathGrid = self.verticalPathGrid

        for y in range(1,self.image.h-1):
            for x in range(1,self.image.w-1):
                e1, e2, e3 = energyComputed[x - 1][y + 1], energyComputed[x][y + 1], energyComputed[x + 1][y + 1]
                e = min(e1, e2, e3)
                (x2, y2) = (x + 1, y + 1) if e == e3 else (x, y + 1) if e == e2 else (x - 1, y + 1)
                pathGrid[x][y] = (x2,y2)



    def intensity(self, pixelColors):
        return int(pixelColors[0]) + int(pixelColors[1]) + int(pixelColors[2])

    def gradient(self, x, y, c_list):
        v = []
        for c in c_list:
            x2, y2 = x + c[0], y + c[1]
            res = self.intensityComputed[x2][y2]
            if res < 0:
                res = self.intensity(self.image.get(x2, y2))
                self.intensityComputed[x2][y2] = res
            v.append(res)

        return v[0] + v[1] * 2 + v[2] - v[3] - v[4] * 2 - v[5]

