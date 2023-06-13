from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class Member:
    summoner_name: str

    @classmethod
    def from_json(cls, json):
        return cls(json["summonerName"])
