from playhouse.shortcuts import model_to_dict
from flask import request, session
from flask_login import login_required, current_user
from typing import Any, Optional, Union

from . import Controller
from ..models.database.user import User
from ..models.database.base_model import database

class UserController(Controller):
    @login_required
    def get(self, username: Optional[str]=None) -> Union[dict[str, Any], tuple[str, int]]:
        if not "leaguepushups-admins" in session["groups"]:
            if not username:
                return "You are not allowed to request all user settings", 403
            if username != current_user.username:
                return "You are not allowed to request user settings for other users", 403

        with database.atomic() as _:
            if username:
                users = User.get(User.username==username)
            else:
                users = User.select()

            return {
                user.username: {
                    "settings": model_to_dict(user),
                    "api_keys": [
                        {"id": api_key.id, "value": api_key.value}
                        for api_key in user.api_keys
                    ],
                    "summoners": [
                        {"id": summoner.id, "name": summoner.name}
                        for summoner in user.summoners
                    ],
                }
                for user in users
            }

    @login_required
    def post(self, username: str) -> tuple[str, int]:
        data = request.get_json()
        assert isinstance(data, dict)
        User.update({
            User.active: data.get("active"),
            User.minimum_push_ups: data.get("minimum_push_ups"),
            User.maximum_push_ups: data.get("maximum_push_ups"),
        }).where(
            User.username == username
        ).execute()
        return "", 201
