import tornado.web


class HomeHandlers:
    def __init__(self):
        self.handlers = [
            (r"/", MainHandler)
        ]


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        response = {"message": "Welcome to Smart Popup!"}
        self.write(response)
        self.set_status(200)
