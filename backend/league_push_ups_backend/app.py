from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_session import Session
import redis

from .controller.login_controller import LoginController
from .controller.logout_controller import LogoutController
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

    app.secret_key = r'^qfT%6e3Sg!y*8QUmmrlSxc^foMaWRFF11b77Tk@tOtgefzR$@P9n&$X!GkDAR0kehjItj#AEOEo@80^i5hSTiGwGF&J&WSMjdst9pxddXxd%K@zPNMWCK%!HvV7GD$Q'

    # Configure Redis for storing the session data on the server-side
    app.config['SESSION_TYPE'] = 'redis'
    app.config['SESSION_PERMANENT'] = False
    app.config['SESSION_USE_SIGNER'] = True
    app.config['SESSION_REDIS'] = redis.from_url('redis://redis:6379')
    _server_session = Session(app)
    create_tables()

    api.add_resource(LoginController, "/login")
    api.add_resource(LogoutController, "/logout")
    api.add_resource(ClientSessionController, "/session")
    api.add_resource(ClientMatchSettingsController, "/match_settings/<session_id>/<int:match_id>")
    api.add_resource(ClientMatchController, "/match/<session_id>/<int:match_id>")
    api.add_resource(ClientScoresController, "/scores/<session_id>/<int:match_id>")
    api.add_resource(ClientEventsController, "/events/<session_id>/<int:match_id>")
    api.add_resource(FrontendMatchesController, "/matches")

    return app
