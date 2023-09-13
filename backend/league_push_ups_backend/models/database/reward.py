import peeweedbevolve as _

from peewee import SmallIntegerField, CharField

from .base_model import BaseModel

class Reward(BaseModel):
    description = CharField()
    push_ups = SmallIntegerField()

    class Meta:
        indexes = (
            (("description", "push_ups"), True),
        )
