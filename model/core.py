import model.image as img
import model.energyComputer as ec

class Core:

    def __init__(self):
        self.image = None
        self.ec = None

    def setImage(self, path):
        self.image = img.Image(path)
        self.energyComputer = ec.EnergyComputer(self.image.grid)


    def checkImage(f):
        def check(self, *args, **kwargs):
            if(self.image is None):
                print("No image available")
            else:
                return f(self, *args, **kwargs)
        return check

    
    @checkImage
    def energyOf(self, x, y):    
        return self.energyComputer.energy(x,y)
