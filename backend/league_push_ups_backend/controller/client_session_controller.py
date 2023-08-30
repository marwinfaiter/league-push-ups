from . import Controller
from ..models.database.session import Session

class ClientSessionController(Controller):
    def get(self):
        session = Session.create()
        return session.id
