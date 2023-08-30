from peewee import CharField, IntegerField, FloatField, ForeignKeyField, BooleanField

from .base_model import BaseModel
from .match import Match

class Event(BaseModel):
    Match = ForeignKeyField(Match, backref="events")
    EventID = IntegerField()
    EventName = CharField(max_length=20)
    EventTime = FloatField()
    KillerName = CharField(null=True)
    VictimName = CharField(null=True)
    KillStreak = IntegerField(null=True)
    Recipient = CharField(null=True)
    Stolen = BooleanField(null=True)
    TurretKilled = CharField(null=True)
    InhibKilled = CharField(null=True)
    InhibRespawningSoon = CharField(null=True)
    InhibRespawned = CharField(null=True)
    DragonType = CharField(null=True)
    Acer = CharField(null=True)
    AcingTeam = CharField(null=True)

    class Meta:
        indexes = (
            (("Match", "EventID",), True)
        )
