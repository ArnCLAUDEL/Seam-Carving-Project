from cv2 import *

class Image:

    def __init__(self, path):
        self.path = path
        self.__initialize()

    def __initialize(self):
        self.grid = imread(self.path)
        print("File loaded")
