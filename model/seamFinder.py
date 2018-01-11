import math
from itertools import chain

import model.energyCalculator as ec
from model.seamCarvingUtil import timer

from model.algoType import AlgoType

class SeamFinder:

    def __init__(self, image):
        self.image = image

        # Object that will provide the energies.
        self.energyCalculator = ec.EnergyCalculator(image)

        # Grid that will contain, for each pixel, a tuple (seam_energy, (x2,y2)).
        # seam_energy : The energy of the lowest-cost seam that ends to this pixel.
        # (x2,y2) : The upper pixel that belongs to the lowest-cost seam.
        # The grid has the following shape : (width,height).
        self.grid = [[(math.inf, (-1, -1)) for y in range(self.image.h)] for x in range(self.image.w)]

        # Variable used to reduce the amount of computation
        # This variable is updated, each time a new minimal seam is computed.
        # It represents the average of the x-part of each pixel coordinate (x,y) that belongs to the seam.
        # @see SeamFinder.compute_paths documentation for more details.
        self.previous_avg_x = 0

        # The algorithm used.
        self.algo_type = AlgoType.SEAM_ENERGY

        # The accuracy of the algorithm.
        # The accuracy should be a value between ]0,1].
        # 1 beeing the highest accuracy.
        self.accuracy = 0.5

    # The given pixel will be avoided in computation as much as possible
    def avoid_pixel(self,x,y):
        self.energyCalculator.avoid_pixel(x,y)

    # Compute, for each pixel, the next pixel to follow to build the lowest-cost vertical seam.
    # This algorithm uses dynamic programming to compute it in a reasonable delay.
    # Pixels in the first row are initialized just with their energies and dummy coordinates.
    #  Starting from the second line, each pixel will look at his 3 upper pixels (top-right, top, top-left).
    # - and will choose the one with the lowest-cost. @see SeamFinder.__get_algo_function for more details.
    # For easiness reasons, we do not compute any pixel in the most-left/right columns.
    # This algorithm is greedy and uses a variable range for his computations, depending on the accuracy.
    # @see SeamFinder.__avg_x_range for nore details.
    # Time consuming operation.
    @timer
    def compute_paths(self):

        # energies in a local variable for better efficiency
        energy_computed = self.energyCalculator.energyComputed
        grid = self.grid

        # Initialization
        self.__init_borders()

        # Determine which function to use to select the lowest-cost pixel
        algo_function = self.__get_algo_function()

        for y in range(1, self.image.h - 1):
            for x in self.avg_x_range():
                # Energy of the three upper pixels
                e1, e2, e3 = algo_function(x,y)
                e = min(e1, e2, e3)

                # We retrieve the coordinates of the lowest energy
                (x2, y2) = (x, y - 1) if e == e2 else (x + 1, y - 1) if e == e3 else (x - 1, y - 1)

                # Data update
                grid[x][y] = (e + energy_computed[x][y], (x2, y2))

    # Return a function used to select the lowest-cost pixel.
    # The function depends on the current algo_type.
    # SEAM_ENERGY : select the pixel with the lowest seam energy.
    # LOCAL_ENERGY : select the pixel with the lowest energy, without looking at the energy of the current seam.
    def __get_algo_function(self):
        energy_computed = self.energyCalculator.energyComputed
        if self.algo_type == AlgoType.SEAM_ENERGY:
            return lambda i, j: (self.grid[i - 1][j - 1][0], self.grid[i][j - 1][0], self.grid[i + 1][j - 1][0])
        else:
            return lambda i, j: (energy_computed[i - 1][j - 1], energy_computed[i][j - 1], energy_computed[i + 1][j - 1])

    # Initialize borders with default values.
    # Each pixel from the first row will take their own energy.
    # Pixel on the last row and the most-right/left column will have a infinite energy.
    def __init_borders(self):
        energy_computed = self.energyCalculator.energyComputed
        grid = self.grid

        for x in range(self.image.w):
            grid[x][0] = (energy_computed[x][0], (-1,-1))
            grid[x][self.image.h-1] = (math.inf, (-1, -1))

        for y in range(self.image.h):
            grid[0][y] = (math.inf, (-1, -1))
            grid[self.image.w-1][y] = (math.inf, (-1, -1))

    # Return a greedy Range object used in path computation.
    # The Range returned depends on the previous computed seam and the accuracy.
    # @see SeamFinder.previous_avg_x for more details.
    # If the x-average is 0 - it usually means that it's the first computation
    # - then we returned a classic range(1,width).
    # Else, we make an area around the x-coordinate that represents the pixels which are the most-likely
    # - to change one, or more, seam. The maximum width of this area is image.width * accuracy.
    # In addition, we re-compute some columns on the right to make sure that they won't lead us to a non-existent pixel.
    def avg_x_range(self):

        # Return a normal range if True
        if self.previous_avg_x == 0:
            return range(1, self.image.w-1)

        accuracy_offset = int(self.image.w*self.accuracy//2)

        # Left limit
        i = max(1, self.previous_avg_x - accuracy_offset)

        # Right limit
        j = min(self.image.w - 1, self.previous_avg_x + accuracy_offset)

        # Right-most columns, always
        k = max(j, self.image.w - 2 - accuracy_offset)

        return chain(range(i,j), range(k,self.image.w-1))

    # Find and return a low-energy seam.
    # Return a dictionary {"seam_energy", "path"}.
    # seam_energy : The energy of the seam found.
    # path : a list of (x,y) coordinates.
    # Time consuming operation
    def seam_finder(self):
        self.compute_paths()
        return self.find_vertical_seam()

    # Find and return a low-energy seam.
    # It loops over the pixels in the most-bottom row and takes the pixel with the lowest seam energy.
    # Then it climbs the grid and add each pixel to a list. After computation, the list is reversed.
    # This will also update the average x-coordinate. @see SeamFinder.previous_avg_x for more details.
    # Return a dictionary {"seam_energy", "path"}.
    # seam_energy : The energy of the seam found.
    # path : a list of (x,y) coordinates, from top to bottom.
    @timer
    def find_vertical_seam(self):

        # width and height in local variables for better efficiency
        w, h = self.image.w, self.image.h

        # Lowest energy currently found
        energy_min = math.inf

        # Bottom pixel of the seam, initialized with dummy coordinates
        bottom = (-1,-1)

        for x in range(w):
            cur = self.grid[x][h-2][0]
            if cur < energy_min:
                energy_min = cur
                bottom = (x, h - 1)

        # Path that contains each pixel from bottom to top
        path = list()

        # Current pixel, initialized with the pixel just above the bottom pixel of the seam
        cur = (bottom[0], bottom[1] - 1)

        # Average x-coordinate of all pixel in the path, @see SeamFinder.previous_avg_x for more details
        avg_x = 0

        for i in range(h - 2, 0, -1):
            x, y = cur[0], cur[1]
            avg_x += x
            path.append((x,y))
            cur = self.grid[x][y][1]

        # @see SeamFinder.previous_avg_x for more details
        self.previous_avg_x = avg_x // h

        # Change the bottom - top direction to a top - bottom one
        path.reverse()

        return {"seam_energy": energy_min, "path": path}

    # Remove every pixel from the path in the grid.
    # Since the grid is shaped like [column][row], it shifts pixels instead of just popping pixels for each row.
    # If the seam is closer to the right-side of the image, then pixels on the right-side of the seam
    #   - are shifted to the left.
    # Else, pixels on the left-side of the seam are shifted to the right.
    # This is computed with the average x-coordinate. @see SeamFinder.previous_avg_x for more details.
    # This technique, in most cases, should not shift more than half of the pixels.
    @timer
    def remove_vertical_seam(self, path):

        # Determine if the average x-coordinate is closer to the right or left side
        right_side = self.previous_avg_x > self.image.w // 2

        if right_side:
            k1, k2, col_to_rm = 0, 1, -1
            r = lambda x: range(x, self.image.w, 1)
        else:
            k1, k2, col_to_rm = 0, -1, 0
            r = lambda x: range(x, 0, -1)

        for (x, y) in path:
            for i in r(x):
                self.grid[i + k1][y] = self.grid[i + k2][y]

        # Pop the first or the last column
        self.grid.pop(col_to_rm)

        # @see EnergyCalculator.remove_vertical_seam for more details
        self.energyCalculator.remove_vertical_seam(path)
