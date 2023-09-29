import peeweedbevolve as _

from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_session import Session
from flask_socketio import SocketIO
from flask_login import LoginManager
import redis
import os
from typing import Optional

from league_push_ups_backend.controller.websocket_controller import WebsocketController

from league_push_ups_backend.controller.login_controller import LoginController
from league_push_ups_backend.controller.logout_controller import LogoutController
from league_push_ups_backend.controller.user_controller import UserController
from league_push_ups_backend.controller.status_controller import StatusController
from league_push_ups_backend.controller.api_keys_controller import APIKeysController
from league_push_ups_backend.controller.rewards_controller import RewardsController
from league_push_ups_backend.controller.summoners_controller import SummonersController

from league_push_ups_backend.controller.client_session_controller import ClientSessionController
from league_push_ups_backend.controller.client_match_settings_controller import ClientMatchSettingsController
from league_push_ups_backend.controller.client_match_controller import ClientMatchController

from league_push_ups_backend.controller.frontend_matches_controller import FrontendMatchesController
from league_push_ups_backend.controller.frontend_progress_controller import FrontendProgressController
from league_push_ups_backend.controller.frontend_match_player_toggle_pushups_finished_controller \
    import FrontendMatchPlayerTogglePushupsFinishedController

from league_push_ups_backend.models.database.user import User
from league_push_ups_backend.models.database.base_model import database

database.evolve(interactive=False, ignore_tables=["basemodel"]) # type: ignore[attr-defined]

def create_app() -> Flask:
    app=Flask(__name__)
    api = Api(app)

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

    api.add_resource(StatusController, "/status")
    api.add_resource(LoginController, "/login")
    api.add_resource(LogoutController, "/logout")
    api.add_resource(UserController, "/user", "/user/<username>")
    api.add_resource(APIKeysController, "/user/<username>/api_keys")
    api.add_resource(SummonersController, "/user/<username>/summoners")
    api.add_resource(RewardsController, "/rewards", "/rewards/<int:reward_id>")
    api.add_resource(ClientSessionController, "/session")
    api.add_resource(ClientMatchSettingsController, "/match_settings/<session_id>/<int:match_id>")
    api.add_resource(ClientMatchController, "/match/<session_id>/<int:match_id>")
    api.add_resource(FrontendMatchesController, "/matches")
    api.add_resource(FrontendProgressController, "/progress")
    api.add_resource(
        FrontendMatchPlayerTogglePushupsFinishedController,
        "/match_player/<int:player_id>/toggle_pushups_finished"
    )

    return app

def create_cors(app: Flask) -> CORS:
    return CORS(app, expose_headers=["Content-Disposition"], supports_credentials=True)

def create_socketio(app: Flask) -> SocketIO:
    sio = SocketIO(app, manage_session=False, cors_allowed_origins=os.environ.get(
        "PUBLIC_URL", "https://leaguepushups.buddaphest.se"
    ))
    sio.on_namespace(WebsocketController("/"))
    return sio

def create_login_manager(app: Flask) -> LoginManager:
    lm = LoginManager(app)
    lm.user_loader(user_loader)
    return lm

def user_loader(uid: str) -> Optional[User]:
    user = User.get_or_none(username=uid)
    assert isinstance(user, User)
    return user

if __name__ == "__main__":
    flask_app = create_app()
    cors = create_cors(flask_app)
    login_manager = create_login_manager(flask_app)
    socketio = create_socketio(flask_app)
    socketio.run(flask_app, host="0.0.0.0", debug=True, allow_unsafe_werkzeug=True)
