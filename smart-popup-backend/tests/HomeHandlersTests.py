import os
import unittest

from tornado.testing import AsyncHTTPTestCase

import TestApp
from config import Config
from dao import DaoLibrary
from rest import HandlersLibrary
from service import ServiceLibrary

context_dir = os.path.dirname(__file__)
config = Config(context_dir)
dao_library_for_tests = DaoLibrary(
    config.get_database_host(),
    config.get_database_port(),
    config.get_database_name(),
)
service_library_for_tests = ServiceLibrary(dao_library_for_tests, context_dir, config)
handlers_library_for_tests = HandlersLibrary(service_library_for_tests)


def clean_db():
    dao_library_for_tests.db.command("dropDatabase")


app = TestApp.make_app(handlers_library_for_tests)


class TestHomeHandlersBase(AsyncHTTPTestCase):

    def setUp(self):
        clean_db()
        super(TestHomeHandlersBase, self).setUp()

    def get_app(self):
        return app


class TestHomeHandlers(TestHomeHandlersBase):

    def test_main_handler(self):
        response = self.fetch(
            "/",
            method="GET"
        )

        self.assertEqual(response.code, 200)
        self.assertEqual(response.body.decode(), '{"message": "Welcome to Smart Popup!"}')


class HomeHandlersTests:

    def __init__(self):
        self.suite = unittest.TestSuite()
        self.suite.addTest(TestHomeHandlers("test_main_handler"))

    def get_suite(self):
        return self.suite
