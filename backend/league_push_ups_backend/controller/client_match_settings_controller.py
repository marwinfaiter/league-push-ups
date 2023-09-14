from flask_login import login_required

from . import Controller
from ..models.database.match import Match

class ClientMatchSettingsController(Controller):
    @login_required
    def post(self, session_id: str, match_id: int) -> None:
        Match.get_or_create(
            Session=session_id,
            MatchID=match_id,
        )
