from domain import InitialModelFeatures


class DummyInitialModelTransformer:

    def get_model_input(self, impute_dict, initial_data, discrete_data):
        initial_model_features = InitialModelFeatures(impute_dict, initial_data, discrete_data)
        return initial_model_features.get_model_input()
