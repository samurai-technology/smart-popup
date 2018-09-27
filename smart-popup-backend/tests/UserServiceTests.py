import os
import unittest

from config import Config
from dao import DaoLibrary
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


def clean_db():
    dao_library_for_tests.db.command("dropDatabase")


class TestUserServiceBase(unittest.TestCase):
    def setUp(self):
        clean_db()
        super(TestUserServiceBase, self).setUp()


class TestUserService(TestUserServiceBase):

    def test_register_new_user(self):
        name = "user name"
        password = "password"
        auth_token = user_service.register_new_user(name, password)
        self.assertIsNotNone(auth_token)

    def test_register_existing_user(self):
        name = "user name"
        password = "password"
        user_service.register_new_user(name, password)
        other_password = "other password"
        self.assertRaises(ValueError, user_service.register_new_user, name, other_password)

    def test_authenticate_existing_user(self):
        name = "user name"
        password = "password"
        auth_token = user_service.register_new_user(name, password)
        user = user_service.authenticate(auth_token)
        self.assertEqual(user.get_name(), name)

    def test_authenticate_existing_user_with_outdated_auth_token(self):
        name = "user name"
        password = "password"
        old_auth_token = user_service.register_new_user(name, password)
        new_auth_token = user_service.refresh_auth_token(name, password)
        self.assertRaises(ValueError, user_service.authenticate, old_auth_token)

    def test_get_auth_token_after_register(self):
        name = "user name"
        password = "password"
        user_service.register_new_user(name, password)
        recovered_auth_token = user_service.refresh_auth_token(name, password)
        user = user_service.authenticate(recovered_auth_token)
        self.assertEqual(user.get_name(), name)

    def test_get_auth_token_after_register_wrong_password(self):
        name = "user name"
        password = "password"
        user_service.register_new_user(name, password)
        wrong_password = "wrong password"
        self.assertRaises(ValueError, user_service.refresh_auth_token, name, wrong_password)


class UserServiceTests:

    def __init__(self):
        self.suite = unittest.TestSuite()
        self.suite.addTest(TestUserService("test_register_new_user"))
        self.suite.addTest(TestUserService("test_register_existing_user"))
        self.suite.addTest(TestUserService("test_authenticate_existing_user"))
        self.suite.addTest(TestUserService("test_authenticate_existing_user_with_outdated_auth_token"))
        self.suite.addTest(TestUserService("test_get_auth_token_after_register"))
        self.suite.addTest(TestUserService("test_get_auth_token_after_register_wrong_password"))

    def get_suite(self):
        return self.suite
