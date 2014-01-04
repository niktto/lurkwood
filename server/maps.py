import tornado.web


class Maps(tornado.web.RequestHandler):
    """This is just a mockup of maps class. Testing only."""
    def get(self):
        self.write({
            'max_y': 30,
            'max_x': 100,
            'things': (
                ('small_house', 20, 12),
                ('small_bush', 10, 40)
            )
        })