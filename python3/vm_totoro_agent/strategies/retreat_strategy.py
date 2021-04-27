from typing import List

from . import strategy
from ..utils.util_functions import get_value_map, get_value_map_objects_from_arr, get_move_from_value_map, get_reachable_tiles


class RetreatStrategy(strategy.Strategy):

    def __init__(self):
        self.reward_map = {
            'hazard': -1,
            'safe': 3,
            'reachable': 1
        }

    def execute(self, game_state: dict) -> List[str]:
        world = game_state['world']
        safe_zones = game_state['safe_zones']
        player_pos = game_state['player_pos']
        entities = game_state['entities']
        reachable = get_reachable_tiles(player_pos, safe_zones, world, entities)
        reachable_objects = get_value_map_objects_from_arr(reachable, 'reachable')
        safe_objects = get_value_map_objects_from_arr(safe_zones, 'safe')
        hazard_objects = get_value_map_objects_from_arr(game_state['hazard_zones'], 'hazard')
        hazard_objects.append(game_state['enemy_obj'])
        game_objects = hazard_objects + safe_objects + reachable_objects
        value_map = get_value_map(world, game_state["wall_blocks"], game_objects, self.reward_map, use_default=False)
        action = get_move_from_value_map(game_state["player_pos"], value_map, world)
        return [action]