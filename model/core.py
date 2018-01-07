import model.image as img
import model.energyCalculator as ec

class Core:

    def __init__(self):
        self.image = None

    def setImage(self, path):
        self.image = img.Image(path)
        self.energyCalculator = ec.EnergyCalculator(self.image)

    def checkImage(f):
        def check(self, *args, **kwargs):
            if(self.image is None):
                print("No image available")
            else:
                return f(self, *args, **kwargs)
        return check

    def getImage(self):
        return self.image.getAsITK()

    @checkImage
    def w(self):
        return self.image.w

    @checkImage
    def h(self):
        return self.image.h

    @checkImage
    def stupid_seam_finder(self, b=True):
        return self.energyCalculator.stupid_seam_finder(b)

    @checkImage
    def removeVerticalSeam(self, path):
        self.image.removeVerticalSeam(path)
        self.energyCalculator.removeVerticalSeam(path)

    @checkImage
    def removeHorizontalSeam(self, path):
        self.image.removeHorizontalSeam(path)
        self.energyCalculator.removeHorizontalSeam(path)