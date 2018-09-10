class DecisionService:

    def __init__(self, model_service, audit_service, user_service, transformer_service):
        self.model_service = model_service
        self.audit_service = audit_service
        self.user_service = user_service
        self.transformer_service = transformer_service
        self.initial_model = self.model_service.get_initial_model()
        self.activity_model = self.model_service.get_activity_model()

    def get_initial_decision(self, user_id, body):
        return self.__get_decision(user_id, body, "INITIAL_DUMMY")

    def get_activity_decision(self, user_id, body):
        return self.__get_decision(user_id, body, "ACTIVITY_DUMMY")

    def __get_decision(self, user_id, body, transformer_id):
        transformer = self.transformer_service.get_transformer(transformer_id)
        client_data = self.user_service.get_client_data_by_user_id(user_id)
        model_input = transformer.get_model_input(client_data, body)
        result = self.activity_model.predict(model_input)
        audit_store_record_input = transformer.get_audit_store_record_input(client_data, body)
        self.audit_service.store(user_id,
                                 transformer_id,
                                 audit_store_record_input,
                                 result)
        return result[0] == 1
