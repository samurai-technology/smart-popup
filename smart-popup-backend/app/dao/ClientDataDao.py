import uuid


class ClientDataDao:
    def __init__(self, db):
        self.client_data = db.clientData

    def add_for_user(self, user_id, client_data):
        query = {
            "_id": str(uuid.uuid4()),
            "user_id": user_id,
            "data": client_data.data
        }
        self.client_data.insert_one(query)

    def get_by_user_id(self, user_id):
        query = {"user_id": user_id}
        return self.client_data.find_one(query)
