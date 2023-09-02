from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_session import Session
from flask_socketio import SocketIO
from flask_login import LoginManager
from peewee import DoesNotExist
import redis

from typing import Optional

from league_push_ups_backend.controller.login_controller import LoginController
from league_push_ups_backend.controller.logout_controller import LogoutController
from league_push_ups_backend.controller.api_keys_controller import APIKeysController
from league_push_ups_backend.controller.client_session_controller import ClientSessionController
from league_push_ups_backend.controller.client_match_settings_controller import ClientMatchSettingsController
from league_push_ups_backend.controller.client_match_controller import ClientMatchController
from league_push_ups_backend.controller.client_scores_controller import ClientScoresController
from league_push_ups_backend.controller.client_events_controller import ClientEventsController
from league_push_ups_backend.controller.frontend_matches_controller import FrontendMatchesController
from league_push_ups_backend.controller.frontend_progress_controller import FrontendProgressController

from league_push_ups_backend.models.database import create_tables
from league_push_ups_backend.models.database.user import User

flask_app = None
socketio = None
login_manager = None

def create_app() -> Flask:
    app=Flask(__name__)
    api = Api(app)
    CORS(app, expose_headers=["Content-Disposition"], supports_credentials=True)

    app.secret_key = (
        r"^qfT%6e3Sg!y*8QUmmrlSxc^foMaWRFF11b77Tk@tOtgefzR$"
        r"@P9n&$X!GkDAR0kehjItj#AEOEo@80^i5hSTiGwGF&J&WSMjdst9pxddXxd%K@zPNMWCK%!HvV7GD$Q"
    )

    # Configure Redis for storing the session data on the server-side
    app.config['SESSION_TYPE'] = 'redis'
    app.config['SESSION_PERMANENT'] = False
    app.config['SESSION_USE_SIGNER'] = True
    app.config['SESSION_REDIS'] = redis.from_url('redis://redis:6379')
    Session(app)
    create_tables()

    api.add_resource(LoginController, "/login")
    api.add_resource(LogoutController, "/logout")
    api.add_resource(APIKeysController, "/api_keys")
    api.add_resource(ClientSessionController, "/session")
    api.add_resource(ClientMatchSettingsController, "/match_settings/<session_id>/<int:match_id>")
    api.add_resource(ClientMatchController, "/match/<session_id>/<int:match_id>")
    api.add_resource(ClientScoresController, "/scores/<session_id>/<int:match_id>")
    api.add_resource(ClientEventsController, "/events/<session_id>/<int:match_id>")
    api.add_resource(FrontendMatchesController, "/matches")
    api.add_resource(FrontendProgressController, "/progress")

    return app

def create_socketio(app: Flask) -> SocketIO:
    return SocketIO(app)

def create_login_manager(app: Flask) -> LoginManager:
    return LoginManager(app)

def user_loader(uid: str) -> Optional[User]:
    try:
        user = User.get(username=uid)
        assert isinstance(user, User)
        return user
    except DoesNotExist:
        return None

if __name__ == "__main__":
    flask_app = create_app()
    socketio = create_socketio(flask_app)
    login_manager = create_login_manager(flask_app)
    login_manager.user_loader(user_loader)
    socketio.run(flask_app, host="0.0.0.0", debug=True, allow_unsafe_werkzeug=True)
