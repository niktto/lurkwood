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


def get_map(addr):
    return requests.get('/'.join((addr, 'maps.json'))).json()


def remove_player(addr, uid):
    requests.delete(
        '/'.join((addr, 'players.json')),
        params={'uid': uid}
    )
