"""
Tracks the game state and decides on next strategy to execute
"""
from ..shared.utils.benchmark import Benchmark
from ..shared.trackers import FinalsTracker


class Brain:
    def __init__(self):
        self.benchmark = Benchmark()
        self.finals_tracker = FinalsTracker()

    def get_next_strategy(self, game_state) -> str:
        self.benchmark.start('tracker')
        self.finals_tracker.update(game_state)
        self.benchmark.end('tracker')
        return 'stalk'
