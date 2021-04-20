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
            'flee': brain.FleeStrategy(),
            'move': brain.MoveStrategy(),
            'bomb': brain.BombPlacementStrategy(),
            'orebomb': brain.OreBombStrategy(),
            'kill': brain.KillStrategy(),
            'combo_kill': brain.ComboKillStrategy(),
            'retreat': brain.RetreatStrategy(),
            'smartbomb': brain.SmartBombStrategy(),
            'smartcollect': brain.SmartCollectionStrategy(),
        }
        self.action_queue = []

        self.end_tick = 1800
        self.step = 0

        self.initial_destroyable_blocks = 0

        # DEBUG
        self.debug_mode = False
        self.filename = datetime.now().strftime('wizard_agent/log/log_%H_%M_%d_%m_%Y.txt')

    def save_action_log(self, step, actions, player_state, strategy_name):
        reward = player_state.reward
        with open(self.filename, 'a+', newline='') as f:
            f.write('Agent ' + str(
                player_state.id) + ' | Tick: {0} - {1} | Current Score: {2} | Strategy Used: {3} \n'.format(step,
                                                                                                            actions,
                                                                                                            reward,
                                                                                                            strategy_name))

    def next_move(self, game_state, player_state):
        """This method is called each time your Agent is required to choose an action"""
        # if queue is empty, get strategy
        if not self.action_queue:
            strategy_name = "retreat"
            can_do_flee = self.strategies["flee"].can_execute(game_state, player_state)
            can_do_bomb = self.strategies["smartbomb"].can_execute(game_state, player_state)
            can_do_kill = self.strategies["kill"].can_execute(game_state, player_state)
            can_do_combo = self.strategies["combo_kill"].can_execute(game_state, player_state)
            can_do_collect = self.strategies["smartcollect"].can_execute(game_state, player_state)

            # Check Destroyable Item

            if self.step == 0:
                self.initial_destroyable_blocks = len(game_state.soft_blocks) + len(game_state.ore_blocks)

            cur_destroyable_items = len(game_state.soft_blocks) + len(game_state.ore_blocks)

            if cur_destroyable_items > int(0.25 * self.initial_destroyable_blocks):
                if can_do_flee:
                    strategy_name = 'flee'
                elif can_do_bomb:
                    strategy_name = 'smartbomb'
                elif can_do_collect:
                    strategy_name = 'smartcollect'
                elif can_do_combo:
                    strategy_name = 'combo_kill'
                elif can_do_kill:
                    strategy_name = 'kill'
            else:
                if can_do_flee:
                    strategy_name = 'flee'
                elif can_do_combo:
                    strategy_name = 'combo_kill'
                elif can_do_kill:
                    strategy_name = 'kill'
                elif can_do_collect:
                    strategy_name = 'smartcollect'
                elif can_do_bomb:
                    strategy_name = 'smartbomb'

            # enqueue next action sequence
            strategy = self.strategies[strategy_name]
            actions = strategy.execute(game_state, player_state)

            # log bot action
            if self.debug_mode:
                if self.step <= 1800:
                    self.save_action_log(self.step, actions, player_state, strategy_name)
                    self.step += 1

            self.action_queue = self.action_queue + actions

        # execute the first action
        return self.action_queue.pop(0)
