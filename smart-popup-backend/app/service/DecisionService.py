from domain.modelFeatures.ActivityModelFeatures import ActivityModelFeatures
from domain.modelFeatures.InitialModelFeatures import InitialModelFeatures


class DecisionService:

    def __init__(self, model_service, audit_service, transformer_service):
        self.model_service = model_service
        self.audit_service = audit_service
        self.transformer_service = transformer_service
        self.initial_model = self.model_service.get_initial_model()
        self.activity_model = self.model_service.get_activity_model()

    def get_initial_decision(self, user_id, impute_dict, initial_data, discrete_data):
        transformer = self.transformer_service.get_transformer("INITIAL_DUMMY")
        model_input = transformer.get_model_input(impute_dict, initial_data, discrete_data)
        result = self.initial_model.predict(model_input)
        self.audit_service.store(user_id,
                                 "initial",
                                 InitialModelFeatures(impute_dict, initial_data, discrete_data).to_dict(),
                                 result)
        return result[0] == 1

    def get_activity_decision(self, user_id, impute_dict, initial_data, discrete_data, recorded_events):
        transformer = self.transformer_service.get_transformer("ACTIVITY_DUMMY")
        model_input = transformer.get_model_input(impute_dict, initial_data, discrete_data, recorded_events)
        result = self.activity_model.predict(model_input)
        self.audit_service.store(
            user_id,
            "activity",
            {
                **InitialModelFeatures(impute_dict, initial_data, discrete_data).to_dict(),
                **ActivityModelFeatures(recorded_events).to_dict()
            },
            result
        )
        return result[0] == 1
