from unittest import IsolatedAsyncioTestCase
from mockito import expect, unstub, ANY, mock, verifyNoUnwantedInteractions
from attrs import define
from cattrs import structure
from league_push_ups.__main__ import LeaguePushUps
from league_push_ups.models.end_of_game.eog_stats_block import EOGStatsBlock
from league_push_ups.models.end_of_game.player import Player
from league_push_ups.models.lobby import Lobby
from league_push_ups.models.lobby.member import Member
from league_push_ups.models.lobby.game_mode import GameMode
from league_push_ups.models.match import Match
from discord import SyncWebhook

class TestLeaguePushUps(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        LeaguePushUps.webhook = SyncWebhook.from_url(f"https://discord.com/api/webhooks/{0:020d}/{0:060d}")
        LeaguePushUps.min = 10
        LeaguePushUps.max = 50
        LeaguePushUps.game_id = None
        LeaguePushUps.lobby = None

    def tearDown(self) -> None:
        verifyNoUnwantedInteractions()
        unstub()

    async def test_lobby_create(self) -> None:
        await LeaguePushUps.lobby_create(None, ExampleLobby())
        assert LeaguePushUps.lobby == structure(ExampleLobby.data, Lobby)

    async def test_lobby_members_update(self) -> None:
        await LeaguePushUps.lobby_create(None, ExampleLobby())
        await LeaguePushUps.lobby_members_update(None, ExampeMemberUpdate())
        if LeaguePushUps.lobby:
            assert LeaguePushUps.lobby.members == [Member("TEST")]

    async def test_lobby_delete(self) -> None:
        await LeaguePushUps.lobby_create(None, ExampleLobby())
        await LeaguePushUps.lobby_delete(None, None)
        assert LeaguePushUps.lobby is None

    async def test_game_start(self) -> None:
        await LeaguePushUps.lobby_create(None, ExampleLobby())
        await LeaguePushUps.game_update(None, ExampleGameStart())
        assert LeaguePushUps.game_id is not None

    async def test_game_end(self) -> None:
        LeaguePushUps.webhook = mock(spec=SyncWebhook)
        expect(LeaguePushUps.webhook, times=1).send(embeds=ANY).thenReturn(True)
        await LeaguePushUps.lobby_create(None, ExampleLobby())
        await LeaguePushUps.game_end(None, ExampleGameEnd())
        await LeaguePushUps.game_update(None, ExampleGameEndUpdate())
        example_game_end = structure(ExampleGameEnd().data, EOGStatsBlock)
        assert LeaguePushUps.matches == [
            Match(
                example_game_end.teams[0].stats.CHAMPIONS_KILLED,
                [
                    Player(player.summonerName, player.teamId, player.stats)
                    for player in example_game_end.teams[0].players
                ]
            )
        ]
        assert LeaguePushUps.game_id is None

@define
class ExampeMemberUpdate:
    data = [{
        "allowedChangeActivity": True,
        "allowedInviteOthers": True,
        "allowedKickOthers": True,
        "allowedStartActivity": True,
        "allowedToggleInvite": True,
        "autoFillEligible": False,
        "autoFillProtectedForPromos": False,
        "autoFillProtectedForSoloing": False,
        "autoFillProtectedForStreaking": False,
        "botChampionId": 0,
        "botDifficulty": "NONE",
        "botId": "",
        "firstPositionPreference": "",
        "isBot": False,
        "isLeader": True,
        "isSpectator": False,
        "primaryChampionPreference": 0,
        "puuid": "f68bf6b7-5b10-5e62-b714-8b115091c757",
        "ready": True,
        "secondPositionPreference": "",
        "secondaryChampionPreference": 0,
        "showGhostedBanner": False,
        "summonerIconId": 907,
        "summonerId": 27926438,
        "summonerInternalName": "TEST",
        "summonerLevel": 270,
        "summonerName": "TEST",
        "teamId": 0
    }]

@define
class ExampleLobby:
    type = GameMode.ARAM
    data = {
        "canStartActivity": True,
        "gameConfig": {
            "allowablePremadeSizes": [
                1,
                2,
                3,
                4,
                5
            ],
            "customLobbyName": "Custom Lobby",
            "customMutatorName": "",
            "customRewardsDisabledReasons": [],
            "customSpectatorPolicy": "NotAllowed",
            "customSpectators": [],
            "customTeam100": [],
            "customTeam200": [],
            "gameMode": "ARAM",
            "isCustom": False,
            "isLobbyFull": False,
            "isTeamBuilderManaged": False,
            "mapId": 12,
            "maxHumanPlayers": 0,
            "maxLobbySize": 5,
            "maxTeamSize": 5,
            "pickType": "",
            "premadeSizeAllowed": True,
            "queueId": 450,
            "shouldForceScarcePositionSelection": False,
            "showPositionSelector": False
        },
        "invitations": [
            {
                "invitationId": "",
                "invitationType": "invalid",
                "state": "Accepted",
                "timestamp": "0",
                "toSummonerId": 27926438,
                "toSummonerName": "Marwinfaiter"
            }
        ],
        "localMember": {
            "allowedChangeActivity": True,
            "allowedInviteOthers": True,
            "allowedKickOthers": True,
            "allowedStartActivity": True,
            "allowedToggleInvite": True,
            "autoFillEligible": False,
            "autoFillProtectedForPromos": False,
            "autoFillProtectedForSoloing": False,
            "autoFillProtectedForStreaking": False,
            "botChampionId": 0,
            "botDifficulty": "NONE",
            "botId": "",
            "firstPositionPreference": "",
            "isBot": False,
            "isLeader": True,
            "isSpectator": False,
            "primaryChampionPreference": 0,
            "puuid": "f68bf6b7-5b10-5e62-b714-8b115091c757",
            "ready": True,
            "secondPositionPreference": "",
            "secondaryChampionPreference": 0,
            "showGhostedBanner": False,
            "summonerIconId": 907,
            "summonerId": 27926438,
            "summonerInternalName": "Marwinfaiter",
            "summonerLevel": 270,
            "summonerName": "Marwinfaiter",
            "teamId": 0
        },
        "members": [
            {
                "allowedChangeActivity": True,
                "allowedInviteOthers": True,
                "allowedKickOthers": True,
                "allowedStartActivity": True,
                "allowedToggleInvite": True,
                "autoFillEligible": False,
                "autoFillProtectedForPromos": False,
                "autoFillProtectedForSoloing": False,
                "autoFillProtectedForStreaking": False,
                "botChampionId": 0,
                "botDifficulty": "NONE",
                "botId": "",
                "firstPositionPreference": "",
                "isBot": False,
                "isLeader": True,
                "isSpectator": False,
                "primaryChampionPreference": 0,
                "puuid": "f68bf6b7-5b10-5e62-b714-8b115091c757",
                "ready": True,
                "secondPositionPreference": "",
                "secondaryChampionPreference": 0,
                "showGhostedBanner": False,
                "summonerIconId": 907,
                "summonerId": 27926438,
                "summonerInternalName": "Marwinfaiter",
                "summonerLevel": 270,
                "summonerName": "Marwinfaiter",
                "teamId": 0
            }
        ],
        "mucJwtDto": {
            "channelClaim": "",
            "domain": "",
            "jwt": "",
            "targetRegion": ""
        },
        "multiUserChatId": "8976d18f-1406-4016-8bed-51dd3a819b9d",
        "multiUserChatPassword": "8976d18f-1406-4016-8bed-51dd3a819b9d",
        "partyId": "8976d18f-1406-4016-8bed-51dd3a819b9d",
        "partyType": "open",
        "restrictions": [],
        "scarcePositions": [],
        "warnings": []
    }

@define
class ExampleGameEndUpdate:
    data = {
        "payload": "{\"id\":6568491591,\"gameState\":\"TERMINATED\",\"gameType\":\"\"}",
        "timestamp": 1693078946955,
    }

@define
class ExampleGameStart:
    data = {
        "payload": "{\"id\":6568491591,\"gameState\":\"START_REQUESTED\",\"gameType\":\"PRACTICE_GAME\"}",
        "timestamp": 1693078946955,
    }

@define
class ExampleGameEnd:
    data = {
        "accountId": 0,
        "basePoints": 0,
        "battleBoostIpEarned": 0,
        "boostIpEarned": 0,
        "boostXpEarned": 0,
        "causedEarlySurrender": True,
        "championId": 0,
        "coOpVsAiMinutesLeftToday": 0,
        "coOpVsAiMsecsUntilReset": 0,
        "completionBonusPoints": 0,
        "currentLevel": 0,
        "customMinutesLeftToday": 0,
        "customMsecsUntilReset": 0,
        "difficulty": "string",
        "earlySurrenderAccomplice": True,
        "elo": 0,
        "eloChange": 0,
        "experienceEarned": 0,
        "experienceTotal": 0,
        "firstWinBonus": 0,
        "gameEndedInEarlySurrender": True,
        "gameId": 0,
        "gameLength": 0,
        "gameMode": "ARAM",
        "gameMutators": [
            "string"
        ],
        "gameType": "string",
        "globalBoostXpEarned": 0,
        "imbalancedTeamsNoPoints": True,
        "invalid": True,
        "ipEarned": 0,
        "ipTotal": 0,
        "leveledUp": True,
        "loyaltyBoostIpEarned": 0,
        "loyaltyBoostXpEarned": 0,
        "missionsXpEarned": 0,
        "myTeamStatus": "string",
        "newSpells": [
            0
        ],
        "nextLevelXp": 0,
        "odinBonusIp": 0,
        "partyRewardsBonusIpEarned": 0,
        "pointsPenalties": {
            "additionalProp1": {}
        },
        "preLevelUpExperienceTotal": 0,
        "preLevelUpNextLevelXp": 0,
        "previousLevel": 0,
        "previousXpTotal": 0,
        "queueBonusEarned": 0,
        "queueType": "string",
        "ranked": True,
        "reportGameId": 0,
        "rerollData": {
            "pointChangeFromChampionsOwned": 0,
            "pointChangeFromGameplay": 0,
            "pointsUntilNextReroll": 0,
            "pointsUsed": 0,
            "previousPoints": 0,
            "rerollCount": 0,
            "totalPoints": 0
        },
        "roomName": "string",
        "roomPassword": "string",
        "rpEarned": 0,
        "sendStatsToTournamentProvider": True,
        "skinId": 0,
        "skinIndex": 0,
        "summonerId": 0,
        "summonerName": "string",
        "talentPointsGained": 0,
        "teamBoost": {
            "availableSkins": [
            0
            ],
            "ipReward": 0,
            "ipRewardForPurchaser": 0,
            "price": 0,
            "skinUnlockMode": "string",
            "summonerName": "string",
            "unlocked": True
        },
        "teamEarlySurrendered": True,
        "teams": [
            {
            "championBans": [
                0
            ],
            "fullId": "string",
            "isBottomTeam": True,
            "isPlayerTeam": True,
            "isWinningTeam": True,
            "memberStatusString": "string",
            "name": "string",
            "players": [
                {
                "botPlayer": True,
                "championId": 0,
                "detectedTeamPosition": "string",
                "elo": 0,
                "eloChange": 0,
                "gameId": 0,
                "isReportingDisabled": True,
                "items": [
                    0
                ],
                "leaver": True,
                "leaves": 0,
                "level": 0,
                "losses": 0,
                "profileIconId": 0,
                "selectedPosition": "string",
                "skinIndex": 0,
                "skinName": "string",
                "spell1Id": 0,
                "spell2Id": 0,
                "stats": {
                    "CHAMPIONS_KILLED": 5,
                    "NUM_DEATHS": 10,
                    "ASSISTS": 20,
                },
                "summonerId": 0,
                "summonerName": "Marwinfaiter",
                "teamId": 0,
                "userId": 0,
                "wins": 0
                }
            ],
            "stats": {
                "CHAMPIONS_KILLED": 20,
                "NUM_DEATHS": 40,
                "ASSISTS": 30,
            },
            "tag": "string",
            "teamId": 0
            }
        ],
        "timeUntilNextFirstWinBonus": 0,
        "userId": 0
    }
