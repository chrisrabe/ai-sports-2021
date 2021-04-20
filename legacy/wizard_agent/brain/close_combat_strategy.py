from typing import List

from .strategy import Strategy
from .utils import util_functions as utils, constants


class CloseCombatStrategy(Strategy):
    def execute(self, game_state: object, player_state: object) -> List[str]:
        location = player_state.location
        opponent_list = game_state.opponents(player_state.id)
        opponent = utils.get_opponent(location, opponent_list)
        # grabs empty tiles near opponent
        surrounding_tiles = utils.get_surrounding_empty_tiles(opponent, game_state)
        reachable_tiles = utils.get_reachable_tiles(location, surrounding_tiles, game_state)
        nearest_tile = utils.get_nearest_tile(location, reachable_tiles)
        # navigate to nearest empty tile
        if nearest_tile is not None:
            path = utils.get_shortest_path(location, nearest_tile, game_state)
            action_seq = utils.get_path_action_seq(location, path)
            action_seq.append(constants.ACTIONS["bomb"])
            return action_seq
        return [constants.ACTIONS["none"]]

    def can_execute(self, game_state: object, player_state: object) -> bool:
        location = player_state.location
        opponent_list = game_state.opponents(player_state.id)
        opponent = utils.get_opponent(location, opponent_list)
        ammo = player_state.ammo
        # grabs empty tiles near opponent
        surrounding_tiles = utils.get_surrounding_empty_tiles(opponent, game_state)
        reachable_tiles = utils.get_reachable_tiles(location, surrounding_tiles, game_state)
        # check if opponent nearby
        opp_distance = utils.manhattan_distance(location, opponent)
        return ammo > 0 and reachable_tiles and opp_distance <= 3
