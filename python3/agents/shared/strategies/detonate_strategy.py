from typing import List

from . import strategy
from ..utils.constants import ACTIONS
from ..utils.util_functions import get_detonation_target


class DetonateStrategy(strategy.Strategy):

    def execute(self, game_state: dict) -> List[str]:
        enemy_pos = game_state['enemy_pos']
        world = game_state['world']
        entities = game_state['entities']
        own_bombs = game_state['own_active_bombs']

        target_bomb = get_detonation_target(enemy_pos, own_bombs, world, entities)
        if target_bomb is None:
            print("Called in detonation. Why? The brain should be decision making -- if you called me, you're doing something wrong.")
            return [ACTIONS["none"]]
        else:
            game_state['detonation_target'] = target_bomb
            return [ACTIONS["detonate"]]
