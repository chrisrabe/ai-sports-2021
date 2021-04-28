from typing import List

from . import strategy
from ..utils.constants import ACTIONS


class SimpleBombStrategy(strategy.Strategy):

    def execute(self, game_state: object) -> List[str]:
        # just put bomb down. Doesn't matter what it is.
        return [ACTIONS['bomb']]
