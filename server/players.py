import rethinkdb as rdb
from rdb_utils import rdb_connection
import tornado.web


class Players(tornado.web.RequestHandler):

    def get(self):
        with rdb_connection() as conn:
            players = rdb.table('players').run(conn)
        self.write({'players': list(players)})

    def put(self):
        uid = self.get_argument('uid')
        x = self.get_argument('x')
        y = self.get_argument('y')

        with rdb_connection() as conn:
            rdb.table('players').get(uid).update(
                {'y': y, 'x': x}
            ).run(conn)

    def post(self):
        name = self.get_argument('name')
        with rdb_connection() as conn:
            output = rdb.table('players').insert(
                {'name': name, 'y': 3, 'x': 3}
            ).run(conn)
        if output.get('generated_keys'):
            uid = output['generated_keys'][0]
        self.write({'uid': uid})

    def delete(self):
        uid = self.get_argument('uid')
        with rdb_connection() as conn:
            rdb.table('players').get(uid).delete().run(conn)
