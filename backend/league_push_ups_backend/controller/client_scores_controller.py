from flask import request
from peewee import DoesNotExist
from flask_login import login_required

from . import Controller
from ..models.database.match import Match
from ..models.database.match_player import MatchPlayer
from ..models.database.base_model import database

class ClientScoresController(Controller):
    @login_required
    def post(self, session_id: str, match_id: int):
        scores = request.get_json()
        with database.atomic() as txn:
            match, _ = Match.get_or_create(
                Session=session_id,
                MatchID=match_id,
            )
            match.TeamKills = sum(score["kills"] for score in scores)
            for score in scores:
                try:
                    match_player = MatchPlayer.get(Match=match.id, SummonerName=score["summonerName"])
                    match_player.Kills = score["kills"]
                    match_player.Deaths = score["deaths"]
                    match_player.Assists = score["assists"]
                    match_player.save()
                except DoesNotExist:
                    pass
            match.save()
