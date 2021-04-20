from typing import List
import random
from . import strategy
from . import utils as _utils

utils = _utils.util_functions
ACTIONS = _utils.constants.ACTIONS


class MoveStrategy(strategy.Strategy):
    def execute(self, game_state: object, player_state: object) -> List[str]:
        location = player_state.location
        surrounding_tiles = utils.get_surrounding_tiles(location, game_state)
        empty_tiles = utils.get_empty_tiles(surrounding_tiles, game_state)

        if empty_tiles:
            # TODO make decision based on future path
            random_tile = random.choice(empty_tiles)
            return [utils.move_to_tile(location, random_tile)]
        else:
            return [ACTIONS["none"]]

    def can_execute(self, game_state: object, player_state: object) -> bool:
        return True
