from datetime import datetime, timedelta

import rethinkdb as rdb
from rdb_utils import rdb_connection
import tornado.web

from timeutils import get_datetimenow_with_server_timezone


class Players(tornado.web.RequestHandler):

    def get(self):
        """Get list of currently active players on the map.

        Before selecting active players, we make sure to delete guys that
        were inactive for more then 30 seconds.

        """
        now = get_datetimenow_with_server_timezone()

        with rdb_connection() as conn:
            # Removing old players
            rdb.table('players').filter(
                lambda player: player['touched'] < (now - timedelta(seconds=30))
            ).delete().run(conn)
            # Selecting active players
            players = rdb.table('players').without('touched').run(conn)

        self.write({'players': list(players)})

    def put(self):
        """Update player position."""
        uid = self.get_argument('uid')
        x = self.get_argument('x')
        y = self.get_argument('y')
        now = get_datetimenow_with_server_timezone()

        # Update player with new coordinates
        with rdb_connection() as conn:
            rdb.table('players').get(uid).update(
                {'y': y, 'x': x, 'touched': now}
            ).run(conn)

    def post(self):
        """Log new player to receive uid."""
        name = self.get_argument('name')
        now = get_datetimenow_with_server_timezone()

        with rdb_connection() as conn:
            output = rdb.table('players').insert(
                {'name': name, 'y': 3, 'x': 3, 'touched': now}
            ).run(conn)

        if output.get('generated_keys'):
            uid = output['generated_keys'][0]

        self.write({'uid': uid})

    def delete(self):
        """Remove player from map."""

        uid = self.get_argument('uid')
        with rdb_connection() as conn:
            rdb.table('players').get(uid).delete().run(conn)
