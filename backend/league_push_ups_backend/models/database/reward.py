import peeweedbevolve as _

from peewee import SmallIntegerField, CharField

from .base_model import BaseModel

class Reward(BaseModel):
    name = CharField()
    description = CharField()
    push_ups = SmallIntegerField()

    class Meta:
        indexes = (
            (("name", "push_ups"), True),
        )
