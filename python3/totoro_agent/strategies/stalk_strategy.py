from typing import List

from . import strategy
from ..utils.util_functions import get_shortest_path, get_path_action_seq
from ..utils.constants import ACTIONS


class StalkStrategy(strategy.Strategy):

    def execute(self, game_state: object) -> List[str]:
        enemy_pos = tuple(game_state['enemy_pos'])
        player_pos = tuple(game_state['player_pos'])
        world = game_state['world']
        entities = game_state['entities']

        print('Enemy at', enemy_pos)
        print('Player at', player_pos)

        # get surrounding empty tile from enemy
        # go to closest one from player

        path = get_shortest_path(player_pos, enemy_pos, world, entities)
        return get_path_action_seq(player_pos, path)
