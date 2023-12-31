from flask import request
from flask_login import login_required

from . import Controller
from ..models.database.match import Match
from ..models.database.match_player import MatchPlayer

class ClientMatchController(Controller):
    @login_required
    def post(self, session_id: str, match_id: int) -> None:
        match_data = request.get_json()
        assert isinstance(match_data, dict)

        match, _ = Match.get_or_create(
            Session=session_id,
            MatchID=match_id,
        )
        match.TeamKills = match_data["team_kills"]
        match.save()
        for player in match_data["players"]:
            if match_player := MatchPlayer.get_or_none(Match=match.id, SummonerName=player["summonerName"]):
                match_player.Kills = player["stats"]["CHAMPIONS_KILLED"]
                match_player.Deaths = player["stats"]["NUM_DEATHS"]
                match_player.Assists = player["stats"]["ASSISTS"]
                match_player.save()
