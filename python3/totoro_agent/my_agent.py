from .strategies import RandomStrategy, RetreatStrategy
from .brain import Brain


class Agent:
    def __init__(self):
        self.brain = Brain()
        self.strategies = {
            'random': RandomStrategy(),
            'retreat': RetreatStrategy()
            # kill: 3
            # trap: 4
            # pickup: 1
        }
        self.action_queue = []
        self.prev_tick = -1

    def next_move(self, tick_number, game_state):
        # If it prints this out in console, it means algorithm is performing suboptimally
        if tick_number - self.prev_tick != 1:
            print(f'Skipped a Tick: Tick #{tick_number}, skipped {tick_number - self.prev_tick}')

        if not self.action_queue:
            # Gets brain to eval environment, then spit out the strategy chosen (as string)
            strategy_name = self.brain.get_next_strategy(game_state)
            strategy = self.strategies.get(strategy_name) 
            actions = strategy.execute(game_state)

            self.action_queue = self.action_queue + actions

        # print(game_state) #-> To check if you've added new things to game_state
        self.prev_tick = tick_number
        return self.action_queue.pop(0)
