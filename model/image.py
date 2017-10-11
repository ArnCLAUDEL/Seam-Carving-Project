import cv2

class Image:

    def __init__(self, path):
        self.path = path
        self.__initialize()

    def __initialize(self):
        self.grid = cv2.imread(self.path)
