import configparser

import os


class Config:
    def __init__(self, context_dir):
        self.config = configparser.ConfigParser()
        config_path = os.path.join(context_dir, "config.ini")
        self.config.read(config_path)

    def get_env(self):
        return self.config["DEFAULT"]["ENV"]

    def get_backend_port(self):
        return int(self.config["BACKEND"]["PORT"])

    def get_database_host(self):
        return self.config["DATABASE"]["HOST"]

    def get_database_port(self):
        return int(self.config["DATABASE"]["PORT"])

    def get_database_name(self):
        return self.config["DATABASE"]["DB_NAME"]

    def get_models_dir(self):
        return self.config["MODELS"]["MODELS_DIR"]

    def get_security_dir(self):
        return self.config["SECURITY"]["SECURITY_DIR"]
