import time
import cv2
import numpy
import PIL.Image as pimg
import PIL.ImageTk as pimgtk

class Image:

    def __init__(self, path):

        # Image path
        self.path = path

        # Grid which contains the image
        # [height][width][[Blue] [Green] [Red]]
        self.grid = cv2.imread(self.path)

        # Width
        self.w = 0

        # Height
        self.h = 0

        self.update_size()

    # Re-compute the width and height of the image using the grid
    def update_size(self):
        self.w = len(self.grid[0])
        self.h = len(self.grid)

    # Return the BGR values of the pixel (x,y) as a list
    def get(self, x, y):
        return self.grid[y][x]

    # Return the image as a PhotoImage
    # This converts first the image from BGR to RGB
    def getAsITK(self):
        newImage = cv2.cvtColor(self.grid, cv2.COLOR_BGR2RGB)
        newImage = pimg.fromarray(newImage)
        return pimgtk.PhotoImage(newImage)

    # Remove each pixel from the given path in the grid
    def remove_vertical_seam(self, path):
        ndarrays = []
        ndarrays.append(numpy.delete(self.grid[path[0][1]], path[0][0], 0))
        for p in path:
            ndarrays.append(numpy.delete(self.grid[p[1]], p[0], 0))
        ndarrays.append(numpy.delete(self.grid[path[len(path)-1][1]], path[len(path)-1][0], 0))
        self.grid = numpy.array(ndarrays)
        self.update_size()

    # Set the intensity of the pixel (x,y) with the given BGR values
    def set_pixel_intensity(self, x, y, bgr_list):
        try :
            self.grid[y][x] = bgr_list
        except IndexError:
            return False