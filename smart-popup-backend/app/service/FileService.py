import os.path
import pickle


class FileService:
    def __init__(self, context_dir, config):
        self.models_dir = os.path.join(context_dir, config.get_models_dir())
        self.security_dir = os.path.join(context_dir, config.get_security_dir())

    def get_models_dir_path(self):
        return self.models_dir

    def get_secret_path(self):
        secret_path = os.path.join(self.security_dir, "secret.txt")
        return secret_path

    @staticmethod
    def read_binary(path):
        file = open(path, "rb")
        content = pickle.load(file)
        file.close()
        return content
