from typing import List
from . import strategy
from ..utils.util_functions import get_surrounding_tiles, get_empty_locations, get_world_dimension, manhattan_distance, get_shortest_path, get_path_action_seq
from ..utils.constants import ACTIONS
import random


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
        path = None
        player_pos = game_state['player_pos'] # Tuple
        hazard_zones = game_state['hazard_zones'] # List of tuples 
        world = game_state['world']
        entities = game_state['entities']
        width, height = get_world_dimension(world)


       # if player_pos in hazard_zones: # Checks if player is on hazard tile (potential blast zone)
        print("YOU'RE IN DANGER DUDE - basic avoid") 

        first_order_surrounding_tiles = get_surrounding_tiles(player_pos, width, height) # List of tiles

        safe_tiles = get_empty_locations(first_order_surrounding_tiles, world, entities) # List of empty tiles (big set). Not actually safe yet.

        for tile in safe_tiles: # Remove any empty tiles that are in hazard zone.
            if tile in hazard_zones:
                safe_tiles.remove(tile) # Safe list of tiles now.
        
        # Minimum distance tile ... or not lmao 
        # dist_list = [manhattan_distance(player_pos, tile) for tile in safe_tiles]
        # min_dist = min(dist_list)
        randomtile = random.choice(safe_tiles)
        path = get_shortest_path(player_pos, randomtile, world, entities, game_state['hazard_zones'])

        if path is None:
            print("shat myself inside basic_avoid. This shouldn't ever happen; means you called this when he wasn't in hazard. (Check the brain?)")
            return [ACTIONS['none']]
        else:
            return get_path_action_seq(player_pos, path)
        