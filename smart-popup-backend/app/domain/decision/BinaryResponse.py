class BinaryResponse:
    def __init__(self, should_show_popup):
        self.should_show_popup = should_show_popup

    def to_dict(self):
        return {"should_show_popup": str(self.should_show_popup).lower()}
