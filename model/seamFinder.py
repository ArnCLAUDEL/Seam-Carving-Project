import model.energyCalculator as ec
import math

class SeamFinder:

    def __init__(self, image):
        self.image = image
        self.energyCalculator = ec.EnergyCalculator(image)

    def stupid_seam_finder(self, b=True):

        # path_energy: minimal path
        pe = {"seam_energy":math.inf, "path":[]}

        pe = self.find_vertical_seams(pe)

        return pe

    # Find a vertical seam in the image
    # pe : [path,energy]
    # w : width of the image
    # h : height of the image
    def find_vertical_seams(self, pe):
        for x in range(0, self.image.w -2):
            pe = self.find_vertical_seam(x, pe)
        return pe

    def find_vertical_seam(self, x, pe):
        # width and height in local variables for better efficiency
        w, h = self.image.w, self.image.h

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

    def remove_vertical_seam(self, path):
        self.energyCalculator.remove_vertical_seam(path)