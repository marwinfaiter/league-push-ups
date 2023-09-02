from flask import request
from flask_login import login_required, current_user
from playhouse.shortcuts import model_to_dict
from typing import Any

from . import Controller
from ..models.database.user.api_key import APIKey

class APIKeysController(Controller):
    @login_required
    def get(self) -> list[dict[str, Any]]:
        return [model_to_dict(api_key) for api_key in current_user.api_keys]

    @login_required
    def post(self) -> tuple[str, int]:
        api_key = APIKey.create(user=current_user.id)
        return api_key.value, 201

    @login_required
    def delete(self) -> None:
        APIKey.delete().where(
            APIKey.user == current_user.id,
            APIKey.value == request.get_json()
        ).execute()
