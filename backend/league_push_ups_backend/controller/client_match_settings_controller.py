from flask import request
from flask_login import login_required

from . import Controller
from ..models.database.match import Match
from ..models.database.match_player import MatchPlayer
from ..models.database.base_model import database

class ClientMatchSettingsController(Controller):
    @login_required
    def post(self, session_id: str, match_id: int) -> None:
        data = request.get_json()
        assert isinstance(data, dict)
        with database.atomic() as _:
            match, _ = Match.get_or_create(
                Session=session_id,
                MatchID=match_id,
                MinPushUps=data["min_push_ups"],
                MaxPushUps=data["max_push_ups"],
            )
            for player in data["lobby"]["members"]:
                MatchPlayer.get_or_create(Match=match.id, SummonerName=player["summonerName"])
