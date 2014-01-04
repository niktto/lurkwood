import curses

import requests


def get_players():
    return requests.get('http://localhost:8888/players.json').json()


def new_player():
    return requests.post(
        'http://localhost:8888/players.json',
        data={'name': 'Marek'}
    ).json()['uid']


def update_player(uid, y, x):
    requests.put(
        'http://localhost:8888/players.json',
        data={
            'y': y,
            'x': x,
            'uid': uid
        }
    )


def remove_player(uid):
    requests.delete(
        'http://localhost:8888/players.json',
        params={'uid':uid}
    )


def main_loop(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(1)
    player_char = curses.ACS_DIAMOND
    stdscr_y, stdscr_x = stdscr.getmaxyx()

    our_uid = new_player()

    try:
        while(True): # I know, ok?

            # Clearing screen from last "frame"
            stdscr.clear()

            players = get_players()

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
                    update_player(uid, y, x)

            stdscr.refresh()
            curses.napms(500)
    except KeyboardInterrupt:
        remove_player(our_uid)


if __name__ == '__main__':
    curses.wrapper(main_loop)
