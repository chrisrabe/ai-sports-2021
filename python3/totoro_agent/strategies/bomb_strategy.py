import random
from typing import List

from . import strategy
from ..utils.constants import ACTIONS
from ..utils.util_functions import death_trap


class BombStrategy(strategy.Strategy):

    def execute(self, game_state: object) -> List[str]:
        world = game_state['world']
        entities = game_state['entities']
        enemy_pos = game_state['enemy_pos']
        player_pos = game_state['player_pos']

        # check if enemy position is trapped
        if game_state['enemy_on_bomb'] or game_state['enemy_near_bomb']:
            print('Totoro laughs at the enemy\'s fate: They\'re in blast range and stuck. Goodbye.')
            return [ACTIONS['none']]
        else:
            print('Totoro leaves a little present')
            return [ACTIONS['bomb']]

        # # Literally just bomb.
        # return [ACTIONS['bomb']]