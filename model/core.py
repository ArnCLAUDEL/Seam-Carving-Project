import model.image as img
import model.seamFinder as sf

class Core:

    def __init__(self):
        # Current image to process
        self.image = None

        # Object that will process the image
        self.seamFinder = None

    # Set the current image with the given path
    def set_image(self, path):
        self.image = img.Image(path)
        self.seamFinder = sf.SeamFinder(self.image)

    # Decorator used to prevent any action while an image is not successfully loaded
    def check_image(f):
        def check(self, *args, **kwargs):
            if(self.image is None):
                return False
            else:
                return f(self, *args, **kwargs)
        return check

    # Delegated method
    # Return the image in a specific format
    @check_image
    def get_image(self):
        return self.image.getAsITK()

    # Return the width of the image
    @check_image
    def w(self):
        return self.image.w

    # Return the height of the image
    @check_image
    def h(self):
        return self.image.h

    # Delegated method
    # Call the stupid seam finder
    @check_image
    def stupid_seam_finder(self, b=True):
        return self.seamFinder.stupid_seam_finder(b)

    # Remove each pixel contained in the given path
    # This will remove first the seam in the real image
    # Then the seam finder will update his information
    @check_image
    def remove_vertical_seam(self, path):
        self.image.remove_vertical_seam(path)
        self.seamFinder.remove_vertical_seam(path)