from domain import InitialModelFeatures, ActivityModelFeatures


class DummyActivityModelTransformer:

    def get_model_input(self, impute_dict, initial_data, discrete_data, recorded_events):
        initial_model_features = InitialModelFeatures(impute_dict, initial_data, discrete_data)
        initial_model_input = initial_model_features.get_model_input()
        activity_model_features = ActivityModelFeatures(recorded_events)
        activity_model_input = activity_model_features.get_model_input()
        return {**initial_model_input, **activity_model_input}
