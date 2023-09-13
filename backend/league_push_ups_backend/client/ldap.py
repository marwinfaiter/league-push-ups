from attrs import define, field
from typing import Any
import ldap


@define
class LDAPClient:
    base_url: str
    ldap: ldap = field()
    @ldap.default
    def _initialize_ldap(self) -> Any:
        ldap_client = ldap.initialize(self.base_url)
        # perform a synchronous bind
        ldap_client.set_option(ldap.OPT_REFERRALS, 0) # pylint: disable=no-member
        ldap_client.simple_bind_s("cn=readonly,dc=buddaphest,dc=se", "readonly")
        return ldap_client

    def check_user_login(self, username: str, password: str) -> None:
        ldap.initialize(self.base_url).simple_bind_s(f"cn={username},ou=users,dc=buddaphest,dc=se", password)

    def get_groups(self) -> dict[str, list[str]]:
        response = self.ldap.search_s(
            'ou=groups,dc=buddaphest,dc=se',
            ldap.SCOPE_SUBTREE, # pylint: disable=no-member
            "(|(cn=leaguepushups-admins)(cn=leaguepushups))",
            ["cn", "memberUid"]
        )
        groups = {}
        for group in response:
            _, group_data = group
            groups[group_data["cn"][0].decode()] = [member.decode() for member in group_data["memberUid"]]
        return groups

    def get_user_groups(self, username: str) -> list[str]:
        groups = self.get_groups()
        return [
            group_name
            for group_name, members in groups.items()
            if username in members
        ]
