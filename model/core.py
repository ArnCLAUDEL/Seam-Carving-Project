import model.image as img
import model.seamFinder as sf

class Core:

    def __init__(self):
        self.image = None

        # Object that will process the image
        self.seamFinder = None

    # Set the current image with the given path.
    def set_image(self, path):
        self.image = img.Image(path)
        self.seamFinder = sf.SeamFinder(self.image)

    # Decorator used to prevent any action while an image is not successfully loaded.
    def check_image(f):
        def check(self, *args, **kwargs):
            if(self.image is None):
                return False
            else:
                return f(self, *args, **kwargs)
        return check

    # Delegated method
    # @see Image.getAsITK for more details.
    @check_image
    def get_image(self):
        return self.image.getAsITK()

    # Return the width of the image.
    @check_image
    def w(self):
        return self.image.w

    # Return the height of the image.
    @check_image
    def h(self):
        return self.image.h

    @check_image
    def get_accuracy(self):
        return self.seamFinder.accuracy

    @check_image
    def set_accuracy(self, accuracy):
        self.seamFinder.accuracy = accuracy

    @check_image
    def get_algo_type(self):
        return self.seamFinder.algo_type

    @check_image
    def set_algo_type(self, algo_type):
        self.seamFinder.algo_type = algo_type

    # Delegated method
    # @see SeamFinder.seam_finder for more details.
    @check_image
    def seam_finder(self):
        return self.seamFinder.seam_finder()

    # Remove each pixel contained in the given path.
    # This will remove first the seam in the real image
    # - then the seam finder will update his information.
    @check_image
    def remove_vertical_seam(self, path):
        self.image.remove_vertical_seam(path)
        self.seamFinder.remove_vertical_seam(path)

    @check_image
    def avoid_pixel(self, x, y):
        self.seamFinder.avoid_pixel(x,y)