from flask_restful import Resource
from flask import make_response, Response
from typing import Any
import os


class Controller(Resource):
    def fetch(self, *_args: Any, **_kwargs: Any) -> Response:
        return self._build_cors_preflight_response()

    def options(self, *_args: Any, **_kwargs: Any) -> Response:
        return self._build_cors_preflight_response()

    @staticmethod
    def _build_cors_preflight_response() -> Response:
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", os.environ.get(
            "PUBLIC_URL", "https://leaguepushups.buddaphest.se"
        ))
        response.headers.add('Access-Control-Allow-Headers', "Content-Type,Authorization")
        response.headers.add('Access-Control-Allow-Methods', "GET,POST,DELETE,OPTIONS")
        response.headers.add('Access-Control-Allow-Credentials', "true")
        return response

    @staticmethod
    def _corsify_actual_response(response: Response) -> Response:
        response.headers.add("Access-Control-Allow-Origin", os.environ.get(
            "PUBLIC_URL", "https://leaguepushups.buddaphest.se"
        ))
        response.headers.add("Access-Control-Expose-Headers", "*")
        return response
