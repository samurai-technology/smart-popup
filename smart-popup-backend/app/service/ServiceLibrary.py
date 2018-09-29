from app.service.AuditService import AuditService
from app.service.DecisionService import DecisionService
from app.service.EncryptionService import EncryptionService
from app.service.FileService import FileService
from app.service.ModelsRegistry import ModelsRegistry
from app.service.PredictorsRegistry import PredictorsRegistry
from app.service.UserService import UserService


class ServiceLibrary:
    def __init__(self, dao_library, context_dir, config):
        self.file_service = FileService(context_dir, config)
        self.audit_service = AuditService(dao_library.audit_dao)
        self.encryption_service = EncryptionService(self.file_service)
        self.user_service = UserService(dao_library.user_dao, dao_library.client_data_dao, self.encryption_service)
        self.models_registry = ModelsRegistry()
        self.predictors_registry = PredictorsRegistry()
        self.decision_service = DecisionService(
            self.audit_service,
            self.user_service,
            self.models_registry,
            self.predictors_registry
        )
