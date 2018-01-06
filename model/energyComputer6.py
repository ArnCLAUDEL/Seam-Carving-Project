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


        #Timer init value
        self.start, self.end = 0,0

        #Coordinates used to compute gradient
        self.__gx_coords = [(-1,-1), (-1,0), (-1,1), (1,-1), (1,0), (1,1)]
        self.__gy_coords = [(-1,-1), (0,-1), (1,-1), (-1,1), (0,1), (1,1)]

    @timer
    def stupid_seam_finder(self, b=True):
        self.compute_energies()

    def findVertical(self):
        #Function calls and variables in local variables for better efficiency
        energyComputed = self.energyComputed

        pathTab = []
        for y in range(1,self.h-1):
            line = []
            for x in range(1,self.w-1):
                e1, e2, e3 = energyComputed[x - 1][y + 1], energyComputed[x][y + 1], energyComputed[x + 1][y + 1]
                e = min(e1, e2, e3)


    def compute_energies(self):
        #Function calls and variables in local variables for better efficiency
        gradient,sqrt,inf = self.gradient,math.sqrt,math.inf
        gx_coords,gy_coords = self.__gx_coords,self.__gy_coords
        energyComputed = self.energyComputed

        for y in range(1,self.image.h-1):
            for x in range(1,self.image.w-1):
                res = inf
                gx, gy = gradient(x, y, gx_coords), gradient(x, y, gy_coords)
                res = sqrt(gx * gx + gy * gy)
                energyComputed[x][y] = res

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

