import cv2
import numpy
import PIL.Image as pimg
import PIL.ImageTk as pimgtk

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
        print("Coordinates:", self.w, ":", self.h)


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