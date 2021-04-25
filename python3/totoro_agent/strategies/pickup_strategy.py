from typing import List

from . import strategy
from ..utils.util_functions import get_shortest_path, manhattan_distance
from ..utils.constants import ACTIONS


class PickupStrategy(strategy.Strategy):

    def execute(self, game_state: object) -> List[str]:
        # if power up priority is ammo_powerup
        # go for closest pickup powerup
        # else
        # go for closest ammo
        return [ACTIONS["none"]]
