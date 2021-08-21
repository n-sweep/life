**Life Class:**

 - Board Class
    - shape, rows and columns of the board
    - seed, starting seed for the game
	    + if shape, center seed in array of shape
	    + else make shape == seed.shape
    - create a new board
	    + reset
	    + new random
    - check for stability
     
- Cell Class 
	- get neighbors
	- update (return) state
		+ look at neighbors
		+ apply rules of the game
	- break this down into deciding if the cell is dead or alive vs deciding it's class
		+ classed: 0 (dead) or 1 (alive)
		+ unclassed: same as above, but live cells have a chance to be one of *n* classes