import numpy as np

class Life:
    """Docstring"""

    generations = 0

    def __init__(self, shape=None, seed=None, weight=0.35, classes=1):
        self.shape = shape
        self.seed = seed
        self.weight = weight
        self.classes = classes

        self.initialize_board(shape, seed)
    
    def new_game(self, reset=True, random=False, new_seed=None):
        if new_seed is not None:
            seed = new_seed
        elif random:
            seed = None
        else:
            seed = self.seed

        self.initialize_board(self.shape, seed)
        return self.board

    def initialize_board(self, shape, seed):
        """Generates our initial game board"""
        if shape is not None:
            if seed is not None:
                # This assumes seed is a smaller size than self.board
                x1 = shape[0]//2 - seed.shape[0]//2
                y1 = shape[1]//2 - seed.shape[1]//2
                x2 = x1 + seed.shape[0]
                y2 = y1 + seed.shape[1]
                
                # Center seed on the board
                board = np.zeros(shape, dtype=int)
                board[x1:x2, y1:y2] = seed

            else:   # If no seed, generate a random board
                board = np.random.choice(
                    self.classes + 1,
                    np.prod(self.shape),
                    p=[1-self.weight] + [self.weight * (1/self.classes)] * self.classes
                ).reshape(self.shape)

            self.board = board
            self.starting_board = board
            self.previous_board = None
            return board

        elif seed is not None:  # If there's no shape, the seed is the entire board
            self.shape = seed.shape
            return seed

        else:       # We need either a shape or a seed to generate a new game board
            raise Exception("Either a shape or a seed are required.")
    
    def _generation(self):
        """
            Apply the rules of Conway's Game of Life to the board and then update it:

                1. Any live cell with fewer than two live neighbours dies, as if by underpopulation.
                2. Any live cell with two or three live neighbours lives on to the next generation.
                3. Any live cell with more than three live neighbours dies, as if by overpopulation.
                4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
        """
        # Increment generations and create new board
        self.generations += 1
        new_board = self.board.copy()

        # For the location of each cell on the game board...
        for loc in np.ndindex(*self.shape): # TODO: see if nested for loop is faster than this
            neighbors = []

            # Find the cell's live neighbors
            for i in range(-1, 2):
                for j in range(-1, 2):
                    try:
                        if (i, j) == (0, 0):
                            continue

                        cell = self.board[loc[0]+i, loc[1]+j]
                        if cell:
                            neighbors.append(cell)
                    except:
                        continue
            
            # Numpy solution is slower
            # loc_arr = np.array(loc)
            # tl = (loc_arr - 1).clip(min=0)
            # br = (loc_arr + 2).clip(max=self.shape)
            # by_3 = self.board[tl[0]:br[0], tl[1]:br[1]]
            # origin = self.board[loc]
            # neighbors = by_3.sum() - origin

            # Apply the rules of Life
            num_neighbors = len(neighbors)
            if not 2 <= num_neighbors <=3:
                new_board[loc] =  0
            elif num_neighbors == 3:
                if self.classes > 1:
                    mutation_prob = 0.01
                    nbr_set = list(set(neighbors))
                    nbr_counts = np.array([neighbors.count(neighbor) for neighbor in nbr_set])
                    probs = np.append((nbr_counts / nbr_counts.sum()) * (1-mutation_prob), mutation_prob)
                    nbr_set.append(np.random.choice(nbr_set))
                    new_board[loc] = np.random.choice(nbr_set, p=probs)

                else:
                    new_board[loc] = 1
        
        # Update the game board
        self.previous_board = self.board
        self.board = new_board
    
    @property
    def next_board(self):
        """Updates and returns the game board"""
        self._generation()
        return self.board

if __name__ == '__main__':
    seed = np.array([
        [0,0,0,0,0],
        [0,1,1,0,0],
        [0,0,1,1,0],
        [0,0,1,0,0],
        [0,0,0,0,0]
    ])
    
    l = Life((5,5))
    print(l.board)
    print(l.board[[seed]])
    