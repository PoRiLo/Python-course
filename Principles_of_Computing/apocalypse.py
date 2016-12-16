"""
Fundamentals of Computing Part 2
Week 1 - June 2016

Miniproject: Apocalypse Zombie

@author: Ruben Dorado
"""

import random
import poc_grid
import poc_queue
import poc_zombie_gui

# global constants
EMPTY = 0
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = "obstacle"
HUMAN = poc_zombie_gui.HUMAN
ZOMBIE = poc_zombie_gui.ZOMBIE


class Apocalypse(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None,
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)
        else:
            self._human_list = []

    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        self._human_list = []
        self._zombie_list = []
        for row in range(self.get_grid_height()):
            for col in range(self.get_grid_width()):
                self.set_empty(row, col)

    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append([row, col])

    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)

    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        for ghoul in self._zombie_list:
            yield tuple(ghoul)

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append([row, col])

    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)

    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        for person in self._human_list:
            yield tuple(person)

    def compute_distance_field(self, entity_type):
        """
        Function computes a 2D distance field
        Distance at member of entity_queue is zero
        Shortest paths avoid obstacles and use distance_type distances
        """
        height = self.get_grid_height()
        width = self.get_grid_width()

        if entity_type == HUMAN:
            entity_list = self._human_list
        elif entity_type == ZOMBIE:
            entity_list = self._zombie_list

        visited = poc_grid.Grid(height, width)
        distance_field = [[height * width for dummy_col in range(width)]
                          for dummy_row in range(height)]
        boundary = poc_queue.Queue()
        for entity in entity_list:
            boundary.enqueue(entity)
            visited.set_full(entity[0], entity[1])
            distance_field[entity[0]][entity[1]] = 0

        while boundary:
            current_cell = boundary.dequeue()
            for neighbor in self.four_neighbors(current_cell[0], current_cell[1]):
                n_row = neighbor[0]
                n_col = neighbor[1]
                if visited.is_empty(n_row, n_col) and self.is_empty(n_row, n_col):
                    distance_field[n_row][n_col] = distance_field[current_cell[0]][current_cell[1]] + 1
                    visited.set_full(n_row, n_col)
                    boundary.enqueue(([n_row, n_col]))

        return distance_field

    def move_humans(self, zombie_distance):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        humans_flee = []
        options = {}

        for human in self._human_list:
            options = [[neighbor[0], neighbor[1], zombie_distance[neighbor[0]][neighbor[1]]] for neighbor
                       in self.eight_neighbors(human[0], human[1])]
            options.append([human[0], human[1], zombie_distance[human[0]][human[1]]])
            values = []

            for option in options:
                if not self.is_empty(option[0], option[1]):
                    option[2] = float("-inf")
                else:
                    values.append(option[2])

            best_move = max(values)
            best_moves = []
            for option in options:
                if option[2] == best_move:
                    best_moves.append((option[0], option[1]))

            humans_flee.append(random.choice(best_moves))

        self._human_list = humans_flee

    def move_zombies(self, human_distance):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        zombies_chase = []
        options = {}

        for zombie in self._zombie_list:
            options = [[neighbor[0], neighbor[1], human_distance[neighbor[0]][neighbor[1]]] for neighbor
                       in self.four_neighbors(zombie[0], zombie[1])]
            options.append([zombie[0], zombie[1], human_distance[zombie[0]][zombie[1]]])
            values = []

            for option in options:
                if not self.is_empty(option[0], option[1]):
                    option[2] = float("inf")
                else:
                    values.append(option[2])

            best_move = min(values)
            best_moves = []
            for option in options:
                if option[2] == best_move:
                    best_moves.append((option[0], option[1]))

            zombies_chase.append(random.choice(best_moves))

        self._zombie_list = zombies_chase

poc_zombie_gui.run_gui(Apocalypse(30, 40))