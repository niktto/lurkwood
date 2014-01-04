import rethinkdb as rdb

RD_CONNECTION_DICT = {
    'host': 'localhost',
    'port': 28015,
    'db': 'lurkwood'
}


class rdb_connection(object):

    """Connect with rethinkdb base.

    Return connection object that is needed in every `run` operation.

    :param connection_dict:
    optional `dictionary` with connection parameters
    (`host`, `port`, `db`, `auth_key`), defaults to
    :data:`bookingcore.settings.RD_CONNECTION_DICT`.

    """

    def __init__(self, connection_dict=None):
        if connection_dict:
            self.conn = rdb.connect(**connection_dict)
        else:
            self.conn = rdb.connect(**RD_CONNECTION_DICT)

    def __enter__(self):
        return self.conn

    def __exit__(self, etype, evalue, traceback):
        self.conn.close()
