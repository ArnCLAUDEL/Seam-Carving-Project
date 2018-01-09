import math
import asyncio
import numpy
from model.seamCarvingUtil import timer

class EnergyCalculator:

    # Coordinates used to compute the gradient
    GX_COORDS = [(-1, -1), (-1, 0), (-1, 1), (1, -1), (1, 0), (1, 1)]
    GY_COORDS = [(-1, -1), (0, -1), (1, -1), (-1, 1), (0, 1), (1, 1)]

    # High energy value
    HIGHT_ENERGY_VALUE = 2**10

    def __init__(self, image):
        self.image = image

        # Tab with the intensity of each pixel. Initial value : -1
        self.intensityComputed = [[-1 for y in range(self.image.h)] for x in range(self.image.w)]

        # Tab with the intensity of each pixel. Initial value : an arbitrary high energy value
        self.energyComputed = [[self.HIGHT_ENERGY_VALUE for y in range(self.image.h)] for x in range(self.image.w)]

        # loop = asyncio.get_event_loop()
        # loop.run_in_executor(None, self.pre_process)
        self.pre_process()

    # Pre-process the image.
    # Compute the enregy for each pixel.
    # Time consuming operation
    def pre_process(self):
        self.compute_energies()

    # Compute the intensity given BGR values of a pixel.
    @staticmethod
    def intensity(pixelColors):
        return int(pixelColors[0]) + int(pixelColors[1]) + int(pixelColors[2])

    # Compute the gradient of the pixel at (x,y).
    # c_lost : list of 6 coordinates (a,b) to get the pixel on top, right, left etc.
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

    # Compute the energy of a pixel at (x,y).
    def energy(self, x, y):
        gx, gy = self.gradient(x, y, self.GX_COORDS), self.gradient(x, y, self.GY_COORDS)
        res = math.sqrt(gx ** 2 + gy ** 2)
        return res

    # Compute the energy of each pixel in the image.
    @timer
    def compute_energies(self):

        # Function calls and variables in local variables for better efficiency
        energy_computed = self.energyComputed
        energy = self.energy

        for y in range(1,self.image.h-1):
            for x in range(1,self.image.w-1):
                energy_computed[x][y] = int(energy(x,y))

    # Remove a vertical seam in the image.
    # c : coordinates (a,b) used to easily adapt the direction.
    def remove_vertical_seam(self, path, c=(1,0)):

        # Function calls and variables in local variables for better efficiency
        energy_computed = self.energyComputed

        ix,iy = c[0], c[1]
        for (x,y) in path:
            for i in range(x,self.image.w):
                energy_computed[i][y] = energy_computed[i+ix][y+iy]
        energy_computed.pop()