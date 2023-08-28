from attrs import define
from typing import List

from ..lobby.game_mode import GameMode
from .team import Team


@define
class EOGStatsBlock:
    gameEndedInEarlySurrender: bool
    gameId: int
    gameLength: int
    gameMode: GameMode
    teams: List[Team]
