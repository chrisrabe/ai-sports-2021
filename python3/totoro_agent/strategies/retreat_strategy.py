from typing import List

from . import strategy
from ..utils.constants import ACTIONS
from ..utils.util_functions import get_shortest_path, get_path_action_seq


class RetreatStrategy(strategy.Strategy):

    def execute(self, game_state: object) -> List[str]:
        # find safest tile
        # run to it!!
        return [ACTIONS["none"]]
