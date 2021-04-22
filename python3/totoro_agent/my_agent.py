import os
from .client import Client
from .strategies import RandomStrategy
from .brain import Brain

uri = os.environ.get(
    'GAME_CONNECTION_STRING') or "ws://127.0.0.1:3000/?role=agent&agentId=agentId&name=defaultName"

class Agent:
    def __init__(self):
        self.brain = Brain()
        self.strategies = {
            'random': RandomStrategy()
        }
        self.action_queue = []
        self.prev_tick = -1

        self.client = Client(uri, self.next_move)

    def next_move(self, tick_number, game_state):
        # If it prints this out in console, it means algorithm is performing suboptimally
        if tick_number - self.prev_tick != 1:
            print(f'Skipped a Tick: Tick #{tick_number}, skipped {tick_number - self.prev_tick}')

        if not self.action_queue:
            strategy_name = self.brain.get_next_strategy(game_state)
            strategy = self.strategies.get(strategy_name)
            actions = strategy.execute(game_state)

            self.action_queue = self.action_queue + actions

        return self.action_queue.pop(0)
