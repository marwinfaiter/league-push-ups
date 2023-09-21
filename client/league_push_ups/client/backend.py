from attrs import define
from cattrs import unstructure
from typing import Optional
from requests import Session
from typing import Any

from ..models.match import Match

@define
class BackendClient:
    base_url: str
    session: Session = Session()

    def get(self, url: str) -> Any:
        with self.session.get(f"{self.base_url}/{url}") as response:
            response.raise_for_status()
            return response.json()

    def post(self, url: str, data: Optional[Any]=None) -> Any:
        with self.session.post(f"{self.base_url}/{url}", json=data) as response:
            response.raise_for_status()
            return response.json()

    def login(self, username: str, password: str) -> None:
        self.post("login", {"username": username, "password": password})

    def send_match(self, session_id: int, game_id: int, match: Match) -> None:
        self.post(f"match/{session_id}/{game_id}", unstructure(match))

    def get_session_id(self) -> int:
        session_id = self.get("session")
        assert isinstance(session_id, int)
        return session_id
