from dataclasses import dataclass
import json


from league_push_ups.models.game_update.payload import Payload

@dataclass(frozen=True, slots=True)
class GameUpdate:
    payload: Payload
    timestamp: int

    @classmethod
    def from_json(cls, data):
        return cls(
            Payload.from_json(json.loads(data["payload"])),
            data["timestamp"]
        )
