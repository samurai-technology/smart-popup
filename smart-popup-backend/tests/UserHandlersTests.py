import json
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
user_service = service_library_for_tests.user_service
handlers_library_for_tests = HandlersLibrary(service_library_for_tests)


def clean_db():
    dao_library_for_tests.db.command("dropDatabase")


app = TestApp.make_app(handlers_library_for_tests)


class TestUsersHandlersBase(AsyncHTTPTestCase):

    def setUp(self):
        clean_db()
        super(TestUsersHandlersBase, self).setUp()

    def get_app(self):
        return app


class TestUserHandlers(TestUsersHandlersBase):

    def test_register_correct_handler(self):
        post_args = {
            "name": "name",
            "password": "password"
        }
        response = self.fetch(
            "/user/register",
            method="POST",
            body=json.dumps(post_args)
        )
        self.assertEqual(response.code, 201)
        self.assertIsNotNone(response.body.decode())

    def test_register_incorrect_handler(self):
        post_args = {
            "name": "name",
        }
        response = self.fetch(
            "/user/register",
            method="POST",
            body=json.dumps(post_args)
        )
        self.assertEqual(response.code, 422)

    def test_register_existing_handler(self):
        name = "name"
        password = "password"
        service_library_for_tests.user_service.register_new_user(name, password)
        post_args = {
            "name": name,
            "password": password
        }
        response = self.fetch(
            "/user/register",
            method="POST",
            body=json.dumps(post_args)
        )
        self.assertEqual(response.code, 409)

    def test_refresh_auth_token_correct_handler(self):
        name = "name"
        password = "password"
        user_service.register_new_user(name, password)
        post_args = {
            "name": name,
            "password": password
        }
        response = self.fetch(
            "/user/refresh-token",
            method="POST",
            body=json.dumps(post_args)
        )
        self.assertEqual(response.code, 200)
        response_dict = json.loads(response.body.decode())
        auth_token = response_dict["auth_token"]
        user = user_service.authenticate(auth_token)
        self.assertEqual(user.get_name(), name)

    def test_refresh_auth_token_incorrect_handler(self):
        post_args = {
            "name": "name",
        }
        response = self.fetch(
            "/user/refresh-token",
            method="POST",
            body=json.dumps(post_args)
        )
        self.assertEqual(response.code, 422)

    def test_refresh_auth_token_non_existing_handler(self):
        post_args = {
            "name": "name",
            "password": "password"
        }
        response = self.fetch(
            "/user/refresh-token",
            method="POST",
            body=json.dumps(post_args)
        )
        self.assertEqual(response.code, 500)


class UserHandlersTests:

    def __init__(self):
        self.suite = unittest.TestSuite()
        self.suite.addTest(TestUserHandlers("test_register_correct_handler"))
        self.suite.addTest(TestUserHandlers("test_register_incorrect_handler"))
        self.suite.addTest(TestUserHandlers("test_register_existing_handler"))
        self.suite.addTest(TestUserHandlers("test_refresh_auth_token_correct_handler"))
        self.suite.addTest(TestUserHandlers("test_refresh_auth_token_incorrect_handler"))
        self.suite.addTest(TestUserHandlers("test_refresh_auth_token_non_existing_handler"))

    def get_suite(self):
        return self.suite
