from typing import List

from . import strategy
from ..utils.constants import ACTIONS


class WaitStrategy(strategy.Strategy):

    def execute(self, game_state: object) -> List[str]:
        return [ACTIONS['none']]
