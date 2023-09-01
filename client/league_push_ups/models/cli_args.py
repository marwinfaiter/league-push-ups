from tap import Tap

class CLIArgs(Tap):
    username: str
    password: str
    league_url: str = "https://leaguepushups.buddaphest.se"
    min: int = 10
    max: int = 50
