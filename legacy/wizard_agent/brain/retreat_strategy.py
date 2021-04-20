from typing import List
import operator
from .strategy import Strategy
from .utils import util_functions as utils, constants


def get_opponent_danger_zone(opponent, game_state):
    max_dist = 3
    tile_queue = [opponent]
    danger_zones = []
    while len(tile_queue) > 0:
        cur_tile = tile_queue.pop(0)
        danger_zones.append(cur_tile)
        surrounding_tile = utils.get_surrounding_tiles(cur_tile, game_state)
        for tile in surrounding_tile:
            if utils.manhattan_distance(opponent, tile) <= max_dist and tile not in danger_zones:
                tile_queue.append(tile)
    return danger_zones


class RetreatStrategy(Strategy):
    def __init__(self):
        self.escape_matrix = []
        self.game_state = None
        self.player_state = None

    def execute(self, game_state: object, player_state: object) -> List[str]:
        self.game_state = game_state
        self.player_state = player_state
        self.escape_matrix = utils.get_escape_matrix(game_state)
        # fields
        location = self.player_state.location
        opponent_list = self.game_state.opponents(self.player_state.id)
        opponent = utils.get_opponent(location, opponent_list)
        # get ideal tile
        ideal_tile = self.get_ideal_tile(location, opponent)
        if ideal_tile is not None:
            path = utils.get_shortest_path(location, ideal_tile, game_state)
            action_seq = utils.get_path_action_seq(location, path)
            return action_seq
        return [constants.ACTIONS["none"]]

    def can_execute(self, game_state: object, player_state: object) -> bool:
        self.game_state = game_state
        self.player_state = player_state
        self.escape_matrix = utils.get_escape_matrix(game_state)
        location = self.player_state.location
        opponent_list = self.game_state.opponents(self.player_state.id)
        opponent = utils.get_opponent(location, opponent_list)
        ideal_tile = self.get_ideal_tile(location, opponent)
        return ideal_tile is not None

    def get_ideal_tile(self, location, opponent):
        tile_map = self.get_tile_map()
        p_tile_map = dict(sorted(tile_map.items(), key=operator.itemgetter(1), reverse=True))
        possible_tiles = list(p_tile_map.keys())
        ideal_tile = None
        while len(possible_tiles) > 0:
            tile = possible_tiles.pop(0)
            path = utils.get_shortest_path(location, tile, self.game_state)
            if path and not utils.is_opponent_closer(location, opponent, tile):
                ideal_tile = tile
                break
        return ideal_tile

    def get_tile_map(self):
        size = self.game_state.size
        width = size[0]
        height = size[1]
        tile_map = {}
        for y in range(height):
            for x in range(width):
                tile = (x, y)
                score = self.get_score(tile)
                tile_map[tile] = score
        return tile_map

    def get_score(self, tile):
        size = self.game_state.size
        width = size[0]
        location = self.player_state.location
        opponent_list = self.game_state.opponents(self.player_state.id)
        opponent = utils.get_opponent(location, opponent_list)
        player_escape = len(utils.get_surrounding_empty_tiles(location, self.game_state))
        bombs = self.game_state.bombs
        x = tile[0]
        y = tile[1]

        danger_zones = []
        for bomb in bombs:
            blast_zone = utils.get_blast_zone(bomb, self.game_state)
            danger_zones += blast_zone

        idx = width * y + x
        e = player_escape if tile == location else self.escape_matrix[idx]  # number of escape paths
        b = 0 if tile in danger_zones else 1  # blast zone factor
        dist_o = utils.manhattan_distance(opponent, tile)  # dist from opponent
        dist_p = utils.manhattan_distance(location, tile)  # dist from player
        return (e * b * dist_o) - dist_p
