class PredictorsRegistry:

    def __init__(self):
        self.predictors = {}

    def set_predictor(self, predictor_id, predictor):
        self.predictors[str(predictor_id)] = predictor

    def get_predictor(self, predictor_id):
        return self.predictors.get(str(predictor_id))
