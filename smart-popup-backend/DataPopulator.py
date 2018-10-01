import os

from app.config import Config
from app.dao import DaoLibrary
from app.service import ServiceLibrary

if __name__ == "__main__":
    #db and services access
    context_dir = os.path.dirname(__file__)
    config = Config(context_dir)
    dao_library = DaoLibrary(config.get_database_host(), config.get_database_port(), config.get_database_name())
    service_library = ServiceLibrary(dao_library, context_dir, config)

    # TODO - populate DB
