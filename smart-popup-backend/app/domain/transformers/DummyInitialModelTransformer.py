from domain import InitialModelFeatures


class DummyInitialModelTransformer:

    @staticmethod
    def get_model_input(client_data, body):
        initial_model_features = DummyInitialModelTransformer.__create_initial_model_features(client_data, body)
        return initial_model_features.get_model_input()

    @staticmethod
    def get_audit_store_record_input(client_data, body):
        initial_model_features = DummyInitialModelTransformer.__create_initial_model_features(client_data, body)
        return initial_model_features.to_dict()

    @staticmethod
    def __create_initial_model_features(client_data, body):
        initial_data = {}
        required_initial_data_keys = client_data["data"]["initial_data"]
        for key in required_initial_data_keys:
            initial_data[key] = body.get(key)

        return InitialModelFeatures(
            client_data["data"]["impute_dict"],
            initial_data,
            client_data["data"]["discrete_data"]
        )
