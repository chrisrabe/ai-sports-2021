import random
from typing import List

from . import strategy
from ..utils.constants import ACTIONS


class RandomStrategy(strategy.Strategy):

    def execute(self, game_state: object) -> List[str]:
        # a list of all the actions your Agent can choose from
        actions = [
            ACTIONS["none"],
            ACTIONS["up"],
            ACTIONS["down"],
            ACTIONS["left"],
            ACTIONS["right"],
            ACTIONS["bomb"]
        ]

        # randomly choosing an action
        action = random.choice(actions)

        return [action]
