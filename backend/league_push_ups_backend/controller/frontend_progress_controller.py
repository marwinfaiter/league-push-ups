from peewee import fn
from typing import Any
from flask import request

from . import Controller
from ..models.database.match_player import MatchPlayer
from ..models.database.match import Match
from ..models.database.user import User
from ..models.database.user.summoner import Summoner

class FrontendProgressController(Controller):
    def post(self) -> list[dict[str, Any]]:
        filters = request.get_json()
        assert isinstance(filters, dict)
        user_stats = MatchPlayer.select(
            User.username,
            fn.SUM(MatchPlayer.Kills).alias("Kills"),
            fn.SUM(MatchPlayer.Deaths).alias("Deaths"),
            fn.SUM(MatchPlayer.Assists).alias("Assists"),
            fn.SUM(MatchPlayer.push_ups).alias("PushUps"),
            ).join(
                Match
            ).switch(
                MatchPlayer
            ).join(
                Summoner, on=(Summoner.name == MatchPlayer.SummonerName,)
            ).join(
                User
            ).group_by(
                User.username
            )
        payloads = []
        for user_stat in user_stats:
            payload = {
                "Username": user_stat.summoner.user.username,
                "Kills": int(user_stat.Kills),
                "Deaths": int(user_stat.Deaths),
                "Assists": int(user_stat.Assists),
                "PushUps": int(user_stat.PushUps),
            }
            payloads.append(payload)
        return payloads
