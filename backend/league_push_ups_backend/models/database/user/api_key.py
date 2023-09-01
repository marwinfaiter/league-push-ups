from peewee import CharField, ForeignKeyField
from uuid import uuid4

from ..base_model import BaseModel
from . import User

class APIKey(BaseModel):
    user = ForeignKeyField(User, backref="api_keys")
    value = CharField(default=lambda: uuid4().hex)

    class Meta:
        indexes = (
            (("user", "value"), True),
        )
