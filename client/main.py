import asyncio
import sys
from importlib.metadata import version
from json import loads
from typing import Optional

import requests.exceptions
from aiohttp import ClientSession
from cattrs import structure, unstructure
from lcu_driver import Connector
from lcu_driver.connection import Connection
from lcu_driver.events.responses import WebsocketEventResponse
from league_push_ups.client.backend import BackendClient
from league_push_ups.client.game import GameClient
from league_push_ups.connector_start_patch import start
from league_push_ups.models.cli_args import CLIArgs
from league_push_ups.models.end_of_game.eog_stats_block import EOGStatsBlock
from league_push_ups.models.event import Event
from league_push_ups.models.event.event_name import EventName
from league_push_ups.models.game_update import GameUpdate
from league_push_ups.models.game_update.game_state import GameState
from league_push_ups.models.game_update.game_type import GameType
from league_push_ups.models.lobby import Lobby
from league_push_ups.models.lobby.member import Member
from league_push_ups.models.match import Match
from league_push_ups.run_ws_patch import run_ws
from packaging.version import parse
from socketio import AsyncClient

__version__ = version("league_push_ups")

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
    async def lobby_members_update(_connection: Connection, event: WebsocketEventResponse) -> None:
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
        await sio.call("join", game_id)

        assert isinstance(LeaguePushUps.lobby, Lobby)
        await sio.call(
            "game_start",
            {
                "session_id": LeaguePushUps.session_id,
                "match_id": LeaguePushUps.game_id,
                "players": [member.summonerName for member in LeaguePushUps.lobby.members]
            }
        )
        while LeaguePushUps.game_id:
            try:
                await asyncio.sleep(1)
                events = LeaguePushUps.game_client.get_events()
                new_events = events - LeaguePushUps.events
                if new_events:
                    LeaguePushUps.events = LeaguePushUps.events | new_events

                    payload = {
                        "match_id": LeaguePushUps.game_id,
                        "events": [unstructure(event) for event in sorted(new_events, key=lambda x: x.EventTime)]
                    }
                    if any(event.EventName == EventName.CHAMPION_KILL for event in new_events):
                        scores = LeaguePushUps.game_client.get_scores_for_team()
                        payload["scores"] = [unstructure(score) for score in scores]

                    await sio.emit("events", payload)

            except (requests.exceptions.ConnectionError, requests.exceptions.HTTPError):
                pass

        await sio.call("leave", game_id)
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

async def run() -> None:
    try:
        async with ClientSession() as session:
            cli_args = CLIArgs().parse_args()
            LeaguePushUps.backend_client = BackendClient(cli_args.backend_url, session)

            backend_status = await LeaguePushUps.backend_client.get_status()
            print(f"League Push Ups client version: {__version__}")
            print(f"League Push Ups backend version: {backend_status['version']}")
            if parse(__version__) < parse(backend_status['version']):
                print("\nYour client version is behind the backend.\n"
                      "Please download the matching version:\n"
                      "https://nexus.buddaphest.se/repository/raw/league-push-ups/"
                      f"leaguepushups-{ backend_status['version'] }.exe"
                )

            await LeaguePushUps.backend_client.login(cli_args.get_username(), cli_args.get_password())
            LeaguePushUps.session_id = await LeaguePushUps.backend_client.get_session_id()
            print("Looking for client...")
            await connector.start()
    except (KeyboardInterrupt, asyncio.exceptions.CancelledError):
        print("Client stopped")

def main() -> None:
    asyncio.run(run())

if __name__ == "__main__":
    main()
