import peeweedbevolve as _

from peewee import ForeignKeyField, SmallIntegerField, BigIntegerField, DateTimeField
from datetime import datetime
from zoneinfo import ZoneInfo
import os

from .base_model import BaseModel
from .session import Session

class Match(BaseModel):
    Session = ForeignKeyField(Session, backref="matches")
    MatchID = BigIntegerField(unique=True)
    date_time = DateTimeField(
        default=lambda: datetime.now(ZoneInfo(os.environ.get("TZ", "Europe/Stockholm"))),
        verbose_name="create time"
    )
    TeamKills = SmallIntegerField(default=0)

    class Meta:
        indexes = (
            (("Session", "MatchID"), True),
        )
