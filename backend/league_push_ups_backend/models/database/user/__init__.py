from peewee import CharField

from ..base_model import BaseModel

class User(BaseModel):
    username = CharField()
