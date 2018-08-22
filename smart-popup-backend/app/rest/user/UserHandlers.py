import json

import tornado.web

from domain import Token
from domain import Error


class UserHandlers:
    def __init__(self, user_service):
        self.services = dict(
            user_service=user_service
        )
        self.handlers = [
            (r"/user/register", RegisterNewUserHandler, self.services),
            (r"/user/refresh-token", RefreshUserTokenHandler, self.services)
        ]


class RegisterNewUserHandler(tornado.web.RequestHandler):

    def initialize(self, user_service):
        self.user_service = user_service

    def post(self):
        body = json.loads(self.request.body)
        name = body.get("name")
        password = body.get("password")
        if name is None or password is None:
            self.write(Error("Name or password missing").to_dict())
            self.set_status(422)
            return
        try:
            auth_token = self.user_service.register_new_user(name, password)
            self.write(Token(auth_token).to_dict())
            self.set_status(201)
        except ValueError:
            self.write(Error("User already exists").to_dict())
            self.set_status(409)


class RefreshUserTokenHandler(tornado.web.RequestHandler):

    def initialize(self, user_service):
        self.user_service = user_service

    def post(self):
        body = json.loads(self.request.body)
        name = body.get("name")
        password = body.get("password")
        if name is None or password is None:
            self.write(Error("Name or password missing").to_dict())
            self.set_status(422)
            return
        try:
            auth_token = self.user_service.refresh_auth_token(name, password)
            self.write(Token(auth_token).to_dict())
            self.set_status(200)
        except ValueError:
            self.write(Error("Incorrect name or password").to_dict())
            self.set_status(500)
