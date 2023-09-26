from flask_socketio import Namespace, join_room, leave_room
from flask_login import current_user
from flask import request
from typing import Any, Union

from peewee import IntegrityError

from ..models.database.match import Match
from ..models.database.match_player import MatchPlayer
from ..models.database.event import Event
from ..models.database.assister import Assister
from ..models.database.user.summoner import Summoner
from ..models.database.base_model import database

class WebsocketController(Namespace):
    def on_connect(self) -> None:
        pass

    def on_disconnect(self) -> None:
        pass

    def on_get_live_games(self) -> None:
        for room in list(self.server.manager.rooms[self.namespace].keys()):
            if match := Match.get_or_none(Match.MatchID==room):
                self._emit_event_to_room(match, request.sid) # type: ignore[attr-defined]

    def on_game_start(self, data: dict[str, Any]) -> None:
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
                    Match=match.id, # pylint: disable=no-member
                    User=summoner.user.id,
                    SummonerName=player,
                    MinPushUps=summoner.user.minimum_push_ups,
                    MaxPushUps=summoner.user.maximum_push_ups,
                    Active=summoner.user.active,
                )

        self._emit_event_to_room(match)

    def on_events(self, data: dict[str, Any]) -> None:
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
                        Event=event_model.id, # pylint: disable=no-member
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

                    self._emit_event_to_room(match)

    def on_join(self, room: str) -> None:
        self.emit("join", room, room="frontend")
        join_room(room)

    def on_leave(self, room: str) -> None:
        self.emit("leave", room, room="frontend")
        leave_room(room)

    def _emit_event_to_room(self, match: Match, room: Union[str, int]="frontend") -> None:
        last_event = Event.select(
                Event.EventTime
            ).where(
                Event.Match == match.id, # type: ignore[attr-defined]
                Event.EventName == "ChampionKill"
            ).order_by(
                Event.EventTime.desc()
        ).get_or_none()

        self.emit(
            "events",
            {
                "match_id": match.MatchID,
                "event_time": last_event.EventTime if last_event else 0,
                "match_players": MatchPlayer.get_match_players(match.id) # type: ignore[attr-defined]
            },
            room=room
        )
