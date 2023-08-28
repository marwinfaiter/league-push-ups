from attrs import define

from .game_state import GameState
from .game_type import GameType

@define(frozen=True)
class Payload:
    id: int
    gameState: GameState
    gameType: GameType
