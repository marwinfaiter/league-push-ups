from attrs import frozen

from .end_of_game.player import Player

@frozen
class Match:
    team_kills: int
    players: list[Player]
