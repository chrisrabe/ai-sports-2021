import random
from typing import List

from . import strategy
from ..utils.constants import ACTIONS


class BombStrategy(strategy.Strategy):

    def execute(self, game_state: object) -> List[str]:
        # Literally just bomb.
        return [ACTIONS['bomb']]