import numpy as np
from numpy import random
from pygame_of_life import Life
# from game_of_life_old import Life

white = (225,225,225)
black = (0,0,0)
grey = (100,100,100)
green = (13, 77, 0)

seed = np.array([
    [0,0,0,0,0],
    [0,1,1,0,0],
    [0,0,1,1,0],
    [0,0,1,0,0],
    [0,0,0,0,0]
])

def main():
    life = Life(
        w=1200,
        h=750,
        scale=8,
        active_color=white,
        inactive_color=grey,
        background_color=black,
        seed=seed,
        # random_weight=0.25
    )

    life.run()

if __name__ == '__main__':
    main()