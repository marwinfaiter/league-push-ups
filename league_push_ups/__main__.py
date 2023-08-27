from typing import Optional
import time
import json
from cattrs import structure

from lcu_driver import Connector
from lcu_driver.events.responses import WebsocketEventResponse
from discord import Colour, SyncWebhook, Embed

from .models.game_update import GameUpdate
from .models.game_update.game_state import GameState
from .models.lobby import Lobby
from .models.lobby.member import Member
from .models.end_of_game.eog_stats_block import EOGStatsBlock
from .models.cli_args import CLIArgs
from .models.end_of_game.stats import Stats
from .models.windows import Windows
from .models.match import Match

connector = Connector()

class LeaguePushUps:
    webhook: SyncWebhook
    min: int
    max: int
    api_key: Optional[str] = None
    lobby: Optional[Lobby] = None
    game_id: Optional[int] = None
    matches: list[Match] = []
    windows: Optional[Windows] = None

    def __enter__(self):
        self.start_gui()

    def __exit__(self, *err):
        pass

    def start_gui(self) -> None:
        LeaguePushUps.windows = Windows(self)

    # fired when LCU API is ready to be used
    @staticmethod
    @connector.ready # type: ignore[misc]
    async def connect(_connector: Connector) -> None:
        print('LCU API is ready to be used.')

    # fired when League Client is closed (or disconnected from websocket)
    @staticmethod
    @connector.close # type: ignore[misc]
    async def disconnect(_connector: Connector) -> None:
        print('The client have been closed!')
        await connector.stop()

    @staticmethod
    @connector.ws.register("/lol-lobby/v2/lobby", event_types=("CREATE","UPDATE")) # type: ignore[misc]
    async def lobby_create(_connector: Connector, event: WebsocketEventResponse) -> None:
        LeaguePushUps.lobby = structure(event.data, Lobby)
        if LeaguePushUps.lobby:
            print(f"Lobby {event.type}: {LeaguePushUps.lobby.gameConfig.gameMode.value}")

    @staticmethod
    @connector.ws.register("/lol-lobby/v2/lobby/members", event_types=("UPDATE",)) # type: ignore[misc]
    async def lobby_members_update(_: Connector, event: WebsocketEventResponse) -> None:
        if LeaguePushUps.lobby:
            print("Updating lobby members")
            LeaguePushUps.lobby.members = [structure(member, Member) for member in event.data]

    @staticmethod
    @connector.ws.register("/lol-lobby/v2/lobby", event_types=("DELETE",)) # type: ignore[misc]
    async def lobby_delete(_connector: Connector, _event: WebsocketEventResponse) -> None:
        if not LeaguePushUps.game_id:
            print("Deleting lobby")
            LeaguePushUps.lobby = None

    @staticmethod
    @connector.ws.register(
        "/riot-messaging-service/v1/message/lol-gsm-server/v1/gsm/game-update",
        event_types=("CREATE",)
    ) # type: ignore[misc]
    async def game_update(_connector: Connector, event: WebsocketEventResponse) -> None:
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

    @staticmethod
    @connector.ws.register('/lol-end-of-game/v1/eog-stats-block', event_types=('CREATE',)) # type: ignore[misc]
    async def game_end(_connector: Connector, event: WebsocketEventResponse) -> None:
        if LeaguePushUps.lobby is None:
            return

        eog_stats_block = structure(event.data, EOGStatsBlock)
        for team in eog_stats_block.teams:
            if team.stats is None:
                continue

            match = Match(team.stats.CHAMPIONS_KILLED, [])
            embeds = []
            for player in team.players:
                if LeaguePushUps.lobby.is_summoner_member(player.summonerName):
                    match.players.append(player)

                    embed = Embed(colour=Colour.green(), title=player.summonerName)
                    embed.add_field(name="Game Mode", value=eog_stats_block.gameMode.value)
                    embed.add_field(name="Game ID", value=eog_stats_block.gameId)
                    embed.add_field(
                        name="Game Length",
                        value=time.strftime('%H:%M:%S', time.gmtime(eog_stats_block.gameLength))
                    )
                    embed.add_field(name="Kills", value=player.stats.CHAMPIONS_KILLED)
                    embed.add_field(name="Deaths", value=player.stats.NUM_DEATHS)
                    embed.add_field(name="Assists", value=player.stats.ASSISTS)

                    kill_participation = LeaguePushUps.calculate_kill_participation(
                        player.stats,
                        team.stats.CHAMPIONS_KILLED
                    )
                    push_ups = LeaguePushUps.calculate_push_ups(kill_participation, player.stats.kda)

                    embed.add_field(name="Kill Participation", value=f"{kill_participation * 100:.2f}%")
                    embed.add_field(name="KDA", value=f"{player.stats.kda:.2f}")
                    embed.add_field(name="Push-ups", value=push_ups)
                    embeds.append(embed)
            LeaguePushUps.matches.append(match)
            if embeds:
                LeaguePushUps.webhook.send(embeds=embeds)
        if LeaguePushUps.windows:
            LeaguePushUps.windows.switch_to_history_view()

    @staticmethod
    def calculate_push_ups(kill_participation: float, kda: float) -> int:
        if kill_participation == 0 or kda == 0:
            return LeaguePushUps.max

        return round(
            min(
                LeaguePushUps.min + \
                    (LeaguePushUps.max/2) / (kda * kill_participation),
                LeaguePushUps.max
            )
        )

    @staticmethod
    def calculate_kill_participation(stats: Stats, team_kills: int) -> float:
        if team_kills:
            return (stats.CHAMPIONS_KILLED + stats.ASSISTS) / team_kills

        return 1


def main() -> None:
    cli_args = CLIArgs().parse_args()
    LeaguePushUps.min = cli_args.min
    LeaguePushUps.max = cli_args.max
    if cli_args.action == "calculate": # type: ignore[attr-defined] # pylint: disable=no-member
        stats = Stats(cli_args.kills, cli_args.deaths, cli_args.assists) # type: ignore[attr-defined] # pylint: disable=no-member
        print(
            LeaguePushUps.calculate_push_ups(
                LeaguePushUps.calculate_kill_participation(stats, cli_args.team_kills), # type: ignore[attr-defined] # pylint: disable=no-member
                stats.kda
            )
        )
    else:
        print(f"Starting with arguments: {cli_args}")
        LeaguePushUps.webhook = SyncWebhook.from_url(cli_args.webhook_url)
        try:
            with LeaguePushUps() as _:
                connector.start()
        except RuntimeError as e:
            print(e)


if __name__ == "__main__":
    main()
