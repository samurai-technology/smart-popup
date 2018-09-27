from app.service.AuditService import AuditService
from app.service.DecisionService import DecisionService
from app.service.EncryptionService import EncryptionService
from app.service.FileService import FileService
from app.service.ModelService import ModelService
from app.service.TransformerService import TransformerService
from app.service.UserService import UserService


class ServiceLibrary:
    def __init__(self, dao_library, context_dir, config):
        self.file_service = FileService(context_dir, config)
        self.model_service = ModelService(self.file_service)
        self.audit_service = AuditService(dao_library.audit_dao)
        self.transformer_service = TransformerService()
        self.encryption_service = EncryptionService(self.file_service)
        self.user_service = UserService(dao_library.user_dao, dao_library.client_data_dao, self.encryption_service)
        self.decision_service = DecisionService(
            self.model_service,
            self.audit_service,
            self.user_service,
            self.transformer_service,
        )
