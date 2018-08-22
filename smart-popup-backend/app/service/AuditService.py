import time

class AuditService:

    def __init__(self, audit_dao):
        self.audit_dao = audit_dao

    def store(self, user_id, model_name, model_input, model_output):
        timestamp = time.time()
        self.audit_dao.store(user_id, model_name, str(model_input), str(model_output), str(timestamp))
