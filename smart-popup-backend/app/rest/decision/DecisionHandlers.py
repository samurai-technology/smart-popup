import json

from domain import BinaryResponse
from rest.authentication import AuthenticatedHandlerBase


class DecisionHandlers:
    def __init__(self, decision_service, user_service):
        self.services = dict(
            decision_service=decision_service,
            user_service=user_service
        )
        self.handlers = [
            (r"/decision/initial", RequestInitialDecisionHandler, self.services),
            (r"/decision/activity", RequestActivityDecisionHandler, self.services)
        ]


class RequestInitialDecisionHandler(AuthenticatedHandlerBase):

    def initialize(self, decision_service, user_service):
        super(RequestInitialDecisionHandler, self).initialize(user_service)
        self.decision_service = decision_service

    def post(self):
        super(RequestInitialDecisionHandler, self).authenticate(self.request)
        if self.current_user is None:
            self.no_access()
            return

        user_id = self.current_user.get_user_id()
        body = json.loads(self.request.body)
        decision = self.decision_service.get_initial_decision(user_id, body)
        self.write(BinaryResponse(decision).to_dict())
        self.set_status(200)


class RequestActivityDecisionHandler(AuthenticatedHandlerBase):

    def initialize(self, decision_service, user_service):
        super(RequestActivityDecisionHandler, self).initialize(user_service)
        self.decision_service = decision_service

    def post(self):
        super(RequestActivityDecisionHandler, self).authenticate(self.request)
        if self.current_user is None:
            self.no_access()
            return

        user_id = self.current_user.get_user_id()
        body = json.loads(self.request.body)
        decision = self.decision_service.get_activity_decision(user_id, body)
        self.write(BinaryResponse(decision).to_dict())
        self.set_status(200)
