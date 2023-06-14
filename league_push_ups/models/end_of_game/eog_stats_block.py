from dataclasses import dataclass
from typing import List

from ..lobby.game_mode import GameMode
from .team import Team


@dataclass
class EOGStatsBlock:
    game_ended_in_early_surrender: bool
    game_id: int
    game_length: int
    game_mode: GameMode
    teams: List[Team]

    @classmethod
    def from_json(cls, json):
        return cls(
            json["gameEndedInEarlySurrender"],
            json["gameId"],
            json["gameLength"],
            GameMode(json["gameMode"]),
            [Team.from_json(team) for team in json["teams"]]
        )
