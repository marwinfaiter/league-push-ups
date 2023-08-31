from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from .controller.client_session_controller import ClientSessionController
from .controller.client_match_settings_controller import ClientMatchSettingsController
from .controller.client_match_controller import ClientMatchController
from .controller.client_scores_controller import ClientScoresController
from .controller.client_events_controller import ClientEventsController
from .controller.frontend_matches_controller import FrontendMatchesController

from .models.database import create_tables

def create_app():
    app=Flask(__name__)
    api = Api(app)
    CORS(app, expose_headers=["Content-Disposition"])
    create_tables()

    api.add_resource(ClientSessionController, "/session")
    api.add_resource(ClientMatchSettingsController, "/match_settings/<session_id>/<int:match_id>")
    api.add_resource(ClientMatchController, "/match/<session_id>/<int:match_id>")
    api.add_resource(ClientScoresController, "/scores/<session_id>/<int:match_id>")
    api.add_resource(ClientEventsController, "/events/<session_id>/<int:match_id>")
    api.add_resource(FrontendMatchesController, "/matches")

    return app
