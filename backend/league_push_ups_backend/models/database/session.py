import peeweedbevolve as _

from peewee import DateTimeField
from datetime import datetime
from zoneinfo import ZoneInfo
import os

from .base_model import BaseModel

class Session(BaseModel):
    date_time = DateTimeField(
        default=lambda: datetime.now(ZoneInfo(os.environ.get("TZ", "Europe/Stockholm"))),
        verbose_name="create time"
    )
