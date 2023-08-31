from playhouse.shortcuts import model_to_dict

from . import Controller
from ..models.database.match import Match

class FrontendMatchesController(Controller):
    def get(self):
        matches = Match.select()
        matches_payload = []
        for match in matches:
            match_payload = model_to_dict(match)
            match_payload["date_time"] = str(match_payload["date_time"])
            match_payload["Session"]["date_time"] = str(match_payload["Session"]["date_time"])
            match_payload["players"] = [{**model_to_dict(player, recurse=False), "PushUps": player.push_ups} for player in match.players]
            matches_payload.append(match_payload)
        return matches_payload
