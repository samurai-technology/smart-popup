import tornado.web

class AuthenticatedHandlerBase(tornado.web.RequestHandler):

    def initialize(self, user_service):
        self.user_service = user_service

    def authenticate(self, request):
        auth_token = request.headers.get("Authorization")
        if auth_token is None:
            return
        try:
            self.current_user = self.user_service.authenticate(auth_token)
        except ValueError:
            return

    def no_access(self):
        self.set_status(401)
        self.finish()
