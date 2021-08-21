import sys
import pygame as pg
import numpy as np
import scipy.stats as stats

white = (225,225,225)
black = (0,0,0)
grey = (100,100,100)
green = (13, 77, 0)

class Life:
    """
        Takes in a pygame display object and displays Conway's Game of Life
        The comination of width, height and scale determines the number of cells

         Parameters:
        -------------------
        surface (class):            pygame display object
        width (int):                width of display in px
        height (int):               height of display in px
        scale (int):                scale of the display
        offset (int):               padding around each cell in px
        active_color (tuple):       color of live cells
        inactive_color (tuple):     color of dead cells
        
        fps (int):                  frames per second
        name (str):                 text in game window's title bar
        seed (np.array):            a binary array to represent starting cells
    """

    clock = pg.time.Clock()

    def __init__(self, surface=None, w=500, h=500, scale=10, offset=1,
                    active_color=(225,225,225), inactive_color=(100,100,100),
                    background_color=(0,0,0), fps=60, name="Conway's Game of Life",
                    seed=None):

        pg.init()
        pg.display.set_caption(name)        

        # If no surface is given, create one based on the dimensions
        if surface:
            self.surface = surface
        else:
            self.surface = pg.display.set_mode((w, h+25))

        self.width = w
        self.height = h
        self.scale = scale
        self.offset = offset
        self.active_color = active_color
        self.inactive_color = inactive_color
        self.background_color = background_color
        self.fps = fps
        self.name = name
        self.seed = seed

        self.columns = int(h/scale)
        self.rows = int(w/scale)

        self.grid = self.generate_random_grid() if self.seed is None else self.generate_seeded_grid(seed)

        # self.grid = process_image(shape=(self.columns, self.rows), threshold=0.25)
    
    def run(self):
        """Runs the Game of Life"""
        # TODO: create a start menu
        # self.intro_loop()
        self.game_loop()
    
    @property
    def mods(self):
        """Returns states of modifier keys - ctrl, alt, shift"""
        return pg.key.get_mods()
    
    def caption(self, text=None, append=False, reset=False):
        """Window caption helper"""
        if text:        # If there is text, set (or append) the new caption
            text = self.name + text if append else text
            pg.display.set_caption(text)
        elif reset:     # If reset is enabled, revert back to the name given at instantiation
            pg.display.set_caption(self.name)
        else:           # If there are no params, just return the current caption
            return pg.display.get_caption()[0]
    
    def generate_random_grid(self, p=0.5):
        """Generate a new random matrix"""
        # TODO: make this an adjustable distribution
        n = self.rows * self.columns
        shape = (self.rows, self.columns)
        return stats.bernoulli(p).rvs(n).reshape(shape)
    
    def generate_seeded_grid(self, seed):
        """Generate a grid based on a given seed"""
        arr = np.zeros((self.rows, self.columns))
        x1, y1 = int((self.rows/2)-(seed.shape[0]/2)), int((self.columns/2)-(seed.shape[1]/2))
        x2, y2 = int(x1 + seed.shape[0]), int(y1 + seed.shape[1])
        arr[x1:x2, y1:y2] = seed
        return arr

    def game_loop(self):
        """The main loop that keeps the game alive"""
        alive = True        # Game state - switching this to false exits the game
        paused = False
        stable = False      # If the game becomes stable, it pauses

        # We're going to keep track of the generations (n of iterations)
        # and periodically check if the game has stabilized
        generation = 0
        check_freq = 100            # Stability check roughly every n frames
        check_thresh = 5            # Number of subsequent grids to check for duplicates
        check_grid = None
        check_count = 0

        while alive:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    alive = False
                
                if event.type == pg.MOUSEBUTTONDOWN:
                    # Right clicking will refresh the game. If the game has stablized, any click will refresh
                    if stable or event.button == pg.BUTTON_RIGHT:
                        self.grid = self.generate_random_grid()    # Generate a new grid
                        self.caption(reset=True)            # Refresh the window title

                        # Reset Generations, unpause & reset stability status
                        generation = 0
                        paused = False
                        stable = False
                    
                    # If shift-click, change active cells to a random color
                    if self.mods & pg.KMOD_SHIFT:
                        self.active_color = (
                            np.random.randint(226),
                            np.random.randint(226),
                            np.random.randint(226)
                        )
                
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:     # Spacebar pauses the game
                        if paused:
                            self.caption(reset=True)
                        else:
                            self.caption(' - Paused', append=True)
                        paused = not paused
                
                    if event.key == pg.K_ESCAPE:    # Escape opens a menu
                        self.menu_loop()

                    if event.key == pg.K_c:         # ctrl+w closes the game
                        mods = self.mods
                        if mods & pg.KMOD_CTRL:
                            alive = False

            if not paused:
                generation += 1

                if check_count > 0:
                    if np.array_equal(check_grid, self.grid):
                        paused = True
                        stable = True
                        if check_count == 1:    # getting a 1 is rare!
                            print("Game is 100% Stable! ")
                            text = f' - 100% Stable! (~{generation} Total)'
                        else:
                            excitement = '!' * (check_count - 2)    # anything more than 2 is rare!
                            print(f"Game is stable with {check_count} generations{excitement} (~{generation} Total)")
                            text = f' - Stable @ {check_count} Generations{excitement} (~{generation} Total)'
                        self.caption(text, append=True)

                    if check_count == check_thresh:
                        check_count = 0
                    else:
                        check_count += 1
                
                if generation % check_freq == 0:
                    check_grid = self.grid
                    check_count = 1
                
                # Redraw and update board
                self.caption(f' ({generation})', append=True)
                self.surface.fill(self.background_color)
                self.draw_grid()
                self.update_grid()

                pg.display.update()
                self.clock.tick(self.fps)
    
    def menu_loop(self):
        menu = True

        while menu:
            for event in pg.event.get():

                if event.type == pg.QUIT:
                    sys.exit()
                
                if event.type == pg.KEYDOWN:
                    if event.key in [pg.K_SPACE, pg.K_ESCAPE]:
                        menu = False
            
            self.draw_menu()
            
            pg.display.update()
            self.clock.tick(self.fps)

    def draw_menu(self):
        width, height = (300, 400)
        xloc, yloc = self.width/2 - width/2, self.height/2 - height/2

        pg.draw.rect(self.surface, (0,0,0), [xloc, yloc, width, height])

    def draw_grid(self):
        """Draw initial grid"""
        for row in range(self.rows):
            for col in range(self.columns):
                x = row * self.scale
                y = col * self.scale
                offset = self.scale - self.offset
                color = self.active_color if self.grid[row, col] else self.inactive_color
                
                pg.draw.rect(self.surface, color, [x+self.offset, y+self.offset, offset, offset])
    
    def update_grid(self):
        """Create a new grid and update each cell"""
        updated_grid = self.grid.copy()
        for row in range(updated_grid.shape[0]):
            for col in range(updated_grid.shape[1]):
                updated_grid[row, col] = self.update_cell(row, col)
        
        self.grid = updated_grid
    
    def update_cell(self, x, y):
        """
            Count each cell's neighbors and update the cell
            
             Parameters:
            -------------------
            x (int):    The location of the cell on the x axis
            y (int):    The location of the cell on the y axis

             Returns:
            -------------------
            current_state (int):    the new state of the cell
        """
        current_state = self.grid[x, y]
        alive_neighbors = 0

        for i in range(-1, 2):
            for j in range(-1, 2):
                try:
                    if (i, j) == (0, 0):
                        continue
                    elif self.grid[x+i, y+j]:
                        alive_neighbors += 1
                except:
                    continue
        
        if current_state:
            if alive_neighbors < 2 or alive_neighbors > 3:
                return 0
            if alive_neighbors in (2, 3):
                return 1
        elif alive_neighbors == 3:
            return 1
        
        return current_state

def main():
    life = Life()

    life.run()

if __name__ == '__main__':
    main()