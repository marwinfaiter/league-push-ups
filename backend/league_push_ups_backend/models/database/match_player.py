import peeweedbevolve as _

from peewee import CharField, SmallIntegerField, ForeignKeyField, Case, fn
from playhouse.hybrid import hybrid_property

from .base_model import BaseModel
from .match import Match

class MatchPlayer(BaseModel):
    Match = ForeignKeyField(Match, backref="players")
    SummonerName = CharField()
    Kills = SmallIntegerField(default=0)
    Deaths = SmallIntegerField(default=0)
    Assists = SmallIntegerField(default=0)

    class Meta:
        indexes = (
            (("Match", "SummonerName"), True),
        )

    @hybrid_property
    def kda(self) -> float:
        if self.Deaths == 0:
            return self.Kills + self.Assists

        return (self.Kills + self.Assists) / self.Deaths

    @kda.expression
    def kda(cls) -> float:
        return Case(
            None,
            [
                ((cls.Deaths==0), cls.Kills + cls.Assists)
            ],
            (cls.Kills + cls.Assists) / cls.Deaths
        )

    @hybrid_property
    def kill_participation(self) -> float:
        if self.Match.TeamKills > 0:
            return (self.Kills + self.Assists) / self.Match.TeamKills
        return 1

    @kill_participation.expression
    def kill_participation(cls) -> float:
        return Case(
            None,
            [
                ((cls.Match.TeamKills==0), 1)
            ],
            (cls.Kills + cls.Assists) / cls.Match.TeamKills
        )

    @hybrid_property
    def push_ups(self) -> int:
        if self.kill_participation == 0 or self.kda == 0: # pylint: disable=comparison-with-callable
            return self.Match.MaxPushUps

        return round(min(
            self.Match.MinPushUps + (self.Match.MaxPushUps/2) / (self.kda * self.kill_participation),
            self.Match.MaxPushUps
        ))

    @push_ups.expression
    def push_ups(cls) -> int:
        return Case(
            None,
            [
                ((cls.kill_participation==0,), cls.Match.MaxPushUps),
                ((cls.kda==0,), cls.Match.MaxPushUps)
            ],
            fn.ROUND(
                Case(
                    None,
                    [
                        ((cls.Match.MinPushUps + (cls.Match.MaxPushUps/2) / (cls.kda * cls.kill_participation)>=cls.Match.MaxPushUps), cls.Match.MaxPushUps)
                    ],
                    cls.Match.MinPushUps + (cls.Match.MaxPushUps/2) / (cls.kda * cls.kill_participation)
                )
            )
        )
