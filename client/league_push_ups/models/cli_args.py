from tap import Tap
from getpass import getpass

class CLIArgs(Tap):
    username: str = ""
    password: str = ""
    backend_url: str = "https://api.leaguepushups.buddaphest.se"

    def parse_args(self, *args, **kwargs) -> "CLIArgs": # type: ignore[no-untyped-def,override]
        cli_args = super().parse_args(*args, **kwargs)
        if cli_args.username == "":
            cli_args.username = input("Username: ").strip()

        if cli_args.password == "":
            cli_args.password = getpass()
        return cli_args
