from typing import List
from . import strategy
from . import utils as _utils

utils = _utils.util_functions
constants = _utils.constants
ACTIONS = constants.ACTIONS


def get_urgent_ores(ore_state):
    """
        Check if any of the values in ore_state is equal to 1
    """
    urgent_ores = []
    for key, value in ore_state.items():
        if value == 1:
            urgent_ores.append(tuple(key))
        
    return urgent_ores


def _get_nearest_ore_block(location, ore_block_list):
    if ore_block_list:
        ore_block_distance = 10
        closest_ore_block = ore_block_list[0]
        for ore_block in ore_block_list:
            new_ore_block_dist = utils.manhattan_distance(location, ore_block)
            if new_ore_block_dist < ore_block_distance:
                ore_block_distance = new_ore_block_dist
                closest_ore_block = ore_block

        return closest_ore_block
    else:
        return None


def get_nearest_empty_ore_tile(location, ores, game_state):
    empty_tiles = utils.get_empty_locations(ores, game_state)
    reachable_tiles = utils.get_reachable_tiles(location, empty_tiles, game_state)
    nearest_tile = utils.get_nearest_tile(location, reachable_tiles)
    return nearest_tile


class OreBombStrategy(strategy.Strategy):
    def __init__(self):
        self.ore_state = {}
    
    def execute(self, game_state: object, player_state: object) -> List[str]:
        location = player_state.location
        ore_blocks = game_state.ore_blocks

        # add ores into state
        for ore in ore_blocks:
            if ore not in self.ore_state:
                self.ore_state[ore] = 3

        # TODO update ore state to account for other player

        urgent_ores = get_urgent_ores(self.ore_state)
        # get the nearest block to the player
        if urgent_ores:
            # grab the nearest empty tile to put bomb
            nearest_tile = get_nearest_empty_ore_tile(location, urgent_ores, game_state)
            safe_tile_to_escape_to = utils.safe_escape(nearest_tile, game_state)
            nearest_ore = utils.get_nearest_tile(nearest_tile, urgent_ores)
            # remove ore from ore_state
            self.ore_state.pop(nearest_ore)
            path = utils.get_shortest_path(location, nearest_tile, game_state)
            action_seq = utils.get_path_action_seq(location, path)
            action_seq.append(ACTIONS["bomb"])
            escape_path = utils.get_shortest_path(nearest_tile, safe_tile_to_escape_to, game_state)
            escape_seq = utils.get_path_action_seq(nearest_tile, escape_path)
            action_seq = action_seq + escape_seq
            return action_seq
        else:
            nearest_tile = get_nearest_empty_ore_tile(location, ore_blocks, game_state)
            safe_tile_to_escape_to = utils.safe_escape(nearest_tile, game_state)
            nearest_ore = utils.get_nearest_tile(nearest_tile, ore_blocks)
            # decrease ore state value
            self.ore_state[nearest_ore] -= 1
            path = utils.get_shortest_path(location, nearest_tile, game_state)
            action_seq = utils.get_path_action_seq(location, path)
            action_seq.append(ACTIONS["bomb"])
            escape_path = utils.get_shortest_path(nearest_tile, safe_tile_to_escape_to, game_state)
            escape_seq = utils.get_path_action_seq(nearest_tile, escape_path)
            action_seq = action_seq + escape_seq
            return action_seq

    def can_execute(self, game_state: object, player_state: object) -> bool:
        location = player_state.location
        ammo = player_state.ammo
        bombs = game_state.bombs
        ore_blocks = game_state.ore_blocks
        if len(ore_blocks) == 0:
            return False

        nearest_tile = get_nearest_empty_ore_tile(location, ore_blocks, game_state)
        safe = False
        safe_tile_to_escape_to = False
        if nearest_tile is not None:
            safe = utils.is_safe_path(location, nearest_tile, bombs, game_state)
            safe_tile_to_escape_to = utils.safe_escape(nearest_tile, game_state)
        return ammo > 0 and nearest_tile and safe and safe_tile_to_escape_to
