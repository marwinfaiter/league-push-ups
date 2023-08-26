from attrs import define
from typing import List

from .player import Player
from .stats import Stats

@define(frozen=True)
class Team:
    teamId: int
    players: List[Player]
    stats: Stats
