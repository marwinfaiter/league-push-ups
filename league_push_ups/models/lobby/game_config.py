from dataclasses import dataclass
from .game_mode import GameMode

@dataclass(frozen=True, slots=True)
class GameConfig:
    game_mode: GameMode
    is_custom: bool

    @classmethod
    def from_json(cls, json):
        return cls(
            GameMode(json["gameMode"]),
            json["isCustom"]
        )
