from playhouse.shortcuts import model_to_dict
from typing import Any

from . import Controller
from ..models.database.match import Match
from ..models.database.match_player import MatchPlayer

class FrontendMatchesController(Controller):
    def get(self) -> list[dict[str, Any]]:
        matches = Match.select()
        matches_payload = []
        for match in matches:
            match_payload = model_to_dict(match)
            match_payload["date_time"] = str(match_payload["date_time"])
            match_payload["Session"]["date_time"] = str(match_payload["Session"]["date_time"])
            match_payload["players"] = MatchPlayer.get_match_players(match.id)
            if match_payload["players"]:
                matches_payload.append(match_payload)
        return matches_payload
