import peeweedbevolve as _

from peewee import CharField, SmallIntegerField, ForeignKeyField, BooleanField, Case, fn
from playhouse.hybrid import hybrid_property

from typing import Any

from .base_model import BaseModel
from .match import Match
from .user import User

class MatchPlayer(BaseModel):
    Match = ForeignKeyField(Match, backref="players")
    User = ForeignKeyField(User, backref="matches")
    SummonerName = CharField()
    Kills = SmallIntegerField(default=0)
    Deaths = SmallIntegerField(default=0)
    Assists = SmallIntegerField(default=0)
    MinPushUps = SmallIntegerField(default=10)
    MaxPushUps = SmallIntegerField(default=50)
    PushUpsFinished = BooleanField(default=True)

    class Meta:
        indexes = (
            (("Match", "SummonerName"), True),
        )

    @hybrid_property
    def kda(self) -> float:
        if self.Deaths == 0:
            return self.Kills + self.Assists

        return (self.Kills + self.Assists) / self.Deaths

    @kda.expression # type: ignore[no-redef]
    def kda(cls) -> float: # pylint: disable=no-self-argument
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

    @kill_participation.expression # type: ignore[no-redef]
    def kill_participation(cls) -> float: # pylint: disable=no-self-argument
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
            return self.MaxPushUps

        return round(min(
            self.MinPushUps + (self.MinPushUps/2) / (self.kda * self.kill_participation),
            self.MaxPushUps
        ))

    @push_ups.expression # type: ignore[no-redef]
    def push_ups(cls) -> int: # pylint: disable=no-self-argument
        push_ups = cls.MinPushUps + (cls.MaxPushUps/2) / (cls.kda * cls.kill_participation)
        return Case(
            None,
            [
                ((cls.kill_participation==0,), cls.MaxPushUps), # pylint: disable=comparison-with-callable
                ((cls.kda==0,), cls.MaxPushUps) # pylint: disable=comparison-with-callable
            ],
            fn.ROUND(
                Case(
                    None,
                    [
                        ((push_ups>=cls.MaxPushUps), cls.MaxPushUps)
                    ],
                    push_ups
                )
            )
        )

    @staticmethod
    def get_match_players(match_id: int) -> list[dict[str, Any]]:
        return list(
            MatchPlayer.select(
            MatchPlayer,
            MatchPlayer.kda.cast("float").alias("kda"), # type: ignore[attr-defined] # pylint: disable=no-member
            MatchPlayer.kill_participation.cast("float").alias("kill_participation"), # type: ignore[attr-defined] # pylint: disable=no-member
            MatchPlayer.push_ups.cast("int").alias("push_ups") # type: ignore[attr-defined] # pylint: disable=no-member
            ).join(
                Match
            ).where(
                MatchPlayer.Match==match_id
            ).dicts()
        )
