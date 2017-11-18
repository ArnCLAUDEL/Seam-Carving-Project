import numpy
import math
import time


class EnergyComputer:
    def __init__(self, image):
        self.image = image
        self.grid = {} # {intensity, energy, }
        self.energyComputed = {}
        self.intensityComputed = {}

    def inbound(self, x, y):
        return (x >= 0 and x < self.image.w
                and y >= 0 and y < self.image.h)

    def fitToGrid(self, x, y):
        x = max(1, x)
        x = min(self.image.w - 3, x)
        y = max(1, y)
        y = max(self.image.h - 3, y)
        return (x, y)

    def timer(f):
        def f_timer(self, *args, **kwargs):
            start = time.time()
            res = f(self, *args, **kwargs)
            end = time.time()
            print("Computation time:", end - start)
            return res

        return f_timer

    @timer
    def stupid_seam_finder(self):
        pe = {"seam_energy": math.inf, "path": []}
        for i in range(1, self.image.w - 2):
            x = i - 1
            seam_energy = 0
            path = []
            for j in range(1, self.image.h - 1):
                y = j
                e1 = self.energy(x - 1, y)
                e2 = self.energy(x, y)
                e3 = self.energy(x + 1, y)
                d = {e1: (x - 1, y), e2: (x, y), e3: (x + 1, y)}
                e = min(e1, e2, e3)
                seam_energy += e
                """
                conserver la seam_energy pour chaque pixel dans pe[]

                if(pe["path"][j] == d[e]):
                    for p in range(j, len(pe["path"])):
                        path.append(p)
                        seam_energy = ?
                else:
                """
                path.append(d[e])
                x = d[e][0]
                x = self.fitToGrid(x, y)[0]
            if (pe["seam_energy"] > seam_energy):
                pe["seam_energy"] = seam_energy
                pe["path"] = path
        # print(pe)
        return pe

    def energy(self, x, y):
        if (x == 0 or y == 0):
            return math.inf
        try:
            res = self.energyComputed[(x, y)]
            return res
        except KeyError:
            pass

        # gx = self.g2(x, y, (-1,-1)) + self.g2(x, y, (-1,0)) * 2 + self.g2(x, y, (-1, 1))
        # gx -= self.g2(x, y, (1,-1)) + self.g2(x, y, (1,0)) * 2 + self.g2(x, y, (1, 1))

        # gy = self.g2(x, y, (-1,-1)) + self.g2(x, y, (0,-1)) * 2 + self.g2(x, y, (1, -1))
        # gy -= self.g2(x, y, (-1,1)) + self.g2(x, y, (0,1)) * 2 + self.g2(x, y, (1, 1))


        gx = self.g(x, y, (-1, -1), (-1, 0), (-1, 1))
        gx -= self.g(x, y, (1, -1), (1, 0), (1, 1))

        gy = self.g(x, y, (-1, -1), (0, -1), (1, -1))
        gy -= self.g(x, y, (-1, 1), (0, 1), (1, 1))

        res = math.sqrt(gx * gx + gy * gy)
        # res = gx*gx + gy*gy
        self.energyComputed[(x, y)] = res
        return res

    def g(self, x, y, c1, c2, c3):
        return self.g2(x, y, c1) + self.g2(x, y, c2) * 2 + self.g2(x, y, c3)

    def g2(self, x, y, c):
        x2 = x + c[0]
        y2 = y + c[1]
        try:
            return self.intensityComputed[(x2, y2)]
        except KeyError:
            res = intensity(self.image.get(x2, y2))
            self.intensityComputed[(x2, y2)] = res
            return res

    def removeVerticalSeam(self, path):
        for (x, y) in path:
            for x2 in range(x, self.image.w - 2):
                self.energyComputed[(x, y)] = self.energy(x + 1, y)
            self.energyComputed[(x - 1, y)] = self.energy(x - 1, y)


def intensity(pixelColors):
    return int(pixelColors[0]) + int(pixelColors[1]) + int(pixelColors[2])
