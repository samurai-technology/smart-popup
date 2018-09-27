import pickle

# This import is needed to correctly unpickle models
from app.domain.modelsDefinitions import *


class ModelService:

    def __init__(self, file_service):
        initial_model_path = file_service.get_initial_model_path()
        initial_model_file = open(initial_model_path, "rb")
        self.initial_model = pickle.load(initial_model_file)
        initial_model_file.close()

        activity_model_path = file_service.get_activity_model_path()
        activity_model_file = open(activity_model_path, "rb")
        self.activity_model = pickle.load(activity_model_file)
        activity_model_file.close()

    def get_initial_model(self):
        return self.initial_model

    def get_activity_model(self):
        return self.activity_model
