"""
Interface for defining strategy pattern.
"""
from typing import List


class Strategy:

    def execute(self, game_state: object) -> List[str]:
        """
        Execute the strategy
        """
        pass
