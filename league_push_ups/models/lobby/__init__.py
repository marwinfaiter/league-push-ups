from dataclasses import dataclass
from typing import List

from league_push_ups.models.lobby.member import Member
from league_push_ups.models.lobby.game_config import GameConfig
from league_push_ups.models.lobby.game_mode import GameMode

@dataclass(slots=True)
class Lobby:
    members: List[Member]
    game_config: GameConfig

    def is_summoner_member(self, summoner_name) -> bool:
        return summoner_name in [member.summoner_name for member in self.members]

    @classmethod
    def from_json(cls, json):
        lobby = cls(
            members=[Member.from_json(member) for member in json["members"]],
            game_config=GameConfig.from_json(json["gameConfig"])
        )
        if lobby.game_config.game_mode == GameMode.TFT:
            print("Skipping game mode TFT")
            return None

        return lobby
