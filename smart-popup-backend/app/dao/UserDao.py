import uuid


class UserDao:

    def __init__(self, db):
        self.users = db.users

    def all(self):
        return list(self.users.find({}))

    def get_by_id(self, user_id):
        query = {"_id": user_id}
        result = self.users.find_one(query)
        if result is None:
            raise ValueError("User with id " + str(user_id) + " does not exist")
        else:
            return result

    def find_by_id(self, user_id):
        query = {"_id": user_id}
        return self.users.find_one(query)

    def find_one_by_name(self, name):
        query = {"name": name}
        return self.users.find_one(query)

    def exists_with_name(self, name):
        query = {"name": name}
        return self.users.find(query).count() > 0

    def add(self, name, salt, hashed_password):
        user_id = str(uuid.uuid4())
        query = {"_id": user_id, "name": name, "salt": salt, "hashed_password": hashed_password}
        self.users.insert_one(query)
        return user_id

    def remove(self, user_id):
        query = {"_id": user_id}
        self.users.remove(query)

    def set_auth_token(self, user_id, auth_token):
        query_filter = {"_id": user_id}
        query_update = {"$set": {"auth_token": auth_token}}
        self.users.find_one_and_update(query_filter, query_update)

    def get_auth_token(self, user_id):
        query = {"_id": user_id}
        query_result = self.users.find_one(query, projection={"_id": False, "auth_token": True})
        return query_result.get("auth_token")
