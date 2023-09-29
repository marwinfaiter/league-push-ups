from flask import request, session
from flask_login import login_required, current_user
from typing import Any, Union

from . import Controller
from ..models.database.user.api_key import APIKey
from ..models.database.user import User

class APIKeysController(Controller):
    @login_required
    def get(self, username: str) -> Union[list[dict[str, Any]], tuple[str, int]]:
        if not "leaguepushups-admins" in session["groups"]:
            if username != current_user.username:
                return "You are not allowed to request api keys for other users", 403

        return list(APIKey.select().join(User).where(User.username == username).dicts())

    @login_required
    def post(self, username :str) -> tuple[str, int]:
        if not "leaguepushups-admins" in session["groups"]:
            if username != current_user.username:
                return "You are not allowed to create api keys for other users", 403

        user = User.get(User.username == username)
        api_key = APIKey.create(user=user.id)
        return api_key.value, 201

    @login_required
    def delete(self, username: str) -> tuple[str, int]:
        if not "leaguepushups-admins" in session["groups"]:
            if username != current_user.username:
                return "You are not allowed to delete api keys for other users", 403

        api_key = request.get_json()
        assert isinstance(api_key, str)
        user = User.get(User.username == username)
        APIKey.get(user=user.id, value=api_key).delete_instance()
        return "", 200
