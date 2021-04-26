from typing import List

from . import strategy
from ..utils.util_functions import get_shortest_path, get_path_action_seq, get_blast_zone, get_nearest_tile


class StalkStrategy(strategy.Strategy):

    def execute(self, game_state: object) -> List[str]:
        enemy_pos = game_state['enemy_pos']
        player_pos = game_state['player_pos']
        world = game_state['world']
        entities = game_state['entities']

        # we want to at least be 3 blocks away from player
        stalk_zone = get_blast_zone(enemy_pos, 5, entities, world)
        closest_tile = get_nearest_tile(player_pos, stalk_zone)

        path = get_shortest_path(player_pos, closest_tile, world, entities)
        if path:
            path = path[:-1]  # remove last because it's the enemy_player
        return get_path_action_seq(player_pos, path)
