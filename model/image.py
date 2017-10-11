import cv2
import PIL.Image as pimg
import PIL.ImageTk as pimgtk

class Image:

    def __init__(self, path):
        self.path = path
        self.__initialize()

    def __initialize(self):
        self.grid = cv2.imread(self.path)

    
    def getAsITK(self):
        newImage = cv2.cvtColor(self.grid, cv2.COLOR_BGR2RGB)
        newImage = pimg.fromarray(newImage)
        return pimgtk.PhotoImage(newImage)
