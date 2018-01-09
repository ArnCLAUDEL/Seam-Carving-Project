import model.energyCalculator as ec
from model.seamCarvingUtil import *
from itertools import chain
import math
class SeamFinder:

    def __init__(self, image):
        self.image = image
        self.energyCalculator = ec.EnergyCalculator(image)
        self.grid = [[(math.inf, (-1, -1)) for y in range(self.image.h)] for x in range(self.image.w)]
        self.previous_avg_x = 0
        self.preprocess()

    def preprocess(self):
        # energies in a local variable for better efficiency
        energy_computed = self.energyCalculator.energyComputed
        grid = self.grid

        # Initialization of the first row
        for x in self.avg_x_range():
            grid[x][0] = (energy_computed[x][0], (-1,-1))

        #print(self.avg_x_range(), len(grid), len(grid[len(grid)-1]), grid[len(grid)-2][100])

        for y in range(1, self.image.h - 1):
            for x in self.avg_x_range():

                # Energy of the three upper pixels
                e1, e2, e3 = grid[x - 1][y - 1][0], grid[x][y - 1][0], grid[x + 1][y - 1][0]
                e = min(e1, e2, e3)

                # We retrieve the coordinates of the lowest energy
                (x2, y2) = (x, y - 1) if e == e2 else (x + 1, y - 1) if e == e3 else (x - 1, y - 1)
                grid[x][y] = (e + energy_computed[x][y], (x2, y2))


    def avg_x_range(self):
        if self.previous_avg_x == 0:
            return range(1, self.image.w-1)
        i = max(1,self.previous_avg_x-self.image.w//3)
        j = min(self.image.w-1,self.previous_avg_x+self.image.w//3)

        j = self.image.w-1
        k = max(j,self.image.w-1-self.image.w//10)
        return chain(range(i,j), range(k,self.image.w-1))

    """
        def f1(energy_computed, grid, y):
            def f2(x):
                e1, e2, e3 = grid[x - 1][y - 1][0], grid[x][y - 1][0], grid[x + 1][y - 1][0]
                e = min(e1, e2, e3)
                (x2, y2) = (x, y - 1) if e == e2 else (x + 1, y - 1) if e == e3 else (x - 1, y - 1)
                grid[x][y] = (e + energy_computed[x][y], (x2, y2))

            return f2

        for y in range(1, self.image.h - 1):
            list(map(f1(energy_computed, grid, y), range(1, self.image.w-1)))
    """

    def stupid_seam_finder(self, b=True):
        pe = {"seam_energy":math.inf, "path":[]}
        pe = self.find_vertical_seams(pe)
        return pe

    # Find a vertical seam in the image
    # pe : [path,energy]
    # w : width of the image
    # h : height of the image
    # Time consuming operation
    @timer
    def find_vertical_seams(self, pe):
        self.preprocess()
        return self.find_vertical_seam()


    @timer
    def find_vertical_seam(self):
        # width and height in local variables for better efficiency
        w, h = self.image.w, self.image.h

        grid = self.grid

        min = math.inf
        bottom = (-1,-1)
        for x in range(w):
            cur = self.grid[x][h-2][0]
            if cur < min:
                min = cur
                bottom = (x,h-1)
        #print(bottom)
        path = list()
        #path.append(bottom)
        energy = grid[bottom[0]][bottom[1]][0]
        cur = (bottom[0],bottom[1]-1)
        avg_x = 0
        for i in range(h-2,0,-1):
            x, y = cur[0], cur[1]
            avg_x += x
            path.append((x,y))
            cur = self.grid[x][y][1]

        self.previous_avg_x = avg_x//h
        #path.append()
        path.reverse()
        print(len(path), path[0], path[len(path)-1])
        print(len(self.grid), len(self.grid[0]), self.image.w, self.image.h)

        return {"seam_energy": energy, "path": path}

    @timer
    def remove_vertical_seam(self, path):
        if self.previous_avg_x > self.image.w // 2:
            k = 1
            i = self.image.w - 1
        else:
            k = -1
            i = 0
        for (x,y) in path:
            for i in range(max(0,x),min(x,self.image.w)):
                self.grid[i+k][y] = self.grid[i+k][y]
        self.grid.pop(i)
        self.energyCalculator.remove_vertical_seam(path)