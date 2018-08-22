from domain.modelFeatures.ActivityModelFeatures import ActivityModelFeatures
from domain.modelFeatures.InitialModelFeatures import InitialModelFeatures


class DecisionService:

    def __init__(self, model_service, audit_service):
        self.model_service = model_service
        self.audit_service = audit_service
        self.initial_model = self.model_service.get_initial_model()
        self.activity_model = self.model_service.get_activity_model()

    def get_initial_decision(self, user_id, impute_dict, initial_data, discrete_data):
        initial_model_features = InitialModelFeatures(impute_dict, initial_data, discrete_data)
        model_input = initial_model_features.get_model_input()
        result = self.initial_model.predict(model_input)
        self.audit_service.store(user_id, "initial", initial_model_features.to_dict(), result)
        return result[0] == 1

    def get_activity_decision(self, user_id, impute_dict, initial_data, discrete_data, recorded_events):
        initial_model_features = InitialModelFeatures(impute_dict, initial_data, discrete_data)
        initial_model_input = initial_model_features.get_model_input()
        activity_model_features = ActivityModelFeatures(recorded_events)
        activity_model_input = activity_model_features.get_model_input()
        model_input = {**initial_model_input, **activity_model_input}
        result = self.activity_model.predict(model_input)
        self.audit_service.store(
            user_id,
            "activity",
            {**initial_model_features.to_dict(), **activity_model_features.to_dict()},
            result
        )
        return result[0] == 1
