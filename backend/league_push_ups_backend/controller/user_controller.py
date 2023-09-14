from peewee import IntegrityError
from playhouse.shortcuts import model_to_dict
from flask import request
from flask_login import login_required, current_user
from typing import Any

from . import Controller

class UserController(Controller):
    def get(self) -> dict[str, Any]:
        return dict(model_to_dict(current_user))

    @login_required
    def post(self) -> tuple[str, int]:
        data = request.get_json()
        assert isinstance(data, dict)
        try:
            current_user.active = data["active"]
            current_user.minimum_push_ups = data["minimum_push_ups"]
            current_user.maximum_push_ups = data["maximum_push_ups"]
            current_user.save()
        except IntegrityError as e:
            return str(e), 400
        return "", 201
