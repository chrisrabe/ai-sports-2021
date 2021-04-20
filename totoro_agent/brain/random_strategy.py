import random
from typing import List

from . import strategy
from . import utils

ACTIONS = utils.constants.ACTIONS


class RandomStrategy(strategy.Strategy):
    def execute(self, game_state: object, player_state: object) -> List[str]:
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

    def can_execute(self, game_state: object, player_state: object) -> bool:
        return True
