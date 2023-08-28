from attrs import define, field
from cattrs import structure
import requests
from urllib3.exceptions import InsecureRequestWarning
from typing import Any

from ..models.event import Event

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning) # type: ignore[attr-defined] # pylint: disable=no-member

@define
class GameClient:
    session: requests.Session = field(factory=requests.Session)

    @property
    def base_url(self) -> str:
        return "https://127.0.0.1:2999/liveclientdata"

    def  get_events(self) -> set[Event]:
        events_dict = self.get("eventdata")
        return {
            structure(
                event,
                structure(event, Event).return_corrent_event_class()
            )
            for event in events_dict["Events"]
        }

    def get(self, url: str) -> dict[Any, Any]:
        response = self.session.get(f"{self.base_url}/{url}", verify=False)
        response.raise_for_status()
        response_json = response.json()
        assert isinstance(response_json, dict)
        return response_json
