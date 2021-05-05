"""
Interface for defining strategy pattern.
"""
from typing import List


class Strategy:

    def update(self, game_state: dict):
        """
        Make additional updates that are specific to the strategy
        """
        pass

    def execute(self, game_state: object) -> List[str]:
        """
        Execute the strategy
        """
        pass
