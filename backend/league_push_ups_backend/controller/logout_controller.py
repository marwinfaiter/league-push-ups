from flask import session

from . import Controller

class LogoutController(Controller):
    def post(self):
        session["name"] = None
