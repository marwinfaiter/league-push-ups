from tap import Tap
from getpass import getpass

class CLIArgs(Tap):
    username: str = ""
    password: str = ""
    backend_url: str = "https://api.leaguepushups.buddaphest.se"

    def get_username(self) -> str:
        if self.username:
            return self.username
        self.username = input("Username: ").strip()
        return self.username

    def get_password(self) -> str:
        if self.password:
            return self.password
        self.password = getpass()
        return self.password
