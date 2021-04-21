"""
Tracks the game state and decides on next strategy to execute
"""

from .bomb_tracker import BombTracker
from .enemy_tracker import EnemyTracker


class Brain:
    def __init__(self):
        self.bomb_tracker = BombTracker()
        self.enemy_tracker = EnemyTracker()

    def get_next_strategy(self, game_state) -> str:
        self.bomb_tracker.update(game_state)
        self.enemy_tracker.update(game_state)

        # TODO Make decisions in terms on what strategy to do next

        return "random"
