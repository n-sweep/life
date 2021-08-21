import curses
from curses import wrapper

def main(screen):
    rows, cols = screen.getmaxyx()
    shape = (rows-2, cols-1)
    key = None
    while key != 'q':
        screen.clear()
        if key:
            screen.addstr(key)
        screen.refresh()
        key = screen.getkey()

if __name__ == "__main__":
    wrapper(main)