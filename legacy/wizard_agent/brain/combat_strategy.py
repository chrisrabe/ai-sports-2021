from typing import List

from .strategy import Strategy
from .utils import util_functions as utils, constants
from .fake_out_strategy import FakeOutStrategy
from .chain_bomb_strategy import ChainBombStrategy
from .close_combat_strategy import CloseCombatStrategy
from .trap_strategy import TrapStrategy
from .retreat_strategy import RetreatStrategy


class CombatStrategy(Strategy):
    def __init__(self):
        self.game_state = None
        self.player_state = None
        self.escape_matrix = []  # num of escape paths for each tile in map
        self.has_advantage = False
        self.bomb_states = {}
        self.strategies = {
            'fakeout': FakeOutStrategy(),
            'chainbomb': ChainBombStrategy(),
            'closecombat': CloseCombatStrategy(),
            'trap': TrapStrategy(),
            'retreat': RetreatStrategy()
        }

    def execute(self, game_state: object, player_state: object) -> List[str]:
        self.game_state = game_state
        self.player_state = player_state
        ammo = player_state.ammo

        strategy_name = "retreat"
        if ammo > 0:  # can be aggressive
            can_do_trap = self.strategies["trap"].can_execute(game_state, player_state)
            can_do_closecombat = self.strategies["closecombat"].can_execute(game_state, player_state)
            can_do_fakeout = self.strategies["fakeout"].can_execute(game_state, player_state)
            can_do_chainbomb = self.strategies["chainbomb"].can_execute(game_state, player_state)

            if can_do_trap:
                strategy_name = "trap"
            elif can_do_closecombat:
                strategy_name = "closecombat"
            elif can_do_fakeout:
                strategy_name = "fakeout"
            elif can_do_chainbomb:
                strategy_name = "chainbomb"

        # enqueue next action sequence
        strategy = self.strategies[strategy_name]
        actions = strategy.execute(game_state, player_state)
        return actions

    def can_execute(self, game_state: object, player_state: object) -> bool:
        self.game_state = game_state
        self.player_state = player_state
        # initialise or update state variables
        self.escape_matrix = utils.get_escape_matrix(game_state)
        self.update_bomb_states()
        # initialise args for strategies
        self.strategies["trap"].update_fields({
            'escape_matrix': self.escape_matrix
        })
        self.strategies["chainbomb"].update_fields({
            'bomb_states': self.bomb_states
        })

        return False  # TODO modify this in future
    # Helper functions

    def update_bomb_states(self):
        bombs = self.game_state.bombs
        cur_tick = self.game_state.tick_number
        # record new bombs
        for bomb in bombs:
            if bomb not in self.bomb_states:
                self.bomb_states[bomb] = cur_tick + constants.BOMB_DURATION
        # remove bombs that has passed its tick
        exploded_bombs = []
        for bomb, tick_due in self.bomb_states.items():
            if cur_tick >= tick_due:
                exploded_bombs.append(bomb)
        # delete them from bomb states
        for bomb in exploded_bombs:
            del self.bomb_states[bomb]
