import model.image as img
import model.energyComputer as ec

class Core:

    def __init__(self):
        self.image = None

    def setImage(self, path):
        self.image = img.Image(path)


 
    def checkImage(f):
        def check(self, *args, **kwargs):
            if(self.image is None):
                print("No image available")
            else:
                f(self, *args, **kwargs)
        return check

    
    @checkImage
    def energyOf(self, x, y):    
        e = ec.EnergyComputer(self.image.grid)
        e.energy((1300,1300))
