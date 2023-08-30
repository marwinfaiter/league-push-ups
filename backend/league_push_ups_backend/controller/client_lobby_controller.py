from flask import request

from . import Controller
from ..models.database.match import Match
from ..models.database.match_player import MatchPlayer
from ..models.database.base_model import database

class ClientLobbyController(Controller):
    def post(self, session_id: str, match_id: int):
        lobby = request.get_json()
        with database.atomic() as txn:
            match, _ = Match.get_or_create(
                Session=session_id,
                MatchID=match_id,
            )
            for player in lobby["members"]:
                MatchPlayer.get_or_create(Match=match.id, SummonerName=player["summonerName"])
