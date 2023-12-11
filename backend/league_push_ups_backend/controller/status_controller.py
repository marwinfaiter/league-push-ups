from importlib.metadata import version
from typing import Any

from . import Controller


class StatusController(Controller):
    def get(self) -> dict[str, Any]:
        return {
            "version": version("league_push_ups_backend")
        }
