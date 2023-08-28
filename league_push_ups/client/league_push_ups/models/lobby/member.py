from attrs import define

@define(frozen=True)
class Member:
    summonerId: int
    summonerName: str
