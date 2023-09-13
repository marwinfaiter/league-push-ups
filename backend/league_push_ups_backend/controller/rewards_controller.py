from peewee import IntegrityError
from flask import request, session
from flask_login import login_required
from typing import Any

from . import Controller
from ..models.database.reward import Reward

class RewardsController(Controller):
    @login_required
    def get(self) -> list[dict[str, Any]]:
        return list(Reward.select().order_by(Reward.push_ups).dicts())

    @login_required
    def post(self) -> tuple[str, int]:
        if "leaguepushups-admins" not in session["groups"]:
            return "You're not allowed to create new rewards", 401
        data = request.get_json()
        try:
            Reward.create(description=data["description"], push_ups=data["push_ups"])
        except IntegrityError as e:
            return str(e), 400
        return "", 201

    @login_required
    def delete(self) -> None:
        if "leaguepushups-admins" not in session["groups"]:
            return "You're not allowed to delete rewards", 401
        reward_id = request.get_json()
        assert isinstance(reward_id, int)
        Reward.get(reward_id).delete_instance()
