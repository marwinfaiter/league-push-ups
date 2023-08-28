from flask_restful import Resource
from flask import make_response


class Controller(Resource):
    def fetch(self, *_args, **_kwargs):
        return self._build_cors_preflight_response()

    def options(self, *_args, **_kwargs):
        return self._build_cors_preflight_response()

    @staticmethod
    def _build_cors_preflight_response():
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Access-Control-Allow-Headers', "*")
        response.headers.add('Access-Control-Allow-Methods', "*")
        return response

    @staticmethod
    def _corsify_actual_response(response):
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Expose-Headers", "*")
        return response
