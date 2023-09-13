from attrs import define, field
import ldap


@define
class LDAPClient:
    base_url: str
    ldap: ldap = field()
    @ldap.default
    def _initialize_ldap(self):
        ldap_client = ldap.initialize(self.base_url)
        # perform a synchronous bind
        ldap_client.set_option(ldap.OPT_REFERRALS, 0) # pylint: disable=no-member
        ldap_client.simple_bind_s("cn=readonly,dc=buddaphest,dc=se", "readonly")
        return ldap_client

    def check_user_login(self, username: str, password: str):
        ldap.initialize(self.base_url).simple_bind_s(f"cn={username},ou=users,dc=buddaphest,dc=se", password)

    def get_groups(self):
        response = self.ldap.search_s(
            'ou=groups,dc=buddaphest,dc=se',
            ldap.SCOPE_SUBTREE,
            "(|(cn=leaguepushups-admins)(cn=leaguepushups))",
            ["cn", "memberUid"]
        )
        groups = {}
        for group in response:
            _, group_data = group
            groups[group_data["cn"][0].decode()] = [member.decode() for member in group_data["memberUid"]]
        return groups

    def get_user_groups(self, username):
        groups = self.get_groups()
        return [
            group_name
            for group_name, members in groups.items()
            if username in members
        ]