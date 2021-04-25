from typing import List
from copy import deepcopy

from . import strategy
from ..utils.constants import ACTIONS
from ..utils.util_functions import get_value_map, get_value_map_object, get_blast_zone


class RetreatStrategy(strategy.Strategy):

    def __init__(self):
        self.reward_map = {
            'potential_blast': -4,
        }

    def execute(self, game_state: object) -> List[str]:
        danger_bombs = deepcopy(game_state['enemy_active_bombs'])
        own_bombs = game_state['own_active_bombs']
        for bomb in own_bombs:
            ttl = (bomb['expires'] - game_state['tick'])
            if ttl == 1:  # need to GTFO!
                danger_bombs.append(bomb)
        blast_zones = []
        for bomb in danger_bombs:
            pass
        # combine blast zones
        # convert to value map objects
        # get value map
        # get the adjacent tile that has the maximum value
        return [ACTIONS["none"]]
