from attrs import define

@define(frozen=True)
class Stats:
    CHAMPIONS_KILLED: int
    NUM_DEATHS: int
    ASSISTS: int

    @property
    def kda(self):
        if not self.NUM_DEATHS:
            return self.CHAMPIONS_KILLED + self.ASSISTS

        return (self.CHAMPIONS_KILLED + self.ASSISTS) / self.NUM_DEATHS
