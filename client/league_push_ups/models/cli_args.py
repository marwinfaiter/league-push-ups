from tap import Tap

class CLIArgs(Tap):
    username: str
    password: str
    backend_url: str = "https://api.leaguepushups.buddaphest.se"
