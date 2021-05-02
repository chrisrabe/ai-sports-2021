"""
Tracks the game state and decides on next strategy to execute
"""

from ..shared.trackers import FinalsTracker


class Brain:
    def __init__(self):
        self.finals_tracker = FinalsTracker()

    def get_next_strategy(self, game_state) -> str:
        self.finals_tracker.update(game_state)
        return 'stalk'
