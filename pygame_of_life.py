import pygame as pg
import numpy as np

import sys
import pygame as pg
import numpy as np
import scipy.stats as stats
from conways import Life as ConwaysLife

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
        random_weight(float):       TODO:
    """

    clock = pg.time.Clock()

    def __init__(self, surface=None, w=500, h=500, scale=10, offset=1,
                    active_color=(225,225,225), inactive_color=(100,100,100),
                    background_color=(0,0,0), fps=60, name="Conway's Game of Life",
                    seed=None, random_weight=0.5):

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

        self.columns = h//scale
        self.rows = w//scale

        self.game = ConwaysLife((self.columns, self.rows), seed=self.seed, weight=random_weight)
        self.grid = self.game.board
    
    def run(self):
        """Runs the Game of Life"""
        # TODO: create a start menu
        self.intro_loop()
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
    
    def intro_loop(self):
        alive = True
        self.surface.fill(self.background_color)
        self.draw_grid()
        self.grid = self.game.board
        pg.display.update()

        while alive:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    sys.exit()
                
                if event.type in [pg.MOUSEBUTTONDOWN, pg.KEYDOWN]:
                    alive = False
            self.clock.tick(self.fps)

    def game_loop(self):
        """The main loop that keeps the game alive"""
        alive = True        # Game state - switching this to false exits the game
        paused = False

        while alive:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    alive = False
                
                if event.type == pg.MOUSEBUTTONDOWN:
                    # Right clicking will refresh the game. If the game has stablized, any click will refresh
                    if event.button == pg.BUTTON_RIGHT:
                        self.grid = self.game.new_game(random=True)    # Generate a new grid
                        self.caption(reset=True)            # Refresh the window title

                        # Reset Generations, unpause & reset stability status
                        paused = False
                    
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
                # Redraw and update board
                self.surface.fill(self.background_color)
                self.draw_grid()
                self.grid = self.game.next_board

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
                color = self.active_color if self.grid[col, row] else self.inactive_color
                
                pg.draw.rect(self.surface, color, [x+self.offset, y+self.offset, offset, offset])

def main():
    life = Life()

    life.run()

if __name__ == '__main__':
    main()