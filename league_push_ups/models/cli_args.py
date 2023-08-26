from tap import Tap

DEFAULT_DISCORD_WEBHOOK = (
    "https://discord.com/api/webhooks/"
    "1117565515079110716/"
    "tE1lZUeXyVVNVXpYW6dUzgrCoUJKUxNWuhLA1J6-G5YGOeUs3hBi1t4bsP5xXFH3kst4"
)

class CLIArgs(Tap):
    min: int = 10
    max: int = 50
    webhook_url: str = DEFAULT_DISCORD_WEBHOOK
