import model.image as img
import model.energyComputer5 as ec

class Core:

    def __init__(self):
        self.image = None

    def setImage(self, path):
        self.image = img.Image(path)
        self.energyComputer = ec.EnergyComputer(self.image)

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
    def energyOf(self, x, y):    
        return self.energyComputer.energy(x,y)

    @checkImage
    def stupid_seam_finder(self):
        return self.energyComputer.stupid_seam_finder()

    @checkImage
    def removeVerticalSeam(self, path):
        self.image.removeVerticalSeam(path)
        self.energyComputer.removeVerticalSeam(path)