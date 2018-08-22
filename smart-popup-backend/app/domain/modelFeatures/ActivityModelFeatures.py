class ActivityModelFeatures:

    def __init__(self, recorded_events):
        self.recorded_events = recorded_events

    def to_dict(self):
        return self.get_model_input()

    def get_model_input(self):
        model_input = {}
        for event in self.recorded_events:
            model_input[event] = [float(1)]
        return model_input
