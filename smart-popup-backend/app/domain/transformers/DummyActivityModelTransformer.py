from domain import InitialModelFeatures, ActivityModelFeatures


class DummyActivityModelTransformer:

    @staticmethod
    def get_model_input(client_data, body):
        initial_model_features = DummyActivityModelTransformer.__create_initial_model_features(client_data, body)
        activity_model_features = DummyActivityModelTransformer.__create_activity_model_features(body)
        return {
            **initial_model_features.get_model_input(),
            **activity_model_features.get_model_input()
        }

    @staticmethod
    def get_audit_store_record_input(client_data, body):
        initial_model_features = DummyActivityModelTransformer.__create_initial_model_features(client_data, body)
        activity_model_features = DummyActivityModelTransformer.__create_activity_model_features(body)
        return {
            **initial_model_features.to_dict(),
            **activity_model_features.to_dict()
        }

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

    @staticmethod
    def __create_activity_model_features(body):
        recorded_events = body["recorded_events"]
        return ActivityModelFeatures(recorded_events)
