from typing import List

from . import strategy
from ..utils.constants import ACTIONS
from ..utils.util_functions import get_entity_coords, get_nearest_tile, get_surrounding_tiles, \
    get_world_dimension, convert_entities_to_coords, get_value_map, get_move_from_value_map, move_results_in_ouchie, \
    update_rec_value_map


class BlockDestroyHuntStrategy(strategy.Strategy):

    def __init__(self):
        self.rewards = {
            'destroys_3': 6,
            'destroys_2': 5,
            'destroys_1': 4,
            'dmg_3': 3,
            'dmg_2': 2,
            'dmg_1': 1,
            'destructibles_plant': 5,
            'hazard_zone': -20,
        }

    def get_next_tile(self, enemy_pos, tiles):
        if len(tiles) > 0:
            # get tile closest to opponent
            return get_nearest_tile(enemy_pos, tiles)
        else:
            return tiles.pop()

    def execute(self, game_state: dict) -> List[str]:
        player_pos = game_state['player_pos']
        enemy_pos = game_state['enemy_pos']
        player_diam = game_state['player_diameter']
        world = game_state['world']
        walls = game_state["wall_blocks"] 
        entities = game_state['entities']
        destroyable_blocks = game_state['destroyable_blocks']
        own_bombs = game_state['own_active_bombs']
        hazard_zones = game_state['hazard_zones']
        destroyable_coords = convert_entities_to_coords(destroyable_blocks)

        world_width, world_height = get_world_dimension(world)

        # move away from hazard if player is standing in it
        if player_pos in hazard_zones:
            # pass hazard zone entities into value map
            hazard_zones_targets = {}
            for coord in hazard_zones:
                hazard_zones_targets['coord'] = coord
                hazard_zones_targets['type'] = 'hazard_zone'

            # navigate to target using value map
            value_map = get_value_map(world, walls, hazard_zones_targets, self.rewards, use_default=False)

            # set wall value with  max spread of 1 to discourage navigating to an enclosed space causing trapping
            walls_entities = {}
            for index, wall in enumerate(walls):
                x, y = wall
                walls_entities[index] = [x, y, -5]

            value_map = update_rec_value_map(walls_entities, value_map, get_world_dimension(world), max_reward_spread=4)

            action = get_move_from_value_map(player_pos, value_map, world)

            return [action]
        
        else:

            # if any active bombs are next to destroyable blocks, detonate them
            can_detonate = False
            for bomb in own_bombs:
                coord = bomb['coord']
                surrounding_tiles = get_surrounding_tiles(coord, world_width, world_height)
                for tile in surrounding_tiles:
                    if tile in destroyable_coords:
                        can_detonate = True
                        game_state['detonation_target'] = coord
                        break
                if can_detonate:
                    break  # no need to look further

            if can_detonate:
                return [ACTIONS['detonate']]  # Blow up the bomb

            if not destroyable_blocks:
                return [ACTIONS['none']]  # do nothing. No hunt

            # get all coordinates of destructible plant tiles
            destructible_plant_coords = []
            for block in destroyable_blocks:
                coord = get_entity_coords(block)
                surrounding_tiles_coords = get_surrounding_tiles(coord, world_width, world_height)
                destructible_plant_coords = destructible_plant_coords + surrounding_tiles_coords
            
            # plants bomb if player already stands next to destructible block
            if player_pos in destructible_plant_coords:
                return [ACTIONS['bomb']]
            else:
                # pass destructible block plant entities into value map
                destructible_plant_targets = {}
                for plant_coord in destructible_plant_coords:
                    destructible_plant_targets['coord'] = plant_coord
                    destructible_plant_targets['type'] = 'destructibles_plant'

                # navigate to target using value map
                value_map = get_value_map(world, walls, destructible_plant_targets, self.rewards, use_default=False)

                action = get_move_from_value_map(player_pos, value_map, world)

                if move_results_in_ouchie(player_pos, action, game_state['hazard_zones']):
                    return [ACTIONS['none']]  # Nah. Not worth it
                else:
                    return [action]
