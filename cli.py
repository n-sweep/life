
import curses
from curses import wrapper
import numpy as np
from time import sleep
from conways import Life

seed = np.array([[0,1,1],[1,1,0],[0,1,0]])
alpha = 'abcdefghijklmnopqrstuvwxyz'
alpha = list(alpha + alpha.upper())
num = [str(i) for i in range(10)]
symb = list('`~!@#$%^&*()-_=+[{]}|;:\'",<.>/?]')
chars = num + symb

# def array_to_ascii(arr, char='#'):
#     if type(char) is str:
#         return '\n'.join([''.join(row) for row in np.array([' ', char])[arr]])
#     elif type(char) is list:
#         return '\n'.join([''.join([np.random.choice(char) if item else ' ' for item in row]) for row in arr])

def array_to_ascii(arr):
    ascii = [''.join([str(item) if item else ' ' for item in row]) for row in arr]
    return '\n'.join(ascii)

def scores(game):
    board = game.board
    live_cells = np.count_nonzero(board)
    counts = np.bincount(board.flatten())[1:]
    classes = np.arange(game.classes + 1)[1:]
    text = [f'{classes[i]}: {counts[i]}' for i in counts.argsort()[::-1] if counts[i]]
    return ' '.join(text)

def pause(screen):
    key = None
    while key != ord(' '):
        key = screen.getch()
        curses.napms(200)

def app(screen):
    curses.curs_set(0)
    rows, cols = screen.getmaxyx()
    shape = (rows-3, cols-2)
    classes = 9
    game = Life(shape, weight=0.35, classes=9)
    text = array_to_ascii(game.board)
    if game.classes > 1:
        hud = '\n' + scores(game)
        text += hud + ' ' * (cols - len(hud))
    screen.addstr(text)
    screen.refresh()
    screen.getch()
    screen.nodelay(1)

    key = None
    while key != ord('q'):
        text = array_to_ascii(game.next_board)
        if game.classes > 1:
            hud = '\n' + scores(game)
            text += hud + ' ' * (cols - len(hud))
        screen.addstr(0, 0, text)
        screen.refresh()
        curses.napms(80)
        key = screen.getch()
        if key == ord(' '):
            pause(screen)

def main():
    s = seed.shape
    r = np.random.choice(range(1,10), size=np.prod(s)).reshape(s)
    print(r * [seed])


if __name__ == '__main__':
    try:
        # main()
        wrapper(app)
    except KeyboardInterrupt:
        pass
