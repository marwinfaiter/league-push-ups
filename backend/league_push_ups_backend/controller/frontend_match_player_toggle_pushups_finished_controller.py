from flask import session
from flask_login import login_required

from . import Controller
from ..models.database.match_player import MatchPlayer

class FrontendMatchPlayerTogglePushupsFinishedController(Controller):
    @login_required
    def post(self, player_id: int) -> tuple[str, int]:
        match_player = MatchPlayer.get(player_id)
        if any([
            all([
                match_player.SummonerName in session["summoners"],
                match_player.PushUpsFinished is True,
            ]),
            "leaguepushups-admins" in session["groups"],
        ]):
            match_player.PushUpsFinished ^= True
            match_player.save()
            return "", 200

        return "You are not allowed to edit this match player", 401
