from collections import defaultdict, OrderedDict
from typing import List

from . import strategy
from ..utils.constants import ACTIONS
from ..utils.util_functions import get_playzone, manhattan_distance, get_shortest_path, is_in_bounds, \
    get_path_action_seq, move_results_in_ouchie


class PlayzoneStrategy(strategy.Strategy):

    def execute(self, game_state: object) -> List[str]:
        player_pos = game_state['player_pos']
        enemy_pos = game_state['enemy_pos']
        playzone = get_playzone(game_state['tick'])

        # find the nearest reachable safe tile from the enemy and go to it
        dist_map = defaultdict(list)
        for tile in game_state['safe_zones']:
            distance = manhattan_distance(player_pos, tile)
            dist_map[distance].append(tile)

        od = OrderedDict(sorted(dist_map.items()))

        world = game_state['world']
        entities = game_state['entities']
        player_invulnerable = game_state['player_is_invulnerable']
        blast_tiles = [enemy_pos]
        path = None

        # graph the shortest path to the closest tile
        for dist in od.keys():
            tiles = dist_map[dist]
            for tile in tiles:
                if is_in_bounds(tile, playzone[0], playzone[1]):
                    path = get_shortest_path(player_pos, tile, world, entities, blast_tiles, player_invulnerable)
                    if path is not None:
                        break  # found reachable tile already. Break out of loop
            else:
                continue
            break  # found reachable tile already. Break out of loop

        if path is None:
            print("Ah crap. We're gonna die!")
            return [ACTIONS['none']]
        else:
            action_seq = get_path_action_seq(player_pos, path)
            next_move = action_seq.pop(0)
            if move_results_in_ouchie(player_pos, next_move, game_state['all_hazard_zones']):
                return [ACTIONS['none']]  # not worth it
            else:
                return [next_move]
