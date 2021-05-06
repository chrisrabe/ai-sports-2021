from typing import List

from . import strategy
from ..utils.constants import ACTIONS
from ..utils.util_functions import get_surrounding_empty_tiles, get_world_dimension, manhattan_distance, move_to_tile


class DodgeFlameStrategy(strategy.Strategy):

    def execute(self, game_state: object) -> List[str]:
        player_pos = game_state['player_pos']
        world = game_state['world']
        entities = game_state['entities']

        # retrieve all empty tiles next to the player
        player_empty_tiles = get_surrounding_empty_tiles(player_pos, world, entities, ignore_player=False)

        # identify the exact center of the map
        world_width, world_height = get_world_dimension(world)
        center_x = world_width // 2
        center_y = world_height // 2
        center_map = (center_x, center_y)

        # find the closest tile to center
        closest_tile_center = player_pos
        closest_dist = 1000

        for tile in player_empty_tiles:
            tile_dist = manhattan_distance(tile, center_map)
            if tile_dist < closest_dist:
                closest_tile_center = tile
                closest_dist = tile_dist

        if closest_tile_center == player_pos:
            # We shall accept our fate. Trapped and death is looming over our heads
            return [ACTIONS['none']]
        else:
            next_move = move_to_tile(player_pos, closest_tile_center)
            return [next_move]
