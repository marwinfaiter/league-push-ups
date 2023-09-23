import peeweedbevolve as _

from peewee import CharField, BooleanField, SmallIntegerField

from ..base_model import BaseModel

class User(BaseModel):
    username = CharField()
    active = BooleanField(default=True)
    minimum_push_ups = SmallIntegerField(default=10)
    maximum_push_ups = SmallIntegerField(default=50)

    class Meta:
        indexes = (
            (("username",), True),
        )

    # These are for flask_login, not related to actual user data
    @property
    def is_active(self) -> bool:
        return True

    @property
    def is_authenticated(self) -> bool:
        return True

    @property
    def is_anonymous(self) -> bool:
        return False

    def get_id(self) -> str:
        return str(self.username)
