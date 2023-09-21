from typing import Any
import pkg_resources

from . import Controller

class StatusController(Controller):
    def get(self) -> dict[str, Any]:
        return {
            "version": pkg_resources.require("league_push_ups_backend")[0].version
        }
