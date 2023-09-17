from typing import Optional
from json import loads
from cattrs import structure, unstructure
import asyncio
from socketio import AsyncClient
import requests.exceptions

from lcu_driver import Connector
from lcu_driver.connection import Connection
from lcu_driver.events.responses import WebsocketEventResponse

from .models.game_update import GameUpdate
from .models.game_update.game_state import GameState
from .models.game_update.game_type import GameType
from .models.lobby import Lobby
from .models.lobby.member import Member
from .models.end_of_game.eog_stats_block import EOGStatsBlock
from .models.cli_args import CLIArgs
from .models.match import Match
from .client.game import GameClient
from .client.backend import BackendClient
from .models.event import Event
from .models.event.event_name import EventName
from .run_ws_patch import run_ws
from .connector_start_patch import start

Connection.run_ws = run_ws
Connector.start = start

connector = Connector()

class LeaguePushUps:
    backend_client: BackendClient
    session_id: int
    lobby: Optional[Lobby] = None
    game_id: Optional[int] = None
    events: set[Event] = set()
    game_client: GameClient = GameClient()

    # fired when LCU API is ready to be used
    @staticmethod
    @connector.ready
    async def connect(_connection: Connection) -> None:
        print('LCU API is ready to be used.')

    # fired when League Client is closed (or disconnected from websocket)
    @staticmethod
    @connector.close
    async def disconnect(_connection: Connection) -> None:
        print('The client have been closed!')

    @staticmethod
    @connector.ws.register("/lol-lobby/v2/lobby", event_types=("CREATE","UPDATE"))
    async def lobby_create(_connection: Connection, event: WebsocketEventResponse) -> None:
        LeaguePushUps.lobby = structure(event.data, Lobby)
        if LeaguePushUps.lobby:
            print(f"Lobby {event.type}: {LeaguePushUps.lobby.gameConfig.gameMode.value}")

    @staticmethod
    @connector.ws.register("/lol-lobby/v2/lobby/members", event_types=("UPDATE",))
    async def lobby_members_update(_: Connector, event: WebsocketEventResponse) -> None:
        if LeaguePushUps.lobby:
            print("Updating lobby members")
            LeaguePushUps.lobby.members = tuple(structure(member, Member) for member in event.data)

    @staticmethod
    @connector.ws.register("/lol-lobby/v2/lobby", event_types=("DELETE",))
    async def lobby_delete(_connection: Connection, _event: WebsocketEventResponse) -> None:
        if not LeaguePushUps.game_id:
            print("Deleting lobby")
            LeaguePushUps.lobby = None

    @staticmethod
    @connector.ws.register(
        "/riot-messaging-service/v1/message/lol-gsm-server/v1/gsm/game-update",
        event_types=("CREATE",)
    )
    async def game_update(_connection: Connection, event: WebsocketEventResponse) -> None:
        event.data["payload"] = loads(event.data["payload"])
        game_update = structure(event.data, GameUpdate)

        if game_update.payload.gameState == GameState.START_REQUESTED:
            print(f"Game starting: {game_update.payload.gameType.value}")
            if game_update.payload.gameType == GameType.PRACTICE_GAME:
                print("Not registering PRACTICE_GAME")
                return

            LeaguePushUps.game_id = game_update.payload.id
            assert isinstance(LeaguePushUps.lobby, Lobby)
            await LeaguePushUps.backend_client.send_match_settings(
                LeaguePushUps.session_id,
                LeaguePushUps.game_id,
            )
            await LeaguePushUps.poll_game_data()
        elif game_update.payload.gameState == GameState.TERMINATED:
            print("Game ended")
            LeaguePushUps.game_id = None
        elif game_update.payload.gameState == GameState.TERMINATED_IN_ERROR:
            print("Game exited early")
            LeaguePushUps.game_id = None

    @staticmethod
    async def poll_game_data() -> None:
        print("Started polling live game")
        sio = AsyncClient(http_session=LeaguePushUps.backend_client.session)
        game_id = LeaguePushUps.game_id
        await sio.connect(LeaguePushUps.backend_client.base_url)
        await sio.emit("join", game_id)
        while LeaguePushUps.game_id:
            try:
                await asyncio.sleep(1)
                events = LeaguePushUps.game_client.get_events()
                new_events = events - LeaguePushUps.events
                if new_events:
                    LeaguePushUps.events = LeaguePushUps.events | new_events

                    payload = {
                        "session_id": LeaguePushUps.session_id,
                        "match_id": LeaguePushUps.game_id,
                        "events": [unstructure(event) for event in new_events]
                    }
                    if any(event.EventName == EventName.CHAMPION_KILL for event in new_events):
                        scores = LeaguePushUps.game_client.get_scores_for_team()
                        payload["scores"] = [unstructure(score) for score in scores]

                    await sio.emit("events", payload)

            except (requests.exceptions.ConnectionError, requests.exceptions.HTTPError):
                pass

        await sio.emit("leave", game_id)
        await sio.disconnect()
        LeaguePushUps.events.clear()
        print("Stopped polling live game")

    @staticmethod
    @connector.ws.register('/lol-end-of-game/v1/eog-stats-block', event_types=('CREATE',))
    async def game_end(_connection: Connection, event: WebsocketEventResponse) -> None:
        if LeaguePushUps.lobby is None:
            return

        eog_stats_block = structure(event.data, EOGStatsBlock)
        for team in eog_stats_block.teams:
            if team.stats is None:
                continue

            match = Match(team.stats.CHAMPIONS_KILLED, [
                player
                for player in team.players
                if LeaguePushUps.lobby.is_summoner_member(player.summonerName)
            ])
            if match.players:
                await LeaguePushUps.backend_client.send_match(
                    LeaguePushUps.session_id,
                    eog_stats_block.gameId,
                    match
                )

async def run(cli_args: CLIArgs):
    async with BackendClient(cli_args.backend_url) as backend_client:
        LeaguePushUps.backend_client = backend_client
        await LeaguePushUps.backend_client.login(cli_args.username, cli_args.password)
        LeaguePushUps.session_id = await LeaguePushUps.backend_client.get_session_id()
        await connector.start()

def main() -> None:
    asyncio.run(
        run(
            CLIArgs().parse_args()
        )
    )

if __name__ == "__main__":
    main()
