from attrs import define

from .member import Member
from .game_config import GameConfig

@define
class Lobby:
    members: list[Member]
    gameConfig: GameConfig

    def is_summoner_member(self, summoner_name: str) -> bool:
        return summoner_name in [member.summonerName for member in self.members]
