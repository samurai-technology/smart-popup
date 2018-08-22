from app.rest.home import HomeHandlers
from app.rest.decision import DecisionHandlers
from app.rest.user import UserHandlers


class HandlersLibrary:
    def __init__(self, service_library):
        self.home_handlers = HomeHandlers()
        self.decision_handlers = DecisionHandlers(service_library.decision_service, service_library.user_service)
        self.user_handlers = UserHandlers(service_library.user_service)
