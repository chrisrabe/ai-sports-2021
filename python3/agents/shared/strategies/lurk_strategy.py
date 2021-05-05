from typing import List
from collections import defaultdict, OrderedDict

from . import strategy
from ..utils.constants import ACTIONS
from ..utils.util_functions import manhattan_distance, get_shortest_path, get_path_action_seq, move_results_in_ouchie


class LurkStrategy(strategy.Strategy):

    def __init__(self):
        self.min_follow_dist = 4

    def execute(self, game_state: object) -> List[str]:
        player_pos = game_state['player_pos']
        enemy_pos = game_state['enemy_pos']

        if manhattan_distance(player_pos, enemy_pos) <= self.min_follow_dist:
            # We're close enough
            return [ACTIONS['none']]

        # find the nearest reachable safe tile from the enemy and go to it
        dist_map = defaultdict(list)
        for tile in game_state['safe_zones']:
            distance = manhattan_distance(enemy_pos, tile)
            dist_map[distance].append(tile)

        od = OrderedDict(sorted(dist_map.items()))

        world = game_state['world']
        entities = game_state['entities']
        player_invulnerable = game_state['player_is_invulnerable']
        blast_tiles = [enemy_pos]
        path = None

        for dist in od.keys():
            tiles = dist_map[dist]
            for tile in tiles:
                path = get_shortest_path(player_pos, tile, world, entities, blast_tiles, player_invulnerable)
                if path is not None:
                    break  # found reachable tile already. Break out of loop
            else:
                continue
            break  # found reachable tile already. Break out of loop

        if path is None:
            # just stand absolutely still. Nothing to move to
            return [ACTIONS['none']]
        else:
            action_seq = get_path_action_seq(player_pos, path)
            next_move = action_seq.pop(0)
            if move_results_in_ouchie(player_pos, next_move, game_state['all_hazard_zones']):
                return [ACTIONS['none']]  # not worth it
            else:
                return [next_move]
