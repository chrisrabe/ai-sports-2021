from typing import List

from .strategy import Strategy
from .utils import util_functions as utils


class FakeOutStrategy(Strategy):
    def __init__(self):
        # store arguments from combat strategy
        self.fields = {}
        self.game_state = None
        self.player_state = None

    def execute(self, game_state: object, player_state: object) -> List[str]:
        self.game_state = game_state
        self.player_state = player_state
        pass

    def can_execute(self, game_state: object, player_state: object) -> bool:
        self.game_state = game_state
        self.player_state = player_state
        return False

    def update_fields(self, new_fields):
        self.fields = new_fields

    def get_escape_path(self, tile):
        empty_tiles = utils.get_surrounding_empty_tiles(tile, self.game_state)
        return len(empty_tiles)
