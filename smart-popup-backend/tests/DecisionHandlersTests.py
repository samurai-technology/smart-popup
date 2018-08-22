import json
import os
import unittest

from tornado.testing import AsyncHTTPTestCase

from app import App
from config import Config
from dao import DaoLibrary
from dbPopulator import DBPopulator
from rest import HandlersLibrary
from service import ServiceLibrary

config = Config()
dao_library_for_tests = DaoLibrary(
    config.get_database_host(),
    config.get_database_port(),
    config.get_database_name(),
)
client_data_dao = dao_library_for_tests.client_data_dao
service_library_for_tests = ServiceLibrary(dao_library_for_tests, os.path.dirname(__file__), config)
user_service = service_library_for_tests.user_service
handlers_library_for_tests = HandlersLibrary(service_library_for_tests)


def clean_db():
    dao_library_for_tests.db.command("dropDatabase")


app = App.make_app(handlers_library_for_tests)


class TestDecisionHandlersBase(AsyncHTTPTestCase):

    def setUp(self):
        clean_db()
        super(TestDecisionHandlersBase, self).setUp()

    def get_app(self):
        return app


class TestDecisionHandlers(TestDecisionHandlersBase):

    def test_initial_decision_not_authenticated_handler(self):
        post_args = {}
        response = self.fetch(
            "/decision/initial",
            method="POST",
            body=json.dumps(post_args)
        )
        self.assertEqual(response.code, 401)

    def test_initial_decision_authenticated_handler(self):
        db_populator = DBPopulator(client_data_dao, user_service)
        auth_token = db_populator.populate_one_client_data()
        post_args = {
            "day_of_week": 1.0,
            "device_category": "tablet",
            "browser": "Chrome",
            "country": "Poland"
        }
        response = self.fetch(
            "/decision/initial",
            method="POST",
            body=json.dumps(post_args),
            headers={
                "Authorization": auth_token
            }
        )
        self.assertEqual(response.code, 200)

    def test_activity_decision_not_authenticated_handler(self):
        post_args = {}
        response = self.fetch(
            "/decision/activity",
            method="POST",
            body=json.dumps(post_args)
        )
        self.assertEqual(response.code, 401)

    def test_activity_decision_authenticated_handler(self):
        db_populator = DBPopulator(client_data_dao, user_service)
        auth_token = db_populator.populate_one_client_data()
        post_args = {
            "day_of_week": 1.0,
            "device_category": "tablet",
            "browser": "Chrome",
            "total_events": 10.0,
            "country": "Poland",
            "recorded_events": ["EVENT_0", "EVENT_11", "EVENT_2", "EVENT_3", "EVENT_4", "EVENT_5", "EVENT_6", "EVENT_7",
                                "EVENT_8", "EVENT_9"]
        }
        response = self.fetch(
            "/decision/activity",
            method="POST",
            body=json.dumps(post_args),
            headers={
                "Authorization": auth_token
            }
        )
        self.assertEqual(response.code, 200)


class DecisionHandlersTests:

    def __init__(self):
        self.suite = unittest.TestSuite()
        self.suite.addTest(TestDecisionHandlers("test_initial_decision_not_authenticated_handler"))
        self.suite.addTest(TestDecisionHandlers("test_initial_decision_authenticated_handler"))
        self.suite.addTest(TestDecisionHandlers("test_activity_decision_not_authenticated_handler"))
        self.suite.addTest(TestDecisionHandlers("test_activity_decision_authenticated_handler"))

    def get_suite(self):
        return self.suite
