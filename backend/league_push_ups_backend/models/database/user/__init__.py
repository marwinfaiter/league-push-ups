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
    def is_active(self):
        return self.active

    @property
    def is_authenticated(self):
        return self.authenticated

    @property
    def is_anonymous(self):
        return self.anonymous

    def get_id(self):
        return self.username
