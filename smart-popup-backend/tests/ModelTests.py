import os
import unittest

from app.domain.modelFeatures.ActivityModelFeatures import ActivityModelFeatures
from app.domain.modelFeatures.InitialModelFeatures import InitialModelFeatures
from config import Config
from dao import DaoLibrary
from dbPopulator import DBPopulator
from service import ServiceLibrary


context_dir = os.path.dirname(__file__)
config = Config(context_dir)
dao_library_for_tests = DaoLibrary(
    config.get_database_host(),
    config.get_database_port(),
    config.get_database_name(),
)
client_data_dao = dao_library_for_tests.client_data_dao
service_library_for_tests = ServiceLibrary(dao_library_for_tests, context_dir, config)
model_service = service_library_for_tests.model_service
user_service = service_library_for_tests.user_service


def clean_db():
    dao_library_for_tests.db.command("dropDatabase")

class ModelTestCase(unittest.TestCase):

    def setUp(self):
        clean_db()

    def test_initial_model(self):
        initial_model = model_service.get_initial_model()
        db_populator = DBPopulator(client_data_dao, user_service)
        auth_token = db_populator.populate_one_client_data()
        user_id = user_service.authenticate(auth_token).get_user_id()
        client_data = user_service.get_client_data_by_user_id(user_id)
        initial_model_features = InitialModelFeatures(
            client_data["data"]["impute_dict"],
            {
                "day_of_week": None,
                "device_category": None,
                "browser": None,
                "country": None
            },
            client_data["data"]["discrete_data"]
        )
        model_input = initial_model_features.get_model_input()
        result = initial_model.predict(model_input)
        self.assertEqual(result, [1])

    def test_activity_model(self):

        def setUp(self):
            clean_db()

        activity_model = model_service.get_activity_model()
        db_populator = DBPopulator(client_data_dao, user_service)
        auth_token = db_populator.populate_one_client_data()
        user_id = user_service.authenticate(auth_token).get_user_id()
        client_data = user_service.get_client_data_by_user_id(user_id)
        initial_model_features = InitialModelFeatures(
            client_data["data"]["impute_dict"],
            {
                "day_of_week": None,
                "device_category": None,
                "browser": None,
                "country": None
            },
            client_data["data"]["discrete_data"]
        )
        initial_model_input = initial_model_features.get_model_input()

        activity_model_features = ActivityModelFeatures(recorded_events=[])
        activity_model_input = activity_model_features.get_model_input()

        model_input = {**initial_model_input, **activity_model_input}
        result = activity_model.predict(model_input)
        self.assertEqual(result, [1])


class ModelTests:

    def __init__(self):
        self.suite = unittest.TestSuite()
        self.suite.addTest(ModelTestCase("test_initial_model"))
        self.suite.addTest(ModelTestCase("test_activity_model"))

    def get_suite(self):
        return self.suite
