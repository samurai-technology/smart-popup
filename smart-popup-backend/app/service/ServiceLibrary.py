from service.AuditService import AuditService
from service.DecisionService import DecisionService
from service.EncryptionService import EncryptionService
from service.FileService import FileService
from service.ModelService import ModelService
from service.TransformerService import TransformerService
from service.UserService import UserService


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
