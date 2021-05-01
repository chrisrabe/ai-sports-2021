from typing import List

from . import strategy
from ..utils.constants import ACTIONS


class BombStrategy(strategy.Strategy):

    def execute(self, game_state: object) -> List[str]:
        if game_state['enemy_on_bomb'] or game_state['enemy_near_bomb']:
            print('Totoro laughs at the enemy\'s fate: They\'re in blast range and stuck. Goodbye.')
            return [ACTIONS['none']]
        else:
            print('Totoro leaves a little present')
            return [ACTIONS['bomb']]
