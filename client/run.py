import sys
import curses

import requests

from network import (
    get_players,
    new_player,
    update_player,
    get_map,
    remove_player
    )
import things


def main_loop(stdscr, server, name):
    curses.curs_set(0)
    stdscr.nodelay(1)
    screen_max_y, screen_max_x = stdscr.getmaxyx()
    half_screen_y = screen_max_y / 2
    half_screen_x = screen_max_x / 2
    player_char = curses.ACS_DIAMOND

    our_uid = new_player(server, name)
    map = get_map(server)
    pad_y = map['max_y']
    pad_x = map['max_x']
    pad = curses.newpad(pad_y, pad_x)

    try:
        while(True): # I know, ok?
            # Grabbing players list for use later
            players = get_players(server)
            # Clearing screen from last "frame"
            pad.clear()

            # Drawing proper border around the pad (no issues with flickering)
            # And no - I have no idea why we need to do -2 and not -1
            things.border_map(pad, pad_y-2, pad_x-2)

            for thing in map['things']:
                name, my, mx = thing
                getattr(things, name)(pad, my, mx)

            for player in players['players']:
                y = int(player['y'])
                x = int(player['x'])
                name = player['name']
                uid = player['id']

                # Adding name of the player above their head
                name_y = y-1
                name_x = x-(len(name)/2)
                if name_y < 1:
                    name_y = 0
                if name_x < 1:
                    name_x = 0
                pad.addstr(name_y, name_x, name)

                # Adding player box
                pad.addch(y, x, player_char)

                # --- OUR PLAYER PART ---
                if uid == our_uid:

                    key_pressed = stdscr.getch()
                    # We react to movement
                    moved = False
                    if key_pressed == curses.KEY_UP and y > 0:
                        y -= 1
                        moved = True
                    elif key_pressed == curses.KEY_DOWN and y < pad_y-1:
                        y += 1
                        moved = True
                    elif key_pressed == curses.KEY_LEFT and x > 0:
                        x -= 1
                        moved = True
                    elif key_pressed == curses.KEY_RIGHT and x < pad_x-1:
                        x += 1
                        moved = True

                    # and send movement update to server
                    if moved:
                        update_player(server, uid, y, x)

                    # We flush input buffer so we wont "stuck in move" if some
                    # one holds a key for too long.
                    curses.flushinp()

            #stdscr.refresh()
            pad.refresh(
                y - half_screen_y-5, x - half_screen_x-5,
                0, 0,
                screen_max_y - 1, screen_max_x - 1
            )
            curses.napms(100)
    except KeyboardInterrupt:
        remove_player(server, our_uid)
        sys.exit()


help_msg = ('\nFirst argument is server address.'
            '\nSecond argument is your name.'
            '\n\nFor example: ./run.py http://localhost:888 Marek'
            '\nHave FUN!\n')

if __name__ == '__main__':
    try:
        if 'help' in sys.argv[1] or sys.argv[1] == '-h':
            print(help_msg)
            sys.exit()
        else:
            try:
                curses.wrapper(main_loop, sys.argv[1], sys.argv[2])
            except requests.exceptions.ConnectionError:
                print('\nBEEP! BEEP! Server is DEAD!\n')
                sys.exit()

    except IndexError:
        print(help_msg)
