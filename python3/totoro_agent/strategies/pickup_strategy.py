from typing import List

from . import strategy
from ..utils.util_functions import get_shortest_path
from ..utils.constants import ACTIONS


class PickupStrategy(strategy.Strategy):

    def execute(self, game_state: object) -> List[str]:
        # TODO algorithm here for pickup
        return [ACTIONS["none"]]
