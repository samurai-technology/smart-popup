class ModelsRegistry:
    
    def __init__(self):
        self.models = {}
        
    def set_model(self, model_id, model):
        self.models[str(model_id)] = model

    def get_model(self, model_id):
        return self.models.get(str(model_id))
