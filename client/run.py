import sys
import curses

import requests


def get_players(addr):
    return requests.get('/'.join((addr, 'players.json'))).json()


def new_player(addr, name):
    return requests.post(
        '/'.join((addr, 'players.json')),
        data={'name': name}
    ).json()['uid']


def update_player(addr, uid, y, x):
    requests.put(
        '/'.join((addr, 'players.json')),
        data={
            'y': y,
            'x': x,
            'uid': uid
        }
    )


def remove_player(addr, uid):
    requests.delete(
        '/'.join((addr, 'players.json')),
        params={'uid':uid}
    )


def main_loop(stdscr, server, name):
    curses.curs_set(0)
    stdscr.nodelay(1)
    player_char = curses.ACS_DIAMOND
    stdscr_y, stdscr_x = stdscr.getmaxyx()

    our_uid = new_player(server, name)

    try:
        while(True): # I know, ok?

            # Clearing screen from last "frame"
            stdscr.clear()

            players = get_players(server)

            for player in players['players']:
                y = int(player['y'])
                x = int(player['x'])
                name = player['name']
                uid = player['id']

                # Adding name of the player above their head
                stdscr.addstr(y-1, x-(len(name)/2), name)

                # Adding player box (new players shine)
                stdscr.addch(y, x, player_char)
                stdscr.addstr(0,0,uid)
                stdscr.addstr(0,0,our_uid)

                # --- OUR PLAYER PART ---
                if uid == our_uid:

                    key_pressed = stdscr.getch()
                    # We react on movement
                    if key_pressed == curses.KEY_UP and y > 0:
                        y -= 1
                    elif key_pressed == curses.KEY_DOWN and y < stdscr_y-1:
                        y += 1
                    elif key_pressed == curses.KEY_LEFT and x > 0:
                        x -= 1
                    elif key_pressed == curses.KEY_RIGHT and x < stdscr_x-1:
                        x += 1

                    # and send movement update to server
                    update_player(server, uid, y, x)

            stdscr.refresh()
            curses.napms(500)
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
