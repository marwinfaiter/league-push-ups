from peewee import CharField, IntegerField, ForeignKeyField

from .base_model import BaseModel
from .match import Match

class MatchPlayer(BaseModel):
    Match = ForeignKeyField(Match, backref="players")
    SummonerName = CharField()
    Kills = IntegerField(default=0)
    Deaths = IntegerField(default=0)
    Assists = IntegerField(default=0)

    @property
    def kda(self) -> float:
        if not self.Deaths:
            return self.Kills + self.Assists

        return (self.Kills + self.Assists) / self.Deaths
