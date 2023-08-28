from attrs import define, field
from requests import Session
from typing import Any, Optional

@define
class RiotClient:
    region: str = "euw1"
    api_key: str = "RGAPI-cd9cf52e-51cc-4c56-8fcd-8dfe4c4623df"
    session: Session = field(factory=Session)

    @property
    def base_url(self) -> str:
        return f"https://{self.region}.api.riotgames.com"

    def get_active_games_by_summoner_id(self, summoner_id: int) -> dict[Any, Any]:
        return self.get(f"lol/spectator/v4/active-games/by-summoner/{summoner_id}")

    def get(self, url: str, data: Optional[dict[str, Any]]=None) -> dict[Any, Any]:
        data = data if data is not None else {}
        response_json = self.session.get(f"{self.base_url}/{url}", data=data).json()
        assert isinstance(response_json, dict)
        return response_json
