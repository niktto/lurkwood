import sys

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options

from players import Players


define("port", default=8888, help="run on the given port", type=int)


def main():
    tornado.options.parse_command_line()

    application = tornado.web.Application([
        (r"/players.json", Players),
    ])

    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()
