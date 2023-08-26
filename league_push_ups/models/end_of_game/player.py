from attrs import define
from .stats import Stats

@define(frozen=True)
class Player:
    summonerName: str
    teamId: int
    stats: Stats
