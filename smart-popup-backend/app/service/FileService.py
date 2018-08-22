import os.path


class FileService:
    def __init__(self, context_dir, config):
        self.models_dir = os.path.join(context_dir, config.get_models_dir())
        self.security_dir = os.path.join(context_dir, config.get_security_dir())

    def get_initial_model_path(self):
        initial_model_path = os.path.join(self.models_dir, "randomized_initial.dat")
        return initial_model_path

    def get_activity_model_path(self):
        activity_model_path = os.path.join(self.models_dir, "randomized_activity.dat")
        return activity_model_path

    def get_secret_path(self):
        secret_path = os.path.join(self.security_dir, "secret.txt")
        return secret_path
