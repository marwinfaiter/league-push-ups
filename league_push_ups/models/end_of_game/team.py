from dataclasses import dataclass
from typing import List, Optional

from .player import Player
from .stats import Stats

@dataclass(frozen=True, slots=True)
class Team:
    id: int
    players: List[Player]
    stats: Optional[Stats]

    @classmethod
    def from_json(cls, json):
        return cls(
            json["teamId"],
            [Player.from_json(player) for player in json["players"]],
            Stats.from_json(
                json.get("stats")
            )
        )
