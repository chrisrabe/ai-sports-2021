"""
TEMPLATE for creating your own Agent to compete in
'Dungeons and Data Structures' at the Coder One AI Sports Challenge 2020.
For more info and resources, check out: https://bit.ly/aisportschallenge

BIO compilation:
helo my name is dongerino pasterino ヽ༼ຈل͜ຈ༽ﾉ, i am 69 year old donger from imaqtmeatloaf’s stream .
420 years ago i was kidnapped and put into a donger concentration camp for 9001 years.
1 year ago, imaqtlasagne and imaqtpie invaded the camp and rescued me.
now i work as teacherino, passing down the wisdom of ( ͡° ͜ʖ ͡°) to young dongers.

“Robots mimic humans but you can't mimic us” ;)
Developed by a group of young and aspiring developers through hard work and dedication.
Through many iterations and optimisation, our born-to-beat (BtoB) agent uses many smart strategies to play the game.
Ours sure will be exciting to watch. Look forward to it. This is the best we can do.
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
