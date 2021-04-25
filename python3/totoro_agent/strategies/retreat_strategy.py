from typing import List
from copy import deepcopy

from . import strategy
from ..utils.constants import ACTIONS
from ..utils.util_functions import get_value_map, get_value_map_objects_from_arr, get_blast_zone


class RetreatStrategy(strategy.Strategy):

    def __init__(self):
        self.reward_map = {
            'hazard': -4,
        }

    def execute(self, game_state: object) -> List[str]:
        danger_bombs = deepcopy(game_state['enemy_active_bombs'])
        own_bombs = game_state['own_active_bombs']
        world = game_state['world']
        for bomb in own_bombs:
            ttl = (bomb['expires'] - game_state['tick'])
            if ttl == 1:  # need to GTFO!
                danger_bombs.append(bomb)
        hazards = []
        for bomb in danger_bombs:
            blast_zone = get_blast_zone(bomb['coord'], bomb['blast_diameter'], game_state['entities'], world)
            hazards += blast_zone
        hazard_objects = get_value_map_objects_from_arr(hazards, 'hazard')
        game_objects = hazard_objects + game_state["non_wall_blocks"]
        value_map = get_value_map(world, game_state["wall_blocks"], game_objects, self.reward_map)
        # get the adjacent tile that has the maximum value
        return [ACTIONS["none"]]
