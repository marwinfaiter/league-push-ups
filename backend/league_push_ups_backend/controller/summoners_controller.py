from flask import request, session
from flask_login import login_required, current_user
from typing import Any, Union
from peewee import IntegrityError

from . import Controller
from ..models.database.user import User
from ..models.database.user.summoner import Summoner

class SummonersController(Controller):
    @login_required
    def get(self, username: str) -> Union[list[dict[str, Any]], tuple[str, int]]:
        if not "leaguepushups-admins" in session["groups"]:
            if username != current_user.username:
                return "You are not allowed to request summoners for other users", 403

        return list(Summoner.select().join(User).where(User.username == username).dicts())

    @login_required
    def post(self, username: str) -> tuple[str, int]:
        if not "leaguepushups-admins" in session["groups"]:
            if username != current_user.username:
                return "You are not allowed to create summoners for other users", 403

        summoner = request.get_json()
        assert isinstance(summoner, str)

        try:
            user = User.get(User.username == username)
            Summoner.create(user=user.id, name=summoner)
            return summoner, 201
        except IntegrityError as e:
            return str(e), 400

    @login_required
    def delete(self, username: str) -> tuple[str, int]:
        if not "leaguepushups-admins" in session["groups"]:
            if username != current_user.username:
                return "You are not allowed to delete summoners for other users", 403

        summoner = request.get_json()
        assert isinstance(summoner, str)

        user = User.get(User.username == username)
        Summoner.get(user=user.id, name=summoner).delete_instance()
        return "", 200
