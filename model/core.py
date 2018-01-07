import model.image as img
import model.energyCalculator as ec
import model.seamFinder as sf

class Core:

    def __init__(self):
        self.image = None
        self.seamFinder = None

    def setImage(self, path):
        self.image = img.Image(path)
        #self.energyCalculator = ec.EnergyCalculator(self.image)
        self.seamFinder = sf.SeamFinder(self.image)

    def checkImage(f):
        def check(self, *args, **kwargs):
            if(self.image is None):
                print("No image available")
                return False
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
        return self.seamFinder.stupid_seam_finder(b)

    @checkImage
    def removeVerticalSeam(self, path):
        self.image.removeVerticalSeam(path)
        self.seamFinder.removeVerticalSeam(path)

    @checkImage
    def removeHorizontalSeam(self, path):
        self.image.removeHorizontalSeam(path)
        self.seamFinder.removeHorizontalSeam(path)