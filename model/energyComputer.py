import numpy
import math
import time

class EnergyComputer:
    
    def __init__(self, grid):
        self.grid = grid
        self.w = len(grid)
        self.h = len(grid[0])
        self.energyComputed = {}
        self.intensityComputed = {}

    def inbound(self, x, y):
        return ( x >= 0 and x < len(self.grid)
                 and y >= 0 and y < len(self.grid[0]))

    def fitToGrid(self, x, y):
        x = max(1, x)
        x = min(self.w-3, x)
        y = max(1,y)
        y = max(self.h-3, y)
        return (x,y)

    def neighborhood(self, c, l1=[-1,0,1], l2=[-1,0,1]):
        for x in l1:
           for y in l2:
               if(y != 0 and x != 0):
                   yield (c[0]+x, c[1]+y)

    def timer(f):
        def f_timer(self, *args, **kwargs):
            start = time.time()
            res = f(self, *args, **kwargs)
            end = time.time()
            print("Computation time:", end-start)
            return res
        return f_timer

    @timer
    def stupid_seam_finder(self):
        pe = {"seam_energy":math.inf, "path":[]}
        for i in range(1, self.w-2):
            x = i-1
            seam_energy = 0
            path = []
            for j in range(1, self.h-2):
                y = j
                e1 = self.energy(x-1, y)
                e2 = self.energy(x, y)
                e3 = self.energy(x+1, y)
                d = {e1: (x-1,y), e2: (x,y), e3: (x+1,y)}
                e = min(e1,e2,e3)
                seam_energy += e
                path.append(d[e])
                x = d[e][0]
                x = self.fitToGrid(x,y)[0]
            if(pe["seam_energy"] > seam_energy):
                pe["seam_energy"] = seam_energy
                pe["path"] = path
        #print(pe)
        return pe
    
    def energy(self, x, y):
        try:
            res = self.energyComputed[(x,y)]
            return res
        except KeyError:
            pass
        gx = self.g(x, y, (-1,-1), (-1,0), (-1,1))
        gx -= self.g(x, y, (1,-1), (1,0), (1,1))

        gy = self.g(x, y, (-1,-1), (0,-1), (1,-1))
        gy -= self.g(x, y, (-1,1), (0,1), (1,1))

        res = math.sqrt(gx*gx + gy*gy)
        self.energyComputed[(x,y)] = res
        return res
    
    def g(self, x, y, c1, c2, c3):
        return self.g2(x, y, c1) + self.g2(x, y, c2) * 2 + self.g2(x, y, c3)

    def g2(self, x, y, c):
        x2 = x +c[0]
        y2 = y +c[1]
        try:
            return self.intensityComputed[(x2,y2)]
        except KeyError:
            res = intensity(self.grid[x2][y2])
            self.intensityComputed[(x2,y2)] = res
            return res
                
def intensity(pixelColors):
    return int(pixelColors[0]) + int(pixelColors[1]) + int(pixelColors[2])
