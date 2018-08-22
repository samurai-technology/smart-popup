import configparser


class Config:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read("config.ini")

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
