from typing import Any
from flask import request

from . import Controller
from ..models.database.match_player import MatchPlayer
from ..models.database.match import Match
from ..models.database.user import User
from ..models.database.user.summoner import Summoner
from ..models.database.session import Session

class FrontendProgressController(Controller):
    def post(self) -> list[dict[str, Any]]:
        filters = request.get_json()
        assert isinstance(filters, dict)
        matches = MatchPlayer.select(
            User.username,
            Session.id.alias("SessionID"),
            Session.date_time.cast("char").alias("SessionDateTime"),
            Match.date_time.cast("char").alias("MatchDateTime"),
            Match.MatchID,
            MatchPlayer.Kills.alias("Kills"),
            MatchPlayer.Deaths.alias("Deaths"),
            MatchPlayer.Assists.alias("Assists"),
            MatchPlayer.kda.cast("float").alias("KDA"),
            MatchPlayer.kill_participation.cast("float").alias("KillParticipation"),
            MatchPlayer.push_ups.cast("int").alias("PushUps"),
            ).join(
                Match
            ).join(
                Session
            ).switch(
                MatchPlayer
            ).join(
                Summoner, on=(Summoner.name == MatchPlayer.SummonerName,)
            ).join(
                User
            ).dicts()
        return {
            match["username"]: [nested_match for nested_match in matches if nested_match["username"] == match["username"]]
            for match in matches
        }
