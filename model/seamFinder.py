import model.energyCalculator as ec
import math

class SeamFinder:


    def __init__(self, image):
        self.image = image
        self.energyCalculator = ec.EnergyCalculator(image)


    def stupid_seam_finder(self, b=True):

        # path_energy: minimal path
        pe = {"seam_energy":math.inf, "path":[]}

        # width and height in local variables for better efficiency
        w,h = self.image.w, self.image.h

        if b:
            pe = self.computeHorizontal(pe, w, h)
        else:
            pe = self.computeVertical(pe, w, h)

        return pe

    # Find a vertical seam in the image
    # pe : [path,energy]
    # w : width of the image
    # h : height of the image
    def computeVertical(self, pe, w, h):
        energyComputed = self.energyCalculator.energyComputed
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
        for i in range(0, h - 2):
            y = i
            # current energy and path
            seam_energy, path = 0, []
            append = path.append

            for j in range(1, w - 1):
                x = j
                e1, e2, e3 = energy(x, y - 1), energy(x, y), energy(x, y + 1)
                e = min(e1, e2, e3)
                y = y + 1 if e == e3 else y if e == e2 else y - 1
                seam_energy += e
                append((x, y))
                y = 1 if y <= 0 else (self.image.h - 3 if y >= self.image.h - 3 else y)

            if pe["seam_energy"] > seam_energy:
                pe = {"seam_energy": seam_energy, "path": path}
        return pe

    def removeVerticalSeam(self, path):
        self.energyCalculator.removeVerticalSeam(path)