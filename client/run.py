import curses

players_checked = 0


def get_players():

    # mocked for now
    global players_checked

    players_checked = players_checked + 1

    result = [
        (10, 12, "Jonasz", 1),
        (15, 32, "Augiasz", 2),
        (2+(players_checked/10), 2+(players_checked/10), "RUN", 3)
    ]

    if players_checked > 100:
        result.append(
            (13,
             players_checked/10,
             "Nowosz",
             4)
        )

    return result


def main_loop(stdscr):
    global players_checked

    curses.curs_set(0)
    player_char = curses.ACS_DIAMOND
    new_player = curses.A_STANDOUT
    old_player = curses.A_DIM

    seen_players_uids = []

    while(players_checked < 300): # I know, ok?

        # Clearing screen from last "frame"
        stdscr.clear()

        players = get_players()

        for player in players:
            y, x, name, uid = player

            # Adding name of the player above their head
            stdscr.addstr(y-1, x-(len(name)/2), name)

            # Adding player box (new players shine)
            if uid in seen_players_uids:
                stdscr.addch(y, x, player_char, old_player)
            else:
                stdscr.addch(y, x, player_char, new_player)
                seen_players_uids.append(uid)

        # "frame" number for debugging
        stdscr.addstr(0,0, str(players_checked))

        stdscr.refresh()
        curses.napms(100)


if __name__ == '__main__':
    curses.wrapper(main_loop)
