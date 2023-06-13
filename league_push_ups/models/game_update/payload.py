from dataclasses import dataclass
from typing import Optional

from league_push_ups.models.game_update.game_state import GameState
from league_push_ups.models.game_update.game_type import GameType

@dataclass(frozen=True, slots=True)
class Payload:
    id: int
    game_state: GameState
    game_type: Optional[GameType]

    @classmethod
    def from_json(cls, json):
        return cls(
            json["id"],
            GameState(json["gameState"]),
            GameType(json["gameType"]) if json["gameType"] else None
        )
