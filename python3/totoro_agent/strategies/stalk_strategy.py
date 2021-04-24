from typing import List

from . import strategy
from ..utils.util_functions import get_shortest_path
from ..utils.constants import ACTIONS


class StalkStrategy(strategy.Strategy):

    def execute(self, game_state: object) -> List[str]:
        enemy_pos = game_state['enemy_pos']
        player_pos = game_state['player_pos']

        print('Enemy at', enemy_pos)
        print('Player at', player_pos)

        # get surrounding empty tile from enemy
        # go to closest one from player

        return [ACTIONS['none']]
