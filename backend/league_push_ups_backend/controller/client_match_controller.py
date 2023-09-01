from flask import request
from flask_login import login_required

from . import Controller
from ..models.database.match import Match
from ..models.database.match_player import MatchPlayer

class ClientMatchController(Controller):
    @login_required
    def post(self, session_id: str, match_id: int):
        match_data = request.get_json()
        match, _ = Match.get_or_create(
            Session=session_id,
            MatchID=match_id,
        )
        match.TeamKills = match_data["team_kills"]
        match.save()
        for player in match_data["players"]:
            match_player = MatchPlayer.get(
                Match=match.id,
                SummonerName=player["summonerName"],
            )
            match_player.Kills = player["stats"]["CHAMPIONS_KILLED"]
            match_player.Deaths = player["stats"]["NUM_DEATHS"]
            match_player.Assists = player["stats"]["ASSISTS"]
            match_player.save()
