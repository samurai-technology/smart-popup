import os.path

import tornado.ioloop
import tornado.web

from config import Config
from dao import DaoLibrary
from domain import DummyInitialModelTransformer, DummyActivityModelTransformer
from rest import HandlersLibrary
from service import ServiceLibrary


def make_app(handlers_library):
    handlers = handlers_library.home_handlers.handlers \
               + handlers_library.decision_handlers.handlers \
               + handlers_library.user_handlers.handlers
    return tornado.web.Application(handlers)


if __name__ == "__main__":
    config = Config()
    dao_library = DaoLibrary(config.get_database_host(), config.get_database_port(), config.get_database_name())

    app_dir = os.path.dirname(__file__)
    backend_dir = os.path.abspath(os.path.join(app_dir, os.pardir))
    service_library = ServiceLibrary(dao_library, backend_dir, config)

    transformer_service = service_library.transformer_service
    transformer_service.set_transformer("INITIAL_DUMMY", DummyInitialModelTransformer())
    transformer_service.set_transformer("ACTIVITY_DUMMY", DummyActivityModelTransformer())

    handlers_library = HandlersLibrary(service_library)
    app = make_app(handlers_library)
    app.listen(config.get_backend_port())
    tornado.ioloop.IOLoop.current().start()
