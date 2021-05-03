from collections import defaultdict, OrderedDict
from typing import List

from . import strategy
from ..utils.constants import ACTIONS
from ..utils.util_functions import get_shortest_path, get_path_action_seq, death_trap, manhattan_distance


class BasicAvoidStrategy(strategy.Strategy):

    def update(self, game_state: dict):
        game_state['enemy_immediate_trapped'] = death_trap(game_state['enemy_pos'], game_state['world'],
                                                           game_state['entities']) and game_state['enemy_near_player']

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
            if game_state['player_inv_bombs'] > 0 and not game_state['player_on_bomb']:
                print('You just played yourself!')
                return [ACTIONS['bomb']]

            if (player_hp - enemy_hp) >= 1:
                print('I shall sacrifice myself for the win!')
                return [ACTIONS['none']]

        print("YOU'RE IN DANGER DUDE - basic avoid")

        # distance -> array of tiles
        dist_map = defaultdict(list)
        for tile in game_state['safe_zones']:
            distance = manhattan_distance(player_pos, tile)
            dist_map[distance].append(tile)

        # Order them from smallest distance to largest
        od = OrderedDict(sorted(dist_map.items()))
        min_dist = list(od.keys())[0]
        min_dist_tiles = dist_map[min_dist]

        blast_tiles = [enemy_pos]
        path = None

        # Grab the first reachable
        for tile in min_dist_tiles:
            path = get_shortest_path(player_pos, tile, world, entities, blast_tiles, game_state['player_is_invulnerable'])
            if path is not None:
                break

        if path is None:
            print(
                "shat myself inside basic_avoid. This shouldn't ever happen; means you called this when he wasn't in hazard, or if path can't be found (Check the brain?)")
            return [ACTIONS['none']]
        else:
            return [get_path_action_seq(player_pos, path).pop(0)]
