from typing import Any
from pkg_resources import get_distribution

from . import Controller

class StatusController(Controller):
    def get(self) -> dict[str, Any]:
        return {
            "version": get_distribution("league_push_ups_backend").version
        }
