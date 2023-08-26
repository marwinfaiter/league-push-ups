from attrs import define
from typing import List, Optional

from .player import Player
from .stats import Stats

@define(frozen=True)
class Team:
    teamId: int
    players: List[Player]
    stats: Optional[Stats]
