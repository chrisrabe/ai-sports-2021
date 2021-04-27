from typing import List
from . import strategy
from ..utils.util_functions import get_shortest_path, get_path_action_seq, get_nearest_tile, get_reachable_tiles, get_empty_locations
from ..utils.constants import ACTIONS


class BlockDestroyingStrategy(strategy.Strategy):

    def execute(self, game_state: object) -> List[str]:
        path = None
        player_pos = tuple(game_state['player_pos'])
        world = game_state['world']
        entities = game_state['entities']

        destroyable_blocks = game_state['destroyable_blocks']

        # Navigating to the box next to them.


        if destroyable_blocks:
            # Get the empty locations next to the tile. get_empty_locations()
            # Filter all the empty locations to reachable_blocks.
            # retrieve the nearest block.
            empty_locations = get_empty_locations(destroyable_blocks, world, entities)
            reachable_blocks = get_reachable_tiles(player_pos, empty_locations, world, entities)
            nearest_blocks = get_nearest_tile(player_pos, reachable_blocks)
            path = get_shortest_path(player_pos, nearest_blocks, world, entities)
        


        if path is None:
            return [ACTIONS['none']]
        else:
            action_sequence = get_path_action_seq(player_pos, path)
            action_sequence.append(ACTIONS['bomb'])
            return action_sequence

