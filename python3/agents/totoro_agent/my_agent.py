from .brain import Brain
from ..shared.strategies import RandomStrategy, RetreatStrategy, StalkStrategy, PickupStrategy, AdvKillStrategy, \
    BasicAvoidStrategy, DetonateStrategy, BombStrategy, SimpleBombStrategy, AdvBlockStrategy, StalkTwoStrategy
from ..shared.utils.benchmark import Benchmark
from copy import deepcopy

class Agent:
    def __init__(self):
        self.brain = Brain()
        self.strategies = {
            'random': RandomStrategy(),
            'retreat': RetreatStrategy(),
            'pickup': PickupStrategy(),
            'stalk': StalkTwoStrategy(),
            'basic_avoid': BasicAvoidStrategy(),
            'kill': AdvKillStrategy(),
            'detonate': DetonateStrategy(),
            'bomb': BombStrategy(),
            'block_destroy': AdvBlockStrategy(),
            'simple_bomb': SimpleBombStrategy()
        }
        self.action_queue = []
        self.prev_tick = -1
        self.benchmark = Benchmark()

    def next_move(self, tick_number, game_state):
        # If it prints this out in console, it means algorithm is performing suboptimally
        game_state = deepcopy(game_state)
        if tick_number - self.prev_tick != 1:
            print(f'Skipped a Tick: Tick #{tick_number}, skipped {tick_number - self.prev_tick}')
        self.benchmark.start('move')
        game_state['tick'] = tick_number
        print(f'Starting tick #{tick_number}')

        if not self.action_queue:
            # Gets brain to eval environment, then spit out the strategy chosen (as string)
            self.benchmark.start('decision')
            strategy_name = self.brain.get_next_strategy(game_state)
            self.benchmark.end('decision')
            self.benchmark.start('execution')
            strategy = self.strategies.get(strategy_name) 
            actions = strategy.execute(game_state)
            self.benchmark.end('execution')
            print(f'Tick {tick_number}: executing {strategy_name}: {actions}')
            self.action_queue = self.action_queue + actions

        # print(game_state) #-> To check if you've added new things to game_state
        self.prev_tick = tick_number
        self.benchmark.end('move')
        return self.action_queue.pop(0)
