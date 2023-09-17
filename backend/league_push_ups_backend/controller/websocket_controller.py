from flask_socketio import Namespace, join_room, leave_room
from flask_login import current_user

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

    def on_events(self, data):
        if not current_user.is_authenticated:
            raise ConnectionAbortedError("You are not authenticated")
        assert isinstance(data, dict)
        session_id = data["session_id"]
        match_id = data["match_id"]
        events = data["events"]
        scores = data.get("scores", [])
        with database.atomic() as _:
            match, _ = Match.get_or_create(
                Session=session_id,
                MatchID=match_id,
            )
            for event in events:
                assisters = event.pop("Assisters", [])
                event_model, _ = Event.get_or_create(
                    Match=match.id,
                    **event
                )
                for assister in assisters:
                    Assister.get_or_create(
                        Event=event_model.id,
                        Assister=assister
                    )

            if scores:
                match.TeamKills = sum(score["kills"] for score in scores)
                for score in scores:
                    if summoner := Summoner.get_or_none(name=score["summonerName"]):
                        match_player, _ = MatchPlayer.get_or_create(
                            Match=match.id,
                            User=summoner.user.id,
                            SummonerName=score["summonerName"],
                            MinPushUps=summoner.user.minimum_push_ups,
                            MaxPushUps=summoner.user.maximum_push_ups,
                            PushUpsFinished=summoner.user.active,
                        )
                        match_player.Kills = score["kills"]
                        match_player.Deaths = score["deaths"]
                        match_player.Assists = score["assists"]
                        match_player.save()
            match.save()

    def on_join(self, room):
        join_room(room)

    def on_leave(self, room):
        leave_room(room)
