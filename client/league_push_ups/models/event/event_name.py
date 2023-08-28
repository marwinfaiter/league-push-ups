from enum import Enum


class EventName(Enum):
    GAME_START = "GameStart"
    MINIONS_SPAWNING = "MinionsSpawning"
    FIRST_BLOOD = "FirstBlood"
    FIRST_BRICK = "FirstBrick"
    TURRET_KILLED = "TurretKilled"
    INHIB_KILLED = "InhibKilled"
    INHIB_RESPAWNING_SOON = "InhibRespawningSoon"
    INHIB_RESPAWNED = "InhibRespawned"
    DRAGON_KILL = "DragonKill"
    HERALD_KILL = "HeraldKill"
    BARON_KILL = "BaronKill"
    CHAMPION_KILL = "ChampionKill"
    MULTI_KILL = "Multikill"
    ACE = "Ace"
