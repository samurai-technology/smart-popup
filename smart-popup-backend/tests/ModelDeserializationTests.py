import os
import pickle
import unittest

from app.service.FileService import FileService
from config import Config

context_dir = os.path.dirname(__file__)
config = Config(context_dir)


class ModelDeserializationTestCase(unittest.TestCase):

    def test_initial_model_deserialization(self):
        initial_model_path = FileService(context_dir, config).get_initial_model_path()
        initial_model_file = open(initial_model_path, "rb")
        initial_model = pickle.load(initial_model_file)
        initial_model_file.close()

    def test_activity_model_deserialization(self):
        activity_model_path = FileService(context_dir, config).get_activity_model_path()
        activity_model_file = open(activity_model_path, "rb")
        activity_model = pickle.load(activity_model_file)
        activity_model_file.close()


class ModelDeserializationTests:
    def __init__(self):
        self.suite = unittest.TestSuite()
        self.suite.addTest(ModelDeserializationTestCase("test_initial_model_deserialization"))
        self.suite.addTest(ModelDeserializationTestCase("test_activity_model_deserialization"))

    def get_suite(self):
        return self.suite
