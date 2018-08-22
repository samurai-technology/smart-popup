import hashlib
import unittest
import uuid

from config import Config
from dao import DaoLibrary

config = Config()
dao_library_for_tests = DaoLibrary(
    config.get_database_host(),
    config.get_database_port(),
    config.get_database_name(),
)
user_dao = dao_library_for_tests.user_dao


def clean_db():
    dao_library_for_tests.db.command("dropDatabase")


class TestUserDaoBase(unittest.TestCase):
    def setUp(self):
        clean_db()
        super(TestUserDaoBase, self).setUp()


class TestUserDao(TestUserDaoBase):

    def test_adding_user_by_id(self):
        name = "user name"
        password = "user password"
        salt = str(uuid.uuid4())
        salted_password = password + salt
        hashed_password = hashlib.sha512(salted_password.encode()).hexdigest()
        user_id = user_dao.add(name, salt, hashed_password)
        user_data_dict = user_dao.get_by_id(user_id)
        self.assertEqual(user_data_dict["name"], name)
        self.assertEqual(user_data_dict["salt"], salt)
        self.assertEqual(user_data_dict["hashed_password"], hashed_password)

    def test_adding_user_by_name(self):
        name = "user name"
        password = "user password"
        salt = str(uuid.uuid4())
        salted_password = password + salt
        hashed_password = hashlib.sha512(salted_password.encode()).hexdigest()
        user_id = user_dao.add(name, salt, hashed_password)
        user_data_dict = user_dao.find_one_by_name(name)
        self.assertEqual(user_data_dict["_id"], user_id)
        self.assertEqual(user_data_dict["name"], name)
        self.assertEqual(user_data_dict["salt"], salt)
        self.assertEqual(user_data_dict["hashed_password"], hashed_password)

    def test_removing_user_by_id(self):
        name = "user name"
        password = "user password"
        salt = str(uuid.uuid4())
        salted_password = password + salt
        hashed_password = hashlib.sha512(salted_password.encode()).hexdigest()
        user_id = user_dao.add(name, salt, hashed_password)
        user_dao.remove(user_id)
        user_data_dict = user_dao.find_by_id(user_id)
        self.assertIsNone(user_data_dict)

    def test_setting_and_getting_auth_token(self):
        name = "user name"
        password = "user password"
        salt = str(uuid.uuid4())
        salted_password = password + salt
        hashed_password = hashlib.sha512(salted_password.encode()).hexdigest()
        user_id = user_dao.add(name, salt, hashed_password)
        auth_token = "auth_token"
        user_dao.set_auth_token(user_id, auth_token)
        auth_token_from_db = user_dao.get_auth_token(user_id)
        self.assertEqual(auth_token_from_db, auth_token)


class UserDaoTests:

    def __init__(self):
        self.suite = unittest.TestSuite()
        self.suite.addTest(TestUserDao("test_adding_user_by_id"))
        self.suite.addTest(TestUserDao("test_adding_user_by_name"))
        self.suite.addTest(TestUserDao("test_removing_user_by_id"))
        self.suite.addTest(TestUserDao("test_setting_and_getting_auth_token"))

    def get_suite(self):
        return self.suite
