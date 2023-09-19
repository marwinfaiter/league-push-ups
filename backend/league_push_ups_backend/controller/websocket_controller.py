from flask_socketio import Namespace, join_room, leave_room
from flask_login import current_user
from flask import request

from peewee import IntegrityError

from ..models.database.match import Match
from ..models.database.match_player import MatchPlayer
from ..models.database.event import Event
from ..models.database.assister import Assister
from ..models.database.user.summoner import Summoner
from ..models.database.base_model import database

class WebsocketController(Namespace):
    def on_connect(self):
        pass

    def on_disconnect(self):
        pass

    def on_get_live_games(self):
        for room in list(self.server.manager.rooms[self.namespace].keys()):
            if match := Match.get_or_none(Match.MatchID==room):
                self.emit(
                    "events",
                    {
                        "match_id": room,
                        "event_time": Event.select(
                                Event.EventTime
                            ).where(
                                Event.Match == match.id,
                                Event.EventName == "ChampionKill"
                            ).order_by(
                                Event.EventTime.desc()
                            ).get_or_none() or 0,
                        "match_players": list(
                            MatchPlayer.select(
                                MatchPlayer,
                                MatchPlayer.kda.cast("float").alias("kda"),
                                MatchPlayer.kill_participation.cast("float").alias("kill_participation"),
                                MatchPlayer.push_ups.cast("int").alias("push_ups")
                            ).join(
                                Match
                            ).where(
                                MatchPlayer.Match == match.id
                            ).dicts()
                        )
                    },
                    room=request.sid
                )

    def on_game_start(self, data):
        if not current_user.is_authenticated:
            raise ConnectionAbortedError("You are not authenticated")

        session_id = data["session_id"]
        match_id = data["match_id"]
        players = data["players"]
        match = Match.create(
            Session=session_id,
            MatchID=match_id,
        )
        for player in players:
            if summoner := Summoner.get_or_none(Summoner.name == player):
                MatchPlayer.create(
                    Match=match.id,
                    User=summoner.user.id,
                    SummonerName=player,
                    MinPushUps=summoner.user.minimum_push_ups,
                    MaxPushUps=summoner.user.maximum_push_ups,
                    PushUpsFinished=summoner.user.active,
                )

        self.emit(
            "events",
            {
                "match_id": match_id,
                "event_time": 0,
                "match_players": list(
                    MatchPlayer.select(
                        MatchPlayer,
                        MatchPlayer.kda.cast("float").alias("kda"),
                        MatchPlayer.kill_participation.cast("float").alias("kill_participation"),
                        MatchPlayer.push_ups.cast("int").alias("push_ups")
                    ).join(
                        Match
                    ).where(
                        MatchPlayer.Match == match.id
                    ).dicts()
                )
            },
            room="frontend"
        )

    def on_events(self, data):
        if not current_user.is_authenticated:
            raise ConnectionAbortedError("You are not authenticated")
        assert isinstance(data, dict)
        match_id = data["match_id"]
        events = data["events"]
        scores = data.get("scores", [])
        with database.atomic() as _:
            match = Match.get(
                MatchID=match_id,
            )
            if scores:
                match.TeamKills = sum(score["kills"] for score in scores)

            match.save()

            for event in events:
                assisters = event.pop("Assisters", [])
                try:
                    event_model = Event.create(
                        Match=match.id,
                        **event
                    )
                except IntegrityError:
                    continue

                for assister in assisters:
                    Assister.get_or_create(
                        Event=event_model.id,
                        Assister=assister
                    )
                if event_model.EventName == "ChampionKill":
                    if killer := MatchPlayer.get_or_none(Match=match.id, SummonerName=event_model.KillerName):
                        killer.Kills += 1
                        killer.save()

                    if victim := MatchPlayer.get_or_none(Match=match.id, SummonerName=event_model.VictimName):
                        victim.Deaths += 1
                        victim.save()

                    for assister in assisters:
                        if match_player := MatchPlayer.get_or_none(Match=match.id, SummonerName=assister):
                            match_player.Assists += 1
                            match_player.save()

                    self.emit(
                        "events",
                        {
                            "match_id": match_id,
                            "event_time": event_model.EventTime,
                            "match_players": list(
                                MatchPlayer.select(
                                    MatchPlayer,
                                    MatchPlayer.kda.cast("float").alias("kda"),
                                    MatchPlayer.kill_participation.cast("float").alias("kill_participation"),
                                    MatchPlayer.push_ups.cast("int").alias("push_ups")
                                ).join(
                                    Match
                                ).where(
                                    MatchPlayer.Match == match.id
                                ).dicts()
                            )
                        },
                        room="frontend"
                    )

    def on_join(self, room):
        self.emit("join", room, room="frontend")
        join_room(room)

    def on_leave(self, room):
        self.emit("leave", room, room="frontend")
        leave_room(room)
