from flask import request
from flask_login import login_required, current_user
from playhouse.shortcuts import model_to_dict
from typing import Any
from peewee import IntegrityError

from . import Controller
from ..models.database.user.summoner import Summoner

class SummonersController(Controller):
    @login_required
    def get(self) -> list[dict[str, Any]]:
        return [model_to_dict(summoner) for summoner in current_user.summoners]

    @login_required
    def post(self) -> tuple[str, int]:
        summoner = request.get_json()
        assert isinstance(summoner, str)
        try:
            Summoner.create(user=current_user.id, name=summoner)
            return summoner, 201
        except IntegrityError as e:
            return str(e), 400

    @login_required
    def delete(self) -> None:
        summoner = request.get_json()
        assert isinstance(summoner, str)
        Summoner.get(user=current_user.id, name=summoner).delete_instance()
