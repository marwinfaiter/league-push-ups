from flask import request
from flask_login import login_required
from peewee import DoesNotExist

from . import Controller
from ..models.database.match import Match
from ..models.database.match_player import MatchPlayer
from ..models.database.event import Event
from ..models.database.assister import Assister
from ..models.database.base_model import database

class ClientEventsController(Controller):
    @login_required
    def post(self, session_id: str, match_id: int) -> None:
        events = request.get_json()
        assert isinstance(events, list)
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
                if assisters:
                    for assister in assisters:
                        Assister.get_or_create(
                            Event=event_model.id,
                            Assister=assister
                        )
                if event_model.EventName == "ChampionKill":
                    match.TeamKills += 1
                    try:
                        killer = MatchPlayer.get(Match=match.id, SummonerName=event_model.KillerName)
                        killer.Kills += 1
                        killer.save()
                    except DoesNotExist:
                        pass
                    try:
                        victim = MatchPlayer.get(Match=match.id, SummonerName=event_model.VictimName)
                        victim.Deaths += 1
                        victim.save()
                    except DoesNotExist:
                        pass

                    for assister in assisters:
                        try:
                            assister_model = MatchPlayer.get(Match=match.id, SummonerName=assister)
                            assister_model.Assists += 1
                            assister_model.save()
                        except DoesNotExist:
                            pass
            match.save()
