from attrs import define, field
from cattrs import unstructure
from typing import Optional
import requests
from typing import Any

from ..models.event import Event
from ..models.match import Match
from ..models.lobby import Lobby

@define
class BackendClient:
    base_url: str
    session: requests.Session = field(factory=requests.Session)

    def get(self, url: str) -> requests.Response:
        response = self.session.get(f"{self.base_url}/{url}")
        response.raise_for_status()
        return response

    def post(self, url: str, data: Optional[Any]=None) -> requests.Response:
        response = self.session.post(f"{self.base_url}/{url}", json=data)
        response.raise_for_status()
        return response

    def send_events(self, session_id: int, game_id: int, events: set[Event]) -> None:
        self.post(f"events/{session_id}/{game_id}", [unstructure(event) for event in events])

    def send_match(self, session_id: int, game_id: int, match: Match) -> None:
        self.post(f"match/{session_id}/{game_id}", unstructure(match))

    def send_lobby(self, session_id: int, game_id: int, lobby: Lobby) -> None:
        self.post(f"lobby/{session_id}/{game_id}", unstructure(lobby))

    def get_session_id(self) -> int:
        response = self.get("session")
        session_id = response.json()
        assert isinstance(session_id, int)
        return session_id