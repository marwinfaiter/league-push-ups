from .session import Session
from .match import Match
from .match_player import MatchPlayer
from .event import Event
from .assister import Assister

from .base_model import database

__all__ = [
    "Session",
    "Match",
    "MatchPlayer",
    "Event",
    "Assister",
]

def create_tables():
    with database:
        database.create_tables([
            Session,
            Match,
            MatchPlayer,
            Event,
            Assister,
        ])
