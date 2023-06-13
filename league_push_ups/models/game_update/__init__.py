from dataclasses import dataclass
import json

from .payload import Payload

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
