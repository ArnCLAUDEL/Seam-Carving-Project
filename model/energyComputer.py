import numpy
import math

class EnergyComputer:
    
    def __init__(self, grid):
        self.grid = grid
        self.energyComputed = {}
        self.intensityComputed = {}

    def inbound(self, x, y):
        return ( x > 0 and x < len(grid)-1
                 and y > 0 and y < len(grid[0])-1)


    def neighborhood(self, c, l1=[-1,0,1], l2=[-1,0,1]):
        for x in l1:
           for y in l2:
               if(y != 0 and x != 0):
                   yield (c[0]+x, c[1]+y)
    
    def energy(self, x, y):
        try:
            return self.energyComputed[(x,y)]
        except KeyError:
            pass
            
        gx = self.g(x, y, (-1,-1), (-1,0), (-1,1))
        gx -= self.g(x, y, (-1,-1), (0,-1), (1,-1))

        gy = self.g(x, y, (-1,-1), (0,-1), (1,-1))
        gy -= self.g(x, y, (-1,-1), (-1,0), (-1,1))

        res = math.sqrt(gx*gx + gy*gy)
        self.energyComputed[(x,y)] = res
        return res
    
    def g(self, x, y, c1, c2, c3):
        return self.g2(x, y, c1) + self.g2(x, y, c2) * 2 + self.g2(x, y, c3)

    def g2(self, x, y, c):
        try:
            return self.intensityComputed[(x,y)]
        except KeyError:
            res = intensity(self.grid[x +c[0]][y +c[1]])
            self.intensityComputed[(x,y)] = res
            return res
                
def intensity(pixelColors):
    return int(pixelColors[0]) + int(pixelColors[1]) + int(pixelColors[2])
