from typing import List
from collections import defaultdict
from . import strategy
from ..utils.util_functions import get_surrounding_empty_tiles, get_entity_coords, get_reachable_tiles, \
    get_num_escape_paths, get_nearest_tile, get_shortest_path, get_path_action_seq
from ..utils.constants import ACTIONS


class BlockDestroyingStrategy(strategy.Strategy):

    def __init__(self):
        self.rewards = {
            'destroys_3': 6,
            'destroys_2': 5,
            'destroys_1': 4,
            'dmg_3': 3,
            'dmg_2': 2,
            'dmg_1': 1,
        }

    def get_next_tile(self, enemy_pos, tiles):
        if len(tiles) > 0:
            # get tile closest to opponent
            return get_nearest_tile(enemy_pos, tiles)
        else:
            return tiles.pop()

    def execute(self, game_state: object) -> List[str]:
        player_pos = game_state['player_pos']
        enemy_pos = game_state['enemy_pos']
        player_diam = game_state['player_diameter']
        world = game_state['world']
        entities = game_state['entities']
        destroyable_blocks = game_state['destroyable_blocks']

        # if any active bombs are next to destroyable blocks, detonate them

        if not destroyable_blocks:
            return [ACTIONS['none']]  # do nothing. No hunt

        # HUNT DOWN THE BLOCK (very algorithmic - where can it go wrong?)

        # empty_tile -> array of affected blocks
        block_map = defaultdict(list)

        for block in destroyable_blocks:
            coord = get_entity_coords(block)
            empty_neighbours = get_surrounding_empty_tiles(coord, world, entities)
            reachable_tiles = get_reachable_tiles(player_pos, empty_neighbours, world, entities)
            for nei in reachable_tiles:
                block_map[nei].append(block)

        if not block_map:
            return [ACTIONS['none']]  # nowhere to go

        # tile coordinate -> reward value
        tile_scores = defaultdict(int)
        for key, value in block_map.items():
            destroys = 0
            # count how many destroys and affected bombs
            for block in value:
                if block['hp'] == 1:
                    destroys += 1
            if destroys > 0:
                tile_scores[key] += self.rewards[f'destroys_{destroys}']
            else:
                tile_scores[key] += self.rewards[f'dmg_{len(value)}']
            # count escape paths
            tile_scores[key] += get_num_escape_paths(player_pos, key, player_diam, entities, world)

        # score -> array of tile coordinates (if there's more than one, we bomb the one closest to opponent
        score_map = defaultdict(list)
        max_score = -1
        for key, value in tile_scores.items():
            if value > max_score:
                value = max_score
            score_map[value].append(key)

        tiles = score_map[max_score]  # get the tiles with largest score
        next_tile = self.get_next_tile(enemy_pos, tiles)
        path = get_shortest_path(player_pos, next_tile, world, entities)
        if path:
            action_seq = get_path_action_seq(player_pos, path)
            action_seq.append(ACTIONS['bomb'])
            return action_seq  # no need to be that reactive because kinda safe (for now)
        else:
            return [ACTIONS['none']]  # technically, it shouldn't reach here but just to be safe
