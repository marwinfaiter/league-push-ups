from flask import session, redirect, request
from playhouse.shortcuts import model_to_dict

from . import Controller
from ..models.database.user.api_key import APIKey

class APIKeysController(Controller):
    def get(self):
        if not session.get("user"):
            return redirect("/")

        return [model_to_dict(api_key) for api_key in session["user"].api_keys]

    def post(self):
        if not session.get("user"):
            return redirect("/")

        api_key = APIKey.create(user=session["user"].id)
        return api_key.value, 201

    def delete(self):
        if not session.get("user"):
            return redirect("/")

        api_key = request.get_json()["api_key"]
        api_key_model = APIKey.get(user=session["user"].id, value=api_key)
        api_key_model.delete_instance()

        return api_key
