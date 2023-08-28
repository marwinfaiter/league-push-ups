from attrs import frozen
from typing import Type

from .event_name import EventName
from .dragon_type import DragonType

@frozen
class Event:
    EventID: int
    EventName: EventName
    EventTime: float

    def return_corrent_event_class(self) -> "Type[Event]":
        match self.EventName:
            case EventName.GAME_START:
                return GameStart
            case EventName.MINIONS_SPAWNING:
                return MinionsSpawning
            case EventName.FIRST_BLOOD:
                return FirstBlood
            case EventName.FIRST_BRICK:
                return FirstBrick
            case EventName.TURRET_KILLED:
                return TurretKilled
            case EventName.INHIB_KILLED:
                return InhibKilled
            case EventName.INHIB_RESPAWNING_SOON:
                return InhibRespawningSoon
            case EventName.INHIB_RESPAWNED:
                return InhibRespawned
            case EventName.DRAGON_KILL:
                return DragonKill
            case EventName.HERALD_KILL:
                return HeraldKill
            case EventName.BARON_KILL:
                return BaronKill
            case EventName.CHAMPION_KILL:
                return ChampionKill
            case EventName.MULTI_KILL:
                return Multikill
            case EventName.ACE:
                return Ace

@frozen
class GameStart(Event):
    ...

@frozen
class MinionsSpawning(Event):
    ...

@frozen
class FirstBrick(Event):
    KillerName: str

@frozen
class FirstBlood(Event):
    Recipient: str

@frozen
class Kill(Event):
    KillerName: str
    Assisters: tuple[str, ...]

@frozen
class CreatureKill(Kill):
    Stolen: bool

@frozen
class TurretKilled(Kill):
    TurretKilled: str

@frozen
class InhibKilled(Kill):
    InhibKilled: str

@frozen
class InhibRespawningSoon(Event):
    InhibRespawningSoon: str

@frozen
class InhibRespawned(Event):
    InhibRespawned: str

@frozen
class DragonKill(CreatureKill):
    DragonType: DragonType

@frozen
class HeraldKill(CreatureKill):
    ...

@frozen
class BaronKill(CreatureKill):
    ...

@frozen
class ChampionKill(Kill):
    VictimName: str

@frozen
class Multikill(Event):
    KillerName: str
    KillStreak: int

@frozen
class Ace(Event):
    Acer: str
    AcingTeam: str
