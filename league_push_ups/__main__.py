import argparse
from typing import Optional
import time

from lcu_driver import Connector
from discord import Colour, SyncWebhook, Embed

from .models.game_update import GameUpdate
from .models.game_update.game_state import GameState
from .models.lobby import Lobby
from .models.lobby.member import Member
from .models.end_of_game.eog_stats_block import EOGStatsBlock

DEFAULT_DISCORD_WEBHOOK = (
    "https://discord.com/api/webhooks/"
    "1117565515079110716/"
    "tE1lZUeXyVVNVXpYW6dUzgrCoUJKUxNWuhLA1J6-G5YGOeUs3hBi1t4bsP5xXFH3kst4"
)

connector = Connector()

class LeaguePushUps:
    min: int
    max: int
    webhook: SyncWebhook
    lobby: Optional[Lobby] = None
    game_id: Optional[int] = None

    @staticmethod
    def init(webhook_url, push_up_min, push_up_max):
        LeaguePushUps.min = push_up_min
        LeaguePushUps.max = push_up_max
        LeaguePushUps.webhook = SyncWebhook.from_url(webhook_url)

    # fired when LCU API is ready to be used
    @staticmethod
    @connector.ready
    async def connect(_):
        print('LCU API is ready to be used.')

    # fired when League Client is closed (or disconnected from websocket)
    @staticmethod
    @connector.close
    async def disconnect(_):
        print('The client have been closed!')
        await connector.stop()

    @staticmethod
    @connector.ws.register("/lol-lobby/v2/lobby", event_types=("CREATE","UPDATE"))
    async def lobby_create(_, event):
        LeaguePushUps.lobby = Lobby.from_json(event.data)
        if LeaguePushUps.lobby:
            print(f"Lobby {event.type}: {LeaguePushUps.lobby.game_config.game_mode.value}")

    @staticmethod
    @connector.ws.register("/lol-lobby/v2/lobby/members", event_types=("UPDATE",))
    async def lobby_members_update(_, event):
        if LeaguePushUps.lobby:
            print("Updating lobby members")
            LeaguePushUps.lobby.members = [Member.from_json(member) for member in event.data]

    @staticmethod
    @connector.ws.register("/lol-lobby/v2/lobby", event_types=("DELETE",))
    async def lobby_delete(*_args):
        if not LeaguePushUps.game_id:
            print("Deleting lobby")
            LeaguePushUps.lobby = None

    @staticmethod
    @connector.ws.register(
        "/riot-messaging-service/v1/message/lol-platform/v1/gsm/game-update",
        event_types=("CREATE",)
    )
    async def game_start(_, event):
        game_update = GameUpdate.from_json(event.data)
        if game_update.payload.game_state == GameState.START_REQUESTED:
            print(f"Game starting: {game_update.payload.game_type.value}")
            LeaguePushUps.game_id = game_update.payload.id
        elif game_update.payload.game_state == GameState.TERMINATED:
            print("Game ended")
            LeaguePushUps.game_id = None
        elif game_update.payload.game_state == GameState.TERMINATED_IN_ERROR:
            print("Game exited early")
            LeaguePushUps.game_id = None
            LeaguePushUps.lobby = None

    @staticmethod
    @connector.ws.register('/lol-end-of-game/v1/eog-stats-block', event_types=('CREATE',))
    async def game_end(_, event):
        eog_stats_block = EOGStatsBlock.from_json(event.data)
        if LeaguePushUps.lobby:
            for team in eog_stats_block.teams:
                embeds = []
                for player in team.players:
                    if LeaguePushUps.lobby.is_summoner_member(player.summoner_name):
                        embed = Embed(colour=Colour.green(), title=player.summoner_name)
                        if team.stats.kills:
                            kill_participation = (player.stats.kills + player.stats.assists) / team.stats.kills
                        else:
                            kill_participation = 1

                        if kill_participation == 0:
                            push_ups = 50
                        else:
                            push_ups = round(
                                min(
                                    LeaguePushUps.min + (LeaguePushUps.max/2) / (player.stats.kda * kill_participation),
                                    LeaguePushUps.max
                                )
                            )
                        embed.add_field(name="Game Mode", value=eog_stats_block.game_mode.value)
                        embed.add_field(name="Game ID", value=eog_stats_block.game_id)
                        embed.add_field(
                            name="Game Length",
                            value=time.strftime('%H:%M:%S', time.gmtime(eog_stats_block.game_length))
                        )
                        embed.add_field(name="Kills", value=player.stats.kills)
                        embed.add_field(name="Deaths", value=player.stats.deaths)
                        embed.add_field(name="Assists", value=player.stats.assists)
                        embed.add_field(name="Kill Participation", value=f"{kill_participation * 100:.2f}%")
                        embed.add_field(name="KDA", value=f"{player.stats.kda:.2f}")
                        embed.add_field(name="Push-ups", value=push_ups)
                        embeds.append(embed)
                LeaguePushUps.webhook.send(embeds=embeds)
        LeaguePushUps.lobby = None

def main():
    parser = argparse.ArgumentParser(prog="League push up calculator")
    parser.add_argument("--min", type=int, default=10)
    parser.add_argument("--max", type=int, default=50)
    parser.add_argument("--webhook_url", type=str, default=DEFAULT_DISCORD_WEBHOOK)
    args = parser.parse_args()
    print(f"Starting with arguments: {args}")
    LeaguePushUps.init(args.webhook_url, args.min, args.max)
    # starts the connector
    connector.start()

if __name__ == "__main__":
    main()
