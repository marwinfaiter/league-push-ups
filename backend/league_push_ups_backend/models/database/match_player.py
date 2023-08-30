from peewee import CharField, SmallIntegerField, ForeignKeyField

from .base_model import BaseModel
from .match import Match

class MatchPlayer(BaseModel):
    Match = ForeignKeyField(Match, backref="players")
    SummonerName = CharField()
    Kills = SmallIntegerField(default=0)
    Deaths = SmallIntegerField(default=0)
    Assists = SmallIntegerField(default=0)

    @property
    def kda(self) -> float:
        if not self.Deaths:
            return self.Kills + self.Assists

        return (self.Kills + self.Assists) / self.Deaths
