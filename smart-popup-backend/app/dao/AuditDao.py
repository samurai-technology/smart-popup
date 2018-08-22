import uuid


class AuditDao:

    def __init__(self, db):
        self.audit = db.audit

    def store(self, user_id, model_name, model_input, model_output, timestamp):
        audit_entry_id = str(uuid.uuid4())
        query = {
            "_id": audit_entry_id,
            "user_id": user_id,
            "model_name": model_name,
            "model_input": model_input,
            "model_output": model_output,
            "timestamp": timestamp,
        }
        self.audit.insert_one(query)
        return audit_entry_id
