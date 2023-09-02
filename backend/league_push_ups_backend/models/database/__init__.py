from .session import Session
from .match import Match
from .match_player import MatchPlayer
from .event import Event
from .assister import Assister
from .user import User
from .user.api_key import APIKey
from .user.summoner import Summoner

from .base_model import database

__all__ = [
    "Session",
    "Match",
    "MatchPlayer",
    "Event",
    "Assister",
    "User",
    "APIKey",
    "Summoner",
]

def create_tables() -> None:
    with database:
        database.create_tables([
            Session,
            Match,
            MatchPlayer,
            Event,
            Assister,
            User,
            APIKey,
            Summoner,
        ])
