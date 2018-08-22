class Token:
    def __init__(self, token):
        self.token = token

    def to_dict(self):
        return {"auth_token": str(self.token)}
