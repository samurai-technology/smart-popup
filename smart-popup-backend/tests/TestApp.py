import tornado.ioloop
import tornado.web


def make_app(handlers_library):
    handlers = handlers_library.home_handlers.handlers \
               + handlers_library.decision_handlers.handlers \
               + handlers_library.user_handlers.handlers
    return tornado.web.Application(handlers)
