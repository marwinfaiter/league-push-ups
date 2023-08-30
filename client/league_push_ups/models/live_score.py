from attrs import frozen

@frozen
class LiveScore:
    summonerName: str
    kills: int
    deaths: int
    assists: int
    creepScore: int
    wardScore: float
