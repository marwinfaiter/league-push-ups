from flask_login import logout_user

from . import Controller

class LogoutController(Controller):
    def post(self) -> None:
        logout_user()
