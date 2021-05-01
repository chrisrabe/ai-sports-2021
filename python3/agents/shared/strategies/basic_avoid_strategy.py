from typing import List

from . import strategy
from ..utils.constants import ACTIONS
from ..utils.util_functions import get_shortest_path, get_path_action_seq, get_nearest_tile


class BasicAvoidStrategy(strategy.Strategy):

    def execute(self, game_state: object) -> List[str]:
        """
        If the player is in a hazard_zones tile:
        move to nearest tile that isn't in hazard_zones
        OR
        Move to a random tile that isn't in the hazard_zone
        Not foolproof, just a good-enough heuristic.
        Should be mentioned that this sees powerups are a wall (only occurs when in hazard zone). Potentially might fix.
        """
        player_pos = game_state['player_pos']  # Tuple
        enemy_pos = game_state['enemy_pos']  # Tuple
        world = game_state['world']
        entities = game_state['entities']
        enemy_hp = game_state['enemy_health']
        player_hp = game_state['player_health']

        # Bomb or sacrificial body block
        if game_state['enemy_immediate_trapped'] and game_state['enemy_near_bomb']:
            if game_state['player_inv_bombs'] > 0:
                print('You just played yourself!')
                return [ACTIONS['bomb']]

            if (player_hp - enemy_hp) >= 1:
                print('I shall sacrifice myself for the win!')
                return [ACTIONS['none']]


        print("YOU'RE IN DANGER DUDE - basic avoid")

        # first_order_surrounding_tiles = get_surrounding_tiles(player_pos, width, height) # List of tiles

        # safe_tiles = get_empty_locations(first_order_surrounding_tiles, world, entities) # List of empty tiles (big set). Not actually safe yet.

        # for tile in safe_tiles: # Remove any empty tiles that are in hazard zone.
        #     if tile in hazard_zones:
        #         safe_tiles.remove(tile) # Safe list of tiles now.

        # Minimum distance tile ... or not lmao 
        # dist_list = [manhattan_distance(player_pos, tile) for tile in safe_tiles]
        # min_dist = min(dist_list)
        closest_tile = get_nearest_tile(player_pos, game_state['safe_zones'])
        blast_tiles = [enemy_pos]
        path = get_shortest_path(player_pos, closest_tile, world, entities, blast_tiles, game_state['player_is_invulnerable'])

        if path is None:
            print(
                "shat myself inside basic_avoid. This shouldn't ever happen; means you called this when he wasn't in hazard, or if path can't be found (Check the brain?)")
            return [ACTIONS['none']]
        else:
            #            print("path, etc", path, get_path_action_seq(player_pos, path))
            return [get_path_action_seq(player_pos, path).pop(0)]
