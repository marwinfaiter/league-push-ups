from flask import request
from peewee import DoesNotExist
from flask_login import login_required

from . import Controller
from ..models.database.match import Match
from ..models.database.match_player import MatchPlayer
from ..models.database.user.summoner import Summoner
from ..models.database.base_model import database

class ClientScoresController(Controller):
    @login_required
    def post(self, session_id: str, match_id: int) -> None:
        scores = request.get_json()
        assert isinstance(scores, list)
        with database.atomic() as _:
            match, _ = Match.get_or_create(
                Session=session_id,
                MatchID=match_id,
            )
            match.TeamKills = sum(score["kills"] for score in scores)
            for score in scores:
                try:
                    summoner = Summoner.get(name=score["summonerName"])
                    match_player, _ = MatchPlayer.get_or_create(
                        Match=match.id,
                        User=summoner.user.id,
                        SummonerName=score["summonerName"],
                        MinPushUps=summoner.user.minimum_push_ups,
                        MaxPushUps=summoner.user.maximum_push_ups,
                        PushUpsFinished=summoner.user.active,
                    )
                    match_player.Kills = score["kills"]
                    match_player.Deaths = score["deaths"]
                    match_player.Assists = score["assists"]
                    match_player.save()
                except DoesNotExist:
                    pass
            match.save()
