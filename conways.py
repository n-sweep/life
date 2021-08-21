import sys
import numpy as np

R_PENTOMINO = np.array([
    [0, 1, 1],
    [1, 1, 0],
    [0, 1, 0]
])

class Cell:
    """
        The cell will have access to the game board, it will look at
        its own neighbors and apply the rules to the game of life,
        returning its updated status
    """
    cell_class = None
    mutation_prob = 0.001

    def __init__(self, loc, board):
        self.loc = loc
        self.board = board

        # Get initial status from the starting board array
        self.status = int(self.board.array[loc] > 0)
        # Get initial neighbors
        self.update_neighbors()

        if board.classes > 1:
            self.cell_class = self.board.array[loc]
    
    def update(self, new_board):
        """
            Wrapper for various update processes
        """
        old_status = self.status
        self.update_neighbors()
        self.update_status()
        if self.status == old_status:
            return
        if self.cell_class != None and self.status:
            self.update_class()
            update = self.cell_class
        else:
            update = self.status
        
        new_board[self.loc] = update

    def update_neighbors(self):
        """
            Look at each cell adjacent to this one
            and return their values
        """
        neighbors = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (i, j) == (0, 0):
                    continue
                try:
                    y, x = self.loc[0]+i, self.loc[1]+j
                    neighbor = self.board.array[y, x]
                    if neighbor > 0:
                        neighbors.append(neighbor)
                except:
                    continue
        
        self.neighbors = neighbors
    
    def update_status(self):
        """
            Appls the rules to the game 
            and update the cells status
        """
        num_nbrs = len(self.neighbors)
        if not 2 <= num_nbrs <= 3:
            self.status = 0
        elif num_nbrs == 3:
            self.status = 1

    def update_class(self):
        """
            Look at neighbors to determine the class of a new cell
        """
        neighbors_set = list(set(self.neighbors))
        counts = np.array([self.neighbors.count(n) for n in neighbors_set])
        probs = (counts / counts.sum()) * (1-self.mutation_prob)
        probs = np.append(probs, self.mutation_prob)
        neighbors_set.append(np.random.choice(np.arange(1, self.board.classes)))        

        self.cell_class = np.random.choice(neighbors_set, p=probs)


class Board:
    """
        The board will hold the numpy array that represents the game board
        It will generate new boards based on input and query cells for updates
    """

    def __init__(self, game):
        self.game = game
        self.classes = game.classes
        self.shape = game.shape
        self.seed = game.seed
        self.cells = []

        self.initialize_board()
        self.initialize_cells()

    def initialize_board(self):
        """Generates a new game board"""
        seed = self.seed and self.seed.any()
        if not (self.shape or seed):
            raise Exception("Either a shape or a seed is required.")

        elif self.shape and seed:
            # Center the seed on a game board
            board = self._center_seed(self.shape, self.seed)

        elif self.shape:
            # The probability a cell starts off dead
            prob_dead = [1 - self.game.weight]
            # Class probabilities for live cells
            probs_alive = [self.game.weight * (1/self.classes)] * self.classes

            board = np.random.choice(
                self.classes + 1,
                np.prod(self.shape),
                p = prob_dead + probs_alive
            ).reshape(self.shape)
            
        else:   # Only a seed is given
            self.shape = self.seed.shape
            board = self.seed

        self.array = board
        self.start_array = board
        self.prev_array = None
    
    def initialize_cells(self):
        """Creates objects for each cell in the game board"""
        for loc in np.ndindex(*self.shape): # TODO: see if nested for loop is faster than this
            c = Cell(loc, self)
            self.cells.append(c)

    # todo:
    def next_generation(self):
        """
            Iterate to the next generation of the gameboard
        """
        new_board = self.array.copy()
        for cell in self.cells:
            cell.update(new_board)
        
        if np.array_equal(self.prev_array, new_board):
            self.game.stable = True
        else:
            self.prev_array = self.array
            self.array = new_board

    def _center_seed(self, shape, seed):
        """Centers the given seed on the size of the game board"""
        board = np.zeros(shape, dtype=int)  # Start with a blank board

        # Find coordinates to place the seed array
        # Note: this assumes the seed <= the size of the game board
        x0 = shape[0]//2 - seed.shape[0]//2
        y0 = shape[1]//2 - seed.shape[1]//2
        x1 = x0 + seed.shape[0]
        y1 = y0 + seed.shape[1]

        # Place the seed on the board
        board[x0:x1, y0:y1] = seed

        return board

    def __repr__(self):
        return str(self.array)

class Life:
    """Docstring"""

    generations = 0
    stable = False

    def __init__(self, shape=None, seed=None, weight=0.35, classes=1):
        self.shape = shape
        self.seed = seed
        self.weight = weight
        self.classes = classes
        self.gameboard = Board(self)
    
    @property
    def board(self):
        return self.gameboard.array
    
    @property
    def next_board(self):
        if not self.stable:
            self.generate()
        return self.board

    def generate(self):
        self.generations += 1
        self.gameboard.next_generation()

    # todo:
    #def stability_check

if __name__ == '__main__':
    game = Life((20,20), classes=9)
    board = game.gameboard
    cell = Cell((10,10), board)
    nb = board.array.copy()
    print(cell.neighbors)
    cell.update(nb)
    print(cell.neighbors)
