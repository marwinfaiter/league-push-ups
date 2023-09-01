from tap import Tap

class CLIArgs(Tap):
    username: str
    password: str
    min: int = 10
    max: int = 50
