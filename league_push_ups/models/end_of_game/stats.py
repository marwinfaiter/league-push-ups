from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class Stats:
    kills: int
    deaths: int
    assists: int

    @property
    def kda(self):
        if not self.deaths:
            return self.kills + self.assists

        return (self.kills + self.assists) / self.deaths

    @classmethod
    def from_json(cls, json):
        if not json:
            return None

        return cls(
            json["CHAMPIONS_KILLED"],
            json["NUM_DEATHS"],
            json["ASSISTS"],
        )
