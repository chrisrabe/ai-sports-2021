from typing import List

from . import strategy
from ..utils.constants import ACTIONS
from ..utils.util_functions import get_value_map_objects_from_arr, convert_entities_to_coords, get_surrounding_tiles, \
    get_world_dimension, get_surrounding_empty_tiles, get_reachable_tiles, get_num_escape_paths, get_value_map, \
    get_move_from_value_map, move_results_in_ouchie


class AdvBlockStrategy(strategy.Strategy):
    def __init__(self):
        self.rewards = {
            'destructible_plant': 5,
            'enemy': 20  # move closer to enemy
        }

    def execute(self, game_state: dict) -> List[str]:
        player_pos = game_state['player_pos']
        player_diam = game_state['player_diameter']
        player_ammo = game_state['player_inv_bombs']
        world = game_state['world']
        walls = game_state['wall_blocks']
        own_bombs = game_state['own_active_bombs']
        destroyable_coords = convert_entities_to_coords(game_state['destroyable_blocks'])
        world_width, world_height = get_world_dimension(game_state['world'])
        entities = game_state['entities']

        # DETONATION ALGORITHM
        # If there's one active bomb that's next to a destroy block, blow it up
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
            print("I see a bomb that we can blow up.")
            return [ACTIONS['detonate']]  # Blow up the bomb

        if not destroyable_coords:
            print("Nothing to destroy. Gonna stand here.")
            return [ACTIONS['none']]  # Nothing to destroy

        # POINTS OF INTEREST
        # get all empty tiles next to destroyable tiles
        # things to avoid:
        # - ones without escape path
        # - ones that are not reachable
        # things to prioritise
        # - closer to enemy
        plant_zones = []
        for coord in destroyable_coords:
            empty_neigh = get_surrounding_empty_tiles(coord, world, entities, ignore_player=True)
            reachable_tiles = get_reachable_tiles(player_pos, empty_neigh, world, entities)
            if player_pos in empty_neigh:
                reachable_tiles.append(player_pos)  # add player back!
            for tile in reachable_tiles:
                escape_paths = get_num_escape_paths(player_pos, tile, player_diam, entities, world)
                # only add points to ones with escape paths
                if escape_paths > 0:
                    plant_zones.append(tile)

        print(f'Player pos: {player_pos}, Plant zones: {plant_zones}')

        # BOMBING ALGORITHM
        # If player is standing on point of interest, put bomb down
        if player_pos in plant_zones:
            if player_ammo > 1:  # conserve at least 1 ammo
                print(f"Player ammo: {player_ammo}. I'm standing where I need to be. I'm gonna plant!")
                return [ACTIONS['bomb']]
            else:
                print(f"No ammo. I'm doing nothing.")
                return [ACTIONS['none']]

        # NAVIGATION ALGORITHM
        # Use value map for navigation
        # Get highest value
        targets = get_value_map_objects_from_arr(plant_zones, 'destructible_plant')
        targets.append(game_state['enemy_obj'])
        value_map = get_value_map(world, walls, targets, self.rewards, use_default=False)
        action = get_move_from_value_map(player_pos, value_map, world)

        # If next move results in stepping into a hazard zone or blast tile, do absolutely nothing
        # Otherwise return the next action
        hazards = game_state['hazard_zones'] + convert_entities_to_coords(game_state['blast_blocks'])
        if move_results_in_ouchie(player_pos, action, hazards):
            return [ACTIONS['none']]
        else:
            return [action]
