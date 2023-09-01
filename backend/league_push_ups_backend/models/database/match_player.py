from peewee import CharField, SmallIntegerField, ForeignKeyField

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

    @property
    def kda(self) -> float:
        if not self.Deaths:
            return float(self.Kills + self.Assists)

        return float((self.Kills + self.Assists) / self.Deaths)

    @property
    def kill_participation(self) -> float:
        if self.Match.TeamKills:
            return float((self.Kills + self.Assists) / self.Match.TeamKills)
        return 1

    @property
    def push_ups(self) -> int:
        if self.kill_participation == 0 or self.kda == 0:
            return int(self.Match.MaxPushUps)

        return int(round(
            min(
                self.Match.MinPushUps + \
                    (self.Match.MaxPushUps/2) / (self.kda * self.kill_participation),
                self.Match.MaxPushUps
            )
        ))
