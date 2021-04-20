from typing import List
from . import strategy
from . import utils as _utils

utils = _utils.util_functions
constants = _utils.constants


class BasicBombStrategy(strategy.Strategy):
    def execute(self, game_state: object, player_state: object) -> List[str]:
        return [constants.ACTIONS["bomb"]]

    def can_execute(self, game_state: object, player_state: object) -> bool:
        ammo = player_state.ammo
        return ammo > 0
