from dataclasses import dataclass
from .stats import Stats

@dataclass(frozen=True, slots=True)
class Player:
    summoner_name: str
    team: int
    stats: Stats

    @classmethod
    def from_json(cls, json):
        return cls(
            json["summonerName"],
            json["teamId"],
            Stats.from_json(
                json["stats"]
            )
        )
