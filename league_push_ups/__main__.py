from typing import Optional
import time
import json
from cattrs import structure

from lcu_driver import Connector
from discord import Colour, SyncWebhook, Embed

from .models.game_update import GameUpdate
from .models.game_update.game_state import GameState
from .models.lobby import Lobby
from .models.lobby.member import Member
from .models.end_of_game.eog_stats_block import EOGStatsBlock
from .models.cli_args import CLIArgs

connector = Connector()

class LeaguePushUps:
    webhook: SyncWebhook
    min: int
    max: int
    lobby: Optional[Lobby] = None
    game_id: Optional[int] = None

    # fired when LCU API is ready to be used
    @staticmethod
    @connector.ready
    async def connect(_):
        print('LCU API is ready to be used.')

    # fired when League Client is closed (or disconnected from websocket)
    @staticmethod
    @connector.close
    async def disconnect(connection):
        print('The client have been closed!')
        await connection.stop()

    @staticmethod
    @connector.ws.register("/lol-lobby/v2/lobby", event_types=("CREATE","UPDATE"))
    async def lobby_create(_, event):
        LeaguePushUps.lobby = structure(event.data, Lobby)
        if LeaguePushUps.lobby:
            print(f"Lobby {event.type}: {LeaguePushUps.lobby.gameConfig.gameMode.value}")

    @staticmethod
    @connector.ws.register("/lol-lobby/v2/lobby/members", event_types=("UPDATE",))
    async def lobby_members_update(_, event):
        if LeaguePushUps.lobby:
            print("Updating lobby members")
            LeaguePushUps.lobby.members = [structure(member, Member) for member in event.data]

    @staticmethod
    @connector.ws.register("/lol-lobby/v2/lobby", event_types=("DELETE",))
    async def lobby_delete(*_):
        if not LeaguePushUps.game_id:
            print("Deleting lobby")
            LeaguePushUps.lobby = None

    @staticmethod
    @connector.ws.register(
        "/riot-messaging-service/v1/message/lol-gsm-server/v1/gsm/game-update",
        event_types=("CREATE",)
    )
    async def game_update(_, event):
        event.data["payload"] = json.loads(event.data["payload"])
        game_update = structure(event.data, GameUpdate)

        if game_update.payload.gameState == GameState.START_REQUESTED:
            print(f"Game starting: {game_update.payload.gameType.value}")
            LeaguePushUps.game_id = game_update.payload.id
        elif game_update.payload.gameState == GameState.TERMINATED:
            print("Game ended")
            LeaguePushUps.game_id = None
        elif game_update.payload.gameState == GameState.TERMINATED_IN_ERROR:
            print("Game exited early")
            LeaguePushUps.game_id = None
            LeaguePushUps.lobby = None

    @staticmethod
    @connector.ws.register('/lol-end-of-game/v1/eog-stats-block', event_types=('CREATE',))
    async def game_end(_, event):
        eog_stats_block = structure(event.data, EOGStatsBlock)
        if LeaguePushUps.lobby:
            for team in eog_stats_block.teams:
                embeds = []
                for player in team.players:
                    if LeaguePushUps.lobby.is_summoner_member(player.summonerName):
                        embed = Embed(colour=Colour.green(), title=player.summonerName)
                        if team.stats.CHAMPIONS_KILLED:
                            kill_participation = (player.stats.CHAMPIONS_KILLED + player.stats.ASSISTS) \
                                / team.stats.CHAMPIONS_KILLED
                        else:
                            kill_participation = 1

                        if any([
                            kill_participation == 0,
                            sum([player.stats.CHAMPIONS_KILLED, player.stats.ASSISTS, player.stats.NUM_DEATHS]) == 0,
                        ]):
                            push_ups = 50
                        else:
                            push_ups = round(
                                min(
                                    LeaguePushUps.min + \
                                        (LeaguePushUps.max/2) / (player.stats.kda * kill_participation),
                                    LeaguePushUps.max
                                )
                            )
                        embed.add_field(name="Game Mode", value=eog_stats_block.gameMode.value)
                        embed.add_field(name="Game ID", value=eog_stats_block.gameId)
                        embed.add_field(
                            name="Game Length",
                            value=time.strftime('%H:%M:%S', time.gmtime(eog_stats_block.gameLength))
                        )
                        embed.add_field(name="Kills", value=player.stats.CHAMPIONS_KILLED)
                        embed.add_field(name="Deaths", value=player.stats.NUM_DEATHS)
                        embed.add_field(name="Assists", value=player.stats.ASSISTS)
                        embed.add_field(name="Kill Participation", value=f"{kill_participation * 100:.2f}%")
                        embed.add_field(name="KDA", value=f"{player.stats.kda:.2f}")
                        embed.add_field(name="Push-ups", value=push_ups)
                        embeds.append(embed)
                if embeds:
                    LeaguePushUps.webhook.send(embeds=embeds)
        LeaguePushUps.lobby = None

def main():
    cli_args = CLIArgs().parse_args()
    print(f"Starting with arguments: {cli_args}")
    LeaguePushUps.webhook = SyncWebhook.from_url(cli_args.webhook_url)
    LeaguePushUps.min = cli_args.min
    LeaguePushUps.max = cli_args.max
    connector.start()

if __name__ == "__main__":
    main()
