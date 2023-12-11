from typing import Any, Optional

import requests
from attrs import define, field
from cattrs import structure
from urllib3.exceptions import InsecureRequestWarning

from ..models.event import Event
from ..models.live_score import LiveScore

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning) # type: ignore[attr-defined] # pylint: disable=no-member

@define
class GameClient:
    session: requests.Session = field(factory=requests.Session)

    @property
    def base_url(self) -> str:
        return "https://127.0.0.1:2999/liveclientdata"

    def get_all_game_data(self) -> dict[str, Any]:
        response = self.get("allgamedata")
        response_json = response.json()
        assert isinstance(response_json, dict)
        return response_json

    def get_events(self) -> set[Event]:
        response = self.get("eventdata")
        response_json = response.json()
        assert isinstance(response_json, dict)
        return {
            structure(
                event,
                structure(event, Event).return_corrent_event_class()
            )
            for event in response_json["Events"]
        }

    def get_scores_for_team(self) -> tuple[LiveScore, ...]:
        game_data = self.get_all_game_data()
        scores = []
        active_player = next(
            player
            for player in game_data["allPlayers"]
            if game_data["activePlayer"]["summonerName"].startswith(player["summonerName"])
        )
        for player in game_data["allPlayers"]:
            if player["team"] != active_player["team"]:
                continue
            scores.append(LiveScore(
                player["summonerName"],
                player["scores"]["kills"],
                player["scores"]["deaths"],
                player["scores"]["assists"],
                player["scores"]["creepScore"],
                player["scores"]["wardScore"],
            ))

        return tuple(scores)

    def get(self, url: str, params: Optional[dict[str, Any]]=None) -> requests.Response :
        response = self.session.get(f"{self.base_url}/{url}", verify=False, params=params)
        response.raise_for_status()
        return response
