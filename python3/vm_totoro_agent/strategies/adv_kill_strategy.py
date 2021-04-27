from typing import List

from . import strategy
from ..utils.constants import ACTIONS
from ..utils.util_functions import get_value_map, death_trap, get_move_from_value_map


class AdvKillStrategy(strategy.Strategy):
    def __init__(self):
        self.rewards = {
            'enemy': 20,
            'pinch': 1
        }

    def execute(self, game_state: dict) -> List[str]:
        world = game_state['world']
        entities = game_state['entities']
        enemy_pos = game_state['enemy_pos']
        player_pos = game_state['player_pos']

        # check if enemy position is trapped
        if death_trap(enemy_pos, world, entities):
            if game_state['enemy_on_bomb'] or game_state['enemy_near_bomb']:
                print('Totoro laughs at the enemy\'s fate')
                return [ACTIONS['none']]
            else:
                print('Totoro leaves a little present')
                return [ACTIONS['bomb']]

        # GO ON A HUNT!
        print('Hipity hopity, Totoro is coming fo yo ass')
        targets = [game_state['enemy_obj']]
        value_map = get_value_map(world, game_state['wall_blocks'], targets, self.rewards, game_state['pinch_points'], False)
        action = get_move_from_value_map(player_pos, value_map, world)
        return [action]
