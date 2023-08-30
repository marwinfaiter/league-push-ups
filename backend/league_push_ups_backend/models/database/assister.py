from peewee import ForeignKeyField, CharField

from .base_model import BaseModel
from .event import Event

class Assister(BaseModel):
    Event = ForeignKeyField(Event, backref="assisters")
    Assister = CharField()

    class Meta:
        indexes = (
            (("Event", "Assister",), True)
        )
