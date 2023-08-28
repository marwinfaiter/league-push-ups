from attrs import define

from .payload import Payload

@define(frozen=True)
class GameUpdate:
    payload: Payload
    timestamp: int
