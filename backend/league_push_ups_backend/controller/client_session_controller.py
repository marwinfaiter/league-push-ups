from flask_login import login_required

from . import Controller
from ..models.database.session import Session

class ClientSessionController(Controller):
    @login_required
    def get(self):
        session = Session.create()
        return session.id
