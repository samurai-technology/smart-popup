class DecisionService:

    def __init__(self, audit_service, user_service, model_registry, predictors_registry):
        self.audit_service = audit_service
        self.user_service = user_service
        self.model_registry = model_registry
        self.predictors_registry = predictors_registry

    def get_initial_decision(self, user_id, body):
        # TODO - generalize
        predictor = self.predictors_registry.get_predictor("predictor_initial")
        return self.__get_decision(user_id, body, predictor, self.model_registry)

    def get_activity_decision(self, user_id, body):
        # TODO - generalize
        predictor = self.predictors_registry.get_predictor("predictor_activity")
        return self.__get_decision(user_id, body, predictor, self.model_registry)

    def __get_decision(self, user_id, body, predictor, models_registry):
        client_data = self.user_service.get_client_data_by_user_id(user_id)
        result = predictor.predict(client_data, body, models_registry)
        self.audit_service.store(user_id, predictor.__class__.__name__, body, result)
        return result[0] == 1
