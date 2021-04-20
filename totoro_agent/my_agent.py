"""
TEMPLATE for creating your own Agent to compete in
'Dungeons and Data Structures' at the Coder One AI Sports Challenge 2021.
For more info and resources, check out: https://bit.ly/aisportschallenge

BIO:
"""

# import time
# import numpy as np
# import pandas as pd
# import sklearn
from . import brain
from datetime import datetime

utils = brain.utils.util_functions


class Agent:
    def __init__(self):
        self.strategies = {
            'random': brain.RandomStrategy(),
        }
        self.action_queue = []

        # DEBUG
        self.debug_mode = False

    def next_move(self, game_state, player_state):
        """This method is called each time your Agent is required to choose an action"""

        # TODO make this more responsive

        if not self.action_queue:
            strategy_name = "random"
            strategy = self.strategies[strategy_name]
            actions = strategy.execute(game_state, player_state)

            self.action_queue = self.action_queue + actions

        return self.action_queue.pop(0)
