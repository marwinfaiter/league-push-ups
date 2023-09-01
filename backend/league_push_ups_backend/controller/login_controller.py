from flask import request
from flask_login import login_user, current_user
from flask_login.mixins import AnonymousUserMixin
from peewee import DoesNotExist
import ldap

from . import Controller
from ..models.database.user import User
from ..models.database.user.api_key import APIKey

class LoginController(Controller):
    def post(self) -> tuple[str, int]:
        credentials = request.get_json()
        assert isinstance(credentials, dict)
        username = credentials["username"]
        password = credentials["password"]
        try:
            # build a client
            ldap_client = ldap.initialize("ldap://192.168.1.2")
            # perform a synchronous bind
            ldap_client.set_option(ldap.OPT_REFERRALS, 0)
            ldap_client.simple_bind_s(f"cn={username},ou=users,dc=buddaphest,dc=se", password)
            user, _ = User.get_or_create(username=username)
            login_user(user)
        except ldap.INVALID_CREDENTIALS:
            ldap_client.unbind()

        if isinstance(current_user, AnonymousUserMixin):
            try:
                api_key = APIKey.get(value=password)
                if api_key.user.username == username:
                    login_user(api_key.user)
            except DoesNotExist:
                pass

        if isinstance(current_user, User):
            return "", 200

        return "", 401
