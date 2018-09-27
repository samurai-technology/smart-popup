import pymongo

from app.dao.UserDao import UserDao
from app.dao.AuditDao import AuditDao
from app.dao.ClientDataDao import ClientDataDao


class DaoLibrary:
    def __init__(self, db_host, db_port, db_name):
        client = pymongo.MongoClient(db_host, db_port)
        self.db = client[db_name]
        self.user_dao = UserDao(self.db)
        self.audit_dao = AuditDao(self.db)
        self.client_data_dao = ClientDataDao(self.db)
