from flask import request, session
from flask_login import login_user, logout_user, current_user
from flask_login.mixins import AnonymousUserMixin
from typing import Union, Any
from ..client.ldap import LDAPClient
import ldap

from . import Controller
from ..models.database.user import User
from ..models.database.user.api_key import APIKey

class LoginController(Controller):
    def post(self) -> tuple[Union[str, dict[str, Any], int], int]:
        logout_user()
        credentials = request.get_json()
        assert isinstance(credentials, dict)
        username = credentials["username"]
        password = credentials["password"]
        try:
            ldap_client = LDAPClient("ldap://192.168.1.2")
            ldap_client.check_user_login(username, password)
            result = ldap_client.get_user_groups(username)
            if not result:
                raise RuntimeError
            user, _ = User.get_or_create(username=username)
            login_user(user)
            session["groups"] = result
            session["summoners"] = [summoner.name for summoner in user.summoners]
        except ldap.INVALID_CREDENTIALS: # pylint: disable=no-member
            ldap_client.ldap.unbind()
        except RuntimeError:
            pass

        if isinstance(current_user, AnonymousUserMixin):
            if api_key := APIKey.get_or_none(value=password):
                if api_key.user.username == username:
                    login_user(api_key.user)

        if isinstance(current_user, User):
            return {
                "username": username,
                "groups": session.setdefault("groups", []),
                "summoners": session.setdefault("summoners", [])
            }, 200

        return "Login Failed", 401
