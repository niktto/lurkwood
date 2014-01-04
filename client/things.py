import curses


def small_house(screen, y, x):
    screen.addch(y+1, x, curses.ACS_ULCORNER)
    screen.addch(y+1, x+1, curses.ACS_HLINE)
    screen.addch(y+1, x+2, curses.ACS_HLINE)
    screen.addch(y+1, x+3, curses.ACS_HLINE)
    screen.addch(y+1, x+4, curses.ACS_URCORNER)
    screen.addch(y+2, x, curses.ACS_LLCORNER)
    screen.addch(y+2, x+1, curses.ACS_HLINE)
    screen.addch(y+2, x+2, curses.ACS_HLINE)
    screen.addch(y+2, x+3, curses.ACS_HLINE)
    screen.addch(y+2, x+4, curses.ACS_LRCORNER)


def small_bush(screen, y, x):
    screen.addch(y, x, curses.ACS_CKBOARD)
    screen.addch(y, x+1, curses.ACS_CKBOARD)
    screen.addch(y+1, x, curses.ACS_CKBOARD)


def border_map(screen, max_y, max_x):
    screen.addch(0, 0, curses.ACS_ULCORNER)
    screen.addch(0, max_x, curses.ACS_URCORNER)
    screen.addch(max_y, 0, curses.ACS_LLCORNER)
    screen.addch(max_y, max_x, curses.ACS_LRCORNER)
    for i in xrange(1, max_y):
        screen.addch(i, 0, curses.ACS_VLINE)
        screen.addch(i, max_x, curses.ACS_VLINE)

    for i in xrange(1, max_x):
        screen.addch(0, i, curses.ACS_HLINE)
        screen.addch(max_y, i, curses.ACS_HLINE)