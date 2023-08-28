from attrs import define
from .game_mode import GameMode

@define(frozen=True)
class GameConfig:
    gameMode: GameMode
    isCustom: bool
