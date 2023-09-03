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
            match_payload["players"] = list(
                MatchPlayer.select(
                MatchPlayer,
                MatchPlayer.kda.cast("float").alias("kda"), # type: ignore[attr-defined] # pylint: disable=no-member
                MatchPlayer.kill_participation.cast("float").alias("kill_participation"), # type: ignore[attr-defined] # pylint: disable=no-member
                MatchPlayer.push_ups.cast("int").alias("push_ups") # type: ignore[attr-defined] # pylint: disable=no-member
                ).join(
                    Match
                ).where(
                    MatchPlayer.Match==match.id
                ).dicts()
            )
            if match_payload["players"]:
                matches_payload.append(match_payload)
        return matches_payload
