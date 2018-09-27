import hashlib
import uuid

from app.domain import User


class UserService:
    def __init__(self, user_dao, client_data_dao, encryption_service):
        self.user_dao = user_dao
        self.client_data_dao = client_data_dao
        self.encryption_service = encryption_service

    def register_new_user(self, name, password):
        if self.user_dao.exists_with_name(name):
            raise ValueError("User " + name + " already exists")
        salt = self.fresh_salt()
        hashed_password = self.hash_password(salt, password)
        user_id = self.user_dao.add(name, salt, hashed_password)
        auth_token = self.encryption_service.encrypt_to_string(user_id)
        self.user_dao.set_auth_token(user_id, auth_token)
        return auth_token

    def refresh_auth_token(self, name, password):
        user_data_dict = self.user_dao.find_one_by_name(name)
        if user_data_dict is None:
            raise ValueError("User " + name + " does not exist")

        salt = user_data_dict["salt"]
        original_hashed_password = user_data_dict["hashed_password"]
        hashed_password = self.hash_password(salt, password)
        if hashed_password != original_hashed_password:
            raise ValueError("Incorrect password")

        user = self.user_from_dict(user_data_dict)
        user_id = user.get_user_id()
        auth_token = self.encryption_service.encrypt_to_string(user_id)
        self.user_dao.set_auth_token(user_id, auth_token)
        return auth_token

    def authenticate(self, auth_token):
        user_id = self.encryption_service.decrypt_to_string(auth_token)
        user_data_dict = self.user_dao.get_by_id(user_id)
        if user_data_dict["auth_token"] != auth_token:
            raise ValueError("Outdated auth token provided")
        return self.user_from_dict(user_data_dict)

    def get_client_data_by_user_id(self, user_id):
        return self.client_data_dao.get_by_user_id(user_id)

    @staticmethod
    def hash_password(salt, password):
        salted_password = password + salt
        return hashlib.sha512(salted_password.encode()).hexdigest()

    @staticmethod
    def fresh_salt():
        return str(uuid.uuid4())

    @staticmethod
    def user_from_dict(user_data_dict):
        return User(user_data_dict["_id"], user_data_dict["name"])
