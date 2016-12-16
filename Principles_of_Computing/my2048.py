"""
Fundamentals of Computing Part 1
Week 1 - June 2016

Miniproject: 2048

@author: Ruben Dorado
"""

#import poc_2048_gui #this loads the GUI in codeskulptor
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    proxy_lst = []
    zeros = 0

    # fills the proxy_list with the non-zero values and counts how many zeroes are there
    for tile in line:
        if tile == 0:
            zeros += 1
        else:
            proxy_lst.append(tile)

    # merges the values in the proxy_list
    for pos in range(len(proxy_lst) - 1):
        if proxy_lst[pos] == proxy_lst[pos + 1]:
            proxy_lst[pos] *= 2
            proxy_lst.pop(pos + 1)
            proxy_lst.append(0)

    # adds the adequate amount of zeroes to the end of proxy_list
    for dummy_i in range(zeros):
        proxy_lst.append(0)

    return proxy_lst

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):

        self._height = grid_height
        self._width = grid_width
        self._grid = [[0 for dummy_col in range(self._width)]
                for dummy_row in range(self._height)]

        # creates a dictionary with the headers
        up_headers = [[0, up_col] for up_col in range(grid_width)]
        down_headers = [[grid_height - 1, down_col] for down_col in range(grid_width)]
        left_headers = [[left_row, 0] for left_row in range(grid_height)]
        right_headers = [[right_row, grid_width - 1] for right_row in range(grid_height)]
        self._headers = {UP: up_headers,
                        DOWN: down_headers,
                        LEFT: left_headers,
                        RIGHT: right_headers}

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        self._grid = [[0 for dummy_col in range(self._width)]
                for dummy_row in range(self._height)]
        self.new_tile()
        self.new_tile()

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        return "current board is: " + str(self._grid)

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self._height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self._width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        in_grid = []
        out_grid = []

        if direction == UP or direction == DOWN:
            num_steps = self._height
        else:
            num_steps = self._width

        # cicle through the grid in the given direction, merges the lines
        # and builds the new array in_grid
        for header in self._headers[direction]:
            line = []
            for step in range(num_steps):
                row = header[0] + step * OFFSETS[direction][0]
                col = header[1] + step * OFFSETS[direction][1]
                line.append(self._grid[row][col])
            in_grid.append(merge(line))

        # cicles through the in_grid array and builds the solution array
        # out_grid
        if direction == UP or direction == DOWN:
            for column in range(self._height):
                line = []
                new_row = column
                if direction == DOWN:
                    new_row = self._height - 1 - column
                for row in range(self._width):
                    new_col = row
                    line.append(in_grid[new_col][new_row])
                out_grid.append(line)
        else:
            for out_header in self._headers[direction]:
                line = []
                for step in range(num_steps):
                    new_row = out_header[0] + step * OFFSETS[direction][0]
                    new_col = out_header[1] + step * OFFSETS[direction][1]
                    line.append(in_grid[new_row][new_col])
                out_grid.append(line)

        # checks if the grid changed and if so, creates a new tile
        if not self._grid == out_grid:
            self._grid = out_grid
            self.new_tile()

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        empty_tiles = False
        for line in self._grid:
            for tile in line:
                if tile == 0:
                    empty_tiles = True

        if empty_tiles:
            new_row = random.randint(0, self._height - 1)
            new_col = random.randint(0, self._width - 1)
            while self._grid[new_row][new_col] != 0:
                new_row = random.randint(0, self._height - 1)
                new_col = random.randint(0, self._width - 1)
            new_val = random.choice([2, 2, 2, 2, 2, 2, 2, 2, 2, 4])
            self.set_tile(new_row, new_col, new_val)

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self._grid[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self._grid[row][col]

#poc_2048_gui.run_gui(TwentyFortyEight(4, 4))