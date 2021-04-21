"""
TEMPLATE for creating your own Agent to compete in
'Dungeons and Data Structures' at the Coder One AI Sports Challenge 2020.
For more info and resources, check out: https://bit.ly/aisportschallenge

BIO:
"""

# import time
# import numpy as np
# import pandas as pd
# import sklearn
# from .utils import util_functions
# from datetime import datetime
from .strategies import RandomStrategy
from .brain import Brain


class Agent:
    def __init__(self):
        self.action_queue = []
        self.brain = Brain()
        self.strategies = {
            'random': RandomStrategy(),
        }
        # DEBUG
        self.debug_mode = False

    def next_move(self, game_state, player_state):
        """This method is called each time your Agent is required to choose an action"""
        # TODO add values to game_state
        # TODO make bot more responsive to changes in game state

        if not self.action_queue:
            strategy_name = self.brain.get_next_strategy(game_state)
            strategy = self.strategies[strategy_name]
            actions = strategy.execute(game_state)

            self.action_queue = self.action_queue + actions

        return self.action_queue.pop(0)
