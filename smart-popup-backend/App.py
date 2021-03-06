import os.path

import tornado.ioloop
import tornado.web

from app.config import Config
from app.dao import DaoLibrary
from app.rest import HandlersLibrary
from app.service import ServiceLibrary
from predictors import DummyPredictor


def make_app(handlers_library):
    handlers = handlers_library.home_handlers.handlers \
               + handlers_library.decision_handlers.handlers \
               + handlers_library.user_handlers.handlers
    return tornado.web.Application(handlers)


if __name__ == "__main__":
    context_dir = os.path.dirname(__file__)
    config = Config(context_dir)
    dao_library = DaoLibrary(config.get_database_host(), config.get_database_port(), config.get_database_name())
    service_library = ServiceLibrary(dao_library, context_dir, config)

    # TODO - register models for predictors in ModelsRegistry

    # TODO - replace dummy predictor
    predictors_registry = service_library.predictors_registry
    predictors_registry.set_predictor("predictor_activity", DummyPredictor())
    predictors_registry.set_predictor("predictor_initial", DummyPredictor())

    handlers_library = HandlersLibrary(service_library)
    app = make_app(handlers_library)
    app.listen(config.get_backend_port())
    tornado.ioloop.IOLoop.current().start()
