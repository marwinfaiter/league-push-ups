from peewee import CharField, ForeignKeyField

from ..base_model import BaseModel
from . import User

class Summoner(BaseModel):
    user = ForeignKeyField(User, backref="summoners")
    name = CharField(unique=True)

    class Meta:
        indexes = (
            (("user", "name"), True),
        )
