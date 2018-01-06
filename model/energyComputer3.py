import numpy
import math
import time


class EnergyComputer:
    def __init__(self, image):
        self.image = image
        self.grid = {} #(x,y):[intensity,energy,seV,seH,pV,pH]
        self.__init_borders()
        #ec
        #ic

    def __init_borders(self):
        for i in range(0,self.image.w -1):
            self.__init_border(i, 0)
        for j in range(0, self.image.h -1):
            self.__init_border(0, j)

    def __init_border(self, x, y):
        self.grid[(x,y)] = {"coord":(x,y),"energy":math.inf,"seV":0,"seH":0,"pV":None,"pH":None}
        """
        self.grid[(x,y)]["coord"] = (x, y)
        if x == 0 or y == 0:
            self.grid[(x,y)]["energy"] = math.inf
            self.grid[(x,y)]["seV"] = 0
            self.grid[(x,y)]["seH"] = 0
            self.grid[(x,y)]["pV"] = None
            self.grid[(x,y)]["pH"] = None
        """

    def inbound(self, x, y):
        return (0 <= x < self.image.w
                and 0 <= y < self.image.h)

    def fitToGrid(self, x, y):
        x = max(1, x)
        x = min(self.image.w - 3, x)
        y = max(1, y)
        y = max(self.image.h - 3, y)
        return x, y

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
        for i in range(1, self.image.w -2):
            x = i
            for j in range(1, self.image.h -2):
                y = i
                self.compute(x,y)

        return self.minimalPath("V")

    def compute(self, x, y):
        e = self.energy(x, y)
        p1, p2, p3 = self.grid[(x -1, y -1)], self.grid[(x, y -1)], self.grid[(x +1, y -1)]
        min_p = self.min_pse(p1, p2, p3, "seV")
        self.grid[(x,y)]["seV"] = min_p["seV"] + e
        self.grid[(x,y)] = min_p["coord"]


    def minimalPath(self,key):
        key1 = "se"+key
        key2 = "p"+key
        pe = {key1:math.inf}
        for i in range(0,self.image.w-1):
            cur = self.grid[(i,self.image.h-1)]
            if(cur[key1] < pe[key1]):
                pe = cur
        path = []
        cur = pe
        for i in range(0, self.image.h-1):
            path.append(cur["coord"])
            cur = self.grid[cur[key2]]
        return path



    def min_pse(self,p1,p2,p3,key):
        pse1, pse2, pse3 = p1[key], p2[key], p3[key]
        if (pse1 < pse2):
            if (pse1 < pse3):
                p = p1
            else:
                p = p3
        elif (pse2 < pse3):
            p = p2
        else:
            p = p3
        return p

    def energy(self, x, y):
        if x == 0 or y == 0:
            return math.inf
        try:
            print(self.grid[(x,y)])
            res = self.grid[(x,y)]["energy"]
            return res
        except KeyError:
            gx = self.g(x, y, (-1, -1), (-1, 0), (-1, 1))
            gx -= self.g(x, y, (1, -1), (1, 0), (1, 1))
            gy = self.g(x, y, (-1, -1), (0, -1), (1, -1))
            gy -= self.g(x, y, (-1, 1), (0, 1), (1, 1))

            res = gx*gx + gy*gy
            self.grid[(x,y)]["energy"] = res
            return res

    def g(self, x, y, c1, c2, c3):
        return self.g2(x, y, c1) + self.g2(x, y, c2) * 2 + self.g2(x, y, c3)

    def g2(self, x, y, c):
        x2 = x+c[0]
        y2 = y+c[1]
        try:
            self.grid[(x,y)]["coord"] = (x,y)
            return self.grid[(x,y)]["intensity"]
        except KeyError:
            res = intensity(self.image.get(x2,y2))
            self.grid[(x,y)] = {}
            self.grid[(x,y)]["intensity"] = res
            return res

    def removeVerticalSeam(self, path):
        pass


def intensity(pixelColors):
    return int(pixelColors[0]) + int(pixelColors[1]) + int(pixelColors[2])
