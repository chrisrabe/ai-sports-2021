"""
Interface for defining strategy pattern.
"""
from typing import List


class Strategy:
    def execute(self, game_state: object, player_state: object) -> List[str]:
        """
        Execute the strategy
        """
        pass

    def can_execute(self, game_state: object, player_state: object) -> bool:
        """
        Returns whether or not the strategy can execute
        """
        pass
