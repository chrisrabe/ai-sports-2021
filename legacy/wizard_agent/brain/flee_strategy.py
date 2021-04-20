from typing import List
from . import strategy
from . import utils as _utils

utils = _utils.util_functions
constants = _utils.constants

ACTIONS = constants.ACTIONS
EXPLOSION_TICKS = 5


def get_danger_zones(bombs, game_state):
    """
    Retrieves the dangerous tiles
    """
    danger_tiles = []
    for bomb in bombs:
        blast_tiles = utils.get_blast_zone(bomb, game_state)
        for tile in blast_tiles:
            if tile not in danger_tiles:
                danger_tiles.append(tile)
    return danger_tiles


def get_exploded_bombs(cur_bombs, prev_bombs, active_bombs):
    """
    Compares the current bombs and the previous bombs and checks
    """
    exploded_bombs = []
    for bomb in prev_bombs:
        if bomb not in cur_bombs and bomb not in active_bombs:
            exploded_bombs.append(bomb)
    return exploded_bombs


def get_active_bombs(exploded_bombs):
    """
    Returns the bombs that has exploded but still has running explosion
    """
    active_bombs = []
    for explosion in exploded_bombs:
        new_ticks = explosion['ticks_left'] - 1
        if new_ticks > 0:
            active_bombs.append({
                'position': explosion['position'],
                'ticks_left': new_ticks
            })
    return active_bombs


def create_new_explosions(exploded_bombs):
    explosions = []
    for bomb in exploded_bombs:
        explosions.append({
            'position': bomb,
            'ticks_left': EXPLOSION_TICKS
        })
    return explosions


class FleeStrategy(strategy.Strategy):

    def __init__(self):
        self.prev_bombs = []
        self.exploded_bombs = []

    def execute(self, game_state: object, player_state: object) -> List[str]:
        location = player_state.location
        bombs = game_state.bombs

        bombs_in_range = utils.get_bombs_in_range(location, bombs)
        # get dangerous tiles
        dangerous_tiles = get_danger_zones(bombs_in_range, game_state)

        # remove exploded bombs that passed number of ticks
        active_bombs = get_active_bombs(self.exploded_bombs)
        active_coords = [b['position'] for b in active_bombs]

        # get exploded bombs from previous bombs
        exploded_bombs = get_exploded_bombs(bombs, self.prev_bombs, active_coords)
        new_active_bombs = create_new_explosions(exploded_bombs)

        # check explosion area
        exploded_bombs = exploded_bombs + active_coords
        explosion_area = get_danger_zones(exploded_bombs, game_state)
        dangerous_tiles = dangerous_tiles + explosion_area

        self.exploded_bombs = active_bombs + new_active_bombs
        self.prev_bombs = bombs

        # wait if not standing in danger zone
        if location not in dangerous_tiles:
            return [ACTIONS["none"]]
        else:
            # find all safe areas
            safe_tiles = utils.get_safe_tiles(dangerous_tiles, game_state)
            reachable_tiles = utils.get_reachable_tiles(location, safe_tiles, game_state)

            # get nearest safe tile
            nearest_tile = utils.get_nearest_tile(location, reachable_tiles)

            if nearest_tile:
                path = utils.get_shortest_path(location, nearest_tile, game_state)
                action_seq = utils.get_path_action_seq(location, path)
                return action_seq
            return [ACTIONS["none"]]

    def can_execute(self, game_state: object, player_state: object) -> bool:
        location = player_state.location
        bombs = game_state.bombs
        bombs_in_range = utils.get_bombs_in_range(location, bombs)
        dangerous_tiles = get_danger_zones(bombs_in_range, game_state)
        return len(bombs_in_range) > 0 and location in dangerous_tiles
