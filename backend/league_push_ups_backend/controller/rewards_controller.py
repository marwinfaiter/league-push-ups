from peewee import IntegrityError
from flask import request, session
from flask_login import login_required
from typing import Any, Optional

from . import Controller
from ..models.database.reward import Reward

class RewardsController(Controller):
    def get(self, reward_id: Optional[int]=None) -> list[dict[str, Any]]:
        if reward_id:
            return Reward.get(reward_id)

        return list(Reward.select().order_by(Reward.push_ups).dicts())

    @login_required
    def post(self, reward_id: Optional[int]=None) -> tuple[str, int]:
        if "leaguepushups-admins" not in session["groups"]:
            return "You're not allowed to create new rewards", 401
        data = request.get_json()
        assert isinstance(data, dict)
        try:
            if reward_id:
                reward = Reward.get(reward_id)
                reward.name = data["name"]
                reward.description = data["description"]
                reward.push_ups = data["push_ups"]
                reward.save()
            else:
                Reward.create(name=data["name"], description=data["description"], push_ups=data["push_ups"])
        except IntegrityError as e:
            return str(e), 400
        return "", 201

    @login_required
    def delete(self, reward_id: Optional[int]=None) -> tuple[str, int]:
        if "leaguepushups-admins" not in session["groups"]:
            return "You're not allowed to delete rewards", 401
        Reward.get(reward_id).delete_instance()
        return "", 200
