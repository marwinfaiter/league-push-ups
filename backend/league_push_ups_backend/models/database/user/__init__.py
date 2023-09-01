from peewee import CharField, BooleanField

from ..base_model import BaseModel

class User(BaseModel):
    username = CharField()
    active = BooleanField(default=True)
    authenticated = BooleanField(default=True)
    anonymous = BooleanField(default=False)

    class Meta:
        indexes = (
            (("username",), True),
        )

    @property
    def is_active(self) -> bool:
        return bool(self.active)

    @property
    def is_authenticated(self) -> bool:
        return bool(self.authenticated)

    @property
    def is_anonymous(self) -> bool:
        return bool(self.anonymous)

    def get_id(self) -> str:
        return str(self.username)
