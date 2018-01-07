import numpy
import math

def timer(f):
    def f_timer(self, *args, **kwargs):
        start = time.time()
        res = f(self, *args, **kwargs)
        end = time.time()
        print(f, "done in", round((end - start), 2), "s")
        return res
    return f_timer

class EnergyCalculator:

    # Coordinates used to compute the gradient
    GX_COORDS = [(-1, -1), (-1, 0), (-1, 1), (1, -1), (1, 0), (1, 1)]
    GY_COORDS = [(-1, -1), (0, -1), (1, -1), (-1, 1), (0, 1), (1, 1)]

    #High energy value
    HIGHT_ENERGY_VALUE = 2**10

    def __init__(self, image):
        self.image = image

        # Tab with the intensity of each pixel. Initial value : -1
        self.intensityComputed = [[-1 for y in range(self.image.h)] for x in range(self.image.w)]

        # Tab with the intensity of each pixel. Initial value : an arbitrary high energy value
        self.energyComputed = [[self.HIGHT_ENERGY_VALUE for y in range(self.image.h)] for x in range(self.image.w)]

        self.compute_energies()

    def stupid_seam_finder(self, b=True):

        # path_energy: minimal path
        pe = {"seam_energy":math.inf, "path":[]}

        # functions calls in local variables for better efficiency
        energy = self.energy

        # width and height in local variables for better efficiency
        w,h = self.image.w, self.image.h

        if b:
            pe = self.computeHorizontal(pe, energy, w, h)
        else:
            pe = self.computeVertical(pe, energy, w, h)
        return pe

    # Find a vertical seam in the image
    # pe : [path,energy]
    # energy : energy function
    # w : width of the image
    # h : height of the image
    def computeVertical(self, pe, energy, w, h):
        energyComputed = self.energyComputed
        for i in range(0, w -2):
            x = i
            #current energy and path
            seam_energy, path = 0, []
            append = path.append
            for j in range(1, h-1):
                y = j
                e1, e2, e3 = energyComputed[x - 1][y + 1], energyComputed[x][y + 1], energyComputed[x + 1][y + 1]
                e = min(e1, e2, e3)
                x = x +1 if e == e3 else x if e == e2 else x -1
                seam_energy += e
                append((x,y))
                x = 1 if x <= 0 else (w - 3 if x >= w - 3 else x)

            if pe["seam_energy"] > seam_energy:
                pe = {"seam_energy":seam_energy,"path":path}
        return pe

    # TODO
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

    # Compute the intensity given RGB values of a pixel
    def intensity(self, pixelColors):
        return int(pixelColors[0]) + int(pixelColors[1]) + int(pixelColors[2])

    # Compute the gradient of the pixel at (x,y)
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

    # Compute the energy of a pixel at (x,y)
    def energy(self, x, y):
        res = math.inf
        gx, gy = self.gradient(x, y, self.GX_COORDS), self.gradient(x, y, self.GY_COORDS)
        res = math.sqrt(gx * gx + gy * gy)
        return res

    # Compute the energy of each pixel in the image
    def compute_energies(self):
        #Function calls and variables in local variables for better efficiency
        energyComputed = self.energyComputed

        for y in range(1,self.image.h-1):
            for x in range(1,self.image.w-1):
                energyComputed[x][y] = self.energy(x,y)

    # Remove a vertical seam in the image.
    def removeVerticalSeam(self, path, c=(1,0)):
        iX,iY = c[0], c[1]
        for (x,y) in path:
            for x2 in range(x-2):
                self.energyComputed[x][y] = self.energyComputed[x+iX][y+iY]

    # TODO
    def removeHorizontalSeam(self, path, c=(0,1)):
        energy = self.energy
        iX,iY = c[0], c[1]
        for (x,y) in path:
            for x2 in range(x,self.image.h-2):
                self.energyComputed[(x,y)] = energy(x+iX,y+iY)


