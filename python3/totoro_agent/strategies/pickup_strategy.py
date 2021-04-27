from typing import List
from . import strategy
from ..utils.util_functions import get_shortest_path, get_path_action_seq, get_nearest_tile, get_reachable_tiles
from ..utils.constants import ACTIONS


class PickupStrategy(strategy.Strategy):

    def execute(self, game_state: object) -> List[str]:
        path = None
        player_pos = tuple(game_state['player_pos'])
        ammo_list = game_state['ammo_list']
        powerup_list = game_state['powerup_list']
        world = game_state['world']
        entities = game_state['entities']

        if ammo_list:
            reachable_ammo = get_reachable_tiles(player_pos, ammo_list, world, entities,game_state['hazard_zones'])
            nearest_ammo = get_nearest_tile(player_pos, reachable_ammo)
            path = get_shortest_path(player_pos, nearest_ammo, world, entities)
        elif powerup_list:
            reachable_powerup = get_reachable_tiles(player_pos, powerup_list, world, entities)
            nearest_powerup = get_nearest_tile(player_pos, reachable_powerup)
            path = get_shortest_path(player_pos, nearest_powerup, world, entities, game_state['hazard_zones'])

        if path is None:
            return [ACTIONS['none']]
        else:
            return get_path_action_seq(player_pos, path)
