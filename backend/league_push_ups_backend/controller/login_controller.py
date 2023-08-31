from flask import request, session
import ldap

from . import Controller
from ..models.database.user import User

class LoginController(Controller):
    def post(self):
        credentials = request.get_json()
        username = credentials["username"]
        password = credentials["password"]
        try:
            # build a client
            ldap_client = ldap.initialize("ldap://192.168.1.2")
            # perform a synchronous bind
            ldap_client.set_option(ldap.OPT_REFERRALS, 0)
            ldap_client.simple_bind_s(f"cn={username},ou=users,dc=buddaphest,dc=se", password)
            user, _ = User.get_or_create(username=username)
            session["user"] = user
            return username, 200
        except ldap.INVALID_CREDENTIALS:
            ldap_client.unbind()
            return username, 401
