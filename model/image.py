import time
import cv2
import numpy
import PIL.Image as pimg
import PIL.ImageTk as pimgtk

def timer(f):
    def f_timer(self, *args, **kwargs):
        start = time.time()
        res = f(self, *args, **kwargs)
        end = time.time()
        print(f, "done in", round((end - start), 2), "s")
        return res
    return f_timer

class Image:

    def __init__(self, path):
        self.path = path
        self.__initialize()

    def __initialize(self):
        self.grid = cv2.imread(self.path)
        self.updateCoordinates()

    def updateCoordinates(self):
        self.w = len(self.grid[0])
        self.h = len(self.grid)
        print("Shape:", self.grid.shape, "Coordinates:", self.w, ":", self.h)

    def get(self, x, y):
        return self.grid[y][x]
    
    def getAsITK(self):
        newImage = cv2.cvtColor(self.grid, cv2.COLOR_BGR2RGB)
        newImage = pimg.fromarray(newImage)
        return pimgtk.PhotoImage(newImage)


    def removeVerticalSeam(self, path):
        ndarrays = []
        ndarrays.append(numpy.delete(self.grid[path[0][1]], path[0][0], 0))
        for p in path:
            ndarrays.append(numpy.delete(self.grid[p[1]], p[0], 0))
        ndarrays.append(numpy.delete(self.grid[path[len(path)-1][1]], path[len(path)-1][0], 0))
        self.grid = numpy.array(ndarrays)
        self.updateCoordinates()

    def removeHorizontalSeam(self, path):
        gridTemp = list()
        for i in range(0, self.w):
            gridTemp.append([])
            for j in range(0, self.h-1):
                gridTemp[i].append(self.grid[j,i])

        gridTemp = numpy.array(gridTemp)
        ndarrays = list()

        ndarrays.append(numpy.delete(gridTemp[path[0][0]], path[0][1], 0))

        for p in path:
            try:
                ndarrays.append(numpy.delete(gridTemp[p[0]], p[1], 0))
            except IndexError:
                print(gridTemp.shape, p[1],p[0])
        ndarrays.append(numpy.delete(gridTemp[path[len(path) -1][0]], path[len(path) - 1][1], 0))
        ndarrays = numpy.array(ndarrays)

        #print(ndarrays.shape)

        gridTemp = list()
        for i in range(0, self.h-1):
            gridTemp.append([])
            for j in range(0, self.w):
                gridTemp[i].append(self.grid[i,j])


        self.grid = numpy.array(gridTemp)

        self.updateCoordinates()