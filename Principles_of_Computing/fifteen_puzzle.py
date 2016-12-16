"""
Principles of Computing- Part 2
Week 4 - June 2016

Miniproject: The Lloyd's Fifteen Puzzle

@author: Ruben Dorado
http://www.codeskulptor.org/#user41_qPJvgquoVaB7l4W.py

Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""

#import poc_fifteen_gui

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction

    ##################################################################
    # Phase one methods

    def lower_row_invariant(self, target_row, target_col):
        """
        This invariant is True if the following three conditions are all True:
            1. Tile zero is positioned at (i,j).
            2. All tiles in rows i+1 or below are positioned at their solved
                location.
            3. All tiles in row i to the right of position (i,j) are positioned
                at their solved location.

        Inputs:
        target_row: row of the target tile
        target_col: column of the target tile

        Returns a boolean
        """
        # check that zero is in position (row, col)
        current_number = self.get_number(target_row, target_col)
        if not current_number == 0:
            return False

        # check if the rows below are in order
        for row in range(self._height):
            if row > target_row:
                for col in range(self._width):
                    current_number = self.get_number(row, col)
                    corresponding_number = col + self._width * row
                    if not current_number == corresponding_number:
                        return False

        # check if the cells to the right are in order
        for col in range(self._width):
            if col > target_col:
                current_number = self.get_number(target_row, col)
                corresponding_number = col + self._width * target_row
                if not current_number == corresponding_number:
                    return False

        return True

    def relocate_tile(self, idx_i, idx_j, idx_k, idx_l):
        """
        Helper function. Gives the secuence of movements required to relocate a
        tile from position (k, l) to target position (i, j)

        Inputs
        idx_i, idx_j: row and column of the target position
        idx_k, idx_l: row and column of the current position

        Output
        sequence: a string representing a series of moves
        """
        sequence = ""

        # case k = i
        if idx_k == idx_i:
            sequence += (idx_j - idx_l) * "l"
            sequence += (idx_j - idx_l - 1) * "urrdl"

        # case k < i, l = j
        elif idx_l == idx_j:
            sequence += (idx_i - idx_k) * "u"
            sequence += "ld"
            sequence += (idx_i - idx_k - 1) * "druld"

        # case k < i, l > j
        elif idx_l > idx_j:
            sequence += (idx_i - idx_k) * "u"
            sequence += (idx_l - idx_j - 1) * "r"
            if idx_k == 0:
                sequence += (idx_l - idx_j) * "rdllu"
            else:
                sequence += (idx_l - idx_j) * "rulld"
            sequence += (idx_i - idx_k) * "druld"

        # case k < i, l < j
        elif idx_l < idx_j:
            sequence += (idx_i - idx_k) * "u"
            sequence += (idx_j - idx_l) * "l"
            sequence += (idx_j - idx_l - 1) * "drrul"
            sequence += (idx_i - idx_k) * "druld"

        return sequence

    def solve_interior_tile(self, target_row, target_col):
        """
        Solves the puzzle at position (i, j) where i>1 and j>0.
        This method takes a puzzle for which lower_row_invariant(i, j) is True
        and repositions the tiles in the puzzle such that
        lower_row_invariant(i, j - 1) is True.

        Inputs:
        target_row: row of the target tile
        target_col: column of the target tile

        Updates the puzzle grid to position (i, j - 1)
        Returns moves: a string representing the chain of moves required to take
        the right tile to the target position
        """
        moves = ""

        # check that the condition to start is satisfied
        assert self.lower_row_invariant(target_row, target_col), "the invariant to start the process is not satisfied"

        # where is the tile we are looking for?
        position = self.current_position(target_row, target_col)

        # call the position_tile function
        moves = self.relocate_tile(target_row, target_col,
                                   position[0], position[1])

        # update the puzzle
        self.update_puzzle(moves)

        # check if the puzzle satisfies the invariant for the next step
        assert self.lower_row_invariant(target_row, target_col - 1), "the invariant for the next step is not satisfied"

        return moves

    def solve_col0_tile(self, target_row):
        """
        Solves the puzzle at position (i, 0) where i > 1.
        This method takes a puzzle for which lower_row_invariant(i, j) is True
        and repositions the tiles in the puzzle such that
        lower_row_invariant(i - 1, self._width - 1) is True.

        Inputs:
        target_row: row of the target tile

        Updates the puzzle grid to position (i - 1, self._width - 1)
        Returns moves: a string representing the chain of moves required to take
        the right tile to the target position
        """
        # check that the condition to start is satisfied
        assert self.lower_row_invariant(target_row, 0), "the invariant to start the process is not satisfied"

        # prepare the puzzle for the next step
        preparation_moves = "ur"
        self.update_puzzle(preparation_moves)
        moves = ""

        # where is the tile we are looking for?
        position = self.current_position(target_row, 0)

        # in case not k == (i - 1) or not l == 0
        if not position == (target_row, 0):
            moves += self.relocate_tile(target_row - 1, 1,
                                        position[0], position[1])
            moves += "ruldrdlurdluurddlur"

        moves += (self._width - 2) * "r"

        # update the puzzle
        self.update_puzzle(moves)

        # check if the puzzle satisfies the invariant for the next step
        assert self.lower_row_invariant(target_row - 1, self._width - 1), "the invariant for the next step is not satisfied"

        return preparation_moves + moves

    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether tile zero is at (0, j) and whether all positions either
        below or to the right of this position are solved, including tile (1, j)

        Input
        target_col: The column of the tile to check

        Returns a boolean
        """
        # check that zero is in position (0, col)
        current_number = self.get_number(0, target_col)
        if not current_number == 0:
            return False

        # check that the tile in row 1 is the right one
        current_number = self.get_number(1, target_col)
        corresponding_number = target_col + self._width
        if not current_number == corresponding_number:
            return False

        # check if the rows below are in order
        for row in range(2, self._height):
            for col in range(self._width):
                current_number = self.get_number(row, col)
                corresponding_number = col + self._width * row
                if not current_number == corresponding_number:
                    return False

        # check if the cells to the right are in order
        for col in range(target_col + 1, self._width):
            for row in [0, 1]:
                current_number = self.get_number(row, col)
                corresponding_number = col + row * self._width
                if not current_number == corresponding_number:
                    return False

        return True

    def row1_invariant(self, target_col):
        """
        Check whether tile zero is at (1, j) and whether all positions either
        below or to the right of this position are solved.

        Input
        target_col: The column of the tile to check

        Returns a boolean
        """
        # check that zero is in position (1, col)
        current_number = self.get_number(1, target_col)
        if not current_number == 0:
            return False

        # check if the rows below are in order
        for row in range(2, self._height):
            for col in range(self._width):
                current_number = self.get_number(row, col)
                corresponding_number = col + self._width * row
                if not current_number == corresponding_number:
                    return False

        # check if the cells to the right are in order
        for col in range(target_col + 1, self._width):
            for row in [0, 1]:
                current_number = self.get_number(row, col)
                corresponding_number = col + row * self._width
                if not current_number == corresponding_number:
                    return False

        return True

    def solve_row1_tile(self, target_col):
        """
        Solves the puzzle at position (1, j) where j > 1.
        This method takes a puzzle for which row1_invariant(j) is True
        and repositions the tiles in the puzzle such that
        row0_invariant(j) is True.

        Inputs:
        target_row: row of the target tile

        Updates the puzzle grid to position (0, j)
        Returns moves: a string representing the chain of moves required to take
        the right tile to the target position
        """
        moves = ""

        # check that the condition to start is satisfied
        assert self.row1_invariant(target_col), "the invariant to start the process is not satisfied"

        # where is the tile we are looking for?
        position = self.current_position(1, target_col)

        # call the position_tile function
        moves += self.relocate_tile(1, target_col, position[0], position[1])
        moves += "ur"

        # update the puzzle
        self.update_puzzle(moves)

        # check if the puzzle satisfies the invariant for the next step
        assert self.row0_invariant(target_col), "the invariant for the next step is not satisfied"

        return moves

    def solve_row0_tile(self, target_col):
        """
        Solves the puzzle at position (0, j) where j > 1.
        This method takes a puzzle for which row0_invariant(j) is True
        and repositions the tiles in the puzzle such that
        row1_invariant(1, j - 1) is True.

        Inputs:
        target_row: row of the target tile

        Updates the puzzle grid to position (1, j - 1)
        Returns moves: a string representing the chain of moves required to take
        the right tile to the target position
        """

        # check that the condition to start is satisfied
        assert self.row0_invariant(target_col), "the invariant to start the process is not satisfied"

        # position the zero tile in the right place
        preparation_moves = "ld"
        self.update_puzzle(preparation_moves)
        moves = ""

        # is the (0, j) tile correct already?
        current_number = self.get_number(0, target_col)
        corresponding_number = target_col
        if not current_number == corresponding_number:
            # where is the tile we are looking for?
            position = self.current_position(0, target_col)

            # move the tile to the (1, j-1) position
            moves += self.relocate_tile(1, target_col - 1, position[0], position[1])

            # position the tile in (0, j)
            moves += "urdlurrdluldrruld"

        # update the puzzle
        self.update_puzzle(moves)

        # check if the puzzle satisfies the invariant for the next step
        assert self.row1_invariant(target_col - 1), "the invariant for the next step is not satisfied"

        return preparation_moves + moves

    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solves a 2x2 puzzle.
        This method takes a puzzle for which row1_invariant(1) is True
        and repositions the tiles to make lower_row_invariant(0, 0) True.

        Updates the puzzle grid to position (0, 0)
        Returns moves: a string representing the chain of moves required to
        finish the puzzle
        """
        # check that the condition to start is satisfied
        assert self.row1_invariant(1), "the invariant to start the process is not satisfied"

        current_00 = self.get_number(0, 0)
        if current_00 == 1:
            moves = "ul"
        elif current_00 == self._width:
            moves = "lu"
        elif current_00 == self._width + 1:
            moves = "uldrul"
        else:
            print "Not solvable configuration!"
            moves = ""

        # update the puzzle
        self.update_puzzle(moves)

        assert self.lower_row_invariant(0, 0), "The 2x2 puzzle couldn't be solved"

        return moves

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle

        Updates the puzzle and returns a move string
        """
        solution = ""

        # First, locate the 0 tile and move it to (m, n)
        start_position = self.current_position(0, 0)
        solution += (self._height - start_position[0] - 1) * "d"
        solution += (self._width - start_position[1] - 1) * "r"
        self.update_puzzle(solution)

        for row in range(self._height - 1, 1, -1):
            for col in range(self._width - 1, 0, -1):
                solution += self.solve_interior_tile(row, col)
            solution += self.solve_col0_tile(row)

        for col in range(self._width - 1, 1, -1):
            solution += self.solve_row1_tile(col)
            solution += self.solve_row0_tile(col)

        solution += self.solve_2x2()

        return solution


# Start interactive simulation
#poc_fifteen_gui.FifteenGUI(obj_2)

#obj = Puzzle(4, 5, [[15, 16, 0, 3, 4], [5, 6, 7, 8, 9], [10, 11, 12, 13, 14], [1, 2, 17, 18, 19]])
#
#print obj
#print obj.solve_puzzle()
#print obj