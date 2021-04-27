import random
from typing import List

from . import strategy
from ..utils.constants import ACTION_LIST


class RandomStrategy(strategy.Strategy):

    def execute(self, game_state: object) -> List[str]:
        # a list of all the actions your Agent can choose from
        actions = ACTION_LIST

        # randomly choosing an action
        action = random.choice(actions)

        return [action]
