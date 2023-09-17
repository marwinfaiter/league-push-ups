from attrs import define
from cattrs import unstructure
from typing import Optional
from aiohttp import ClientSession
from typing import Any

from ..models.match import Match

@define
class BackendClient:
    base_url: str
    session: Optional[ClientSession] = None

    async def __aenter__(self):
        self.session = ClientSession()
        return self

    async def __aexit__(self, *_):
        await self.session.close()
        self.session = None

    async def get(self, url: str):
        async with self.session.get(f"{self.base_url}/{url}") as response:
            response.raise_for_status()
            return await response.json()

    async def post(self, url: str, data: Optional[Any]=None):
        async with self.session.post(f"{self.base_url}/{url}", json=data) as response:
            response.raise_for_status()
            return await response.json()

    async def login(self, username: str, password: str) -> None:
        await self.post("login", {"username": username, "password": password})

    async def send_match(self, session_id: int, game_id: int, match: Match) -> None:
        await self.post(f"match/{session_id}/{game_id}", unstructure(match))

    async def send_match_settings(self, session_id: int, game_id: int) -> None:
        await self.post(f"match_settings/{session_id}/{game_id}")

    async def get_session_id(self) -> int:
        session_id = await self.get("session")
        assert isinstance(session_id, int)
        return session_id
