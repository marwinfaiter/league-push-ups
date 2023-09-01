from flask import session, redirect, request
from flask_login import login_required, current_user
from playhouse.shortcuts import model_to_dict

from . import Controller
from ..models.database.user.api_key import APIKey

class APIKeysController(Controller):
    @login_required
    def get(self):
        return [model_to_dict(api_key) for api_key in current_user.api_keys]

    @login_required
    def post(self):
        api_key = APIKey.create(user=current_user.id)
        return api_key.value, 201

    @login_required
    def delete(self):
        api_key = request.get_json()["api_key"]
        api_key_model = APIKey.get(user=current_user.id, value=api_key)
        api_key_model.delete_instance()

        return api_key