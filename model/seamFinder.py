import model.energyCalculator as ec
from model.seamCarvingUtil import *
import math
import time
class SeamFinder:

    def __init__(self, image):
        self.image = image
        self.energyCalculator = ec.EnergyCalculator(image)
        self.grid = [[(math.inf, (-1, -1)) for y in range(self.image.h)] for x in range(self.image.w)]

    def stupid_seam_finder(self, b=True):

        # path_energy: minimal path
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
        # energies in a local variable for better efficiency
        energy_computed = self.energyCalculator.energyComputed
        grid = self.grid

        for x in range(self.image.w):
            grid[x][0] = (energy_computed[x][0], (-1,-1))

        for y in range(1, self.image.h - 1):
            for x in range(1, self.image.w - 1):
                e1, e2, e3 = grid[x - 1][y - 1][0], grid[x][y - 1][0], grid[x + 1][y - 1][0]
                e = min(e1, e2, e3)
                (x2, y2) = (x, y - 1) if e == e2 else (x + 1, y - 1) if e == e3 else (x - 1, y - 1)
                grid[x][y] = (e + energy_computed[x][y],(x2,y2))

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
        print(bottom)
        path = list()
        #path.append(bottom)
        energy = grid[bottom[0]][bottom[1]][0]
        cur = (bottom[0],bottom[1]-1)
        for i in range(h-2,0,-1):
            x, y = cur[0], cur[1]
            path.append((x,y))
            cur = grid[x][y][1]

        #path.append()
        path.reverse()
        print(len(path), path[0], path[len(path)-1])

        return {"seam_energy": energy, "path": path}

        # energies in a local variable for better efficiency
        energy_computed = self.energyCalculator.energyComputed

        seam_energy, path = 0, []
        append = path.append

        for y in range(1, h-1):
            e1, e2, e3 = energy_computed[x - 1][y + 1], energy_computed[x][y + 1], energy_computed[x + 1][y + 1]
            e = min(e1, e2, e3)
            x = x if e == e2 else x + 1 if e == e3 else x - 1
            seam_energy += e
            append((x,y))
            x = 1 if x <= 0 else (w - 3 if x >= w - 3 else x)
        if pe["seam_energy"] > seam_energy:
            pe = {"seam_energy": seam_energy, "path": path}
        return pe

    @timer
    def remove_vertical_seam(self, path):
        for (x,y) in path:
            for i in range(x,self.image.w):
                self.grid[i][y] = self.grid[i+1][y]
        self.grid.pop()
        self.energyCalculator.remove_vertical_seam(path)