class TransformerService:

    def __init__(self):
        self.transformers = {}

    def set_transformer(self, transformer_id, transformer):
        self.transformers[str(transformer_id)] = transformer

    def get_transformer(self, transformer_id):
        return self.transformers.get(str(transformer_id))
