from typing import List

from . import strategy
from . import utils as _utils

utils = _utils.util_functions
constants = _utils.constants


def _get_nearest_treasure(location, treasure_list):
    if treasure_list:
        treasure_distance = 10
        closest_treasure = treasure_list[0]
        for treasure in treasure_list:
            new_treasure_dist = utils.manhattan_distance(location, treasure)
            if new_treasure_dist < treasure_distance:
                treasure_distance = new_treasure_dist
                closest_treasure = treasure
        return closest_treasure
    else:
        return None


def _get_furthest_treasure_from_opponent(opponent_location, treasure_list):
    if treasure_list and len(treasure_list) > 1:
        treasure_distance = 0
        furthest_treasure = treasure_list[0]
        for treasure in treasure_list:
            new_treasure_dist = utils.manhattan_distance(opponent_location, treasure)
            if new_treasure_dist > treasure_distance:
                treasure_distance = new_treasure_dist
                furthest_treasure = treasure
        return furthest_treasure
    else:
        return None


class TreasureStrategy(strategy.Strategy):
    def execute(self, game_state: object, player_state: object) -> List[str]:
        location = player_state.location
        treasure = game_state.treasure
        list_of_opponents = game_state.opponents(player_state.id)
        opponent_location = utils.get_opponent(location, list_of_opponents)
        treasures = utils.get_reachable_tiles(location, treasure, game_state)
        # get the nearest treasure to the player
        nearest_treasure = _get_nearest_treasure(location, treasures)

        # get the furthest treasure from the opponent player
        furthest_treasure_from_opponent = _get_furthest_treasure_from_opponent(opponent_location, treasures)

        # navigate to the treasure
        if nearest_treasure is not None:
            if not utils.is_opponent_closer(location, opponent_location, nearest_treasure):
                path = utils.get_shortest_path(location, nearest_treasure, game_state)
                action_seq = utils.get_path_action_seq(location, path)
                return action_seq


        if furthest_treasure_from_opponent is not None:
            path = utils.get_shortest_path(location, furthest_treasure_from_opponent, game_state)
            action_seq = utils.get_path_action_seq(location, path)
            return action_seq

        return [constants.ACTIONS["none"]]

    def can_execute(self, game_state: object, player_state: object) -> bool:
        location = player_state.location
        treasures = game_state.treasure
        bombs = game_state.bombs
        list_of_opponents = game_state.opponents(player_state.id)
        opponent_location = utils.get_opponent(location, list_of_opponents)
        reachable_treasure = utils.get_reachable_tiles(location, treasures, game_state)
        furthest_treasure = _get_furthest_treasure_from_opponent(opponent_location, reachable_treasure)
        nearest_treasure = _get_nearest_treasure(location, reachable_treasure)
        is_opponent_closer = utils.is_opponent_closer(location, opponent_location, nearest_treasure)

        closest_treasure_safe = False
        furthest_treasure_safe = False

        if nearest_treasure:
            closest_treasure_safe = utils.is_safe_path(location, nearest_treasure, bombs, game_state)
        if furthest_treasure:
            furthest_treasure_safe = utils.is_safe_path(location, furthest_treasure, bombs, game_state)
        
        can_reach_nearest_treasure = nearest_treasure is not None and not is_opponent_closer and closest_treasure_safe
        can_reach_furthest_treasure = furthest_treasure is not None and not is_opponent_closer and furthest_treasure_safe
        
        return can_reach_nearest_treasure or can_reach_furthest_treasure
