from attrs import define
from typing import Optional

from .player import Player
from .stats import Stats

@define(frozen=True)
class Team:
    teamId: int
    players: list[Player]
    stats: Optional[Stats]
